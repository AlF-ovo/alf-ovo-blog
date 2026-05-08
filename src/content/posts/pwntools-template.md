---
title: "pwntools-template"
published: 2026-05-08T19:10:00+08:00
description: "记录一个通用的 pwntools 起手模板，包含本地、远程和调试三种切换。"
image: ""
tags: ["模板", "Pwn", "pwntools"]
category: "模板"
categoryPath: ["模板"]
series: ""
draft: false
lang: "zh_CN"
---

附件：[`template.py`](/attachments/模板/pwntools-template/template.py)

这是一个最基础的 pwntools 模板，先把 `binary_path`、`host`、`port` 改掉，再按需要补 exploit 逻辑就能直接开写。

```python
"""
- 本地正常：python3 exp.py
- 本地 debug：python3 exp.py DEBUG
- 远程正常：python3 exp.py REMOTE
- 远程 debug 日志：python3 exp.py REMOTE DEBUG
"""
from pwn import *

context(os="linux", terminal=["cmd.exe", "/c", "start"])

binary_path = "./pwn"
host = "127.0.0.1"  # 地址
port = 9999  # 端口

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


# todo

io.interactive()
```
