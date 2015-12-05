__author__ = 'Matias Estrada'

import sys

import format

def main():
	for line in sys.stdin:
		format.set_index(line, 'author')

if __name__ == '__main__':
	main()