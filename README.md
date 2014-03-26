Steganize
=========

A python program to insert hidden messages with steganography.

Welcome to Steganize. This program will encode and decode secret messages into jpg files.

Please see the below examples for proper usage syntax.

**Encode**
```
steganize.py e 'top secret' inconspicuous.jpg
steganize.py e /top_secret.txt inconspicuous.jpg
steganize.py e 'top_secret.txt' inconspicuous.jpg p@ssw0rd!
```

**Decode**
```
steganize.py d inconspicuous.jpg
steganize.py d inconspicuous.jpg p@ssw0rd!
```

**Changelog:**

* v 0.5 03 25 2014
⋅⋅* Initial release. Encoding function is built and working. Decoding is not yet built.