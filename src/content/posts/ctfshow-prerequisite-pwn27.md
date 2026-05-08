---
title: "ctfshow 前置基础 pwn27"
published: 2026-05-08T21:30:00+08:00
description: "记录 ctfshow 前置基础 pwn27 里在开启 ASLR 时继续确认关键地址的过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目和分析过程：

![截图 1](/attachments/ctfshow/prerequisite-basics/pwn27/01-shot-1.png)

![截图 2](/attachments/ctfshow/prerequisite-basics/pwn27/02-shot-2.png)

这题和 `pwn26` 的区别，就在于这里把 ASLR 打开了：

```sh
echo "1" > /proc/sys/kernel/randomize_va_space
```

![截图 3](/attachments/ctfshow/prerequisite-basics/pwn27/03-shot-3.png)

懂得都懂，这不是正确的虚拟机，这只是 WSL。在奇怪的地方，WSL 反而不如虚拟机好用。

最终答案：

`ctfshow{0x400687_0x400560_0x603260}`
