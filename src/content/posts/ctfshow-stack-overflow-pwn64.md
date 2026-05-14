---
title: "ctfshow stack overflow pwn64"
published: 2026-05-14T00:06:00+08:00
description: "Writeup for ctfshow stack overflow pwn64."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "shellcode", "mmap"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

![shot 1](/attachments/ctfshow/stack-overflow/pwn64/01-shot-1.png)

![shot 2](/attachments/ctfshow/stack-overflow/pwn64/02-shot-2.png)

![shot 3](/attachments/ctfshow/stack-overflow/pwn64/03-shot-3.png)

六百六十六，`mmap` 里敢给权限 `7`。那这道题 hint 的意思就是，这题表面上开了 NX 保护无法注入 shellcode，但其实在程序运行过程中申请了可读可写可执行、大小为 `0x400` 的 `buf`，而且有直接指向 `buf` 的片段。

所以本题的思路还是 shellcode 注入。

exp：

![shot 4](/attachments/ctfshow/stack-overflow/pwn64/04-shot-4.png)

![shot 5](/attachments/ctfshow/stack-overflow/pwn64/05-shot-5.png)

`ctfshow{49094757-869f-4492-82a2-36c9afa2b7d7}`
