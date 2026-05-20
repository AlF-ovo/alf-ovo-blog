---
title: "ctfshow stack overflow pwn77"
published: 2026-05-20T19:36:11+08:00
description: "Writeup for ctfshow stack overflow pwn77."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ret2libc"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
附件：[`libc-2.27.so`](/attachments/ctfshow/stack-overflow/pwn77/libc-2.27.so)

![shot 1](/attachments/ctfshow/stack-overflow/pwn77/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn77/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn77/03-shot-3.png)

这里用 `rbp+var_4` 的方式调用，所以可以溢出。

![shot 4](/attachments/ctfshow/stack-overflow/pwn77/04-shot-4.png)

单字节读入，特殊之处在于作为指针的 `v4` 被压在栈上。所以在覆盖的时候会修改掉这里的指针变量，需要提前规划覆盖时的值来篡改指针。我和别的师傅 wp 里写的方式方法不同，他们是直接把指针指到了 `0x118`，而我一时想到的只有是去写入特殊值，不改变 `i` 的正常递增。

exp：

![shot 5](/attachments/ctfshow/stack-overflow/pwn77/05-shot-5.png)
![shot 6](/attachments/ctfshow/stack-overflow/pwn77/06-shot-6.png)

`ctfshow{29c5a13b-232b-4e5c-8d1b-595922db3dc5}`
