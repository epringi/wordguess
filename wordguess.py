#!/usr/bin/env python3

#add option to continue playing instead of exiting, and add Q for quit

import random, getch, signal, sys, os, time
import glob

# sigint is ok!
def signal_handler(sig, frame):
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

wd=os.path.dirname(os.path.realpath(__file__))

difficulty={
  1: "easiest",
  2: "medium",
  3: "harder",
  4: "hardest"
}

#-- intro
print()
print("                  Welcome to Word Guess!")
print()
print("   In the Word Guess game, you must guess a word from the")
print("  blank spaces you are given before you run out of wrong")
print(" guesses.  Kind of like hangman, but without the brutality.")
print()
print()

#-- Choose word list
# use glob to get a dir listing
wlists=glob.glob(wd+"/wlists/*")
# pre set the choice so it plays nice with the while loop
wlchoice=""
# loop in here if user makes an invalid choice
while not wlchoice.isnumeric() or int(wlchoice) not in range(1, len(wlists)+1):
  print("First, choose a list of words to guess from (1-%i):" %(len(wlists)))
  print()
  # print a nice list of the available word lists - TODO: perhaps word lists should have a desc and proper name that gets displayed
  for idx, wlist in enumerate(wlists):
    f=open(wlists[idx], 'r')
    wlistname=f.readline()[0:-1]
    wlistdesc=f.readline()[0:-1]
    print("%i: %s - %s" %(idx+1, wlistname, wlistdesc))
  wlchoice=getch.getch()

#-- load words
f=open(wlists[int(wlchoice)-1], 'r')
# take the first line as the name, then skip the next line because that's the desc
wlname=f.readline()[0:-1]
words=f.readlines()[1:]
words=[item.strip() for item in words]
#wlchoice=os.path.relpath(wlists[int(wlchoice)-1], wd+"/wlists")

print()
print()
#print("--- You chose the %s wordlist ---" %(os.path.relpath(wlists[int(wlchoice)-1], wd+"/wlists")))
print("--- You chose the %s wordlist ---" %(wlname))
print()
print()
time.sleep(1)

#-- choose difficulty
diff=""
print("Next, choose a difficulty.  The difficulty level means how many")
print("letters are revealed in the beginning, and how many wrong letter")
print("guesses you have to figure out the word, based on how long the word is.")
# loop in here if an invalid choice is made
while not diff.isnumeric() or int(diff) not in range(1,5):
  print()
  print("Choose a difficulty from 1 to 4, 4 being the hardest and revealing no letters:")
  diff=getch.getch()

diff=int(diff)
print()
print()

print("--- You chose the %s difficulty ---" %(difficulty[diff]))

'''if int(diff)==1:
  print("--- You chose the easiest difficulty ---")

elif int(diff)==2:
  print("--- You chose the medium difficulty ---")

elif int(diff)==3:
  print("--- You chose the harder difficulty ---")

elif int(diff)==4:
  print("--- You chose the hardest difficulty ---")'''

playagain="y"

def gameloop():
  global playagain
  global words
  global guesses
  global maxguesses
  global oword

  while playagain=="y" or playagain=="Y":
    # difficulty settings: less letter hints and longer words for greater difficulty
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

    print()
    print()
    time.sleep(1)

    missing=list(set(missing))

    # save the original word, then make a list of the word's letters to parse
    oword=word
    word=list(word)

    # no guesses less than 2, and no more than 6, not sure what I was doing with the string formatting...
    maxguesses=int(len(oword)/2)-int(diff)+2
    if int(diff)==4:
      maxguesses=int("{mg}".format(mg=5 if int(len(oword)/3)+2 < 5 else int(len(oword)/3)+int(len(oword)/3)))
      maxguesses=6
    elif maxguesses<2:
      maxguesses=2
    elif maxguesses>6:
      maxguesses=6

    # make a list of guessed letters
    guessedlist=[]
    for idx in range(0, maxguesses):
      guessedlist.append("_")

    nword="_".ljust(len(word), "_")
    nword=list(nword)

    for idx, letter in enumerate(word):
      if letter in missing:
        word[idx]="_"
        nword[idx]=letter

    thing=0
    guess="start"
    guesses=0
    guessed=""

    while guesses<maxguesses and ''.join(word)!=oword:
      if guess.isalpha() or "start" in guess:
        showguessed=""
        print("=".ljust(20, "="))
        print(wlname.center(20, " "))
        print()
        print()
        print(" ", ' '.join(word))
        print()
        print()
        print("Misses:", " ".join(guessedlist))
        print()
        print("Which letter do you guess? ")
        print()

      guess=getch.getch()
      guess=guess.upper()

      if guess.isalpha() or "start" in guess:
        print(guess)

        print()

        if guess in missing and guess not in word:
          for idx, letter in enumerate(nword):
            if letter==guess:
              nword[idx]=""
              word[idx]=letter
          print("It's there!")
        elif guess in guessed:
          print("You already tried that!")
        elif guess in word:
          print("It's already there!")
        else:
          guesses=guesses+1
          guessed=guessed+" "+guess
          guessedlist[guesses-1]=guess
          print("Unfortunately, %s is not there." %(guess))

        print()
        print()
        time.sleep(1)

    print()

    if guesses < maxguesses:
      print("".join(["*** It was ", oword, ", you got it!! ***"]))
    else:
      print("Nice try, it was", oword)

    print()
    print()

    print("Continue with %s on %s difficulty? (Y/N)" %(wlname, difficulty[diff]))
    playagain=getch.getch()

gameloop()


print()
