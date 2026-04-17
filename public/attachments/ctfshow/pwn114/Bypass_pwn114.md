![[Pasted image 20260414144117.png]]
![[Pasted image 20260414143915.png]]
![[Pasted image 20260414144134.png]]
看似1000<1004没有溢出啊，实则256<<1000，明显栈溢出。
![[Pasted image 20260414145514.png]]
同时注意到flag被写入signal(11)即访问非法地址时会触发的函数中
![[Pasted image 20260414151026.png]]
exp:
![[Pasted image 20260414150939.png]]
![[Pasted image 20260414150924.png]]
![[Pasted image 20260414151002.png]]