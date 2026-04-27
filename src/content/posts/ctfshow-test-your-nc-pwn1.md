---
title: "ctfshow test_your_nc pwn1"
published: 2026-04-23T19:21:00+08:00
description: "记录 ctfshow test_your_nc 系列 pwn1 的分析与取 flag 过程。"
image: ""
tags: ["ctfshow", "test_your_nc", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "test_your_nc"]
series: "ctfshow-test_your_nc"
draft: false
lang: "zh_CN"
---

![程序信息](/attachments/ctfshow/test_your_nc/pwn1/01-checksec.png)

![反汇编结果](/attachments/ctfshow/test_your_nc/pwn1/02-disasm.png)

反汇编看一眼就能知道，直接用 `nc` 连上即可获得 flag。

![拿到 flag](/attachments/ctfshow/test_your_nc/pwn1/03-flag.png)

flag：`ctfshow{7badceb1-c0ce-4acd-b119-48b6cc2a8ab3}`
