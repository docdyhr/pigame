# PIGAME - How many decimals of π can you remember?

## Name: pigame

* Version: 1.5
* Programming language: Bash Shell Script
* Author: Thomas J. Dyhr
* Purpose: Memorisation of π
* Release date: 11. April 2020
  
## Usage:  pigame [-v] [-p LENGTH] [-V] YOUR_PI

    Evaluate your version of π (3.141.. )
    -v          Increase verbosity.
    -p LENGTH   Calculate and show π with LENGTH number of decimals.
    -V          Version.

### installation

clone repo and install pigame in your $PATH

#### clone the repository

```shell
git clone https://github.com/docdyhr/pigame
```

#### install in path

install pigame somewhere in your $PATH

```shell
cd pigame/
chmod 755 pigame
mv pigame ~/bin
```

#### installattion requirements

    bc - An arbitrary precision calculator language  
    Linux/Unix: install with your standard package manager on most linux systems
    Windows: a 32 bit windows version is available.  
    Ref.: https://www.gnu.org/software/bc/bc.html  

### usage examples

```shell
pigame 3.14158
```

```shell
3.14159  
3.14158  
No match  
```

```shell
pigame -v -p 25 
```

```shell
π with 25 decimals: 3.14159265358979323846264
```

```shell
pigame -v 3.1415926
```

```shell
π with 7 decimals: 3.1415926  
Your version of π: 3.1415926  
Number of errors: 0  
Perfect!  
```

### history

I am facinated by the beauty of π and it's number sequence.

### todo

[TODO.md](https://github.com/docdyhr/pigame/blob/master/TODO.md)

### license

[MIT](https://github.com/docdyhr/pigame/blob/master/LICENSE)
