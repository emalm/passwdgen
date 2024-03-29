#! /usr/bin/env python
import random, sys
import getopt
import argparse
from math import log

version = '0.06'

def buildusage(name):
	return 'Usage: ' + name + """ [-hvb] [-t <template>] [-n <number>]
Options:
  -h: Prints this help message and quits.
  -v: Prints version information.
  -t: Sets password template (default: cvcpcvccvcpdd).
  -n: Sets number of passwords to generate (default 10).
  -b: Calculates number of bits in specified pattern; no passwords generated.

Password templates use the following characters:
  c     lowercase consonant
  v     lowercase vowel
  l     lowercase letter
  C     mixed-case consonant
  V     mixed-case vowel
  L     mixed-case letter
  d, D  digit
  p, P  punctuation symbol (from !@#%^&()-_+=[]{};,.?)
  h, H  hex digit (h for lowercase a-f, H for uppercase)
	"""

def main(argv = None):
	if argv is None:
		argv = sys.argv

	parser = argparse.ArgumentParser(description='Batch password generator script.')

	parser.add_argument('-t', '--template',
		default='cvcpcvccvcpdd',
		help="""Password template. Recognized characters: cvlCVLdph.""")
	parser.add_argument('-n', '--num', type=int, default=10, help='number of passwords to generate')
	parser.add_argument('-b', '--bits', action='store_true')

	parser.add_argument('-k', '--keyboard', 
		choices=['uniform', 'u', 'qwerty', 'q', 'dvorak', 'd'],
		default='uniform',
		help='Keyboard key distribution to prefer: dvorak, qwerty, or uniform')
		
	parser.add_argument('-v', '--version', action='version', 
						version='%(prog)s' + version)
						
	args = parser.parse_args(argv[1:])
	# print args
	
	bitsonly = args.bits
	patterns = []
	patterns.append(args.template)
	numtogen = args.num
	keyboard = args.keyboard

	pools = make_pools(keyboard)

	if len(patterns) == 0:
		patterns.append("cvcpcvccvcpdd")
		
	if bitsonly:
		for pattern in patterns:
			print(pattern + ": " + str(pattern_entropy(pattern, pools)))
	else:
		random.seed()
		for pattern in patterns:
			for i in range(numtogen):
				print(make_passwd(pattern, pools))
				
	return 0
	

def make_passwd(pattern, pools):
	passwd = ""
	for char in pattern:
		passwd += random.choice(pools[char])
	return passwd


def make_pools(keyboard):
	consonants = {
		'u': 'bcdfghjklmnpqrstvwxz',
		'd': (('htns' * 2 + 'd') * 3 + 
			  ('gcrl' * 2 + 'f') * 2 +
			  ('mwvz' * 2 + 'b')) +
			 ('p' * 2 * 2 + ('qjk' * 2 + 'x')),
		'q': 'sdfghjkl' * 4 + 'qwrtp' * 2 + 'zxcvbnm'
	}
	
	consonants['uniform'] = consonants['u']
	consonants['dvorak'] = consonants['d']
	consonants['qwerty'] = consonants['q']
	
	vowels = {
		'u': 'aeiouy',
		'd': ('aoeu' * 2 + 'i') * 2 + 'y',
		'q': 'a' * 3 + 'eyuio' * 2
	}
	
	vowels['uniform'] = vowels['u']
	vowels['dvorak'] = vowels['d']
	vowels['qwerty'] = vowels['q']
	
	punct = {
		'u': '!@#%^&()-_+=[]{};,.?',
		'd': '---,,..//=[]' * 2 + '___??++~!@#$%^&(){}',
		'q': ';;;,./[[]]-=' * 2 + '???{{}}~!@#$%^&()_+'
	}

	punct['uniform'] = punct['u']
	punct['dvorak'] = punct['d']
	punct['qwerty'] = punct['q']
	
	pools = {}
	
	pools['c'] = list(consonants[keyboard])
	pools['C'] = pools['c'] + [ch.upper() for ch in pools['c']]
	
	pools['v'] = list(vowels[keyboard])
	pools['V'] = pools['v'] + [ch.upper() for ch in pools['v']]
	
	pools['l'] = pools['c'] + pools['v']
	pools['L'] = pools['l'] + [ch.upper() for ch in pools['l']]
	
	pools['d'] = [str(digit) for digit in range(10)]
	pools['D'] = pools['d']
	
	pools['p'] = list(punct[keyboard])
	pools['P'] = pools['p']
	
	pools['h'] = pools['d'] + list('abcdef')
	pools['H'] = pools['d'] + list('ABCDEF')

	pools['-'] = ['-']
	
	return pools
	
def array_entropy(seq):
	if len(seq) == 0:
		return 0

	counts = {}
	for elt in seq:
		counts[elt] = 0
	for elt in seq:
		counts[elt] += 1
		
	# compute entropy S = \sum_i -p_i \log_2 p_i
	# if each p_i = c_i/t, reduces to S = \log_2 t - \sum_i c_i/t \log_2 c_i
	bits = log(len(seq))
	
	for key in list(counts.keys()):
		bits -= counts[key] * log(counts[key]) / len(seq)
		
	# convert to base-2 logs
	bits /= log(2)
	
	return bits
	
def pattern_entropy(pattern, pools):
	return sum([array_entropy(pools[ch]) for ch in pattern])
	
if __name__ == "__main__":
	sys.exit(main())
