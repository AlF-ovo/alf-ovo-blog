---
title: "ctfshow stack overflow pwn74"
published: 2026-05-18T23:27:12+08:00
description: "Writeup for ctfshow stack overflow pwn74."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "one_gadget", "ret2libc"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
![shot 1](/attachments/ctfshow/stack-overflow/pwn74/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn74/02-shot-2.png)

这保护开的，不像栈题。

![shot 3](/attachments/ctfshow/stack-overflow/pwn74/03-shot-3.png)

先别慌，先看题，发现题目提供了一个 `printf` 的地址。这就代表程序段的地址是已知的，我们可以调用这些函数。这里不能用 `LibcSearcher` 查询函数，不然用不了 `one_gadget`，因为 `one_gadget` 刚需一个 `libc.so` 文件。题目又没有提供，怎么办呢？

`libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')`，假装它提供了。这个 `libc` 是 ctfshow 给的虚拟机里的 libc 库。

exp：（记得用 `printf` 来做基址泄露）

![shot 4](/attachments/ctfshow/stack-overflow/pwn74/04-shot-4.png)
![shot 5](/attachments/ctfshow/stack-overflow/pwn74/05-shot-5.png)

`ctfshow{d336df0c-e7dd-43b7-906d-212df47b7c57}`

那这里 `one_gadget` 是怎么用的呢？

`one_gadget /lib/x86_64-linux-gnu/libc.so.6`

![shot 6](/attachments/ctfshow/stack-overflow/pwn74/06-shot-6.png)

一个个试过去就好。
