---
title: "ctfshow stack overflow pwn60"
published: 2026-05-14T00:02:00+08:00
description: "Writeup for ctfshow stack overflow pwn60."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ret2shellcode"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

![shot 1](/attachments/ctfshow/stack-overflow/pwn60/01-shot-1.png)

![shot 2](/attachments/ctfshow/stack-overflow/pwn60/02-shot-2.png)

![shot 3](/attachments/ctfshow/stack-overflow/pwn60/03-shot-3.png)

由于堆栈可执行，第一时间考虑 ret2shellcode。

这边有一个 `s` 对 `buf2` 的 copy，想到的是布置 shellcode 在 `buf2` 上然后 `s` 栈溢出构造 ROP 链回指向 shellcode 所在位置。

但是为什么 gets 这里构造了 ROP 链之后会是先 cpy 再走 ROP 链的后续流程，我就不清楚了？

![shot 4](/attachments/ctfshow/stack-overflow/pwn60/04-shot-4.png)

不知道为什么这里偏移本地不对。

![shot 5](/attachments/ctfshow/stack-overflow/pwn60/05-shot-5.png)

跑了下脚本得知是 `112`。

exp：

![shot 6](/attachments/ctfshow/stack-overflow/pwn60/06-shot-6.png)

![shot 7](/attachments/ctfshow/stack-overflow/pwn60/07-shot-7.png)

`ctfshow{e663cb50-ccfd-4f5f-b525-7116ebe9a126}`
