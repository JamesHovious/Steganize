#!/usr/bin/python
import sys
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
# release date: 03 25 2014
# changelogs:
#   * 0.5 - 03 25 2014 - initial release
#
#=======================================
#DEFINE THE FUNCTIONS OF THIS SCRIPT
#=======================================


def main(args):
    """This is the main function for the program.

    Args:
    args[1] (str): The command to encode or decode

    args[2] (str): For encoding commands the message or text file to encode
                   For decoding commands the file to decode

    args[3] (str): For encoding commands the file in which the message will be encoded
                   For decoding commands the password to decrypt the message

    args[4] (str): For encoding commands the password to encrypt the message

    """

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
        steganize.py e 'top secret' inconspicuous.jpg
        steganize.py e /top_secret.txt inconspicuous.jpg
        steganize.py e 'top_secret.txt' inconspicuous.jpg p@ssw0rd!

        [Decode]
        steganize.py d inconspicuous.jpg
        steganize.py d inconspicuous.jpg p@ssw0rd!

        '''
    else:
        print 'Please type "python steganize help" for usage'


def encode(msg, m_file, password=None):
    """This functions encodes the given secret into a destination file.

    Args:

        msg (str): For encoding commands the message or text file to encode
                   For decoding commands the file to decode

        m_file (str): For encoding commands the file in which the message will be encoded
                   For decoding commands the password to decrypt the message

    Kwargs:

        password (str): For encoding commands the password to encrypt the message


    """
    #	TODO use OS.stat() to test for proper RW permission
    if msg[-3:] == 'txt':
        with open(msg, "r") as secret_file:
            secret = secret_file.read().replace('\n', '')
    else:
        secret = msg
    with open(m_file, "rb") as dest_file:
        destination = dest_file.read()
    secret = encode_hex(secret)
    destination = encode_hex(destination)
    free_space = size_of_free_space(destination)
    if free_space < len(secret.replace(':', '')):
        print 'Your message is too big for the amount of free space in the given file. Please shorten the message ' \
              'or select a file with more free space. '
        print 'There is space for ', free_space, ' characters.'
        exit()
    else:

        if len(secret) <= free_space:
            text_to_replace = '20:' * len(secret)
        else:
            text_to_replace = '20:' * free_space
        destination = destination.replace(text_to_replace, secret, 1)
        destination = destination.replace(':', '')
        try:
            destination = bytearray.fromhex(destination)
        except ValueError, e:
            if 'non-hexadecimal number found in fromhex() arg at position' in e:
                destination = destination[:-1]
                destination = bytearray.fromhex(destination)
        f = open('steganized_' + m_file, 'w')
        f.write(destination)
        f.close()
    print m_file + ' successfully steganized!'


def encode_binary(m_input):
    return ''.join(bin(ord(c))[2:].zfill(8) for c in m_input)


def encode_hex(m_input):
    return ":".join("{0:x}".format(ord(c)) for c in m_input)


def decode_hex(m_input):
    m_input = m_input.replace(':', '')
    return '{0:b}'.format(int(m_input, 16))


def size_of_free_space(m_input):
    m_max = m_input.count('20')
    m_max_free = '20:' * m_max
    while True:
        if m_max_free in m_input:
            break
        m_max_free = m_max_free[:-2].strip()
    return m_max_free.count('20')


def decode(m_file, password=None):
    """This function finds and decodes secret messages in a given file

    Args:

    m_file (str): For decoding commands the file to decode

    password (str): For decoding commands the password to decrypt the message

    """
    pass

if __name__ == "__main__":
    main(sys.argv)