---
title: "ctfshow test_your_nc pwn0"
published: 2026-04-23T19:20:00+08:00
description: "记录 ctfshow test_your_nc 系列 pwn0 的连接与取 flag 过程。"
image: ""
tags: ["ctfshow", "test_your_nc", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "test_your_nc"]
series: "ctfshow-test_your_nc"
draft: false
lang: "zh_CN"
---

![登录信息](/attachments/ctfshow/test_your_nc/pwn0/01-login.png)

先连题目环境：

```shell
ssh ctfshow@pwn.challenge.ctf.show -p28252
name: ctfshow
passwd: 123456
```

连接之后先观察交互逻辑。

![启动界面](/attachments/ctfshow/test_your_nc/pwn0/02-banner.png)

这里会先展示一段较长动画，等待约 3 秒后进入命令行。

![命令行环境](/attachments/ctfshow/test_your_nc/pwn0/03-input.png)

简单尝试后可以发现，这里仍然会执行输入的命令，但环境里存在一些限制。

![回显测试](/attachments/ctfshow/test_your_nc/pwn0/04-echo.png)

有些指令能正常回显，但 `ls` 和 `/bin/sh` 在当前目录下没有效果。

![切回上级目录](/attachments/ctfshow/test_your_nc/pwn0/05-ls-parent.png)

往回退一个目录后再 `ls` 就成功了，说明问题不在于 `ls` 被禁用，而是当前落点目录本身有限制。

![拿到 flag](/attachments/ctfshow/test_your_nc/pwn0/06-flag.png)

flag：`ctfshow{10bbd8ff-5093-44f4-9ddb-024b4b3599c6}`
