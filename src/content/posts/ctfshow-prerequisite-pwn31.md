---
title: "ctfshow 前置基础 pwn31"
published: 2026-05-10T22:30:00+08:00
description: "记录 ctfshow 前置基础 pwn31 的解题过程与关键利用点。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目先泄露了 `main` 的地址，可以据此反推出其他函数地址。

![截图 1](/attachments/ctfshow/prerequisite-basics/pwn31/01-shot-1.png)
![截图 2](/attachments/ctfshow/prerequisite-basics/pwn31/02-shot-2.png)
![截图 3](/attachments/ctfshow/prerequisite-basics/pwn31/03-shot-3.png)

起初尝试 `ret2libc` 失败，泄露值不是有效 libc 地址（不像 `0xf7xxxxxx` / `0xf6xxxxxx`）。

![截图 4](/attachments/ctfshow/prerequisite-basics/pwn31/04-shot-4.png)
![截图 5](/attachments/ctfshow/prerequisite-basics/pwn31/05-shot-5.png)

关键点是 `ebx` 参与了 GOT 泄露流程。由于溢出覆盖导致 `ebx` 异常，需要手动恢复。
根据题目泄露的程序基址和偏移关系，可构造正确的 `ebx`：

`ebx = base + 0x1FC0`

![截图 6](/attachments/ctfshow/prerequisite-basics/pwn31/06-shot-6.png)
![截图 7](/attachments/ctfshow/prerequisite-basics/pwn31/07-shot-7.png)
![截图 8](/attachments/ctfshow/prerequisite-basics/pwn31/08-shot-8.png)
![截图 9](/attachments/ctfshow/prerequisite-basics/pwn31/09-shot-9.png)

在第一次 payload 中伪造 `ebx` 后，泄露流程恢复正常。

![截图 10](/attachments/ctfshow/prerequisite-basics/pwn31/10-shot-10.png)
![截图 11](/attachments/ctfshow/prerequisite-basics/pwn31/11-shot-11.png)
![截图 12](/attachments/ctfshow/prerequisite-basics/pwn31/12-shot-12.png)

最终答案：

`ctfshow{c8748e3b-0cf1-4689-9640-6b7d18019f79}`

另一个可行思路是利用 `write` 而不是 `read` 完成泄露与利用：

![截图 13](/attachments/ctfshow/prerequisite-basics/pwn31/13-shot-13.png)
![截图 14](/attachments/ctfshow/prerequisite-basics/pwn31/14-shot-14.png)
