#!/usr/bin/env python
"""
Calculates and analyzes scrabble scores for words in a file
Requires Python 2.7+
"""
__author__ = "Max Rothman"
__email__ = "whereswalden90@gmail.com"
__license__ = "GPL v2"
__version__ = "1.1"

import sys, collections, math

HIST_STEP = 2         #Size of steps in the histogram
HIST_MAX = 40         #Ignored if AUTO_RANGE is True. Histogram max value
AUTO_RANGE = True     #HIST_MAX will be the value of the highest-scoring word
HIST_SCALE_MAX = 30   #Maximum height of any bar in the graph (in characters)

scrabble = {'a':1, 'b':3, 'c':3, 'd':2, 'e':1, 'f':4, 'g':2, 'h':4, 'i':1, 'j':8,
            'k':5, 'l':1, 'm':3, 'n':1, 'o':1, 'p':3, 'q':10, 'r':1, 's':1,
            't':1, 'u':1, 'v':4, 'w':4, 'x':8, 'y':4, 'z':10}

def word_score(word):
  return sum(scrabble[c] for c in word if c in scrabble)

def line_text(line):
  return ' '.join(i[0] for i in line)

def main():
  try:
    with open(sys.argv[1]) as f:
      song_txt = f.readlines()
  except IOError:
    print("Cannot open", sys.argv[1])
    sys.exit(0)
  
  song = []
  for line in song_txt:
    song.append([(word, word_score(word)) for word in line.split()])
  
  print ""
  print "Highest scoring line: {0} ({1})".format(*max(((line_text(line), sum(word[1] for word in line)) for line in song), key=lambda x:x[1]))
  maxword = max(((word, score) for line in song for word, score in line), key=lambda x:x[1])
  print "Highest scoring word: {0} ({1})".format(*maxword)
  print ""
  print "Total score:", sum(i[1] for line in song for i in line)
  count = float(sum(len(line) for line in song))
  avg = sum(i[1] for line in song for i in line)/count
  print "Average word score: {0:.3f}".format(avg)
  print "Standard deviation: {0:.3f}".format((sum((i[1]-avg)**2 for line in song for i in line)/count)**.5)
  hist = collections.Counter(i[1] for line in song for i in line)
  theRange = range(HIST_STEP, maxword[1]+HIST_STEP, HIST_STEP) if AUTO_RANGE else range(HIST_STEP, HIST_MAX+HIST_STEP, HIST_STEP)
  pretty_hist = dict((val, sum(hist[i] for i in range(val-HIST_STEP, val+1))) for val in theRange)
  scale = float(HIST_SCALE_MAX)/max(pretty_hist.values())
#  print scale
#  for val in sorted(pretty_hist.keys()): print val, pretty_hist[val]
  print ""
  print "Histogram of scores: (max={0})".format(max(pretty_hist.values()))
  for val in sorted(pretty_hist.keys()):
    print "{0:2} {1}".format(val, '#'*int(math.ceil(pretty_hist[val]*scale)))

if __name__ == '__main__':
  main()
