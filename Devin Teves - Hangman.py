import random
import string
word_bank = ["special", "computer", "python", "programming", "burger",
             "tablet", "pycharm", "github", "edison", "javascript"]
guesses = 10
guessesTaken = []
random_word = random.choice(word_bank)
wordList1 = list(random_word)
input("Press enter to play Hangman")
wordList2 = []
for letter in random_word:
    wordList2.append("*")

while guesses != 0:
    display_wordList = []
    print(''.join(wordList2))
    guess = input("Guesses left: %s\nGuess a letter >" % guesses)
    guess = guess.lower()
    if guess in guessesTaken:
        guess = input("You already guessed that letter. Try again >")
    elif guess not in wordList1:
        guessesTaken.append(guess)
        guesses -= 1
        continue
    for letter1, letter2 in zip(wordList1, wordList2):
        if guess == letter1:
            display_wordList.append(guess)
        elif letter2 != "*":
            display_wordList.append(letter2)
        else:
            display_wordList.append("*")
    guessesTaken.append(guess)
    wordList2[:] = display_wordList[:]
    if "*" not in wordList2:
        print("You win! You guessed the word, '%s'." % random_word)
        break
if guesses == 0:
    print("You have 0 guesses left! Game over.")
