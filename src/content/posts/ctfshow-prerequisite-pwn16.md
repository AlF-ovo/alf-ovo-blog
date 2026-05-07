---
title: "ctfshow 前置基础 pwn16"
published: 2026-05-07T15:49:00+08:00
description: "记录 ctfshow 前置基础 pwn16 的汇编源码编译过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：
![题目截图](/attachments/ctfshow/prerequisite-basics/pwn16/01-question.png)

这题基本就是把汇编源码直接编译成可执行文件：

```bash
gcc flag.s -o flag
./flag
```

结果截图：
![结果截图](/attachments/ctfshow/prerequisite-basics/pwn16/02-result.png)

最终答案：

`ctfshow{daniuniuda}`
