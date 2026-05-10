---
title: "ctfshow 前置基础 pwn34"
published: 2026-05-10T23:00:00+08:00
description: "记录 ctfshow 前置基础 pwn34 与 FORTIFY_SOURCE=2 的知识点。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn", "FORTIFY_SOURCE"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

本题与 pwn32/33 的利用过程同类，关键是理解加固级别差异：

![截图 1](/attachments/ctfshow/prerequisite-basics/pwn34/01-shot-1.png)
![截图 2](/attachments/ctfshow/prerequisite-basics/pwn34/02-shot-2.png)
![截图 3](/attachments/ctfshow/prerequisite-basics/pwn34/03-shot-3.png)
![截图 4](/attachments/ctfshow/prerequisite-basics/pwn34/04-shot-4.png)

最终答案：

`ctfshow{4c96d8ce-f286-46b3-9b39-de34633c67c3}`

## 知识点：FORTIFY_SOURCE=2

- `FORTIFY_SOURCE=2` 是常见的默认强化级别（在发行版构建中经常出现）。
- 相比级别 1，编译器会尽可能做更严格的对象大小推断并插入更激进的检查。
- 对明显不安全调用更容易在编译期告警，运行时也更容易触发检查失败。
