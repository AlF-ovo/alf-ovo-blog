---
title: "ctfshow stack overflow pwn71"
published: 2026-05-18T22:00:39+08:00
description: "Writeup for ctfshow stack overflow pwn71."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ret2syscall"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
![shot 1](/attachments/ctfshow/stack-overflow/pwn71/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn71/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn71/03-shot-3.png)

这是一个静态编译的题目。ret2syscall 要怎么去做呢，我大致去网上查了一下。

![shot 4](/attachments/ctfshow/stack-overflow/pwn71/04-shot-4.png)
![shot 5](/attachments/ctfshow/stack-overflow/pwn71/05-shot-5.png)
![shot 6](/attachments/ctfshow/stack-overflow/pwn71/06-shot-6.png)

那么来尝试做一下吧，写汇编之前也已经尝试过了，应该不是太困难。

![shot 7](/attachments/ctfshow/stack-overflow/pwn71/07-shot-7.png)
![shot 8](/attachments/ctfshow/stack-overflow/pwn71/08-shot-8.png)
![shot 9](/attachments/ctfshow/stack-overflow/pwn71/09-shot-9.png)
![shot 10](/attachments/ctfshow/stack-overflow/pwn71/10-shot-10.png)

偏移为 112。

![shot 11](/attachments/ctfshow/stack-overflow/pwn71/11-shot-11.png)

`/bin/sh` 的位置为 `0x80be400`。

![shot 12](/attachments/ctfshow/stack-overflow/pwn71/12-shot-12.png)

失败。

![shot 13](/attachments/ctfshow/stack-overflow/pwn71/13-shot-13.png)

`/bin/sh` 位置找错了，IDA 里查看出来是这样的，做法是 `Shift+F12`，然后直接搜索 `/bin/sh`。再试成功。

exp：

![shot 14](/attachments/ctfshow/stack-overflow/pwn71/14-shot-14.png)
![shot 15](/attachments/ctfshow/stack-overflow/pwn71/15-shot-15.png)

`ctfshow{d829eb0d-a619-44c7-8de0-91e87f3b6da1}`
