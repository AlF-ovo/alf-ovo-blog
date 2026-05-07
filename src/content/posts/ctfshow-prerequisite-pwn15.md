---
title: "ctfshow 前置基础 pwn15"
published: 2026-05-07T15:44:00+08:00
description: "记录 ctfshow 前置基础 pwn15 的汇编编译与链接过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：
![题目截图](/attachments/ctfshow/prerequisite-basics/pwn15/01-question.png)

这题就是把汇编代码编译成可执行文件，流程上分成编译和链接两步。

### 1. 编译

32 位系统：

```bash
nasm test.asm -o test.o
```

64 位系统：

```bash
nasm -f elf64 test.asm -o test.o
```

### 2. 链接

```bash
ld -s test.o -o test
```

实际做的时候链接阶段报错，后面排查下来就是 `ld` 默认按 64 位处理，而 `nasm` 这边的目标格式如果没统一，就会出现位数不匹配。把目标格式统一之后就能正常出结果。

结果截图：
![结果截图](/attachments/ctfshow/prerequisite-basics/pwn15/02-result.png)

最终答案：

`ctfshow{@ss3mb1y_1s_3@sy}`
