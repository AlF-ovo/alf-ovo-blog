---
title: "ctfshow stack overflow pwn68"
published: 2026-05-17T00:09:00+08:00
description: "Writeup for ctfshow stack overflow pwn68."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ROP"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
![shot 1](/attachments/ctfshow/stack-overflow/pwn68/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn68/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn68/03-shot-3.png)
![shot 4](/attachments/ctfshow/stack-overflow/pwn68/04-shot-4.png)
和上一题没什么区别a，我想应该只是ROP链和偏移需要稍微改变一下。
别的参数都没变，只有中间返回地址与rbp位置变长了各0x4，所以+0x8
![shot 5](/attachments/ctfshow/stack-overflow/pwn68/05-shot-5.png)
![shot 6](/attachments/ctfshow/stack-overflow/pwn68/06-shot-6.png)
ctfshow{d30e2658-bfc3-4d8d-a149-193537350b57}
顺带提一嘴，64bit对比32bit对recvuntil的检查更严格，在32bit使用recvuntil("")是被允许的，而在64bit使用recvuntil("")会报错。要用recvuntil(b"")

