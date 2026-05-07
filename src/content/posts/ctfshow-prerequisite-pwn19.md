---
title: "ctfshow 前置基础 pwn19"
published: 2026-05-07T22:23:00+08:00
description: "记录 ctfshow 前置基础 pwn19 在 stdout 被关闭后，怎样把回显重新绑回远程 socket。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：

![题目截图 1](/attachments/ctfshow/prerequisite-basics/pwn19/01-question-1.png)

![题目截图 2](/attachments/ctfshow/prerequisite-basics/pwn19/02-question-2.png)

![题目截图 3](/attachments/ctfshow/prerequisite-basics/pwn19/03-overview.png)

这题的关键点很直接：程序把 `stdout` 给关掉了，所以想靠正常回显拿结果是行不通的。

![stdout 被关闭](/attachments/ctfshow/prerequisite-basics/pwn19/04-stdout-closed.png)

中间顺手补了一下 `if (fork())` 的用法：

![fork 说明](/attachments/ctfshow/prerequisite-basics/pwn19/05-fork-note.png)

参考：
[Linux 进程 父进程与子进程（详细篇）](https://blog.csdn.net/qq_66337990/article/details/132589191)

那怎么办？既然它把标准输出关了，那就自己再造一个 `stdout`。

我之前参考过一篇把 `pwn18` 和 `pwn19` 放在一起讲的文章，但那篇在这个点上的结论有误，容易把思路带偏：
[CTFshow PWN 前置基础（pwn18-pwn19）](https://blog.csdn.net/Myon5/article/details/137891670)

最后用的命令是：

```bash
exec cat /ctfshow_flag 1>&0
```

![payload](/attachments/ctfshow/prerequisite-basics/pwn19/06-payload.png)

这里的 `1>&0` 是重定向写法，把文件描述符 `1`（标准输出）绑定到文件描述符 `0`（标准输入）指向的同一个位置。因为远程连接的 socket 还连着标准输入，所以把标准输出也绑过去之后，就等于重新拿回了回显通道。

最后结果：

![结果截图](/attachments/ctfshow/prerequisite-basics/pwn19/07-result.png)

最终答案：

`ctfshow{8c8551ae-3c9f-4a37-857b-2c1a11e2a501}`
