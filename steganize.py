#!/usr/bin/python
#imports
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
		decode(args[2], args[3], args[4])
	else:
		print 'Please type "python steganize help" for usage'


def encode(message, file, password=None):
	if message[-3:] == 'txt': #message is treated as a path
		pass

def decode(file, password=None):
	pass

if __name__ == "__main__":
	main(sys.argv)


'''
use cases
steganize.py e 'my message' test.jpg
steganize.py e /message.txt test.jpg
steganize.py e 'my message' test.jpg password

steganize.py d test.jpg
steganize.py d test.jpg password


TODO encrypt with keyczar, RSA, PGP
TODO add resume buzzword feature
'''
