---
title: "ctfshow 前置基础 pwn26"
published: 2026-05-08T20:50:00+08:00
description: "记录 ctfshow 前置基础 pwn26 里结合关闭 ASLR 的环境观察关键地址的过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目和分析过程：

![截图 1](/attachments/ctfshow/prerequisite-basics/pwn26/01-shot-1.png)

![截图 2](/attachments/ctfshow/prerequisite-basics/pwn26/02-shot-2.png)

重点注意 `system()` 那一行，题目已经注明了 ASLR 保护参数值存放在哪里。

```sh
echo "0" > /proc/sys/kernel/randomize_va_space
```

需要 `root` 权限。

![截图 3](/attachments/ctfshow/prerequisite-basics/pwn26/03-shot-3.png)

最终答案：

`ctfshow{0x400687_0x400560_0x603260_0x7ffff7fd64f0}`

你别说你还真别说，不用它给的那个虚拟机做，还是得不出 flag。
