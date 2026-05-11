---
title: "baby_shellcode（2023愚人杯）"
published: 2026-05-11T00:00:00+08:00
description: "记录 baby_shellcode 的初步逆向与思路整理。"
image: ""
tags: ["ctfshow", "Pwn", "shellcode", "逆向", "2023愚人杯"]
category: "ctfshow"
categoryPath: ["ctfshow", "草稿"]
series: "ctfshow-草稿"
draft: true
lang: "zh_CN"
---

![截图 1](/attachments/ctfshow/drafts/baby-shellcode-2023-yurenbei/01-overview.png)
![截图 2](/attachments/ctfshow/drafts/baby-shellcode-2023-yurenbei/02-file-type.png)

不是 xd，这是什么，`.shellcode`？！

所幸能用 IDA 打开，只是只有三个函数：

![截图 3](/attachments/ctfshow/drafts/baby-shellcode-2023-yurenbei/03-func-list.png)
![截图 4](/attachments/ctfshow/drafts/baby-shellcode-2023-yurenbei/04-read-func.png)
![截图 5](/attachments/ctfshow/drafts/baby-shellcode-2023-yurenbei/05-start-flow.png)

`sub_4000E1` 的作用很明显是一个 `read`，只能读入 9 个字符；
`start` 是程序入口，它先调用了一次 `sub_4000E1` 再调用一次 `sub_4000F9`，然后程序就退出了。
`sub_4000F9` 这里需要一定的逆向功底。

![截图 6](/attachments/ctfshow/drafts/baby-shellcode-2023-yurenbei/06-xor-48.png)

这里有个异或 48，也就是说 payload 写好之后要异或 48，毕竟异或的解密和加密方式是同一套。

这里我没有思路了，去看了别的 blog。
我这才知道说，通过写汇编语言的方式压缩字节，可以在特定情况下，把 `read` 指令在 9 字节的读取完成，从而读取一个较大块的 shellcode。具体原理我还是不很清楚，这是汇编语言很细的知识点了。
