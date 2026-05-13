---
title: "ctfshow stack overflow pwn53"
published: 2026-05-13T22:41:04+08:00
description: "Writeup for ctfshow stack overflow pwn53."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "Canary", "bruteforce"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

附件：[`pwn53-ret2text-canary.py`](/attachments/ctfshow/stack-scripts/pwn53-ret2text-canary.py)，[`binary_break.py`](/attachments/ctfshow/stack-scripts/binary_break.py)

![shot 1](/attachments/ctfshow/stack-overflow/pwn53/01-shot-1.png)

![shot 2](/attachments/ctfshow/stack-overflow/pwn53/02-shot-2.png)

![shot 3](/attachments/ctfshow/stack-overflow/pwn53/03-shot-3.png)

这个canary为固定值是第一次见蛤

想办法给它泄露出来后面直接伪造就好了

![shot 4](/attachments/ctfshow/stack-overflow/pwn53/04-shot-4.png)

可以看到这边s1承载了canary，想办法给它泄露出来（这里有格式化字符串漏洞嘛？）

我注意到一个细节：它在与canary作比较的时候只比较了4u个字节，这点字节量完全可以爆破处理。

![shot 5](/attachments/ctfshow/stack-overflow/pwn53/05-shot-5.png)

最后跳转到flag函数获取flag

exp：

![shot 6](/attachments/ctfshow/stack-overflow/pwn53/06-shot-6.png)

![shot 7](/attachments/ctfshow/stack-overflow/pwn53/07-shot-7.png)

第一波canary爆破结果：canary: 0x21443633

![shot 8](/attachments/ctfshow/stack-overflow/pwn53/08-shot-8.png)

![shot 9](/attachments/ctfshow/stack-overflow/pwn53/09-shot-9.png)

ctfshow{31023554-e3ec-46a9-b6ae-85a07e4ecc45}