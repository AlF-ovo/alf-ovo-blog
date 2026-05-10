---
title: "ctfshow 前置基础 pwn32"
published: 2026-05-10T22:40:00+08:00
description: "记录 ctfshow 前置基础 pwn32 解题过程与 FORTIFY_SOURCE=0 基础知识。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn", "FORTIFY_SOURCE"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目利用本身不复杂，满足参数条件即可拿到结果：

![截图 1](/attachments/ctfshow/prerequisite-basics/pwn32/01-shot-1.png)
![截图 2](/attachments/ctfshow/prerequisite-basics/pwn32/02-shot-2.png)
![截图 3](/attachments/ctfshow/prerequisite-basics/pwn32/03-shot-3.png)
![截图 4](/attachments/ctfshow/prerequisite-basics/pwn32/04-shot-4.png)
![截图 5](/attachments/ctfshow/prerequisite-basics/pwn32/05-shot-5.png)

最终答案：

`ctfshow{75290787-66c0-4083-8b8a-6f1cc046a3c1}`

## 知识点：FORTIFY_SOURCE=0

- `FORTIFY_SOURCE=0` 表示关闭 Fortify 加固检查。
- 关闭后，不会插入额外的 `_chk` 保护调用，也不会执行对应运行时边界检查。
- 题目里强调 “理解这些保护机制”，核心就是区分“功能可利用”和“编译期/运行期加固是否开启”。
