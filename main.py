# 17591996 - Sense Hat reaction testing game

from sense_hat import SenseHat
import time
import random
import os

sense = SenseHat()

filename = "scores.txt"

def view_instructions():

	# print out of game instructions

    print(" ------------------------------ INSTRUCTIONS ------------------------------ ")
    print("")
    print("The game will display an arrow and select a random orientation for it.")
    print("You must rotate the board to match the arrow.") 
    print("If you match it in time, the arrow turns green and your score increases")
    print("If you don't match it in time the game is over.")
    print("The game will keep displaying arrows faster and faster until you lose.")
    print("")
    print(" -------------------------------------------------------------------------- ")
    
def view_highscores():

	if os.path.exists(filename): #Looks for the scores text file
		with open("scores.txt") as file:
			csv_reader = csv.reader(file) #looks at csv for each row
			sorted_list = sorted(csv_reader, key=lambda row: int(row[1]), reverse=True) 
			# sorts each row by the second record in the row - the score
		print ("High Scores")
		print("")
		for name, score in sorted_list: #loop through each record in scores
			if name[len(name)-1] == "s": #if the name ends in s dont put an s on the end
				print("{0}' Score = {1}".format(name, score)) # format the output in a readable way
			else:
				print("{0}'s Score = {1}".format(name, score)) 
	else: #if the scores text file is not found
		print("")
		print("No one has played the game yet :(")
		# either no one has played the game yet, or the text file cannot be found
		# user has option to start a new game, which in
		if (raw_input("Do you want to play? y/n: ") == "y"):
			main_game() 
		else:
			pass #does nothing
              
        


def main_game():

    r = [255,0,0] #red
    g = [0,255,0] #green
    w = [150,150,150] #white
    b = [0,0,0] #blank
    
    # Matrixes for arrow colours
    
    redArrow = [b,b,b,r,r,b,b,b,
                 b,b,r,r,r,r,b,b,
                 b,r,r,r,r,r,r,b,
                 r,r,r,r,r,r,r,r,
                 b,b,b,r,r,b,b,b,
                 b,b,b,r,r,b,b,b,
                 b,b,b,r,r,b,b,b,
                 b,b,b,r,r,b,b,b]
    
    greenArrow = [b,b,b,g,g,b,b,b,
                 b,b,g,g,g,g,b,b,
                 b,g,g,g,g,g,g,b,
                 g,g,g,g,g,g,g,g,
                 b,b,b,g,g,b,b,b,
                 b,b,b,g,g,b,b,b,
                 b,b,b,g,g,b,b,b,
                 b,b,b,g,g,b,b,b]
    
    whiteArrow = [b,b,b,w,w,b,b,b,
                 b,b,w,w,w,w,b,b,
                 b,w,w,w,w,w,w,b,
                 w,w,w,w,w,w,w,w,
                 b,b,b,w,w,b,b,b,
                 b,b,b,w,w,b,b,b,
                 b,b,b,w,w,b,b,b,
                 b,b,b,w,w,b,b,b]
    
    # User input for name - will be added to high score list
    name = raw_input("What is your name: ")
    print "Hello " + name + ", welcome to the game"

    #setting initial values 

    play = True
    pause = 3
    score = 0
    angle = 0

    #sense.show_message("Keep the arrow pointing up", scroll_speed = 0.05, text_colour=[100,100,100])
    
    while play:
        last_angle = angle
        while angle == last_angle:
            angles = [0,90,180,270] # list to store 4 different angle possibilities
            angle = random.choice(angles) # picks a random angle
            sense.set_rotation(angle)
            sense.set_pixels(whiteArrow)
            time.sleep(pause) 

            x,y,z = sense.get_accelerometer_raw().values() #gets the current position of the sensehat
            x = round(x, 0)
            y = round(y, 0)

            # prints current angle and x,y values to console
            print(angle) 
            print(x)
            print(y)

            # this block of if statements measures the current position of the pi and the angle of the arrow
            # if the values are correct (user turns pi in direction of arrow)
            # then their score is increased by one, otherwise the game ends 

            if x == -1 and angle == 180:
                sense.set_pixels(greenArrow)
                score = score + 1
            elif x == 1 and angle == 0:
                sense.set_pixels(greenArrow)
                score = score + 1
            elif y == -1 and angle == 90:
                sense.set_pixels(greenArrow)
                score = score + 1
            elif y == 1 and angle == 270:
                sense.set_pixels(greenArrow)
                score = score + 1
            else:
                sense.set_pixels(redArrow)
                time.sleep(0.5)
                play = False
                sense.show_message("Game Over!", scroll_speed = 0.05, text_colour=[255,0,0])

        	# this will increment the time between orientation change by 0.95 each time
        	# essentially making the game harder each time the user turns the arrow the right way

            pause = pause * 0.95
            time.sleep(1)

    sense.show_message("Your score is: " + str(score), scroll_speed = 0.05, text_colour=[255,0,0])

    # The game ends by telling the player their score, writing it to a text file


    # if there is already a scores file, append to existing file
    # if not, write new file
    if os.path.exists(filename):
        append_write = 'a'
    else:
        append_write = 'w'
    
    score_to_write = open(filename, append_write)
    score_to_write.write(name +"," + str(score) +'\n')
    # formats the scores in a csv ready format 
    score_to_write.close()

    # the user can then choose to view the scoreboard or exit the game

    if (raw_input("Do you want to view the high scores? y/n: ") == "y"):
    	view_highscores()
    else:
    	pass


def main():
	# main menu
    print ("Welcome to the game")
    print ("")
    print ("----------------------")
    print ("1. Play the game")
    print ("2. View highscores")
    print ("----------------------")
    print ("")

    answer = int(input("What do you want to do: "))

    while True:
        try:
            answer = int(raw_input("What do you want to do: "))
            while answer not in [1,2]:
                print ("")
                answer = int(raw_input("What do you want to do: "))
            break
        except:
            print("That is not a valid option")
            print("")
    
    print ("----------------------")          
    if answer == 1:
        main_game()
    elif answer == 2:
        view_highscores()
        
main()
