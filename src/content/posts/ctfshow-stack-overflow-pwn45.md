---
title: "ctfshow stack overflow pwn45"
published: 2026-05-12T15:00:00+08:00
description: "Writeup for ctfshow stack overflow pwn45."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ROP", "ret2libc"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

![shot 1](/attachments/ctfshow/stack-overflow/pwn45/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn45/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn45/03-shot-3.png)
![shot 4](/attachments/ctfshow/stack-overflow/pwn45/04-shot-4.png)

这次我是真一点招都没了。先去看了看别人写的 wp。[CTFshow-PWN-栈溢出（pwn45）](https://blog.csdn.net/Myon5/article/details/138815469)

![shot 5](/attachments/ctfshow/stack-overflow/pwn45/05-shot-5.png)
![shot 6](/attachments/ctfshow/stack-overflow/pwn45/06-shot-6.png)

思路为利用 got 函数泄露 libc，然后从 libc 里拿 `system` 函数与 `/bin/sh` 字符串。
我记起来了！这才是最纯粹的 ret2libc！

![shot 7](/attachments/ctfshow/stack-overflow/pwn45/07-shot-7.png)

main 函数里调用过了一次 `puts` 函数，所以这次使用的时候可以直接拿 got 表的地址，而不需要考虑延迟绑定机制。

![shot 8](/attachments/ctfshow/stack-overflow/pwn45/08-shot-8.png)

第一次泄露的时候 `puts_real` 的地址没出来，因为我不很熟悉这里的回显逻辑。

![shot 9](/attachments/ctfshow/stack-overflow/pwn45/09-shot-9.png)

exp：

![shot 10](/attachments/ctfshow/stack-overflow/pwn45/10-shot-10.png)

在这里我第一个 payload 使用了 `flat` 函数而第二个 payload 没有使用，权当做一个对比，做一次尝试。当然，使用 `cyclic` 函数，不使用 `b"A" * offsets` 也是一种尝试。

本题我使用的是 `puts` 来泄露 libc 基址，而当然使用 `write` 函数也是 OK 的。方法见[ctfshow pwn45](https://blog.csdn.net/weixin_68408599/article/details/153638578?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-153638578-blog-138815469.235%5Ev43%5Epc_blog_bottom_relevance_base5&spm=1001.2101.3001.4242.1&utm_relevant_index=3)。

![shot 11](/attachments/ctfshow/stack-overflow/pwn45/11-shot-11.png)
![shot 12](/attachments/ctfshow/stack-overflow/pwn45/12-shot-12.png)

`ctfshow{b35732c3-b5aa-4d24-9461-5f773460c4ac}`
