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
# version: 0.8
# release date: 07 04 2014
# changelogs:
#   * 0.5 - 03 25 2014 - initial release
#   * 0.8 - 07 04 2014 - encode/decode works, password functionality w/o error checking
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
        if len(args) == 4:
            encode(args[2], args[3])
        else:
            encode(args[2], args[3], args[4])
    elif command == 'd':
        if len(args == 3):
            decode(args[2])
        else:
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
        print 'Please type "python steganize.py help" for usage'


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
    
    
    #Deciding if the user gave us a string or a text file to steganize
    if msg[-4:] == '.txt':
        with open(msg, "r") as secret_file:
            secret = secret_file.read().replace('\n', '')
    else:
        secret = msg
        
    #Convert the destination file into hex so that we can measure its free space
    with open(m_file, "rb") as dest_file:
        destination = dest_file.read()


    #ecnrypt if using a password
    if password is not None:
        from simplecrypt import encrypt
        secret = encrypt(password, secret)

    msg_chars = len(secret)
    secret = secret.encode('hex')
    destination = destination.encode('hex')
    #At this point 'secret'(str) and 'destination'(file) are now hex values(str)
    
    
    #Free space in the destination is currently defined as 20  or blank spaces
    #We decide if there is enough plank space to just plug in the secret message
    free_space = size_of_free_space(destination)
    if free_space < msg_chars:
        print 'Your message is too big for the amount of free space in the' \
                ' given file. Please shorten the message ' \
                'or select a file with more free space. '
        print 'There is space for ', free_space, ' characters.'
        exit()
    else:
        text_to_replace = '20' * msg_chars
        secret = add_sig(secret)
        destination = destination.replace(text_to_replace, secret, 1)
        #destination = destination.replace(':', '')
        try:
            destination = bytearray.fromhex(destination)
        except ValueError, e:
            print e
            destination = destination[:-1]
            destination = destination + '0a'
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
    m_max = m_input.count('20')
    m_max_free = '20' * m_max
    while True:
        if m_max_free in m_input:
            break
        m_max_free = m_max_free[:-2].strip()
    return m_max_free.count('20') - 4 #subtracting a total of 2 hex values to make room for the signature


def add_sig(secret):
    """
    This function will add a signature "jh[SECRET]hj" to the secret message. This will be used in decoding.
    :param secret: A string of the secret to be encoded
    :return: The original secret with a header and footer on concatenated to the beginning and end
    """
    return '6a' + '68' + secret + '68' + '6a'

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
    header = '6a68'
    footer = '686a'
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
    header = '6a68'
    footer = '686a'
    try:
        start = secret_blob.index( header ) + len( header )
        end = secret_blob.index( footer, start )
        return secret_blob[start:end]
    except ValueError, e:
        print e
        exit()



if __name__ == "__main__":
    main(sys.argv)