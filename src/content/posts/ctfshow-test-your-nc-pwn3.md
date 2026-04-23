---
title: "ctfshow test_your_nc pwn3"
published: 2026-04-23T19:23:00+08:00
description: "记录 ctfshow test_your_nc 系列 pwn3 的分析与取 flag 过程。"
image: ""
tags: ["ctfshow", "test_your_nc", "Pwn"]
category: "ctfshow/test_your_nc"
draft: false
lang: "zh_CN"
---

![程序逻辑](/alf-ovo-blog/attachments/ctfshow/test_your_nc/pwn3/01-main.png)

![case 分析](/alf-ovo-blog/attachments/ctfshow/test_your_nc/pwn3/02-case.png)

![选择 6](/alf-ovo-blog/attachments/ctfshow/test_your_nc/pwn3/03-choose-6.png)

看过逻辑后就能确定答案是 `case 6`。  
`nc` 连入后选择 `6`，直接拿 flag。

![拿到 flag](/alf-ovo-blog/attachments/ctfshow/test_your_nc/pwn3/04-flag.png)

flag：`ctfshow{7796c338-38ad-4107-8cf6-5cbb4ec232b5}`
