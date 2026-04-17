from pwn import *
from LibcSearcher import *

#context(arch = "amd64",os = 'linux',log_level = 'debug')
context(arch = "i386", os = 'linux', log_level = 'debug')

#io = process("./pwn")
io = remote('pwn.challenge.ctf.show', 28136)
elf = ELF("./pwn")
libc = ELF('./libc.so.6')

# 发送空字符串
io.sendline('')

io.interactive()

"""
【知识点讲解】
1. 题目类型：interactive - 简单交互程序
2. 核心原理：
   - 程序可能存在输入处理漏洞
   - 通过发送空字符串触发某种行为
3. 执行流程：
   - 连接到远程服务器
   - 发送空字符串
   - 进入交互模式查看程序响应
4. 可能的漏洞点：
   - 空字符串处理逻辑
   - 输入验证不严格
   - 边界条件处理
5. 调试建议：
   - 观察程序对空输入的处理
   - 检查是否存在缓冲区溢出或其他漏洞
"""
