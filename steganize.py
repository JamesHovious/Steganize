#!/usr/bin/python
#imports
import sys
import os
#
#   _____      _ _ _          _   ______             _   
#  / ____|    | (_) |        (_) |  ____|           | |  
# | |     ___ | |_| |__  _ __ _  | |__ _ __ ___  ___| |_ 
# | |    / _ \| | | '_ \| '__| | |  __| '__/ _ \/ __| __|
# | |___| (_) | | | |_) | |  | | | |  | | | (_) \__ \ |_ 
#  \_____\___/|_|_|_.__/|_|  |_| |_|_ |_|  \___/|___/\__|
#  / ____| |                       (_)                   
# | (___ | |_ ___  __ _  __ _ _ __  _ _______            
#  \___ \| __/ _ \/ _` |/ _` | '_ \| |_  / _ \           
#  ____) | ||  __/ (_| | (_| | | | | |/ /  __/           
# |_____/ \__\___|\__, |\__,_|_| |_|_/___\___|           
#                  __/ |                                 
#                 |___/                                  
#                 
#   by James Hovious
#   https://github.com/hoviousj/Steganize
#
# version: 0.1
# release date: TODO add date
# changelogs:
#   * 0.1 - TODO date - Initial release
#
#=======================================
#DEFINE THE FUNCTIONS OF THIS SCRIPT
#=======================================


def main(args):
    '''Allowed input is e for Encode or d for Decode.'''
    command = args[1]
    if command == 'e':
        encode(args[2], args[3])
    elif command == 'd':
        decode(args[2], args[3])
    elif command == 'help':
        print '''
        Welcome to Steganize. This program will encode and decode secret messages into jpg files.
        Please see the below examples for proper usage syntax.

        [Encode]
        steganize.py e 'my message' test.jpg
        steganize.py e /message.txt test.jpg
        steganize.py e 'my message' test.jpg password

        [Decode]
        steganize.py d test.jpg
        steganize.py d test.jpg password

        TODO encrypt with keyczar, RSA, PGP
        TODO add resume buzzword feature
        '''
    else:
        print 'Please type "python steganize help" for usage'


def encode(msg, file, password=None):
#	'''TODO use OS.stat() to test for proper RW permission'''
    if msg[-3:] == 'txt':
        with open(msg, "r") as secret_file:
            secret = secret_file.read().replace('\n', '')
    else:
        secret = msg
    with open(file, "rb") as dest_file:
            destination = dest_file.read()
    secret = encode_hex(secret)
    destination = encode_hex(destination)
    free_space = size_of_free_space(destination)
    print 'free space is ', free_space
    if free_space < len(secret.replace(':','')):
        print 'Your message is too big for the amount of free space in the given file. Please shorten the message' \
              'or select a file with more free space. '
    else:
        import binascii
        text_to_replace = '20:' * free_space
        destination = destination.replace(text_to_replace, secret)
        destination_hex = destination.replace(':','')



def encode_hex(input):
    return ":".join("{0:x}".format(ord(c)) for c in input)

def size_of_free_space(input):
    max = input.count('20')
    max_free = '20:' * max
    while True:
        if max_free in input:
            break
        max_free = max_free[:-2].strip()
    return max_free.count('20')

def decode(file, password=None):
    pass

if __name__ == "__main__":
    main(sys.argv)