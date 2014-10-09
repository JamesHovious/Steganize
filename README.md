Steganize
=========

Welcome to Steganize. This program will encode and decode secret messages into jpg files.

Encryption is supported via the [simple-crypt](https://pypi.python.org/pypi/simple-crypt) module.

Steganize is currently tested for Python v 2.7

Please see the below examples for proper usage syntax.


    Welcome to Steganize. This program will encode and decode secret messages into jpg files.

**Encode**
```
steganize.py -e --message 'top secret' --filename inconspicuous.jpg
steganize.py -e --message /top_secret.txt --filename inconspicuous.jpg
steganize.py -e --message 'top_secret.txt' --filename inconspicuous.jpg p@ssw0rd!
```
**Decode**
```
steganize.py -d --filename inconspicuous.jpg
steganize.py -d --filename inconspicuous.jpg --password p@ssw0rd!
```  


**Changelog:**

* v 0.5 03 25 2014 
  * Initial release. Encoding function is built and working. Decoding is not yet built.
* v 0.8 - 07 04 2014
  * encode/decode works, password functionality w/o error checking
* v 1.0 08 22 2014
  * Program works as intended. No known bugs.
* v 1.0.1 10 08 2014
  * Fixed bug that inserted too many characters into free space 