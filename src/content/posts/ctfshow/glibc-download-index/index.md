---
title: 常用 glibc / libc 下载索引与利用差异说明
published: 2026-04-17
updated: 2026-04-17
description: 整理 Ubuntu 16/18/19/20 常见 32 位和 64 位 libc 下载链接，并从 PWN 利用角度说明版本差异。
tags: [glibc, libc, Pwn, Linux, Toolchain]
category: ctfshow
draft: false
---
杩欑瘒鏂囩珷鎶婃垜鎵嬪ご甯哥敤鐨?`glibc / libc.so` 鐗堟湰鍏堟暣鐞嗘垚涓€涓珯鍐呬笅杞界储寮曪紝鍚庣画鍋氶鏃跺氨涓嶇敤姣忔鍐嶇炕鏈湴鐩綍銆?
## 鏁村寘涓嬭浇

- [涓嬭浇鏁村寘锛歭ibcs.zip](../../attachments/ctfshow/libcs.zip)

## 鍗曟枃浠朵笅杞?
| Ubuntu 鐜 | 32 浣?| 64 浣?|
| --- | --- | --- |
| Ubuntu 16.04 / glibc 2.23 | [libc-2.23.so](../../attachments/ctfshow/ubuntu16/32bit/libc-2.23.so) | [libc-2.23.so](../../attachments/ctfshow/ubuntu16/64bit/libc-2.23.so) |
| Ubuntu 18.04 / glibc 2.27 | [libc-2.27.so](../../attachments/ctfshow/ubuntu18/32bit/libc-2.27.so) | [libc-2.27.so](../../attachments/ctfshow/ubuntu18/64bit/libc-2.27.so) |
| Ubuntu 19.04 / glibc 2.29 | [libc-2.29.so](../../attachments/ctfshow/ubuntu19/32bit/libc-2.29.so) | [libc-2.29.so](../../attachments/ctfshow/ubuntu19/64bit/libc-2.29.so) |
| Ubuntu 20.04 / glibc 2.30 | [libc-2.30.so](../../attachments/ctfshow/ubuntu20/32bit/libc-2.30.so) | [libc-2.30.so](../../attachments/ctfshow/ubuntu20/64bit/libc-2.30.so) |

## 鍋氶鏃舵渶鍏冲績鐨勫尯鍒?
### 1. 鍏堝垎鏋舵瀯锛屽啀鍒嗙増鏈?
- `32-bit` 鍜?`64-bit` 鐨勭鍙峰亸绉汇€佽皟鐢ㄧ害瀹氥€丷OP 閾炬嫾娉曢兘涓嶅悓锛屼笉鑳芥贩鐢ㄣ€?- 鍗充娇棰樼洰鍚嶅瓧涓€鏍凤紝`x86` 鍜?`x86_64` 涓嬬殑 `one_gadget`銆乣_IO_2_1_stdout_`銆乣__malloc_hook` 鍋忕Щ涔熶笉浼氫竴鏍枫€?
### 2. 浣犺繖鎵圭増鏈噷锛屾渶澶х殑鍒╃敤鍒嗙晫绾挎槸 `2.23` 鍜?`2.27+`

- `glibc 2.23` 杩樺鍦?**tcache 寮曞叆涔嬪墠**锛屽緢澶氳€侀鐨勫爢鍒╃敤閾炬洿鎺ヨ繎浼犵粺 `fastbin / unsorted bin / smallbin`銆?- 浠?`glibc 2.26` 寮€濮嬶紝`malloc` 寮曞叆浜?**per-thread cache锛坱cache锛?*锛涙墍浠ヤ綘杩欐壒 `2.27 / 2.29 / 2.30` 鐜閲岋紝寰堝鍫嗛閮戒細浼樺厛纰板埌 tcache 鐩稿叧琛屼负銆?- 杩欎篃鏄负浠€涔堝悓涓€浠?exp 鍦ㄦ湰鍦版柊鐜鍜岃繙绋嬭€佺幆澧冧笂锛岀粡甯镐細鍑虹幇鈥滆繙绋嬭兘鎵擄紝鏈湴涓嶉€氣€濇垨鑰呪€滄湰鍦板厛瑙﹀彂 tcache 妫€鏌モ€濈殑鎯呭喌銆?
### 3. `__malloc_hook / __free_hook` 杩欏嚑绫昏€佹墦娉曪紝鍦ㄤ綘杩欐壒鐗堟湰閲屽熀鏈兘杩樿兘瑙佸埌

- 浣犵幇鍦ㄦ敹鐨?`2.23 / 2.27 / 2.29 / 2.30` 閮芥棭浜?`glibc 2.34`銆?- 浠庡仛棰樿搴︾湅锛岃繖鎰忓懗鐫€鑰侀閲屽父瑙佺殑 `__malloc_hook`銆乣__free_hook`銆乣stdout` 浼€犺繖绫绘€濊矾锛屽湪杩欎簺鐗堟湰閲屼粛鐒舵槸楂橀鎵撴硶銆?- 鐪熸瑕佽鎯曗€滆€?hook 鎵撴硶澶辨晥鈥濈殑鍒嗙晫绾匡紝閫氬父鏄?`2.34` 鍙婁互鍚庛€?
### 4. 鐗堟湰涓€鍙橈紝鍋忕Щ灏辫閲嶇畻

- `system`
- `puts`
- `__malloc_hook`
- `__free_hook`
- `_IO_2_1_stdout_`
- `main_arena`
- `one_gadget`

杩欎簺閮戒笉鏄€済libc 閫氱敤甯搁噺鈥濓紝鑰屾槸**璺熷叿浣撶増鏈拰鍏蜂綋鏋舵瀯缁戝畾**鐨勩€?
鎵€浠ヤ竴涓鐩渶绋崇殑娴佺▼閫氬父鏄細

1. 鍏堢‘璁よ繙绋嬫垨棰樼洰缁欑殑鐜鐗堟湰銆?2. 閫夊鏋舵瀯鐨?`libc.so`銆?3. 鍐嶅幓绠楃鍙峰亸绉汇€乣one_gadget`銆乣stdout` / `main_arena` 绛夊湴鍧€銆?
## 浠€涔堟椂鍊欎紭鍏堥€夊摢浠?libc

- 棰樼洰鐩存帴缁欎簡 `libc.so.6`锛氫紭鍏堢敤棰樼洰缁欑殑锛屼笉瑕佺寽銆?- 棰樼洰鍙 `Ubuntu 16.04`锛氬厛璇?`glibc 2.23`銆?- 棰樼洰鍙 `Ubuntu 18.04`锛氬厛璇?`glibc 2.27`銆?- 棰樼洰鍙粰浜嗚繙绋嬬幆澧冦€佹病鏈?libc锛氬厛鐪?`checksec`銆侀鐩檮浠躲€丏ockerfile銆乣ldd`銆侀鐩弿杩帮紝鍐嶅喅瀹氥€?- 鏈湴澶嶇幇鍜岃繙绋嬭涓轰笉涓€鑷存椂锛氱涓€鏃堕棿鎬€鐤?`libc` 鐗堟湰涓嶄竴鑷达紝鑰屼笉鏄厛鎬€鐤?exp 鎬濊矾銆?
## 鎴戣嚜宸辩殑鍒嗙被寤鸿

濡傛灉鍚庨潰缁х画寰€鍗氬閲屽姞璧勬枡锛岃繖涓€绫诲唴瀹规渶濂藉崟鐙寜璧勬簮椤电淮鎶わ紝鑰屼笉鏄贩杩涙煇涓€绡囬瑙ｉ噷锛?
- `libc` 涓嬭浇绱㈠紩
- `ld-linux` / `loader` 涓嬭浇绱㈠紩
- `one_gadget` / `patchelf` / `pwninit` 浣跨敤绗旇
- `stdout` 浼€犮€乣tcache poisoning`銆乣house of *` 杩欑被涓撻鏂囩珷

杩欐牱鍚庨潰棰樿В姝ｆ枃閲屽彧闇€瑕佽创鈥滄湰棰樹娇鐢ㄧ幆澧冣€濆拰鈥滈檮浠朵笅杞解€濓紝涓嶄細鎶婂叕鍏辫祫鏂欓噸澶嶅啓寰堝娆°€?
## 鍙傝€?
- glibc 2.23 鍙戝竷璇存槑锛?https://sourceware.org/pipermail/libc-alpha/2016-February/068711.html>
- glibc 2.26 鍙戝竷璇存槑锛坱cache 寮曞叆锛夛細<https://sourceware.org/ml/libc-alpha/2017-08/msg00010.html>
- glibc 2.27 鍙戝竷璇存槑锛?https://sourceware.org/pipermail/libc-announce/2018/000018.html>
- glibc 2.29 鍙戝竷璇存槑锛?https://sourceware.org/ml/libc-announce/2019/msg00000.html>
- glibc 2.30 鍙戝竷璇存槑锛?https://sourceware.org/legacy-ml/libc-announce/2019/msg00001.html>
- glibc 2.34 閲?malloc hooks 鐨?API 绉婚櫎璇存槑锛?https://sourceware.org/pipermail/libc-announce/2021/000032.html>



