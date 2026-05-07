---
title: "ctfshow 前置基础 pwn14"
published: 2026-05-07T15:30:00+08:00
description: "记录 ctfshow 前置基础 pwn14 的 key 文件写入与编译运行过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：
![题目截图](/attachments/ctfshow/prerequisite-basics/pwn14/01-question.png)

分析截图：
![分析截图](/attachments/ctfshow/prerequisite-basics/pwn14/02-analysis.png)

一开始我没理解题目里“给定 key 为 `CTFshow`”的意思，所以先在本地新建了一个 `key.txt` 文档，把 `CTFshow` 放进去。后来才发现，题目真正需要的是创建一个名为 `key` 的文件。

正确做法是：

```bash
echo "CTFshow" > key
gcc flag.c -o flag
./flag
```

结果截图：
![结果截图](/attachments/ctfshow/prerequisite-basics/pwn14/03-result.png)

最终答案：

`ctfshow{01000011_01010100_01000110_01110011_01101000_01101111_01110111_00001010}`
