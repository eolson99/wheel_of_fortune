import random
#Since this application is relatively small, I decided to make the main variables global instead of passing the same cumbersome parameter between all of my functions.
player_list = []
word = ''
hidden_consonants = set()
hidden_vowels = set()
active_player_index = 0


#Next, I define some helper functions
def get_names():
    global player_list
    player1_name = input('Please enter player 1\'s name: ')
    player2_name = input('Please enter player 2\'s name: ')
    player3_name = input('Please enter player 3\'s name: ')
    player_list = [{'name':player1_name, 'bank':0},{'name':player2_name, 'bank':0},{'name':player3_name, 'bank':0}]


def choose_input(*options):
    #Here I use a magic variable so that it's easy to choose which input options are available when I run the function. Guessing the whole word is always an option, so it's not handled as a parameter.
    turn_active = True
    round_active = True
    player_name = player_list[active_player_index]['name']
    message = f'What would you like to do, {player_name}?'
    choices = ['g']
    if 'consonant' in options: 
        message += '\n-Type \'c\' to spin the wheel and guess a consonant.'
        choices.append('c')
    if 'vowel' in options:
        message += '\n-Type \'v\' to buy a vowel for $250.'
        choices.append('v')
    message += '\n-Type \'g\' to guess the answer to the puzzle.'
    print(message)
    choice = input('\nPlease enter your selection: ')
    while choice not in choices:
        choice = input('\nOops! That option is not valid. Please try again.')
    if choice == 'c': 
        turn_active = guess_consonant()
    if choice == 'v':
        turn_active = guess_vowel()
    if choice == 'g':
        [turn_active, round_active] = guess_word()
    return [turn_active, round_active]
  

def initialize_round():
    global word
    global hidden_consonants
    global hidden_vowels
    word_lower = word.lower()
    hidden_consonants.clear()
    hidden_vowels.clear()
    for i in range(0, len(word_lower)):
        letter = word_lower[i]
        if letter in ['a', 'e', 'i', 'o', 'u']:
            hidden_vowels.add(letter)
        #note: the consonant array is hard-coded here so that whitespace and punctuation characters aren't accidentally treated as letters
        elif letter in ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']:
            hidden_consonants.add(letter)
    return

def spin_wheel():
    wheel = ['BANKRUPT', 'Lose Turn', 100, 100, 150, 200, 250, 300, 350, 400, 450, 450, 500, 500, 550, 600, 650, 700, 750, 750, 800, 850, 900, 900]
    random_number = random.randint(0,23)
    return  wheel[random_number]

def guess_consonant():
    global active_player_index
    global player_list
    global hidden_consonants
    turn_active = True
    wheel_result = spin_wheel()
    if wheel_result == 'BANKRUPT':
        player_list[active_player_index]['bank']= 0
        print('\nYou landed on BANKRUPT! Your turn is over and your bank has been emptied of funds.')
        turn_active = False
    elif wheel_result == 'Lose Turn':
        turn_active = False
        print('\nYou landed on Lose Turn! Your turn is over.')
    else:
        print(f'\nYou landed on {wheel_result}! Now you can guess a consonant.')
        letter = input('\nPlease choose a consonant: ')
        while letter not in ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']:
            letter = input('Oops! Please enter a lower-case consonant.')
        if letter in hidden_consonants:
            print(f'\nGood guess! You just earned ${wheel_result}!')
            hidden_consonants.discard(letter)
            player_list[active_player_index]['bank'] += wheel_result
            turn_active = True
        else: 
            print('\nOops, that isn\'t one of the hidden consonants. Better luck next time!')
            turn_active = False
    return turn_active
            

def guess_vowel():
    global active_player_index
    global player_list
    global hidden_vowels
    turn_active = True
    player_list[active_player_index]['bank'] -= 250
    vowel = input('Which vowel would you like to buy?')
    while vowel not in ['a', 'e', 'i', 'o', 'u']:
        vowel = input('Oops! Please enter a lower-case vowel.')
    if vowel in hidden_vowels:
        print('Good pick!')
        turn_active = True
        hidden_vowels.discard(vowel)
    else: 
        print('\nOops, that\'s not one of the hidden vowels. Better luck next time!')
        turn_active = False
    return turn_active

def guess_word():
    global word
    guess = input('\nWhat do you think the word/phrase is? Make a guess!')
    if guess == word:
        print('Yep, that\'s it! The round is over now.')
        round_active = False
        turn_active = False
        return [turn_active, round_active]
    else:
        print('Nope. That\'s not it. Your turn is over now.')
        round_active = True
        turn_active = False
        return [turn_active, round_active]
        

def display_word():
    global word
    global hidden_consonants
    global hidden_vowels
    display_string = ''
    for i in range(0, len(word)):
        letter = word[i]
        letter = letter.lower()
        if letter in hidden_consonants or letter in hidden_vowels:
            display_string += '_'
        else:
            display_string += word[i]
    print(f'\nThis is how the puzzle looks so far: {display_string}')

def play_round():
    #the nested loops in this function run the turns and the actions within a given turn respectively.
    global word
    global player_list
    global active_player_index
    global hidden_consonants
    global hidden_vowels
    initialize_round()
    round_active = True
    active_player_index = 0
    while (len(hidden_consonants) > 0 or len(hidden_vowels) > 0) and round_active:
        turn_active = True
        player_name = player_list[active_player_index]['name']
        print(f'\n-----------------\nIt\'s {player_name}\'s turn.')
        display_word()
        [turn_active, round_active] = choose_input('consonant')
        player_bank = player_list[active_player_index]['bank']
        while turn_active:
            if len(hidden_vowels) == 0 and len(hidden_consonants) == 0:
                print('\nGreat guess! That solves the rest of the puzzle.')
                [turn_active, round_active] = [False, False]
                break
            display_word()
            if player_bank >= 250: 
                [turn_active, round_active] = choose_input('consonant', 'vowel')
            else:
                [turn_active, round_active] = choose_input('consonant')
                print(turn_active)
        player_bank = player_list[active_player_index]['bank']
        print(f'\nThat\'s the end of {player_name}\'s turn. They have ${player_bank} in the bank.')
        active_player_index = (active_player_index + 1) % 3
    print(f'\nThat\'s the end of the round. Here was the answer to the puzzle: {word} \n---------------')
       
def initialize_final_round():
    global word
    global hidden_consonants
    global hidden_vowels
    global active_player_index
    word_lower = word.lower()
    hidden_consonants.clear()
    hidden_vowels.clear()
    #here, the string processing is altered so that R,S,T,L,N and E are not hidden letters.
    for i in range(0, len(word_lower)):
        letter = word_lower[i]
        if letter in ['a', 'i', 'o', 'u']:
            hidden_vowels.add(letter)
        elif letter in ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'p', 'q', 'v', 'w', 'x', 'y', 'z']:
            hidden_consonants.add(letter)
    #Next, I decide who's moving to the final round.
    max_bank = 0
    for j in range(0, 3):
          if player_list[j]['bank'] > max_bank:
            max_bank = player_list[j]['bank']
            active_player_index = j
    return
          
        
def play_final_round():
    global word
    global hidden_consonants
    global hidden_vowels
    global active_player_index
    player_name = player_list[active_player_index]['name']
    print(f'\n------------\nWelcome to the final round, {player_name}! Sorry, everyone else. :( The category is names for ghosts.')
    print('\nFor this special round, the letters R, S, T, L, N, and E have been revealed.')
    display_word()
    print('Now, you can choose 3 consonants and one vowel to reveal.')
    for i in range(0, 3):
        letter = input('Please choose a consonant to reveal. ')
        while letter not in ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'p', 'q', 'v', 'w', 'x', 'y', 'z']:
            letter = input('Oops! Please choose a lower-case consonant. You cannot choose R S T L or N, because those letters have already been revealed.')
        hidden_consonants.discard(letter)
    vowel = input('Please choose a vowel to reveal. ')
    while vowel not in ['a', 'i', 'o', 'u']:
        letter = input('Oops! Please choose a lower-case vowel. You cannot choose E, because it has already been revealed.')
    hidden_vowels.discard(vowel)
    display_word()
    print('All right. Now the only thing left to do is guess the phrase. You only get one chance, so be careful!')
    final_guess = input('Type your final guess here: ')
    if final_guess == word:
        print(f'CONGRATULATIONS, {player_name}! You won a cash prize of $10,000!')
        player_list[active_player_index]['bank'] += 10000
    else:
        print(f'Oof, I\'m afraid that wasn\'t the answer, {player_name}. Too bad. The phrase was: {word}')

def end_game():
    global player_list
    message = '\nPOST-GAME REPORT\n----------------\nHere\'s how everything turned out at the end: '
    for i in range(0,3):
        name = player_list[i]['name']
        bank = player_list[i]['bank']
        message += f'\n{name}: ${bank}'
    print(message)
    file = open('wheel_fortune_log.txt', 'w')
    file.write(message)
    file.close()
    print('\nA log of these results has been saved to wheel_fortune_log.txt.\n\nGoodbye!')

def get_words(file):
    global word
    f = open(file, 'r')
    words = f.read().splitlines()
    f.close()
    random_number = random.randint(0, 9)
    word = words[random_number]
    return

        
#Finally, here's the main function that runs the game.
def main():
    global player_list
    global word
    global hidden_vowels
    global hidden_consonants
    print('WELCOME TO WHEEL OF FORTUNE!\n----------------')
    get_names()
    print('\nFirst up, it\'s round 1! The category is media featuring vampires.')
    get_words('vampires.txt')
    initialize_round()
    play_round()
    print("\nAll right, let's do round 2! The category is types of candy.")
    get_words('candy.txt')
    initialize_round()
    play_round()
    get_words('ghost.txt')
    initialize_final_round()
    play_final_round()
    end_game()
    return
          

main()
