![[Pasted image 20260413205159.png]]


![[Pasted image 20260413205538.png]]
题目示意我们去把qword_3094改成0x11来获得flag，那么跟进var发现：
![[Pasted image 20260413205522.png]]
var和qword_3094在物理内存上是连续的。%s的读取没有长度限制，因此这里直接输入0x34个字符再加上qword_3094所需要的0x11就好了
exp:
![[Pasted image 20260413210123.png]]
![[Pasted image 20260413210046.png]]
![[Pasted image 20260413210109.png]]