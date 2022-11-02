#!/usr/bin/env python3

import random, getch, signal, sys

# sigint is ok
def signal_handler(sig, frame):
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# load words
f=open("words", 'r')
words=f.readlines()
words = [item.strip() for item in words]

print()

# choose difficulty
print("Choose a difficulty from 1 to 4, 4 being the hardest:")
diff=getch.getch()
while not diff.isnumeric() or int(diff) not in range(1,5):
  print("Choose a difficulty from 1 to 4, 4 being the hardest:")
  diff=getch.getch()

# difficulty settings: less letter hints for greater difficulty
if int(diff)==1:
  words=list(filter(lambda item: len(item) < 8, words))
  word=random.choice(words)
  missing=random.choices(word, k=int(len(word)/2))

elif int(diff)==2:
  words=list(filter(lambda item: len(item) > 4, words))
  word=random.choice(words)
  missing=random.choices(word, k=int(int(len(word)/2)+int(len(word)/2)/3))

elif int(diff)==3:
  words=list(filter(lambda item: len(item) > 5, words))
  word=random.choice(words)
  missing=random.choices(word, k=int(int(len(word)/2)+int(len(word)/2)/2))

elif int(diff)==4:
  word=random.choice(words)
  missing=word

missing=list(set(missing))

oword=word
word=list(word)

maxguesses=int(len(oword)/2)-int(diff)+2
if int(diff)==4:
  maxguesses=int("{mg}".format(mg=4 if int(len(oword)/3)+2 < 4 else int(len(oword)/3)+2))
if maxguesses<2:
  maxguesses=2
elif maxguesses>6:
  maxguesses=6

nword="_".ljust(len(word), "_")
nword=list(nword)

for idx, letter in enumerate(word):
  if letter in missing:
    word[idx]="_"
    nword[idx]=letter

thing=0
guess=""
guesses=0
guessed=""
while guesses<maxguesses and ''.join(word)!=oword:
  print()
  print("-".ljust(20, "-"))
  print()
  print("You have", maxguesses-guesses, "wrong guesse{s} left to get it".format(s="" if maxguesses-guesses<2 else "s"))
  print("Letters used:", guessed)
  print()
  print(' '.join(word))
  print()
  print("Which letter do you guess? ")
  print()
  guess=getch.getch()
  guess=guess.upper()
  print(guess)
  print()

  #print()
  #print(' '.join(nword))

  if guess in missing:
    for idx, letter in enumerate(nword):
      if letter==guess:
        nword[idx]=""
        word[idx]=letter
  elif guess in guessed:
    print("You already tried that!")
  elif guess in word:
    print("It's already there!")
  elif guess.isalpha():
    guesses=guesses+1
    guessed=guessed+" "+guess



print()

if guesses < maxguesses:
  print("".join(["It was ", oword, ", you got it!"]))
else:
  print("Nice try!")
  print()
  print("It was", oword)

print()
