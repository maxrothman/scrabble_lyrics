#!/usr/bin/env python
"""
Gets lyrics for songs via LyricsWiki API and calculates scrabble scores for them.
Requires Python 2.7+
"""
__author__ = "Max Rothman"
__email__ = "max.r.rothman@gmail.com"
__license__ = "GPL v2"
__version__ = "1.0"

import sys

scrabble = {'a':1, 'b':3, 'c':3, 'd':2, 'e':1, 'f':4, 'g':2, 'h':4, 'i':1, 'j':8,
            'k':5, 'l':1, 'm':3, 'n':1, 'o':1, 'p':3, 'q':10, 'r':1, 's':1,
            't':1, 'u':1, 'v':4, 'w':4, 'x':8, 'y':4, 'z':10}

def word_score(word):
  return sum(scrabble[c] for c in word if c in scrabble)

def line_text(line):
  return ' '.join(i[0] for i in line)

def main():
  try:
    with open(sys.arg[1]) as f:
      song_txt = f.readlines()
  except IOError:
    print("Cannot open", sys.argv[1])
    sys.exit(0)
  
  song = []
  for line in song_txt:
    song.append([(word, word_score(word)) for word in line.split()])
  
  print "Total score:", sum(i[1] for line in song for i in line)
  print "Score per word: {:.3f}".format(sum(i[1] for line in song for i in line)/float(sum(len(line) for line in song)))
  print "Highest scoring line: {} ({})".format(*max(((line_text(line), sum(word[1] for word in line)) for line in song), key=lambda x:x[1]))
  print "Highest scoring word: {} ({})".format(*max(((word, score) for line in song for word, score in line), key=lambda x:x[1]))

if __name__ == '__main__':
  main()
