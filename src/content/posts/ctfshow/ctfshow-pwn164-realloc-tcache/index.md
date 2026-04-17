---
title: CTFshow pwn164 Realloc Tcache Poisoning WP
published: 2026-04-16
updated: 2026-04-17
description: 围绕单全局指针的 realloc/free 逻辑，先 fake stdout 泄露 libc，再把 __free_hook 改到 system。
tags: [CTFshow, Pwn, Heap, Tcache Poisoning, Realloc]
category: ctfshow
draft: false
---
# pwn164 WP

## 鍩烘湰淇℃伅

- 杩滅▼锛歚pwn.challenge.ctf.show:28240`
- 鏋舵瀯锛歚amd64`
- 淇濇姢锛歚Full RELRO / Canary / NX / PIE`
- libc锛歚glibc 2.27`

## 闄勪欢涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn164/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn164/exp.py)
- [涓嬭浇瀵瑰簲 libc `libc-2.27.so`](../../attachments/ctfshow/pwn164/libc-2.27.so)

## 绋嬪簭閫昏緫

棰樼洰鏈川涓婂彧鏈変竴涓叏灞€鍫嗘寚閽堬細

- `1. Add`
  - 璇诲叆 `size`
  - 鎵ц `ptr = realloc(ptr, size)`
  - `read(0, ptr, size)`
- `2. Delete`
  - 鐩存帴 `free(ptr)`
  - 浣?**涓嶄細缃┖**
- `3. Exit`
  - 瀹為檯鏄亣鐨勶紝鍙細鍥炲埌寰幆

杩樻湁涓€涓殣钘忓垎鏀細

- 褰撹緭鍏?`1433233`锛堝嵆 `0x15de91`锛夋椂锛?  - 鑻ヨ繕娌¤Е鍙戣繃锛屽氨鎶婂叏灞€鎸囬拡缃浂
  - 绗簩娆″啀瑙﹀彂浼氱洿鎺ラ€€鍑?
杩欑浉褰撲簬缁欎簡鎴戜滑涓€娆♀€滈噸缃叏灞€鎸囬拡浣嗕笉娓呯┖ tcache 鐘舵€佲€濈殑鏈轰細銆?
## 婕忔礊鐐?
鏍稿績鐐规湁涓や釜锛?
1. `realloc + free` 鍙搷浣滀竴涓叏灞€鎸囬拡锛屽彲浠ュ弽澶嶅湪涓嶅悓澶у皬鐨?bin 闂存惉杩?chunk銆?2. 闅愯棌鍒嗘敮 `1433233` 鍙互鍦?chunk 浠嶇暀鍦?tcache/unsorted bin 鏃舵妸鍏ㄥ眬鎸囬拡娓呴浂锛屼究浜庝笅涓€娆￠噸鏂扮敵璇峰悓灏哄 chunk銆?
杩欐牱鍙互鍒嗕袱娈靛埄鐢細

1. 鍏堟瀯閫?libc 娉勯湶
2. 鍐嶅仛 tcache poisoning锛屾敼鍐?`__free_hook` 涓?`system`

## 鍒╃敤鎬濊矾

### 1. 浼€?`stdout` 娉勯湶 libc

鍏堥€氳繃澶氭 `realloc(ptr, 0)` / `realloc(ptr, size)` 鍜?`free(ptr)` 璋冩暣鍫嗙姸鎬侊紝鎶?unsorted bin chunk 鐨勬寚閽堜綆涓ゅ瓧鑺傛敼鍒?`_IO_2_1_stdout_` 闄勮繎锛?
- `_IO_2_1_stdout_ = 0x3ec760`
- `__malloc_initialize_hook = 0x3ed8f0`
- 浣庝袱瀛楄妭瑕嗙洊鐢ㄧ殑鏄?`0xc760`

闅忓悗浼€?`stdout`锛?
- `flags = 0xfbad1800`
- 鍏朵綑璇诲啓鎸囬拡娓呴浂

杩欐牱绋嬪簭杈撳嚭鏃朵細鎶?libc 鍦板潃甯﹀嚭鏉ャ€?
璁＄畻鏂瑰紡锛?
```python
libc.address = leak + 0x40 - libc.sym["__malloc_initialize_hook"]
```

### 2. tcache poisoning 鎵?`__free_hook`

娉勯湶瀹?libc 鍚庯紝璋冪敤闅愯棌鍒嗘敮 `1433233` 鎶婂叏灞€鎸囬拡娓呴浂锛岄噸鏂板紑濮嬬浜屾鍫嗛姘淬€?
杩欐鎶?tcache 閾捐〃鎸囬拡鏀瑰埌锛?
```python
__free_hook - 8
```

鐒跺悗鐢宠鍒拌繖涓綅缃紝鍐欏叆锛?
```python
b"/bin/sh\\x00" + p64(system)
```

鍥犱负鍒嗛厤鍦板潃鏄?`__free_hook - 8`锛?
- 鍓?8 瀛楄妭鏄瓧绗︿覆 `"/bin/sh\x00"`
- 鍚?8 瀛楄妭姝ｅソ瑕嗙洊 `__free_hook`

鏈€鍚庡啀娆?`free(ptr)` 鏃讹紝灏辩瓑浠蜂簬锛?
```c
system("/bin/sh");
```

鎷垮埌 shell 鍚庢墽琛岋細

```sh
cat /flag
```

## 娉ㄦ剰鐐?
- 杩欓鍒╃敤瀵逛氦浜掕妭濂忔瘮杈冩晱鎰燂紝`read` 鐭鏃舵洿瀹规槗绋冲畾鍛戒腑銆?- 杩滅▼ flag 涓嶅湪 `/ctfshow_flag`锛屽疄闄呰矾寰勬槸 `/flag`銆?- 鎴戝湪鏈€缁?`exp.py` 閲屽姞浜嗛噸璇曢€昏緫锛岃繙绋嬩笉绋冲畾鏃朵細鑷姩閲嶈繛銆?
## Flag

```text
ctfshow{d0c0d146-fb79-43b3-8a64-520b33ea84d4}
```


