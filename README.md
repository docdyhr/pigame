# PIGAME - How many decimals of π can you remember?
* Name: pigame
* Version: 1.4
* Programming language: Bash Shell Script
* Author: Thomas J. Dyhr
* Purpose: Learn π
* Release date: 8. April 2020
### Usage:  pigame [-v] [-l LENGTH][-p] [-h] [-V] YOUR_PI
    Evaluate your version of π (3.141.. )
    -v          Increase verbosity.
    -l LENGTH   Calculate π with LENGTH number of decimals.
    -p          Show π.
    -h          Usage.
    -V          Version.

### installation
clone repo and install in your $PATH
### clone the repository
```shell
git clone https://github.com/docdyhr/pigame
```
### install in $PATH
install pigame somewhere in your $PATH
```Bash Shell
cd pigame/
chmod 755 pigame
mv pigame ~/bin
```

### usage examples
```shell
pigame 3.14158
```
**result:**
3.14159
3.14158
False

```shell
pigame -v -l 25 -p 3.1415926
```
**result:**
π with 25 decimals: 3.14159265358979323846264
π with 7 decimals:  3.1415926
Your version of π:  3.1415926
Well done.

### history
I am facinated by the beauty of π and it's number sequence.

### todo
[TODO.md](https://github.com/docdyhr/pigame/blob/master/TODO.md)
### license
[MIT](https://github.com/docdyhr/pigame/blob/master/LICENSE)
