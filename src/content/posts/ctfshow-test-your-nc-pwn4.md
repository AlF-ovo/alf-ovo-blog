---
title: "ctfshow test_your_nc pwn4"
published: 2026-04-23T19:24:00+08:00
description: "记录 ctfshow test_your_nc 系列 pwn4 的分析与取 flag 过程。"
image: ""
tags: ["ctfshow", "test_your_nc", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "test_your_nc"]
series: "ctfshow-test_your_nc"
draft: false
lang: "zh_CN"
---

![程序逻辑](/attachments/ctfshow/test_your_nc/pwn4/01-logic.png)

![关键比较](/attachments/ctfshow/test_your_nc/pwn4/02-compare.png)

当 `s1 == s2` 时会 getshell。`s1` 是 `CTFshowPWN`，`s2` 是读取的用户输入，所以直接输入 `CTFshowPWN` 即可获取 flag。

![拿到 flag](/attachments/ctfshow/test_your_nc/pwn4/03-flag.png)

flag：`ctfshow{1320fb82-5ff9-4a09-9e14-14334f603f04}`
