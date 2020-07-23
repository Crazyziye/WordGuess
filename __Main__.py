#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File       : __Main__.py
# @Version    : 1.0 21/7/20 10:52 pm
# @Email Id   : zhazy119@mymail.unisa.edu,au
# @Author: Zia
# @Description: Word Guessing Game by Python
# This game gave me a preliminary understanding of the basic framework of python.
# Later I will write more games to integrate my knowledge.
# Maybe after this course is over, I can use python proficiently.
# This development made me understand a truth.
# If you don't know much, then you can only change your needs.

# import copy
import random
import re
import time

import pymysql
import json
import requests

print("The Minimum operating environment is Python 3.0")


# ########################################################################################################################
# This is a word guessing game. I entered 466k words into the database,
# and then used the random method to randomize the id to achieve random vocabulary.
# I could use json to complete all of this, but although the dictionary is easy to use,
# I still haven't figured out how to get the information in the complex dictionaries.

# If you need to implement random selection of words,
# then I welcome you to use my database. It has 466k known words.
# You can copy the function directly.

def Get_data(number):
    sql = "use Guess"
    host = '172.105.191.113'
    port = 3306
    user = 'Guess'
    password = '!@#PSPzhazy119'

    db = pymysql.connect(host=host, port=port, user=user, password=password)
    cursor = db.cursor()
    line1 = cursor.execute('USE Guess')
    command = str('SELECT id,word FROM word_guess where id=' + str(number))
    line2 = cursor.execute(command)
    data = str(cursor.fetchall())
    data1 = re.findall('[a-z]+', data)
    data2 = str(data1)
    data3 = data2.replace("['", "").replace("']", "")
    cursor.close()
    db.close()
    return data3


# #########################################################################################################################
# This is a function to get pronunciation.I use the Oxford dictionary api.
# You can also use the key and id in the function,
# but the number of requests per month should not exceed 1000.
# Otherwise I will turn it off.

def get_api_pronunciation(word_api='aces', language='en-gb', strictMatch='false'):
    app_id = 'd96098d2'
    app_key = '528d26875fe09a855afeb6ff1ac2b088'

    # default: en-gb
    language = language
    word_id = word_api
    # default: pronunciations
    fields2 = 'pronunciations'
    strictMatch = strictMatch

    url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' \
          + language \
          + '/' \
          + word_id.lower() \
          + '?fields=' \
          + fields2 \
          + '&strictMatch=' \
          + strictMatch

    r1 = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
    dic_text = r1.text
    dic_json = json.loads(dic_text)
    list_result = dic_json['results']
    list_dic_result = [1, 2]
    dic_result = dict(zip(list_dic_result, list_result))
    list_lexicalEntries = dic_result[1]['lexicalEntries']
    list_dic_lexicalEntries = [1, 2, 3]
    dic_lexicalEntries = dict(zip(list_dic_lexicalEntries, list_lexicalEntries))
    list_entries_1 = dic_lexicalEntries[1]['entries']
    list_entries_2 = [1]
    dic_entries = dict(zip(list_entries_2, list_entries_1))

    list_pronunciations = dic_entries[1]['pronunciations']
    list_pronunciations_1 = [1]
    dic_pronunciations = dict(zip(list_pronunciations_1, list_pronunciations))
    # audio = dic_pronunciations[1]['audioFile']
    print(print(dic_pronunciations[1]['phoneticSpelling']))


# #########################################################################################################################
# I use the random function to randomly select words
def get_word():
    guess_word_id = random.randint(1, 370100)
    word = Get_data(guess_word_id)
    return word


# #########################################################################################################################
# This is a simple anti-riot mechanism I wrote to prevent users from maliciously sabotaging the game.
# For example, the game requires the user to enter a string but he enters a number.
#
# This function is not particularly important,
# but if I consider making the game a product I will expand this function.

def check_letter(letter):
    # What you see is a regular expression, and I am not proficient in it.
    # It means "If the input value is not a letter, it will return an boolean."
    if not re.match("^[a-z]*$", letter):
        return False
    else:
        return True


# #########################################################################################################################
# This is a hint.
# This function is more complicated.
# I will explain the important variables in the comments
# @seat_dict @seat_list: the conversion of ordinal numbers
# @Seat_display: Tell the player the position of the prompted letter in the word.
# @seat_int: The corresponding position in the actual string.
# @word: Target word
#
#

def Hint(Seat_display, seat_int, word):
    seat_dict = {"1": "first", "2": "second", "3": "third"}
    seat_list = [1, 2, 3]
    if Seat_display in seat_list:
        print(seat_dict[str(Seat_display)])
        print("The " + str(seat_dict[str(Seat_display)]) + " letter of this word is " + word[seat_int])
    else:
        print("The " + str(Seat_display) + "th letter of this word is " + word[seat_int])


# #########################################################################################################################
# how many times a certain letter appears in the word?

def word_count(word):
    print("You only have one chance to ask how many times a certain letter appears in the word")
    letter_know = str(input("Hello, Which letter do you want to ask: "))

    # String and number conversion
    if len(letter_know) == 1:
        number_appeared = word.count(letter_know, 0, len(word))
        if number_appeared == 1:
            print("It appears one time")
        elif number_appeared == 0:
            print("It never appeared")
        else:
            print("It appears " + str(number_appeared) + " times")
    else:
        print("You can only enter one letter!!!")


# #########################################################################################################################
# I wanted to use try...except statements before, but then I gave up.
# Because the game itself is already very complicated,
# I don't want to make it more complicated.
#
#

def end_letter(word):
    print("You have only one chance to ask what letter the word ends in.")
    print("And you can input 3 letters")
    letter_input = input("Please input 3 letters: ")
    # This is a simple anti-riot mechanism.
    # When I write here I want to use custom exceptions.
    # But then I forgot how to use it, and this will not happen next time.
    # I promise.

    if len(letter_input) > 3:
        print("Error:400----Only 3 letters")
    if not check_letter(letter_input):
        print("Error:401----Please input letter!!!")
    # word.endswith can answer player whether their guess is correct.
    # word.endswith is boolean.
    # word.endswith(letters, start_location, end_location)

    print(word.endswith(letter_input, len(word) - 3, len(word)))


# #########################################################################################################################
# There has some random.
# You can view up to the first n letters,
# but the n is random.
# n = word length * 0.45
#
def view_starting_letter(word):
    view_number = int(len(word) * 0.45)
    if view_number < 1:
        view_number = 1

    print("You can view up to the first " + str(view_number) + " letters")
    print("the first " + str(view_number) + " letters word is " + word[:view_number])

# #########################################################################################################################

def view_last_letter(word):
    view_number = int(len(word) * 0.45)
    if view_number < 1:
        view_number = 1
    print("You can view up to the last " + str(view_number) + " letters")
    print("the last " + str(view_number) + " letters word is " + word[view_number * (-1):])


# #########################################################################################################################


def word_len(word):
    print("Its length is " + str(len(word)) + ".")



# #########################################################################################################################


def begin(Time, do='do'):
    print("You will have " + str(Time) + " times to " + do + ". Please cherish these opportunities.")


# #########################################################################################################################


print('''

This is a word guessing game.

Although this game may seem simple, what you have to face is a vocabulary with 466k words. So good luck to you.

If you think the game is too difficult, 

I can consider adding a dictionary function, but only if there are many people who like this game.

I use random function in many functions, so I don't know what the final result of the game will be. 

I like this feeling and hope you will like it.''')

time.sleep(2)

print(""
      "Your chance of guessing is different every time. "
      "The formula for calculating the number of your opportunities is: word length x0.5, "
      "and then take the integer part."
      "")
time.sleep(2)

# #########################################################################################################################
# Sorry, this function was closed. If you continue to read, you will know why I closed it.
# def get_Time(input_word):
#     return_times = int(len(input_word) * 0.5)
#     if return_times < 1:
#         return_times = 1
#     return return_times


# #########################################################################################################################

# Calculate the number of times to use help based on the length of the word
def prompt_Times_Int(word):
    prompt_times_int = int(word_len(word) * 0.5)
    return prompt_times_int


# #########################################################################################################################
# Prompt a letter randomly

def prompt_Seat_Int(word):
    prompt_seat_int = random.randint(0, len(word) - 1)
    return prompt_seat_int


# #########################################################################################################################
# Tell the player where the letter is prompted
def prompt_Display(word):
    prompt_display1 = prompt_Seat_Int(word) + 1
    return prompt_display1


# #########################################################################################################################
# This is the main program,the above are the functions needed to run the program.
# I closed all statements about ‘time’.
# This may be because I cannot solve the problem of whether the string passed is a reference or a copy.
#
start = True

while start:
    # I want to use the copy function of the dictionary,
    # but the result is not ideal.
    word_start = {1: get_word()}

    guess = True
    prompt = True

    while guess:
        word_dic_copy = word_start.copy()
        # Test purpose
        # print("word_dic_copy:" + str(word_dic_copy))
        word_copy = word_dic_copy[1]
        word = word_copy
        # times = get_Time(word)
        prompt_times = prompt_Seat_Int(word)
        prompt_display = prompt_Display(word)
        prompt_seat_int = prompt_Seat_Int(word)
        # begin(times, 'guess this word')

        if prompt_times < 3:
            prompt_times = 2
            # if times == 0:
            #     guess = False
            #     word_dic_copy = word_start

            # if times != 0:

            # Test purpose
            # print(word)
            print('''
             Before you start guessing, you have the following ways to get clues about this word.
             a. Word length

             b. The first few letters of the word

             c. The last few letters of the word

             d. Number of occurrences of a letter

             e. Use hint(You only have a limited number of times)

             f. Get pronunciation

             p. pass the Prompt box

             ''')
            time.sleep(2)
            while prompt:
                # The prompt loop is used to loop the number of prompts,
                # if there is no number of prompt times then jump out of the loop
                # This loop is very successful, and I want to use similar ideas to realize the function of repeating
                # guessing words, but I have encountered problems with quoting and copying.

                begin(prompt_times, "use help")

                if prompt_times != 0:
                    choose = str(input("Choose what you want to know: "))

                    if choose == "a":
                        prompt_times -= 1
                        word_len(word)
                        print("You still have " + str(prompt_times) + " times to use help")

                    elif choose == 'b':
                        prompt_times -= 1
                        view_starting_letter(word)
                        print("You still have " + str(prompt_times) + " times to use help")
                    elif choose == 'c':
                        prompt_times -= 1
                        view_last_letter(word)
                        print("You still have " + str(prompt_times) + " times to use help")
                    elif choose == 'd':
                        prompt_times -= 1
                        word_count(word)
                        print("You still have " + str(prompt_times) + " times to use help")
                    elif choose == 'e':
                        prompt_times -= 1
                        Hint(prompt_display, prompt_seat_int, word)
                        print("You still have " + str(prompt_times) + " times to use help")
                    elif choose == 'f':
                        prompt_times -= 1
                        #  The try...except statement must be used here,
                        #  because if the api encounters an unlisted word,
                        #  it will return an error. Otherwise, it will cause the game to crash.

                        try:
                            get_api_pronunciation(word)

                        except:
                            print("Not included")

                        finally:
                            print("You still have " + str(prompt_times) + " times to use help")
                    elif choose == 'p':
                        prompt = False
                    else:
                        print("As punishment, you will lose a chance to use help.")
                        print("You still have " + str(prompt_times) + " times to use help")
                        prompt_times = prompt_times - 1
                        # times = times - 1
                if prompt_times == 0:
                    # jump out the loop
                    print("You can no longer use help")
                    prompt = False
            guessWord = input("What is this word: ")
            if guessWord == word:
                # jump out the loop
                # My idea is to get new words in the start loop,
                # and reuse the old words in the guess loop.
                print('You win!!!')
                guess = False
                word_dic_copy = word_start
            # if guessWord != word:
            #     begin(times, 'guess this word')

            print(
                '''
        a. continue
        b. give up
        ''')

            # This is an anti-violence mechanism, but I did not improve it.
            # try:
            play = input("Give up or continue? Please input a or b: ")
            # except:
            #     print("You can only input a or b")
            # else:
            #     guess = False

            if play == "a":

                # I want to say that if I can't guess the word,
                # then I can continue to guess the word,
                # otherwise change to a new word to start the game again.

                # if guessWord != word:
                #     times = times - 1
                #     begin(times, 'guess this word')
                if guessWord == word:
                    guess = False
                # if player choose give up, the guess loop will stop.
            if play == "b":
                guess = False


    else:
        # if player choose give up, the game will stop.
        if play == 'b':
            print("See you later!!!")
            start = False

# #########################################################################################################################
