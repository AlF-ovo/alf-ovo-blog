---
title: "ctfshow stack overflow pwn78"
published: 2026-05-22T20:10:00+08:00
description: "Writeup for ctfshow stack overflow pwn78."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "one_gadget", "syscall"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
![shot 1](/attachments/ctfshow/stack-overflow/pwn78/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn78/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn78/03-shot-3.png)

看看 `syscall` 需要用到的 `one_gadget`：

![shot 4](/attachments/ctfshow/stack-overflow/pwn78/04-shot-4.png)
![shot 5](/attachments/ctfshow/stack-overflow/pwn78/05-shot-5.png)
![shot 6](/attachments/ctfshow/stack-overflow/pwn78/06-shot-6.png)
![shot 7](/attachments/ctfshow/stack-overflow/pwn78/07-shot-7.png)
![shot 8](/attachments/ctfshow/stack-overflow/pwn78/08-shot-8.png)

`rcx` 好像用不到其实。。

然后再找一段可写入的 `bss` 段调用下 `read` 写入，因为没有现成的 `/bin/sh`：

![shot 9](/attachments/ctfshow/stack-overflow/pwn78/09-shot-9.png)

随便用中间一点的 `0x6c2000`

`syscall`：

![shot 10](/attachments/ctfshow/stack-overflow/pwn78/10-shot-10.png)

exp：

![shot 11](/attachments/ctfshow/stack-overflow/pwn78/11-shot-11.png)
![shot 12](/attachments/ctfshow/stack-overflow/pwn78/12-shot-12.png)

`ctfshow{f04d9512-e1ee-4bdf-8537-e5ae96374c79}`

我用 `flat` 尝试写 payload 结果失败了，把错误归咎于 `flat` 没法自动识别 32 位与 64 位程序 :(

用 `p64()` 的方式就对了
