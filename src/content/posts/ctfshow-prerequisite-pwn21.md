---
title: "ctfshow 前置基础 pwn21"
published: 2026-05-07T22:55:00+08:00
description: "记录 ctfshow 前置基础 pwn21 里继续判断 .got 与 .got.plt 可写性的过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：

![题目截图 1](/attachments/ctfshow/prerequisite-basics/pwn21/01-question-1.png)

![题目截图 2](/attachments/ctfshow/prerequisite-basics/pwn21/02-question-2.png)

这题和前一题基本是同一套思路，还是去看 `.got` 和 `.got.plt` 的地址，以及它们所在内存段的权限。

调试结果：

![vmmap 结果](/attachments/ctfshow/prerequisite-basics/pwn21/03-vmmap.png)

关键输出是：

```text
.got              PROGBITS         0000000000600ff0  00000ff0
.got.plt          PROGBITS         0000000000601000  00001000
0x0000000000600000 0x0000000000601000 0x0000000000000000 r-- /mnt/c/Users/34831/Desktop/pwn
0x0000000000601000 0x0000000000602000 0x0000000000001000 rw- /mnt/c/Users/34831/Desktop/pwn
```

这回能看出区别了：

- `.got` 落在 `r--` 段里，只读，不能写。
- `.got.plt` 落在 `rw-` 段里，可读可写。

所以这一题里只有 `plt` 表可写，`got` 表不可写。

最终答案：

`ctfshow{0_1_0x600ff0_0x601000}`
