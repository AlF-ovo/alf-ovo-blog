---
title: "ctfshow 前置基础 pwn25"
published: 2026-05-08T19:01:00+08:00
description: "记录 ctfshow 前置基础 pwn25 里在 NX 开启时通过 ret2libc 处理 32 位栈溢出的过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目和分析过程：

![截图 1](/attachments/ctfshow/prerequisite-basics/pwn25/01-shot-1.png)

![截图 2](/attachments/ctfshow/prerequisite-basics/pwn25/02-shot-2.png)

`NX enabled`，代表的是栈不可执行。栈上的数据不能被当做代码执行。这种时候，构造 ROP 链打 `ret2libc` 是可行的一种方式。

![截图 3](/attachments/ctfshow/prerequisite-basics/pwn25/03-shot-3.png)

`0x100` 明显大于 `132`。再点开详细确认下，有时 IDA 会骗人。

![截图 4](/attachments/ctfshow/prerequisite-basics/pwn25/04-shot-4.png)

总之，要覆盖到返回地址，要覆盖 `0x88`，也就是 `128 + 4 = 132`，是对的。这题就是标准的 32 位 `ret2libc`。

编写 exp：

![截图 5](/attachments/ctfshow/prerequisite-basics/pwn25/05-shot-5.png)

![截图 6](/attachments/ctfshow/prerequisite-basics/pwn25/06-shot-6.png)

![截图 7](/attachments/ctfshow/prerequisite-basics/pwn25/07-shot-7.png)

最终答案：

`ctfshow{76e31863-e48c-4b4e-a75d-d6668cd20387}`
