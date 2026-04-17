![[Pasted image 20260413210449.png]]
![[Pasted image 20260414140326.png]]
main函数的输入没有检测stdin的长度，而是仅仅以“/n”为分隔符。因此这里存在严重的栈溢出问题。
第一次栈溢出使用ret2libc首先获取puts表的实际映射地址，算出偏移，以此获取gets函数与mprotect函数的实际位置；
第二次溢出
![[Pasted image 20260414141608.png]]
exp:
![[Pasted image 20260414141742.png]]
![[Pasted image 20260414140708.png]]
![[Pasted image 20260414140312.png]]
![[Pasted image 20260414140257.png]]