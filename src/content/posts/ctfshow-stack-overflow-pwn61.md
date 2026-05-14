---
title: "ctfshow stack overflow pwn61"
published: 2026-05-14T00:03:00+08:00
description: "Writeup for ctfshow stack overflow pwn61."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "PIE", "shellcode"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

![shot 1](/attachments/ctfshow/stack-overflow/pwn61/01-shot-1.png)

![shot 2](/attachments/ctfshow/stack-overflow/pwn61/02-shot-2.png)

![shot 3](/attachments/ctfshow/stack-overflow/pwn61/03-shot-3.png)

问题来了，这里输出的地址是什么？

![shot 4](/attachments/ctfshow/stack-overflow/pwn61/04-shot-4.png)

![shot 5](/attachments/ctfshow/stack-overflow/pwn61/05-shot-5.png)

低四位在变化，因为开了 PIE 保护，导致堆栈内存地址映射随机化。它这里泄露出一个 `v5` 的地址，就相当于把堆栈地址泄露出来了。于是可以通过 `v5` 位置布 shellcode。只是 `v5` 太短，要布置到 return address 后面的位置去才行。

exp：

![shot 6](/attachments/ctfshow/stack-overflow/pwn61/06-shot-6.png)

![shot 7](/attachments/ctfshow/stack-overflow/pwn61/07-shot-7.png)

`ctfshow{71c7d7c7-6824-4f2c-9cc5-b195c000e2f5}`
