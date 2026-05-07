---
title: "ctfshow 前置基础 pwn22"
published: 2026-05-07T23:00:00+08:00
description: "记录 ctfshow 前置基础 pwn22 里只剩 .got 表时的判断过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：

![题目截图 1](/attachments/ctfshow/prerequisite-basics/pwn22/01-question-1.png)

![题目截图 2](/attachments/ctfshow/prerequisite-basics/pwn22/02-question-2.png)

这题继续往下收紧，直接把 `.got.plt` 去掉了。

分析截图：

![只剩 got](/attachments/ctfshow/prerequisite-basics/pwn22/03-got-only.png)

关键结果是：

```text
.got              PROGBITS         0000000000600fc0  00000fc0

0x0000000000600000 0x0000000000601000 0x0000000000000000 r-- /mnt/c/Users/34831/Desktop/pwn
```

这时候情况就很明确了：

- `.got.plt` 不存在。
- `.got` 所在段是 `r--`，只读，不能写。

所以答案也就只剩这一种填法。

最终答案：

`ctfshow{0_0_0x600fc0}`
