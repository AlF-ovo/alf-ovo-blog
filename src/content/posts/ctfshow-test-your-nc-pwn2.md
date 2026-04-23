---
title: "ctfshow test_your_nc pwn2"
published: 2026-04-23T19:22:00+08:00
description: "记录 ctfshow test_your_nc 系列 pwn2 的解题过程。"
image: ""
tags: ["ctfshow", "test_your_nc", "Pwn"]
category: "ctfshow/test_your_nc"
draft: false
lang: "zh_CN"
---

![连接后的界面](/alf-ovo-blog/attachments/ctfshow/test_your_nc/pwn2/01-landing.png)

![获得 shell](/alf-ovo-blog/attachments/ctfshow/test_your_nc/pwn2/02-shell.png)

题目直接给了 shell，之后就是 `nc` 连入，执行 `ls` 和 `cat flag` 即可。

![拿到 flag](/alf-ovo-blog/attachments/ctfshow/test_your_nc/pwn2/03-flag.png)

flag：`ctfshow{cd156ccc-1ae0-49ab-9850-75cd1fa7bb3f}`
