#!/usr/bin/env python3

import random, getch

f=open("words", 'r')
words=f.readlines()
words = [item.strip() for item in words]

print()
print("Choose a difficulty from 1 to 3, 3 being the hardest:")
diff=getch.getch()
while not diff.isnumeric() or int(diff) not in range(1,4):
  print("Choose a difficulty from 1 to 3, 3 being the hardest:")
  diff=getch.getch()

if int(diff)==2:
  words=list(filter(lambda item: len(item) > 4, words))

if int(diff)==3:
  words=list(filter(lambda item: len(item) > 5, words))

if int(diff)==1:
  words=list(filter(lambda item: len(item) < 8, words))

word=random.choice(words)

missing=random.choices(word, k=int(len(word)/2))
missing=list(set(missing))

if len(missing)<len(word)/2 and int(diff)==3:
  missing=random.choices(word, k=int(int(len(word)/2)+int(len(word)/2)/2))
  missing=list(set(missing))
  if len(missing)<len(word)/2 and int(diff)==3:
    missing=random.choices(word, k=int(int(len(word)/2)+1))
    missing=list(set(missing))

oword=word
word=list(word)

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
maxguesses=int(len(oword)/2)-int(diff)+2
if maxguesses<2:
  maxguesses=2
elif maxguesses>6:
  maxguesses=6
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
