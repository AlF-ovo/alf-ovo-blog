---
title: "御网杯 PWN UserManager"
published: 2026-05-30T16:46:03+08:00
description: "Delete 存在 UAF，原始 Word 记录主要以截图为主。"
image: ""
tags: ["御网杯PWN2026", "Pwn", "UAF", "Heap"]
category: "《御网杯PWN2026》"
categoryPath: ["《御网杯PWN2026》"]
series: "御网杯PWN2026"
draft: false
lang: "zh_CN"
---

附件：[`PWN-UserManager.docx`](/attachments/《御网杯PWN2026》/PWN-UserManager.docx)

原始 WP 中能直接提取出的正文文字较少，核心内容主要在截图里。已有文字记录如下：

> 可以看到，Delete 函数存在 UAF 漏洞，就和题目提示说的一致。

题目附件截图：

![截图 1](/attachments/《御网杯PWN2026》/pwn-usermanager/01.png)

![截图 2](/attachments/《御网杯PWN2026》/pwn-usermanager/02.png)

从截图可以先看到程序保护情况：

- Full RELRO
- Canary found
- NX enabled
- PIE enabled

漏洞点截图：

![Register 逻辑](/attachments/《御网杯PWN2026》/pwn-usermanager/03.png)

![Delete 逻辑](/attachments/《御网杯PWN2026》/pwn-usermanager/04.png)

从 `Delete` 的伪代码可以直接看到：

- `free(users[id]->data);`
- `free(users[id]);`
- 但释放后没有把 `users[id]` 清空

因此这里形成了一个典型的 UAF 条件，后续利用可以围绕悬空指针展开。当前先按原始 Word 内容与截图归档，后续如果你要，我可以再把这篇补成完整的文字版利用过程和 exp。
