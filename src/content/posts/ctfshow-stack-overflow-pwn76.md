---
title: "ctfshow stack overflow pwn76"
published: 2026-05-19T20:09:47+08:00
description: "Writeup for ctfshow stack overflow pwn76."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ret2text"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
![shot 1](/attachments/ctfshow/stack-overflow/pwn76/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn76/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn76/03-shot-3.png)
![shot 4](/attachments/ctfshow/stack-overflow/pwn76/04-shot-4.png)
![shot 5](/attachments/ctfshow/stack-overflow/pwn76/05-shot-5.png)

`v7 <= 0xc` 代表输入长度小于等于 12。然而 `v2` 最多只有 8 字节，此处存在栈溢出。
想办法通过此处的栈溢出使得 input 满足 correct 条件。
或者直接调用 system 走 binsh，两种方法都可以完成这道题目。由于题目已经给了 correct 函数，这里只尝试第一种。

![shot 6](/attachments/ctfshow/stack-overflow/pwn76/06-shot-6.png)

exp：

![shot 7](/attachments/ctfshow/stack-overflow/pwn76/07-shot-7.png)
![shot 8](/attachments/ctfshow/stack-overflow/pwn76/08-shot-8.png)

`ctfshow{a9218822-b7d2-42dc-b3ae-ab5d12ecc0c9}`
