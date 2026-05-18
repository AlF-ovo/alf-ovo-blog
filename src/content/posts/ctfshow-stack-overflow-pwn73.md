---
title: "ctfshow stack overflow pwn73"
published: 2026-05-18T23:05:16+08:00
description: "Writeup for ctfshow stack overflow pwn73."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ROP", "ret2syscall"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
![shot 1](/attachments/ctfshow/stack-overflow/pwn73/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn73/02-shot-2.png)

主要咱也不记得一把梭对应的代码是什么了呀，唉。

好像是什么 `ROPchain`？搜了一下，是：

`ROPgadget --binary pwn --ropchain`

![shot 3](/attachments/ctfshow/stack-overflow/pwn73/03-shot-3.png)

劲啊！

就是别忘了 `from struct import pack`，不然用不了。

exp：

![shot 4](/attachments/ctfshow/stack-overflow/pwn73/04-shot-4.png)

之前自己写的版本偏移算错了，所以重新写了个平民版本。

![shot 5](/attachments/ctfshow/stack-overflow/pwn73/05-shot-5.png)

`ctfshow{833e8ced-0f9e-4296-867b-777ba7190367}`
