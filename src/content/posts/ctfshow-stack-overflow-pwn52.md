---
title: "ctfshow stack overflow pwn52"
published: 2026-05-13T22:16:01+08:00
description: "Writeup for ctfshow stack overflow pwn52."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ret2text"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

附件：[`pwn52-ret2text.py`](/attachments/ctfshow/stack-scripts/pwn52-ret2text.py)

![shot 1](/attachments/ctfshow/stack-overflow/pwn52/01-shot-1.png)

![shot 2](/attachments/ctfshow/stack-overflow/pwn52/02-shot-2.png)

![shot 3](/attachments/ctfshow/stack-overflow/pwn52/03-shot-3.png)

题目让我尝试修改a1的值为876，a2的值为877，从而getflag。而a1与a2是flag()函数的两个参数。

![shot 4](/attachments/ctfshow/stack-overflow/pwn52/04-shot-4.png)

直接输入即可，注意参数顺序。

exp：

![shot 5](/attachments/ctfshow/stack-overflow/pwn52/05-shot-5.png)

![shot 6](/attachments/ctfshow/stack-overflow/pwn52/06-shot-6.png)

ctfshow{09b516d6-3d5b-4f0a-821b-771cca64f95d}