![[Pasted image 20260414154722.png]]
![[Pasted image 20260414154900.png]]
这里还是有格式化字符串漏洞啊
![[Pasted image 20260414155006.png]]
偏移为7
那和上题一模一样，改个偏移的事
(0x2C-0xC)/4+7=15
偏移值为15，用b'%15$p'读取canary
exp:
![[Pasted image 20260414160814.png]]
![[Pasted image 20260414160757.png]]
![[Pasted image 20260414160739.png]]