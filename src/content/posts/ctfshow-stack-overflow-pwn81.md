---
title: "ctfshow stack overflow pwn81"
published: 2026-06-02T00:10:00+08:00
description: "Writeup for ctfshow stack overflow pwn81."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ret2libc"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
![shot 1](/attachments/ctfshow/stack-overflow/pwn81/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn81/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn81/03-shot-3.png)

这道题目的 `libc` 去 ctfshow 专门给的虚拟机里找，路径放 `exp` 里了。

这里给了一个 `system` 函数的地址，然后转进 `ctfshow()` 函数。

![shot 4](/attachments/ctfshow/stack-overflow/pwn81/04-shot-4.png)

`ctfshow` 函数中有一个明显的栈溢出。`0x100 - 0x88 = 0x78`

GOT 表没法改，栈不可执行，运行地址随机化。

![shot 5](/attachments/ctfshow/stack-overflow/pwn81/05-shot-5.png)

先想办法利用 `puts` 将 `binsh` 上传至 `bss` 段然后再 `system` 调用 `binsh` 是否可行？

![shot 6](/attachments/ctfshow/stack-overflow/pwn81/06-shot-6.png)

不可行，因为有程序基址随机化。

在已知 `system` 函数地址的情况下我们是已知 `libc` 的，换言之直接用 `libc` 找 `binsh` 做 `system("/bin/sh")` 即可。

exp：

![shot 7](/attachments/ctfshow/stack-overflow/pwn81/07-shot-7.png)
![shot 8](/attachments/ctfshow/stack-overflow/pwn81/08-shot-8.png)

`ctfshow{cf17cdbc-6596-4766-8a3c-7518b1a16ac5}`
