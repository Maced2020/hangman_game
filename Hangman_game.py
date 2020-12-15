# Hangman complete as of 9/8/2020

# module imports
import pygame
import math
import random
# end of module imports

#global game window
# window size,color, and headline title, FPS, game run mode

pygame.init()
HEIGHT, WIDTH = 800,800
win = pygame.display.set_mode((HEIGHT, WIDTH))
FPS = 60
clock = pygame.time.Clock()
pygame.display.set_caption('Game')
run_game = True


# Global variables 
# colors 
WHITE = (255,255,255)
BLACK = (0,0,0)

# buttion varibles
RAIDUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RAIDUS * 2 + GAP)* 13) / 2)
starty = 400 
A = 65
# this math is to center the buttons on the screen
for i in range(26):
    x = startx + GAP * 2 + ((RAIDUS * 2 + GAP) * (i % 13))
    y = starty +  ((i // 13)* (GAP + RAIDUS * 2))
    letters.append([x, y, chr(A + i), True])


# fonts 
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 40)
TITLE_FONT = pygame.font.SysFont('comicsans', 60)


# load images
images = []
# we Say range of 7 Because we start counting at 0 and go until 6
for i in range(7):
    image = pygame.image.load('hangman' + str(i) + '.png')
    images.append(image)
# picks out which picture from the array we will display

#game varibles 
hangman_status = 0


#getting a random word out of a text file
wordlist = []
filepath = 'words.txt'
with open(filepath) as fp:
   line = fp.readline()
   cnt = 0
   while cnt < 51:
       wordlist.append(line.strip())
       line = fp.readline()
       cnt = cnt + 1
       

# choising a random word from an array (making them all capital letters also)
word = random.choice(wordlist).upper()
guessed = []

#this is our drawing function for the entire Screen 
def draw():
    win.fill(WHITE)
    # Draw title
    text = TITLE_FONT.render('HANGMAN', 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    # Draw word
    display_word = ''
    for letter in word:
        if letter in guessed:
            display_word += letter + ' '
        else:
            display_word += '_ '
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    #draw buttons with letters 
    for letter in letters:
        x,y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x,y), RAIDUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            # math for centering the letters with in the butions 
            win.blit(text, (x - text.get_width()/ 2, y - text.get_height() /2))

    win.blit(images[hangman_status], (150,100)) 
    pygame.display.update()
# end of Draw Function


# this is the innning or loosing message function 
# start of display_mession Function 
def display_message(message):

    pygame.time.delay(1000) # time here is in milliseconds
    win.fill(WHITE)
    text = TITLE_FONT.render('HANGMAN', 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(6000)    
#end of display_message  function

# creating a while loop to get the screen and everything on it to load 
while run_game:
    clock.tick(FPS)
    draw()
    # Setting up the window Close action
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            # Setting up mouse button click action 
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RAIDUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
    
    # brodcasting 

    draw()
    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break

    if won == True:
        display_message('YOU ARE A WINNER!')
        break
    if hangman_status == 6:
        display_message('YOU ARE A LOSER! The word was ' + word)
        run = True
        break
    
pygame.quit()