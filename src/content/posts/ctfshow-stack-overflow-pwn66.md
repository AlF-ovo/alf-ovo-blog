---
title: "ctfshow stack overflow pwn66"
published: 2026-05-14T00:08:00+08:00
description: "Writeup for ctfshow stack overflow pwn66."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "shellcode"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

![shot 1](/attachments/ctfshow/stack-overflow/pwn66/01-shot-1.png)

![shot 2](/attachments/ctfshow/stack-overflow/pwn66/02-shot-2.png)

![shot 3](/attachments/ctfshow/stack-overflow/pwn66/03-shot-3.png)

![shot 4](/attachments/ctfshow/stack-overflow/pwn66/04-shot-4.png)

这里的 `check()` 函数 `"ZZJ loves shell_code,and here is a gift:"` 只校验了 shellcode 的字符是否属于该字符串，没有校验顺序。因此有要输入有奇奇怪怪要求的 shellcode 了。

![shot 5](/attachments/ctfshow/stack-overflow/pwn66/05-shot-5.png)

按 “A”

![shot 6](/attachments/ctfshow/stack-overflow/pwn66/06-shot-6.png)

可惜这些字符组不成完整的 shellcode。所以要想办法让第一位为 `\x00` 来绕过检查机制。注意后续访问的也是 `buf` 的首地址，也就是说从 `\x00` 开始访问，这个 `\x00` 一定要有意义。

![shot 7](/attachments/ctfshow/stack-overflow/pwn66/07-shot-7.png)

直接打一个 `"\x00"` 是打不通的。我看网上别人的 wp 里，用 `b'\x00B\x00'` 就打通了。

![shot 8](/attachments/ctfshow/stack-overflow/pwn66/08-shot-8.png)

![shot 9](/attachments/ctfshow/stack-overflow/pwn66/09-shot-9.png)

`ctfshow{1b5bc9d7-5d87-4305-bda3-d23c5597a260}`

为什么呢？
