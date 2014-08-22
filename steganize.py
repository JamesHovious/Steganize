#!/usr/bin/python
import sys
import argparse
from argparse import RawTextHelpFormatter, SUPPRESS

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
# version: 1.0
#
#=======================================
#DEFINE THE GLOBAL VARIABLES OF THIS SCRIPT
#=======================================
#These are signatures that will be used to detect hidden messages

header = '6a68' # equivalent of 'jh' in hex
footer = '686a' # equivalent of 'hj' in hex

space = '20' # equivalent of a space in hex





#=======================================
#DEFINE THE FUNCTIONS OF THIS SCRIPT
#=======================================


def main(args):
    args = get_args()

    if args.e:
        if args.password:
            import_simplecrypt()
            print "embedding '%s' into %s with password %s...." % (args.message, args.filename, args.password)
            encode(args.message, args.filename, args.password)
        else:
            print "embedding '%s' into %s...." % (args.message, args.filename)
            encode(args.message, args.filename)

    elif args.d:
        if args.password:
            import_simplecrypt()
            print "extracting message from %s with password: %s...." % (args.filename, args.password)
            decode(args.filename, args.password)
        else:
            print "extracting message from %s...." % args.filename
            decode(args.filename)


def import_simplecrypt():
    try:
        import simplecrypt
    except Exception:
        print 'You must install simplecrypt. Run the command \npip install -r requirements.txt'
        sys.exit()

def get_args():
    """
    Set up the arguments for the command line tool

    Either -e or -d is required.
    For both -e and -d --message and --filename are required
    For -d --password is optional.

    """
    parser = argparse.ArgumentParser(description='''
    Welcome to Steganize. This program will encode and decode secret messages into jpg files.

    **Encode**

    steganize.py -e --message 'top secret' inconspicuous.jpg
    steganize.py e /top_secret.txt inconspicuous.jpg
    steganize.py e 'top_secret.txt' inconspicuous.jpg p@ssw0rd!


    **Decode**

    steganize.py d inconspicuous.jpg
    steganize.py d inconspicuous.jpg p@ssw0rd!
    ''',formatter_class=RawTextHelpFormatter,usage=SUPPRESS)

    command_group = parser.add_mutually_exclusive_group(required=True)
    command_group.add_argument('-e', action='store_true', help='Encode a secret message',)
    command_group.add_argument('-d', action='store_true', help='Decode a secret message',)
    parser.add_argument('--filename', help='Name of the file from which encoding/decoding takes place', required=True)
    parser.add_argument('--message', help='Secret message to encode', required=False)
    parser.add_argument('--password',  help='Encrypt/decrypt message with PASSWORD', required=False)

    return parser.parse_args()

def encode(msg, m_file, passwd=None):
    """This functions encodes the given secret into a destination file.

    Args:
        msg (str): For encoding commands the message or text file to encode
                   For decoding commands the file to decode

        m_file (str): For encoding commands the file in which the message will be encoded
                   For decoding commands the password to decrypt the message

    Kwargs:
        password (str): For encoding commands the password to encrypt the message

    """
    secret = get_secret_msg(msg)

    #Convert the destination file into hex so that we can measure its free space
    with open(m_file, "rb") as dest_file:
        destination = dest_file.read()

    if passwd is not None:
        from simplecrypt import encrypt
        secret = encrypt(passwd, secret)

    msg_chars = len(secret)
    secret = secret.encode('hex')
    destination = destination.encode('hex')
    #At this point 'secret'(str) and 'destination'(file) are now hex values(str)

    #Free space in the destination is currently defined as spaces
    #We decide if there is enough blank space to just plug in the secret message
    free_space = size_of_free_space(destination)
    write_steganized_output_file(free_space, msg_chars, m_file, secret, destination)

def get_secret_msg(msg):
    """
    Decide if the user gave us a string or a text file to steganize

     Args:
        msg (str | file): the string or text file containing the secret message

    """
    if msg[-4:] == '.txt':
        with open(msg, "r") as secret_file:
            secret = secret_file.read().replace('\n', '')
    else:
        secret = msg
    return secret

def write_steganized_output_file(free_space, msg_chars, m_file, secret, destination):
    """
    This function takes the secret and writes it into the originally given file

    Args:
        :param free_space(int): The amount of free space in the given file
        :param msg_chars(int):  The number of characters of the secret message
        :param m_file(str):  The name of the original file in which we place our staganized message
        :param secret(str): The secret message that we are encoding/encrypting
        :param destination(file): The file to which we will write out seganized message
        :return:
    """
    if free_space < msg_chars:
        print 'Your message is too big for the amount of free space in the' \
                ' given file. Please shorten the message ' \
                'or select a file with more free space. '
        print 'There is space for ', free_space, ' characters.'
        exit()
    else:
        text_to_replace = space * msg_chars
        secret = add_sig(secret)
        destination = destination.replace(text_to_replace, secret, 1)
        try:
            destination = bytearray.fromhex(destination)
        except ValueError, e:
            print e
            destination = destination[:-1]
            destination = destination + '0a' # new line in hex
            destination = bytearray.fromhex(destination)
        f = open('steganized_' + m_file, 'w')
        f.write(destination)
        f.close()
    print m_file + ' successfully steganized!'


def size_of_free_space(m_input):
    """
    Determine the amount of free space in a given file in relation to the size of the secret
    :param m_input: the hex string value of the file in which we hide the secret
    :return: an integer of the amount of free space in the given file
    """
    m_max = m_input.count(space)
    m_max_free = space * m_max
    while True:
        if m_max_free in m_input:
            break
        m_max_free = m_max_free[:-2].strip()
    return m_max_free.count(space) - 4 #subtracting a total of 2 hex values to make room for the signature


def add_sig(secret):
    """
    This function will add a signature "jh[SECRET]hj" to the secret message. This will be used in decoding.
    :param secret: A string of the secret to be encoded
    :return: The original secret with a header and footer on concatenated to the beginning and end
    """
    return header + secret + footer

def decode(m_file, password=None):
    """This function finds and decodes secret messages in a given file

    Args:
        m_file (str): For decoding commands the file to decode

    Kwargs:
        password (str): For decoding commands the password to decrypt the message

    """
    #Convert the steganized file into hex so that we can look for the secret
    with open(m_file, "rb") as secret_file:
        destination = secret_file.read()
    secret_blob = destination.encode('hex')
    #At this point 'secret_blob' is now a string of hex values
    if sig_detected(secret_blob):
        secret = simple_carve(secret_blob)
        secret = secret.decode('hex')
        if password is not None:
            from simplecrypt import decrypt
            secret = decrypt(password, secret)
        print secret
    else:
        print 'No secret detected in file ' + str(m_file) #TODO use least significant pixel algorithm


def sig_detected(hex):
    """
    Detect a signiture "jh...hj" in a given hex string
    :param hex: a string of hex characters of the file being analysed
    :return: boolean value if the signature is detected
    """
    if header in hex:
        if footer in hex:
            return True
    else:
        return False

def simple_carve(secret_blob):
    """
    Carve a secret message that is in between a header and footer
    :param secret_blob: a hex string of the file being analysed
    :return: the string found in between the header and footer
    """
    try:
        start = secret_blob.index( header ) + len( header )
        end = secret_blob.index( footer, start )
        return secret_blob[start:end]
    except ValueError, e:
        print e
        exit()



if __name__ == "__main__":
    main(sys.argv)