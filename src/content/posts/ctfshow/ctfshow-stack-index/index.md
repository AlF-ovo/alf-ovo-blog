---
title: CTFshow 栈溢出知识点索引与脚本下载
published: 2026-03-26
updated: 2026-04-17
description: 汇总 CTFshow 栈题的知识点索引、利用方式分类和现有 exp 脚本下载入口。
tags: [CTFshow, Pwn, Stack Overflow, Index, Exploit]
category: ctfshow
draft: false
---
## 下载

- [下载整包脚本 `stack-scripts.zip`](../../../attachments/ctfshow/stack-scripts.zip)
- [在线浏览栈题脚本目录](../../../attachments/ctfshow/stack-scripts/)
# CTFshow 栈溢出题目知识点索引

## 一、按位数分类

### 32位题目

| 题号 | 文件名 | 考察类型 | 特殊知识点 |
|------|--------|----------|------------|
| pwn36 | pwn36-ret2text.py | ret2text | 基础栈溢出 |
| pwn37 | pwn37-ret2text.py | ret2text | 基础ret2text |
| pwn39 | pwn39-ret2text.py | ret2text | system和/bin/sh分离 |
| pwn41 | pwn41-ret2text.py | ret2text | system传参 |
| pwn43 | pwn43-ret2text.py | ret2text | gets写bss + ret2text |
| pwn45 | pwn45-ret2libc.py | ret2libc | write泄露libc |
| pwn47 | pwn47-ret2libc.py | ret2libc | puts泄露libc |
| pwn48 | pwn48-ret2libc.py | ret2libc | puts泄露 + 循环 |
| pwn49 | pwn49-ret2shellcode.py | ret2shellcode | mprotect + 静态编译 |
| pwn51 | pwn51-ret2text.py | ret2text | 字符替换绕过 |
| pwn52 | pwn52-ret2text.py | ret2text | 函数参数传递 |
| pwn53 | pwn53-ret2text-canary.py | ret2text + canary | canary爆破 |
| pwn55 | pwn55-ret2text.py | ret2text | 32位函数传参 |
| pwn58 | pwn58-ret2shellcode.py | ret2shellcode | 基础shellcode |
| pwn60 | pwn60-ret2shellcode.py | ret2shellcode | shellcode填充 |
| pwn64 | pwn64-ret2shellcode.py | ret2shellcode | mmap可执行内存 |
| pwn67 | pwn67-ret2shellcode-nop.py | ret2shellcode + nop sled | nop sled技术 |
| pwn71 | pwn71-ret2syscall.py | ret2syscall | 32位syscall |
| pwn72 | pwn72-ret2syscall.py | ret2syscall | read写bss + syscall |
| pwn73 | pwn73-ret2syscall.py | ret2syscall | 连续syscall |
| pwn75 | pwn75-栈迁移.py | 栈迁移 | leave_ret栈迁移 |
| pwn76 | pwn76-ret2text.py | ret2text | base64编码 |
| pwn79 | pwn79-ret2libc.py | ret2libc | strcpy注意点 |
| pwn82 | pwn82-ret2libc-no-relro.py | ret2libc + No RELRO | GOT表可写 |
| pwn83 | pwn83-ret2libc-partial-relro.py | ret2libc + Partial RELRO | 部分RELRO |
| pwn91 | pwn91-fmtstr.py | fmtstr | 格式化字符串写入 |
| pwn92 | pwn92-fmtstr.py | fmtstr | 格式化字符串读取 |
| pwn93 | pwn93-interactive.py | interactive | 简单交互 |
| pwn94 | pwn94-fmtstr-got.py | fmtstr + GOT | GOT表劫持 |
| pwn95 | pwn95-fmtstr-leak-got.py | fmtstr + leak + GOT | 信息泄露 + GOT表劫持 |
| pwn96 | pwn96-fmtstr-leak.py | fmtstr | 格式化字符串泄露flag |
| pwn97 | pwn97-fmtstr-write.py | fmtstr | 格式化字符串修改变量 |
| pwn98 | pwn98-fmtstr-canary.py | fmtstr + stack overflow | 泄露canary + 栈溢出 |
| pwn99 | pwn99-fmtstr-offset.py | fmtstr | 格式化字符串偏移量测试 |
| pwn100 | pwn100-fmtstr-64.py | fmtstr | 64位格式化字符串漏洞 |
| pwn111 | pwn111-stack-overflow-64.py | stack overflow | 64位栈溢出 |
| pwn112 | pwn112-stack-overflow-32.py | stack overflow | 32位栈溢出 |
| pwn113 | pwn113-rop-mprotect.py | ROP + mprotect | ROP链 + mprotect + shellcode |
| pwn114 | pwn114-stack-overflow-simple.py | stack overflow | 简单栈溢出 |
| pwn115 | pwn115-canary-bypass.py | canary bypass | Canary保护绕过 |
| pwn116 | pwn116-canary-bypass-fmt.py | canary bypass + fmtstr | 格式化字符串泄露canary |
| pwn117 | pwn117-stack-overflow-64.py | stack overflow | 64位栈溢出 |
| pwn118 | pwn118-fmtstr-got.py | fmtstr + GOT | 格式化字符串劫持GOT表 |
| pwn119 | pwn119-canary-brute.py | canary bypass | Canary爆破 |
| pwn120 | pwn120-stack-migration.py | stack migration | 栈迁移 + ROP + one_gadget |
| pwn121 | pwn121-rop-one-gadget.py | ROP + one_gadget | 64位ROP链 + one_gadget |
| pwn122 | pwn122-rop-stack-migration.py | ROP + stack migration | 32位ROP链 + 栈迁移 |
| pwn123 | pwn123-array-index.py | array index | 数组索引修改 |
| pwn124 | pwn124-shellcode.py | ret2shellcode | 32位shellcode执行 |
| pwn125 | pwn125-ret2text.py | ret2text | 64位栈溢出执行system |
| pwn126 | pwn126-ret2libc.py | ret2libc | 64位ret2libc |
| pwn127 | pwn127-ret2libc.py | ret2libc | 64位ret2libc |
| pwn128 | pwn128-vulnerability-exploit.py | vulnerability exploit | 64位漏洞利用 |
| pwn129 | pwn129-vsyscall.py | vsyscall | vsyscall区域利用 |

### 64位题目

| 题号 | 文件名 | 考察类型 | 特殊知识点 |
|------|--------|----------|------------|
| pwn38 | pwn38-ret2text.py | ret2text | 64位栈对齐 |
| pwn40 | pwn40-ret2text.py | ret2text | pop_rdi传参 |
| pwn42 | pwn42-ret2text.py | ret2text | 64位pop_rdi |
| pwn44 | pwn44-ret2text.py | ret2text | 64位gets写bss |
| pwn46 | pwn46-ret2libc.py | ret2libc | 64位write泄露 |
| pwn50 | pwn50-ret2libc.py | ret2libc | LibcSearcher使用 |
| pwn59 | pwn59-ret2shellcode.py | ret2shellcode | 64位shellcode |
| pwn61 | pwn61-ret2shellcode.py | ret2shellcode | leave影响rsp |
| pwn62 | pwn62-ret2shellcode.py | ret2shellcode | 短shellcode |
| pwn65 | pwn65-ret2shellcode.py | ret2shellcode | alpha3编码 |
| pwn66 | pwn66-ret2shellcode.py | ret2shellcode | \x00\xc0绕过 |
| pwn68 | pwn68-ret2shellcode-nop.py | ret2shellcode + nop sled | 64位nop sled |
| pwn69 | pwn69-ret2shellcode-orw.py | ret2shellcode + ORW | jmp_rsp + ORW |
| pwn70 | pwn70-ret2shellcode-orw.py | ret2shellcode + ORW | 手写ORW shellcode |
| pwn74 | pwn74-one_gadget.py | one_gadget | one_gadget使用 |
| pwn77 | pwn77-ret2libc.py | ret2libc | 数组下标覆盖 |
| pwn78 | pwn78-ret2libc.py | ret2libc | \x18控制转移 |
| pwn81 | pwn81-ret2libc.py | ret2libc | system地址泄露 |
| pwn84 | pwn84-ret2libc-no-relro.py | ret2libc + No RELRO | 64位No RELRO |
| pwn85 | pwn85-ret2libc-partial-relro.py | ret2libc + Partial RELRO | 64位Partial RELRO |
| pwn100 | pwn100-fmtstr-64.py | fmtstr | 64位格式化字符串漏洞 |
| pwn111 | pwn111-stack-overflow-64.py | stack overflow | 64位栈溢出 |
| pwn113 | pwn113-rop-mprotect.py | ROP + mprotect | ROP链 + mprotect + shellcode |
| pwn117 | pwn117-stack-overflow-64.py | stack overflow | 64位栈溢出 |
| pwn120 | pwn120-stack-migration.py | stack migration | 栈迁移 + ROP + one_gadget |
| pwn121 | pwn121-rop-one-gadget.py | ROP + one_gadget | 64位ROP链 + one_gadget |
| pwn125 | pwn125-ret2text.py | ret2text | 64位栈溢出执行system |
| pwn126 | pwn126-ret2libc.py | ret2libc | 64位ret2libc |
| pwn127 | pwn127-ret2libc.py | ret2libc | 64位ret2libc |
| pwn128 | pwn128-vulnerability-exploit.py | vulnerability exploit | 64位漏洞利用 |
| pwn129 | pwn129-vsyscall.py | vsyscall | vsyscall区域利用 |

---

## 二、按攻击方式分类

### ret2text
- **基础**: pwn36, pwn37
- **64位栈对齐**: pwn38
- **system和/bin/sh分离**: pwn39
- **pop_rdi传参**: pwn40, pwn42
- **函数参数传递**: pwn52, pwn55
- **字符替换绕过**: pwn51
- **base64编码**: pwn76
- **64位执行system**: pwn125

### ret2libc
- **32位write泄露**: pwn45
- **32位puts泄露**: pwn47, pwn48
- **64位write泄露**: pwn46, pwn50
- **数组下标覆盖**: pwn77, pwn78
- **system地址泄露**: pwn81
- **strcpy注意点**: pwn79
- **64位ret2libc**: pwn126, pwn127

### ret2shellcode
- **基础32位**: pwn58, pwn60, pwn64, pwn124
- **基础64位**: pwn59, pwn61, pwn62
- **alpha3编码**: pwn65
- **\x00\xc0绕过**: pwn66
- **nop sled**: pwn67, pwn68

### ret2shellcode + ORW
- **jmp_rsp**: pwn69
- **手写ORW**: pwn70

### ret2syscall
- **32位基础**: pwn71
- **read写bss**: pwn72
- **连续syscall**: pwn73

### one_gadget
- **基础**: pwn74

### 栈迁移
- **leave_ret**: pwn75

### ret2text + canary
- **canary爆破**: pwn53

### ret2libc + RELRO
- **No RELRO 32位**: pwn82, pwn83
- **No RELRO 64位**: pwn84
- **Partial RELRO 64位**: pwn85

### fmtstr
- **基础写入**: pwn91, pwn97
- **基础读取**: pwn92
- **GOT表劫持**: pwn94, pwn118
- **信息泄露 + GOT表劫持**: pwn95
- **泄露flag**: pwn96
- **泄露canary**: pwn98
- **偏移量测试**: pwn99
- **64位格式化字符串**: pwn100

### interactive
- **简单交互**: pwn93

### stack overflow
- **32位基础**: pwn112
- **64位基础**: pwn111, pwn117
- **简单栈溢出**: pwn114

### canary bypass
- **栈溢出泄露canary**: pwn115
- **格式化字符串泄露canary**: pwn116

### ROP + mprotect
- **ROP链 + mprotect + shellcode**: pwn113

### stack migration
- **栈迁移 + ROP + one_gadget**: pwn120

### ROP + one_gadget
- **64位ROP链 + one_gadget**: pwn121

### ROP + stack migration
- **32位ROP链 + 栈迁移**: pwn122

### array index
- **数组索引修改**: pwn123

### vulnerability exploit
- **64位漏洞利用**: pwn128

### vsyscall
- **vsyscall区域利用**: pwn129

---

## 三、共性考察点

### 1. 栈溢出基础
- 所有题目都涉及栈溢出漏洞利用
- 需要计算准确的offset（偏移量）
- 理解栈帧结构和返回地址覆盖

### 2. 函数调用约定
- **32位**: 参数通过栈传递
- **64位**: 参数通过寄存器传递（rdi, rsi, rdx, rcx, r8, r9）

### 3. 地址泄露
- GOT表泄露libc地址
- 利用write/puts等函数泄露
- 计算libc基址和函数偏移

### 4. 保护机制绕过
- **Canary**: 爆破或泄露
- **NX**: 使用ret2text/ret2libc/ret2syscall
- **RELRO**: No RELRO可写GOT表

---

## 四、区分度查找

### 按难度分级

**入门**: pwn36, pwn37, pwn38, pwn39, pwn58, pwn59, pwn64
**进阶**: pwn40, pwn41, pwn42, pwn45, pwn47, pwn60, pwn61
**中等**: pwn43, pwn44, pwn46, pwn48, pwn50, pwn51, pwn52, pwn53
**较难**: pwn62, pwn65, pwn66, pwn67, pwn68, pwn69, pwn70
**困难**: pwn71, pwn72, pwn73, pwn74, pwn75, pwn77, pwn78

### 按特殊技术

**需要编码**: pwn65 (alpha3), pwn76 (base64)
**需要爆破**: pwn53 (canary)
**需要栈迁移**: pwn75
**需要ORW**: pwn69, pwn70
**需要syscall**: pwn71, pwn72, pwn73
**需要nop sled**: pwn67, pwn68

---

## 五、文件清单

```
pwn36-ret2text.py
pwn37-ret2text.py
pwn38-ret2text.py
pwn39-ret2text.py
pwn40-ret2text.py
pwn41-ret2text.py
pwn42-ret2text.py
pwn43-ret2text.py
pwn44-ret2text.py
pwn45-ret2libc.py
pwn46-ret2libc.py
pwn47-ret2libc.py
pwn48-ret2libc.py
pwn49-ret2shellcode.py
pwn50-ret2libc.py
pwn51-ret2text.py
pwn52-ret2text.py
pwn53-ret2text-canary.py
pwn55-ret2text.py
pwn58-ret2shellcode.py
pwn59-ret2shellcode.py
pwn60-ret2shellcode.py
pwn61-ret2shellcode.py
pwn62-ret2shellcode.py
pwn64-ret2shellcode.py
pwn65-ret2shellcode.py
pwn66-ret2shellcode.py
pwn67-ret2shellcode-nop.py
pwn68-ret2shellcode-nop.py
pwn69-ret2shellcode-orw.py
pwn70-ret2shellcode-orw.py
pwn71-ret2syscall.py
pwn72-ret2syscall.py
pwn73-ret2syscall.py
pwn74-one_gadget.py
pwn75-栈迁移.py
pwn76-ret2text.py
pwn77-ret2libc.py
pwn78-ret2libc.py
pwn79-ret2libc.py
pwn81-ret2libc.py
pwn82-ret2libc-no-relro.py
pwn83-ret2libc-partial-relro.py
pwn84-ret2libc-no-relro.py
pwn85-ret2libc-partial-relro.py
pwn91-fmtstr.py
pwn92-fmtstr.py
pwn93-interactive.py
pwn94-fmtstr-got.py
pwn95-fmtstr-leak-got.py
pwn96-fmtstr-leak.py
pwn97-fmtstr-write.py
pwn98-fmtstr-canary.py
pwn99-fmtstr-offset.py
pwn100-fmtstr-64.py
pwn111-stack-overflow-64.py
pwn112-stack-overflow-32.py
pwn113-rop-mprotect.py
pwn114-stack-overflow-simple.py
pwn115-canary-bypass.py
pwn116-canary-bypass-fmt.py
pwn117-stack-overflow-64.py
pwn118-fmtstr-got.py
pwn119-canary-brute.py
pwn120-stack-migration.py
pwn121-rop-one-gadget.py
pwn122-rop-stack-migration.py
pwn123-array-index.py
pwn124-shellcode.py
pwn125-ret2text.py
pwn126-ret2libc.py
pwn127-ret2libc.py
pwn128-vulnerability-exploit.py
pwn129-vsyscall.py
```

ROPgadget --binary pwn --ropchain(one_gadget一把梭)
