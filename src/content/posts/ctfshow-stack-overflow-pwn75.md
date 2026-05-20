---
title: "ctfshow stack overflow pwn75"
published: 2026-05-19T19:27:35+08:00
description: "Writeup for ctfshow stack overflow pwn75."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "stack-pivot", "ret2libc"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
![shot 1](/attachments/ctfshow/stack-overflow/pwn75/01-shot-1.png)

栈空间不够怎么办，栈空间不够就去做栈迁移。

![shot 2](/attachments/ctfshow/stack-overflow/pwn75/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn75/03-shot-3.png)

这个函数从调用层面讲毫无用处，然而却实打实的给了我们 system 函数。

![shot 4](/attachments/ctfshow/stack-overflow/pwn75/04-shot-4.png)

ctfshow 这个函数有两次输入，但均只有两个字节的溢出，写 ROP 链的位置肯定是不够的。
这里就要用到栈迁移的知识点了，然而我只知道要 `leave; leave; ret`，具体的操作方式和运行结果我是不清楚的。所以我去网上搜索了资料：

[栈迁移的原理&&实战运用 - ZikH26 - 博客园](https://www.cnblogs.com/ZIKH26/articles/15817337.html)

![shot 5](/attachments/ctfshow/stack-overflow/pwn75/05-shot-5.png)
![shot 6](/attachments/ctfshow/stack-overflow/pwn75/06-shot-6.png)

exp：

![shot 7](/attachments/ctfshow/stack-overflow/pwn75/07-shot-7.png)

其中 `0x38 = 0x28 + 0x10`，`0x10` 是 `main_ebp` 与 `buf_ebp` 之间的相对偏移。
这里的 `system` 函数后跟的 `b"aaaa"` 是作为 `system` 函数的返回地址存在，`p32(buf+16)` 作为其参数调用，指向写在之后的 `b"/bin/sh\\x00"`。

![shot 8](/attachments/ctfshow/stack-overflow/pwn75/08-shot-8.png)

`ctfshow{681b8551-ba3e-414b-94f5-9f8655ccca62}`
