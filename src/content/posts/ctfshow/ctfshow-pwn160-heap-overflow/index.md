---
title: CTFshow pwn160 Heap Overflow WP
published: 2026-04-15
updated: 2026-04-17
description: 典型的堆风水加跨块覆盖题，最后把 free@got 劫持到 system。
image: "./heap-logic-1.png"
tags: [CTFshow, Pwn, Heap, Heap Overflow, GOT Hijack]
category: ctfshow
draft: false
---
![绋嬪簭閫昏緫鎴浘 1](./heap-logic-1.png)
![绋嬪簭閫昏緫鎴浘 2](./heap-logic-2.png)
鏈変釜鎸囬拡鍦ㄥ垹闄ゆ椂娌℃湁娓呴浂锛佽绌虹疆鐨勬寚閽堝鏋滆鍐嶆璁块棶浼氬嚭闂\[纭俊鈾]鍏跺疄杩欓娌＄敤鍒?![绋嬪簭閫昏緫鎴浘 3](./heap-logic-3.png)
杩欓噷鍦╝dd_a_user鎸囦护涓涓€娆alloc浜哸1瀛楄妭(娌℃湁鍋氭竻绌?锛岀浜屾malloc浜?x80瀛楄妭骞舵竻绌猴紝涓よ€呭湪鍐呭瓨涓婃槸鐩歌繛鐨勶紝绗竴娆alloc鐨刢hunk0.0鏄瓨鏀緉ame鐨勶紝绗簩娆alloc鐨刢hunk0.1鏄瓨鏀?..鍟ョ殑锛焩3鎸囬拡瀛樺叆浜唘serlist\[x\]鎸囧悜绗瑇+1浣島sernamechunk鐨勫ご鍦板潃
![绋嬪簭閫昏緫鎴浘 4](./heap-logic-4.png)
濡傛灉褰撳墠user鐨刢hunk澶村湴鍧€+鐢宠鐨刢ontentchunk澶у皬>=褰撳墠chunk鐨剆ize锛宲uts("wtf")鍚﹀垯瀛樺叆text銆傚洜姝hunk0.1鏄瓨user缁欑殑text鐨勩€俢hunk0.1鐨勫墠4涓瓧鑺傛槸瀛樻斁浜嗗墠涓€涓猚hunk鐨勫湴鍧€锛屼笖璁块棶鐢ㄧ殑閮芥槸杩欎釜銆?杩欓噷娉ㄦ剰鍒帮紝濡傛灉缁檝2璧嬪€?1鐨勮瘽锛岃兘澶熺粫杩囨娴嬫潯浠讹紝鑾峰緱寰堝ぇ涓€鍧楀唴瀛樺尯鍩熺殑鍙啓鏉冮檺锛屽彲鑳借兘澶熻鐩栧埌user_list鍒楄〃鍋歞ouble_free銆備絾杩欓鐢ㄤ笉浜嗚繖涓€?杩欓鍙戠幇Update鍑芥暟涓殑鍒ゆ柇鏉′欢寰堝鎬紝濡傛灉chunkx.0鍜宑hunkx.1涔嬮棿闅斾簡鍑犱釜chunk锛岄偅涔堝緢杞绘澗灏卞彲浠ュ仛鍒板爢婧㈠嚭锛寁2鍙互鐢宠寰楀緢澶ф潵瑕嗙洊涓棿涓€浜沜hunk鐨刢hunkn.1鐨勫墠鍥涘瓧鑺傞儴鍒嗐€?
tips:
鐢宠涓や釜chunk锛屼竴鑸敵璇穋hunk鏃讹紝鏈夐檮甯︾殑chunk锛屽緢澶ф鐜囨槸鏀诲嚮鐐?
![鍫嗛姘寸ず鎰?1](./heap-layout-1.png)

![鍫嗛姘寸ず鎰?2](./heap-layout-2.png)

瀹為檯涓婏紝杩欐槸閬撳爢椋庢按鐨勯鐩€?閫氳繃鐢宠鍫嗗潡閲婃斁鍫嗗潡鐨勬柟寮忥紝浣垮悓涓€娆＄敵璇风殑涓や釜chunk鐩搁殧鍑犱釜chunk锛岃繖鏍蜂腑闂寸殑chunk閮戒細鈥滃彲鍐欌€濄€?
# Heap_Overflow WP

  

## 1. 绋嬪簭涓庝繚鎶?
  

- 鏋舵瀯锛歚ELF 32-bit`

- 淇濇姢锛歚NX`銆乣Canary`銆乣No PIE`銆乣Partial RELRO`

- 鍔熻兘锛?
聽 - `0` 娣诲姞鐢ㄦ埛

聽 - `1` 鍒犻櫎鐢ㄦ埛锛堝厛 `free(desc)` 鍐?`free(node)`锛?
聽 - `2` 鏄剧ず鐢ㄦ埛锛坄name: %s` / 
description: %s`锛?
聽 - `3` 鏇存柊鎻忚堪

  

鐢ㄦ埛缁撴瀯鍙繕鍘熶负锛?
  

```c

struct user {

聽 聽 char *desc; 聽 聽 聽// +0x0

聽 聽 char name[0x7c]; // +0x4

}; // malloc(0x80)

```

  

## 2. 婕忔礊鐐?
  

`update` 涓竟鐣屾鏌ラ€昏緫锛堝弽姹囩紪杩樺師锛夛細

  

```c

if (desc_ptr + len >= node_ptr - 4) {

聽 聽 puts("Wtf?");

聽 聽 exit(1);

}

fgets(desc_ptr, len + 1, stdin);

```

  

闂鏄笂鐣岀敤鐨勬槸 `node_ptr - 4`锛岃€屼笉鏄?`desc_chunk` 鐨勫疄闄呭ぇ灏忋€?聽

褰撴垜浠 `desc` 鍜?`node` 鍦ㄥ爢涓婅窛绂诲緢杩滄椂锛岃繖涓鏌ュ氨浼氭斁琛岃秴闀垮啓鍏ワ紝瀵艰嚧璺?chunk 鍫嗘孩鍑恒€?
  

## 3. 鍒╃敤鎬濊矾

  

1. 鍏堝垎閰?3 涓敤鎴凤細`user0`銆乣user1`銆乣user2`锛坄user2->desc` 鍐?`/bin/sh`锛夈€?
2. `delete(user0)`锛屽舰鎴愬彲澶嶇敤绌洪棽鍧椼€?
3. 鍐?`add` 涓€涓緝澶?`desc`锛坄0x100`锛夛紝澶嶇敤鏃у潡锛涙柊鐨?`node` 浼氳鍒嗗埌鏇磋繙浣嶇疆銆?
4. 鍦ㄨ繖娆?`add` 鍐呴儴鑷姩瑙﹀彂鐨?`update` 閲岃秴闀垮啓锛岃鐩?`user1->desc` 鎸囬拡涓?`free@got`銆?
5. `display(user1)` 娉勯湶 `free` 瀹為檯鍦板潃锛岃绠?`system`銆?
6. `update(user1)` 鎶?`free@got` 鏀规垚 `system`銆?
7. `delete(user2)` 瑙﹀彂 `system("/bin/sh")`銆?
  

## 4. 鍋忕Щ璇存槑

  

瑕嗙洊鍒?`user1->desc` 鐨勫亸绉诲彈 glibc 瀵归綈褰卞搷锛?
  

- 甯歌鏃х幆澧冿細`0x198`

- 鎴戞湰鍦?WSL glibc 2.39锛歚0x1b0`

  

`exp.py` 宸插唴缃弻鍋忕Щ鑷姩灏濊瘯锛歚0x198 -> 0x1b0`銆?
## 闄勪欢涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn160/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn160/exp.py)

  

## 5. EXP

  

鑴氭湰瑙侊細[exp.py](../../attachments/ctfshow/pwn160/exp.py)

  

鏈湴楠岃瘉鍛戒护锛?
  

```bash

python3 exp.py CHECK

```

  

鎴愬姛鍏抽敭杈撳嚭锛堟湰鍦板疄娴嬶級锛?
  

```text

[+] free@libc = 0xf7dec1f0

[+] system = 0xf7d9d430

[+] Exploit succeeded (shell command executed).

```

  

## 6. 澶嶇幇澶囨敞

  

- 璇ラ鎬濊矾鏄粡鍏?`free@got -> system`銆?
- 鏂扮増 glibc 鏈?tcache 鏃讹紝寤鸿鏈湴璋冭瘯鍏抽棴 tcache锛?
聽 - `GLIBC_TUNABLES=glibc.malloc.tcache_count=0`

- `exp.py` 鏈湴妯″紡宸茶嚜鍔ㄨ缃鐜鍙橀噺锛堝彲鐢?`TCACHE` 鍙傛暟鍏抽棴杩欎釜琛屼负锛夈€?
Q锛歸p涓紝鍒╃敤鎬濊矾鐨勭鍥涙鎵ц鏃讹紝鍐呭瓨绌洪棿鏄€庢牱鐨勶紝鐢ㄤ粈涔堣鐩栦簡浠€涔堬紝褰㈣薄鍦拌瑙ｄ竴涓?

A锛氬搴斾綘 WP 閲岀 4 姝ワ紝鏈川鏄竴娆♀€滆秴闀跨瑪鍒掔┛澶氬潡鍫嗗唴瀛樷€濈殑瀹氬悜瑕嗙洊銆?
鍙互鎶婂爢鎯虫垚涓€鎺掕繛缁埧闂达紙浣庡湴鍧€ -> 楂樺湴鍧€锛夛細

`[ user0.desc ][ user0.node ][ user1.desc ][ user1.node ][ user2.desc ][ user2.node ] ...`

delete(user0)聽鍚庯紝鍓嶄袱涓埧闂磋鑵剧┖骞跺悎骞舵垚澶х┖娲炪€? 
鎺ョ潃聽add(reclaim, size=0x100)聽鏃讹細

1. reclaim.desc聽琚垎閰嶈繘杩欎釜澶х┖娲烇紙鍦ㄥ墠闈紝浣庡湴鍧€锛夈€?2. reclaim.node聽鍥犱负绌烘礊涓嶅鏀?0x80 缁撴瀯浣擄紝浼氬幓鍚庨潰鍐嶆壘浣嶇疆锛堥珮鍦板潃锛岄€氬父鍦?user2 鍚庯級銆?
浜庢槸鍙樻垚锛?
`[ reclaim.desc(浣? ][ user1.desc ][ user1.node ][ user2.desc ][ user2.node ] ... [ reclaim.node(楂?]`

鍏抽敭 bug 鍦爑pdate聽鐨勬鏌ワ細瀹冩嬁聽reclaim.node聽褰撯€滀笂鐣屸€濓紝鑰屼笉鏄爎eclaim.desc聽鐪熷疄闀垮害銆? 
鎵€浠ユ垜浠紶涓€涓緢闀柯爐ext_len锛堟瘮濡傚亸绉宦?x198/0x1b0锛夛紝绋嬪簭璁や负鈥滆繕娌¤秺鐣屸€濓紝瀹為檯聽fgets聽宸茬粡浠幝爎eclaim.desc聽涓€璺啓绌胯繃鍘汇€?
鍐欏叆杞借嵎鏄細

`b"C" * offset + p32(free_got)`

鏁堟灉鏄細

- 鍓嶉潰鐨劼燙聽濉弧/韪╄繃涓棿鍖哄煙锛?- 鏈€鍚?4 瀛楄妭鍒氬ソ钀藉湪聽user1.node聽鐨勭涓€涓瓧娈碉紙user1->desc聽鎸囬拡锛夛紱
- 鎶婂畠浠庘€滃師鏉ユ寚鍚?user1.desc鈥濇敼鎴愨€滄寚鍚懧爁ree@got鈥濄€?
鎵€浠ョ 4 姝ュ彲浠ュ舰璞＄悊瑙ｄ负锛? 
鈥滄嬁涓€鏀秴闀胯鍙风瑪浠?reclaim.desc 寮€濮嬬敾锛岀敾绌夸腑闂村嚑闂存埧锛屾渶鍚庢妸 user1 闂ㄧ墝涓婄殑鍦板潃鏀规垚 free@got鈥濄€? 
鍚庣画聽display(user1)聽灏变細鎸夎繖涓亣鍦板潃鍘昏锛屼粠鑰屾硠闇?libc銆?

![瓒婄晫鍐欒鐩栫ず鎰廬(./heap-overwrite.png)




