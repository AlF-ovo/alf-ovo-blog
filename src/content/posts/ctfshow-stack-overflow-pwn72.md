---
title: "ctfshow stack overflow pwn72"
published: 2026-05-18T22:40:44+08:00
description: "Writeup for ctfshow stack overflow pwn72."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ret2syscall"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
![shot 1](/attachments/ctfshow/stack-overflow/pwn72/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn72/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn72/03-shot-3.png)

上来问个 `where_is_my_system`，是把 `int 0x80` 搞没了嘛，查看下。（还有后面会讲这里用到的是 `int 0x80; ret` 而非单纯的 `int 0x80`）

![shot 4](/attachments/ctfshow/stack-overflow/pwn72/04-shot-4.png)

并非 `a`。那 `/bin/sh` 呢？

![shot 5](/attachments/ctfshow/stack-overflow/pwn72/05-shot-5.png)

那确实是搜不到。如何处理这种情况并使用 ret2syscall 呢，我一点头绪都没有，所以又只好依赖别人的 wp 了。用来找找思路，具体做的时候还是自己动手。

...

进修回来了，总结下思路，就是如果 `/bin/sh` 没有，那就通过 `read` 自己造，这点我早该想到的。那么 `read` 读入 `/bin/sh` 放在哪呢，使用 `vmmap` 找到可读写段就好了。

![shot 6](/attachments/ctfshow/stack-overflow/pwn72/06-shot-6.png)

`read` 函数不好搜，搜索 `mov eax,3; ret`。

![shot 7](/attachments/ctfshow/stack-overflow/pwn72/07-shot-7.png)

乐，没有 `read` 函数，这里系统调用 `0x3` 就是 `read`。

那么现在就畅通无阻了：

![shot 8](/attachments/ctfshow/stack-overflow/pwn72/08-shot-8.png)
![shot 9](/attachments/ctfshow/stack-overflow/pwn72/09-shot-9.png)
![shot 10](/attachments/ctfshow/stack-overflow/pwn72/10-shot-10.png)

`ropper --file pwn --search "int 0x80"`

`ropper` 找指令比 `ROPgadget` 找得更全。

![shot 11](/attachments/ctfshow/stack-overflow/pwn72/11-shot-11.png)

exp：

![shot 12](/attachments/ctfshow/stack-overflow/pwn72/12-shot-12.png)
![shot 13](/attachments/ctfshow/stack-overflow/pwn72/13-shot-13.png)

`ctfshow{6aaf9702-dc0e-4108-8179-a035be138190}`
