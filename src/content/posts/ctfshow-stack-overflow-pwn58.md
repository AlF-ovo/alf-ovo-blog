---
title: "ctfshow stack overflow pwn58"
published: 2026-05-14T00:00:00+08:00
description: "Writeup for ctfshow stack overflow pwn58."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ret2shellcode"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

附件：[`pwn58-ret2shellcode.py`](/attachments/ctfshow/stack-scripts/pwn58-ret2shellcode.py)

![shot 1](/attachments/ctfshow/stack-overflow/pwn58/01-shot-1.png)

![shot 2](/attachments/ctfshow/stack-overflow/pwn58/02-shot-2.png)

![shot 3](/attachments/ctfshow/stack-overflow/pwn58/03-shot-3.png)

F5发现无法反编译

![shot 4](/attachments/ctfshow/stack-overflow/pwn58/04-shot-4.png)

找到报错段一看，好家伙，`call eax`，演都不演了，直接明晃晃要我写 shellcode 是吧。

exp：

![shot 5](/attachments/ctfshow/stack-overflow/pwn58/05-shot-5.png)

![shot 6](/attachments/ctfshow/stack-overflow/pwn58/06-shot-6.png)

`ctfshow{62759ac8-0753-4ce3-9855-506f9cae1048}`
