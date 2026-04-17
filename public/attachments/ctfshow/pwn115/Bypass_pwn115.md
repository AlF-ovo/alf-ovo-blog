![[Pasted image 20260414151613.png]]
![[Pasted image 20260414154526.png]]
格式化字符串漏洞%p查看栈偏移，直接读取canary
![[Pasted image 20260414153958.png]]
栈偏移为5
(0xD4-0xC)/4+5=55
偏移值为55，用b'%55$p'读取canary
exp:
![[Pasted image 20260414154409.png]]
![[Pasted image 20260414154336.png]]
![[Pasted image 20260414154353.png]]