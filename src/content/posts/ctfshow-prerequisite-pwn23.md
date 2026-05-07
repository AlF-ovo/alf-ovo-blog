---
title: "ctfshow 前置基础 pwn23"
published: 2026-05-07T23:22:00+08:00
description: "记录 ctfshow 前置基础 pwn23 里借栈溢出触发 SIGSEGV 处理函数的过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：

![题目截图 1](/attachments/ctfshow/prerequisite-basics/pwn23/01-question-1.png)

![题目截图 2](/attachments/ctfshow/prerequisite-basics/pwn23/02-question-2.png)

题目逻辑大概是这样：

![整体逻辑](/attachments/ctfshow/prerequisite-basics/pwn23/03-overview.png)

这里先要搞清楚 `argc` 是什么。通俗点说，`argc` 就是命令行参数的数量。

比如：

- 只执行 `./pwnme`，那 `argc` 就是 1。
- 执行 `./pwnme aaa`，那 `argc` 就是 2。
- 再多加一个参数，`argc` 就会继续往上加。

在这题里，只要 `argc > 1`，就会触发 `ctfshow` 函数，并把 `./pwnme` 后面的第一个参数当成它的输入。问题就在于这个函数里有明显的栈溢出。

后面要借的是 `sigsegv_handler`。`SIGSEGV` 也就是 Segmentation Fault，表示程序访问了非法内存地址。常见原因包括空指针、野指针、越界访问、写只读内存这些。

这题里反而要主动把它打出来，因为触发崩溃之后会进入对应的处理函数。

处理函数位置：

![handler 分析](/attachments/ctfshow/prerequisite-basics/pwn23/04-handler.png)

也就是说，利用思路不是正常返回，而是故意让溢出把程序打进 `sigsegv_handler`，借这个异常处理流程拿 flag。

最后跑通后的结果：

![结果截图](/attachments/ctfshow/prerequisite-basics/pwn23/05-result.png)

最终答案：

`ctfshow{949252f0-fc75-4b4b-8dbf-e3f21b666c53}`
