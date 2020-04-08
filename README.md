# PIGAME - How many decimals of π can you remember?
* Name: pigame
* Version: 1.2
* Programming language: Bash Shell Script
* Author: Thomas J. Dyhr
* Purpose: Learn π
* Release date: 8. April 2020
### Usage:  pigame [-v] [-p][-l LENGTH] YOUR_PI
    Evaluate your version of π (3.141.. )
    -v          Increase verbosity.
    -l LENGTH   Calculate π with LENGTH number of decimals.
    -p          Show π.
    -h          Print usage.

### installation
clone repo and install requirements.
### clone the repository
```shell
git clone https://github.com/docdyhr/pigame
cd pigame/
chmod 755 pigame
```
### install requirements
```Bash Shell
install in your $PATH
```

### usage examples
```shell
./pigame 3.14158
```
```shell
pigame -p -l 35
```
**result:**
π with 5 decimals:  3.14159
Your version of π:  3.14158
False

### history
I am facinated by the beauty of π and it's number sequence.

Comments and suggestions are welcome!

### todo
[TODO.md](https://github.com/docdyhr/pigame/blob/master/TODO.md)
### license
[MIT](https://github.com/docdyhr/pigame/blob/master/LICENSE)
