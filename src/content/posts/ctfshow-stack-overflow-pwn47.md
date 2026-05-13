---
title: "ctfshow stack overflow pwn47"
published: 2026-05-12T22:26:33+08:00
description: "Writeup for ctfshow stack overflow pwn47."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ROP", "ret2libc"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

附件：[`pwn47-ret2libc.py`](/attachments/ctfshow/stack-scripts/pwn47-ret2libc.py)

![shot 1](/attachments/ctfshow/stack-overflow/pwn47/01-shot-1.png)

![shot 2](/attachments/ctfshow/stack-overflow/pwn47/02-shot-2.png)

![shot 3](/attachments/ctfshow/stack-overflow/pwn47/03-shot-3.png)

先承接这些外部函数地址供后续使用。

![shot 4](/attachments/ctfshow/stack-overflow/pwn47/04-shot-4.png)

useful里放的是binsh，且位置固定。

exp：

![shot 5](/attachments/ctfshow/stack-overflow/pwn47/05-shot-5.png)

这里用了eval(io.recvuntil("\n",drop=True))来承接地址。

drop=True会把\n扔掉，只保留前面的东西（又在"puts："之后）所以能够正常承接地址。

![shot 6](/attachments/ctfshow/stack-overflow/pwn47/06-shot-6.png)

ctfshow{f38a8057-d4cb-41d0-bf96-1a483db2f7a2}