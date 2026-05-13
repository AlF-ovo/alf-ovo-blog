---
title: "ctfshow stack overflow pwn50"
published: 2026-05-13T21:08:39+08:00
description: "Writeup for ctfshow stack overflow pwn50."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ret2libc", "mprotect"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

附件：[`pwn50-ret2libc.py`](/attachments/ctfshow/stack-scripts/pwn50-ret2libc.py)

![shot 1](/attachments/ctfshow/stack-overflow/pwn50/01-shot-1.png)

![shot 2](/attachments/ctfshow/stack-overflow/pwn50/02-shot-2.png)

这题我想直接用ret2libc做，完全没问题。但出题者的预期解为用 ret2libc 泄露 mprotect 地址，然后修改内存权限，再 ret2shellcode。

这题得用ctfshow给的虚拟机做，不然libc版本对不上

exp：

![shot 3](/attachments/ctfshow/stack-overflow/pwn50/03-shot-3.png)

![shot 4](/attachments/ctfshow/stack-overflow/pwn50/04-shot-4.png)

ctfshow{501b7e13-68ef-431b-addf-c805ece007ca}