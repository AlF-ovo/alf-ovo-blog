---
title: "ctfshow 前置基础 pwn13"
published: 2026-05-06T21:26:00+08:00
description: "记录 ctfshow 前置基础 pwn13 的 GCC 编译与结果观察过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：
![题目截图](/attachments/ctfshow/prerequisite-basics/pwn13/01-question.png)

分析截图：
![分析截图](/attachments/ctfshow/prerequisite-basics/pwn13/02-analysis.png)

其实这题不用 GCC 编译也可以直接做。虽然但是，尊重题目，还是用 GCC 编译一下看看：

```bash
gcc hello.c -o hello
```

编译截图：
![编译截图](/attachments/ctfshow/prerequisite-basics/pwn13/03-build.png)

结果截图：
![结果截图](/attachments/ctfshow/prerequisite-basics/pwn13/04-result.png)

最终答案：

`ctfshow{hOw_t0_us3_GCC?}`
