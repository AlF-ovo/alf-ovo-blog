---
title: "ctfshow stack overflow pwn54"
published: 2026-05-13T23:10:29+08:00
description: "Writeup for ctfshow stack overflow pwn54."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "infoleak", "strcat"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

![shot 1](/attachments/ctfshow/stack-overflow/pwn54/01-shot-1.png)

![shot 2](/attachments/ctfshow/stack-overflow/pwn54/02-shot-2.png)

![shot 3](/attachments/ctfshow/stack-overflow/pwn54/03-shot-3.png)

![shot 4](/attachments/ctfshow/stack-overflow/pwn54/04-shot-4.png)

`strcat` 之后会有栈溢出，覆盖 `\n` 导致一个 `puts` 把后面一大坨东西都顺了出来，包括 `password`。因为 `puts` 是看到 `\n` 再截止输出。

exp:

![shot 5](/attachments/ctfshow/stack-overflow/pwn54/05-shot-5.png)

一下子就把 `password` 顺出来了。

第二次登录输入 `CTFshow_PWN_r00t_p@ssw0rd_1s_h3r3` 作为 `password`。

![shot 6](/attachments/ctfshow/stack-overflow/pwn54/06-shot-6.png)

`ctfshow{b96a9336-2383-4ef0-959e-402f82e22c1d}`
