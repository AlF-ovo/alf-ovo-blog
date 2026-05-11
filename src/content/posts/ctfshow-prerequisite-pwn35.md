---
title: "ctfshow 前置基础 pwn35"
published: 2026-05-11T00:10:00+08:00
description: "记录 ctfshow 前置基础 pwn35 的解题过程与关键现象。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn", "Stack Overflow", "SIGSEGV"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

![截图 1](/attachments/ctfshow/prerequisite-basics/pwn35/01-shot-1.png)
![截图 2](/attachments/ctfshow/prerequisite-basics/pwn35/02-shot-2.png)

专属镜像用户名 `ctfshow`，密码 `ctfshow`。  
我平时使用的是 `wsl`，这里改用虚拟机继续测试。

![截图 3](/attachments/ctfshow/prerequisite-basics/pwn35/03-shot-3.png)
![截图 4](/attachments/ctfshow/prerequisite-basics/pwn35/04-shot-4.png)
![截图 5](/attachments/ctfshow/prerequisite-basics/pwn35/05-shot-5.png)

当栈溢出时，触发 `sigsegv_hander` 报错（访问非法内存）会输出 flag。

![截图 6](/attachments/ctfshow/prerequisite-basics/pwn35/06-shot-6.png)
![截图 7](/attachments/ctfshow/prerequisite-basics/pwn35/07-shot-7.png)

最终答案：

`ctfshow{4e55938d-915f-4dfc-aab4-d3d946f4d7fd}`
