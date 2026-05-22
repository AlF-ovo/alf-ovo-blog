---
title: "ctfshow stack overflow pwn80"
published: 2026-05-22T20:30:00+08:00
description: "Writeup for ctfshow stack overflow pwn80."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ret2csu", "ret2libc"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
附件：[exp.py](/attachments/ctfshow/stack-overflow/pwn80/exp.py)

![shot 1](/attachments/ctfshow/stack-overflow/pwn80/01-shot-1.png)

先跑出栈的长度：72 一到 73 程序就会崩溃，因为访问了非法地址

![shot 2](/attachments/ctfshow/stack-overflow/pwn80/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn80/03-shot-3.png)

再找合适的 `stop_gadget`（防止后续测试 gadget 的时候每次都崩溃，那样就看不出来是否是想要的 gadget 了）寻找的点：返回值为空，不报错。

![shot 4](/attachments/ctfshow/stack-overflow/pwn80/04-shot-4.png)
![shot 5](/attachments/ctfshow/stack-overflow/pwn80/05-shot-5.png)

做一个小测试避免搞错：

![shot 6](/attachments/ctfshow/stack-overflow/pwn80/06-shot-6.png)

确实成功返回了 `main` 函数（结果太长了就不在这演示了）

下一步找 `ret2csu` 的 gadget 链（主要是为了获得 `pop rdi;ret` 来做 `puts`）。

寻找的点：gadget 连续 6 个 `pop`

再获取 `puts_plt`

利用 `puts` 函数泄露 `libc` 版本走 `ret2libc`

![shot 7](/attachments/ctfshow/stack-overflow/pwn80/07-shot-7.png)

`ctfshow{5f066181-da96-402e-ab03-c8dce3e44cb6}`
