#! /usr/bin/env python
import random, sys, getopt
from math import log

usage = """
Usage: passwdgen.py [-hvb] [-t <template>] [-n <number>]
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

versionstring = "Password generator script, version 0.05."

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
	try:
		(opts, args) = getopt.getopt(argv[1:], "hvbt:n:", ["help", "version"])
	except getopt.GetoptError, err:
		print str(err) # will print something like "option -a not recognized"
		print usage
		return 2

	patterns = []
	bitsonly = False
	numtogen = 10

	for (o, a) in opts:
		if o in ("-h", "--help"):
			print buildusage(argv[0])
			return 0
		elif o in ("-v", "--version"):
			print versionstring
			return 0
		elif o == "-t":
			# should check this is a valid pattern
			patterns.append(a)
		elif o == "-n":
			# should check this is a valid integer
			numtogen = int(a)
		elif o == "-b":
			bitsonly = True

	pools = make_pools()

	if len(patterns) == 0:
		patterns.append("cvcpcvccvcpdd")
		
	if bitsonly:
		for pattern in patterns:
			print pattern + ": " + str(pattern_entropy(pattern, pools))
	else:
		random.seed()
		for pattern in patterns:
			for i in range(numtogen):
				print make_passwd(pattern, pools)
				
	return 0
	

def make_passwd(pattern, pools):
	passwd = ""
	for char in pattern:
		passwd += random.choice(pools[char])
	return passwd


def make_pools():
	pools = {}
	
	pools['c'] = list('bcdfghklmnprstvwxz')
	pools['C'] = pools["c"] + [ch.upper() for ch in pools["c"]]
	
	pools['v'] = list('aeiouy')
	pools['V'] = pools["v"] + [ch.upper() for ch in pools["v"]]
	
	pools['l'] = pools["c"] + pools["v"]
	pools['L'] = pools["l"] + [ch.upper() for ch in pools["l"]]
	
	pools['d'] = [str(digit) for digit in range(10)]
	pools['D'] = pools["d"]
	
	pools['p'] = list('!@#%^&()-_+=[]{};,.?')
	pools['P'] = pools["p"]
	
	pools['h'] = pools["d"] + list('abcdef')
	pools['H'] = pools["d"] + list('ABCDEF')
	
	return pools
	
def array_entropy(seq):
	counts = {}
	for elt in seq:
		counts[elt] = 0
	for elt in seq:
		counts[elt] += 1
		
	# compute entropy S = \sum_i -p_i \log_2 p_i
	# if each p_i = c_i/t, reduces to S = \log_2 t - \sum_i c_i/t \log_2 c_i
	bits = log(len(seq))
	
	for key in counts.keys():
		bits -= counts[key] * log(counts[key]) / len(seq)
		
	# convert to base-2 logs
	bits /= log(2)
	return bits
	
def pattern_entropy(pattern, pools):
	return sum([array_entropy(pools[ch]) for ch in pattern])
	
if __name__ == "__main__":
	sys.exit(main())
