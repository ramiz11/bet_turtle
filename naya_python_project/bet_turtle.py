from turtle import *
from random import randint
from pathlib import Path
import time
from selectorlib import Extractor
import requests
import json
from playsound import playsound
from pygame import mixer


chosen_turtle = ""  # the turtle which the user bets on
bet_amount = 0  # the betting amount
guessed_steps = 0  # guessed number of steps of the winning turtle
finished_race_info = []  # info about the race : winning turtle, colour of winning turtle, and the number of steps it took
turtle_step_counter = [0, 0, 0, 0]    # create a list of steps of turtles
e = Extractor.from_yaml_file('selectors.yml')  # Create an Extractor by reading from the YAML file
budget=0
wins_and_losses=[] # a list of wins and losses of user for each round
turtle_colours=['green','purple','blue','orange']
rounds_counter=0   # counts the number of rounds played

#set up the screen width and height
wh=Screen()
wh.setup(width=1.0,height=1.0)
onscreenclick
#create an instance of turtle for writing messages
message=Turtle()
message.hideturtle()
message.speed('fastest')
message.color('black')
message.style = ('Courier', 30, 'italic')

#create instances of mixer and some sound variables
mixer.init()
lanes_music=mixer.Sound('chrono_12.mp3')
background_noise=mixer.Sound('background_noise.mp3')
crowd_applause=mixer.Sound('crowd_applause.mp3')
dissapointed_crowd=mixer.Sound('disappointed_Sound_effect.mp3')
suspense=mixer.Sound('suspense.mp3')


def introduce_turtles()->None:
    "a function that introduces the turtles to the user and returns nothing"

    go_to=[(-100,100),(-100,0),(100,100),(100,0)]
    for i in range(1,5):
        ti=Turtle()
        ti.shape('turtle')
        ti.color(turtle_colours[i-1])
        ti.shapesize(2.5)
        ti.penup()
        ti.goto(go_to[i-1][0],go_to[i-1][1])
        ti.write('t'+str(i)+':', True, align="center",font=('Arial',35,'normal'))
        time.sleep(1)
    time.sleep(3)
    clearscreen()


def create_race(T:str) -> dict:
    "function that creates the race and returns a dictionary which contains all the infromation about the winning turtle"
    lanes_music.play(True)
# create a pen to write the lanes of the race track
    lanes_pen = Turtle()
    lanes_pen.speed('fastest')
    lanes_pen.penup()
    lanes_pen.goto(-150, 150)
# creating the race track which consists of 12 vertical lanes (0-11)
    for lane_numb in range(11 + 1):
        lanes_pen.write(lane_numb, align='center')
        lanes_pen.right(90)
        # make the line sectioned
        for num in range(9 + 1):
            lanes_pen.penup()  # move the pen without leaving a mark
            lanes_pen.forward(10)
            lanes_pen.pendown()  # move and make a mark
            lanes_pen.forward(10)
 # now go back up - move a little bit to the right and create a new lane
        lanes_pen.penup()
        lanes_pen.backward(200)  # 200= 10 iterations *(20) forward - 10 with penup and 10 with pen down
        lanes_pen.left(90)
        lanes_pen.forward(20)
# creating the racing turtles
    turtle_list=[]
    heights=[110,75,40,5]
    for i in range(1,5):
        ti = Turtle()
        ti.speed('normal')
        ti.color(turtle_colours[i-1])
        ti.shape('turtle')
        # move turtles to its starting point of the race which is (-160 , yi)
        ti.penup()
        ti.goto(-160, heights[i-1])
        ti.pendown()
# introduce the turtles  turn the turtle by 360 degrees (doesnt change nothing - just a cool way to introduce the turtle)
        for turn in range(36):
            ti.right(10)

        turtle_list.append(ti)

    playsound('Mario Kart Race Start - Gaming Sound Effect (HD).mp3')
    lanes_music.stop()
    background_noise.play(True)
# create a list of info about the turtle
    global turtle_step_counter
    turtle_names = ["t1", "t2", "t3", "t4"]
    turtle_colors = ["green", "purple", "blue", "orange"]
 #create a list of passive turtles - which the user doesn't control
    passive_turtles=[]
    for i in range(len(turtle_names)):
        if turtle_names[i]!=T:
            passive_turtles.append(turtle_list[i])
    index_of_chosen_turtle=turtle_names.index(T)
    #send the passive turtles along with the chosen turtle, and move them passively/actively accordingly.
    move_turtle(passive_turtles,turtle_list[index_of_chosen_turtle],turtle_list)
    global finished_race_info  # i want to use the variable outside the method thus 'global'
    finished_race_info = list(zip(turtle_step_counter, turtle_names, turtle_colors))
    time.sleep(2)
 #clear the screen from the prevoius race
    clearscreen()
#return winner info
    return (
        {"name": max(finished_race_info)[1], "color": max(finished_race_info)[2], "steps": max(finished_race_info)[0]})

def move_turtle(passive_t:list,T:Turtle,t_list:list)->None:
    "a function that moves the passive turtles randomly and the chosen turtle according to user speed"
    #initilize turtle step counter to 0
    for i in range(len(turtle_step_counter)):
        turtle_step_counter[i]=0
    #unpack the passive turtles, unpack all turtles --> this is done to compare and figure out who is who
    p1,p2,p3=passive_t
    t1,t2,t3,t4=t_list
    for _ in range(50):
        for i in range(1,4):
            pi=passive_t[i-1]
            #move passive turtles
            pi_steps = randint(1, 5)
            pi.forward(pi_steps)
            if pi==t1:
                turtle_step_counter[0] += pi_steps
            elif pi==t2:
                turtle_step_counter[1]+=pi_steps
            elif pi==t3:
                turtle_step_counter[2]+=pi_steps
            else:
                turtle_step_counter[3]+=pi_steps
        #move my turtle
        clicked=numinput("move your turtle turtle", "enter any number from 0-9 to move turtle:", default=5, minval=1, maxval=9)
        T_steps=-1
        if clicked==1 or clicked==9:     #diagonal numbers produce the least amount of steps (1)
            T_steps=1
        elif clicked==3 or clicked==7:   #diagonal number that are not 1 and 9 produce slightly more steps (to eliminate user expectation)
            T_steps=2
        elif clicked==4 or clicked==6:   #buttons in the middle of a column produce the maximum amount of steps (5)
            T_steps=5
        elif clicked==8 or clicked==2:   #buttons in the middle of a row produce the second  largest amount of steps
            T_steps=4
        else:    # 5 is in diagonal position but it is also the middle of both row and column - so it produces a moderate number of steps - not too large- not to small
            T_steps=3
        # move the turtle a number of steps according to the input
        T.forward(T_steps)
        if T==t1:
            turtle_step_counter[0] += T_steps
        elif T==t2:
            turtle_step_counter[1]+= T_steps
        elif T==t3:
            turtle_step_counter[2]+= T_steps
        else:
            turtle_step_counter[3]+= T_steps
    background_noise.stop()


def check_draw(l: list, d: dict) -> bool:
    "functions that checks if there was a draw between the winning turtle and a different turtle and re-creates the race"
    to_return = False
    for steps, turtle_name, turtle_color in l:
        if d["steps"] == steps and d["name"] != turtle_name:
            print("there was a Draw! the race will be re-created!")
            to_return = True
    return to_return

def current_budget() -> int:
    "function that returns the current budget of the user"
    return budget

def summary()->None:
    "this function writes the summary of the user wins and losses thus far"
    message.color('green')
    to_print=f""" 
        \tSUMMARY:\n\n
        your starting budget is: {starting_budget}$\n
        your current budget is: {current_budget()}$ \n
        your peformance in the game:\n
        you have won: {sum([numb for numb in wins_and_losses if numb>0])}$\n
        you have lost: {sum([numb for numb in wins_and_losses if numb<0])}$
        """
    message.write(to_print, move=False, align="center", font=("Arial", 25, "normal",'bold','italic'))
    time.sleep(6)
    clearscreen()

def enough_money_to_play() -> bool:
    "function that check if the user still has enough money to play(minimum 15$), returns True or False"
    if current_budget() < 15:
        return False
    else:
        return True

def scrape(url):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    # download the page using requests
    print(f"Downloading {url}")
    r = requests.get(url, headers=headers)
    # simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print(f"Page{url} was blocked by Amazon. Please try using better proxies\n")
        else:
            print(f"Page must have been blocked by Amazon as the status code was {r.status_code}")
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)

# intoduce the user to the game
suspense.play()
intro="""\n\n\
welcome to the turtle race betting, carefully read the instructions, then place your bet.\n\n
the minimum entry amount for each round is 15$\n\n
in this race four turtles 't1' (green turtle),'t2' (purple),'t3' (blue),'t4' (orange) will participate, pick one of them to win\n\n
if you choose correctly - we will triple your winnings, however if you lose, then you will lose 50% of the entered amount\n\n
IMPORTANT: after finishing the game, stick around for some cool gifts!
"""
message.write(intro, move=False, align="center", font=("Arial", 24, "normal",'bold','italic'))
time.sleep(22)
clearscreen()
#introduce the user to the rules of moving the turtles:
rules="""\t\t\t           RULES:\n\n
          to move your turtle, click on any number from 1 to 9 and then click enter\n
          or just click enter with the default value\n
          each number moves the turtle an x amount of steps, some buttons more than the others...\n
          figuring out the pattern will increase your chance of winning!
"""
message.write(rules, move=False, align="center", font=("Arial", 25, "normal",'bold','italic'))
time.sleep(16)
clearscreen()
# let the user enter his initial budget, it should be greater than 15$ - the minimum entry for each round
while True:
    suspense.play(True)
    message.color('red')
    try:
        starting_budget = float(textinput("starting budget","please enter your initial budget -- it should be equal to or larger than 15$  "))
        if starting_budget < 15:
            message.write("you have entered a budget less than 15$",move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
            time.sleep(3)
            clearscreen()
        else:
            break
    except Exception as x:
        message.write(x,move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
        time.sleep(3)
        clearscreen()
budget+=starting_budget

# start interacting with the user
#introuce the turtles:
message.color('green')
message.write("introducing the racing turtles", move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
time.sleep(4)
clearscreen()
introduce_turtles()
quit_game = False
while not (quit_game):
    # show the user his performance summary
    suspense.play()
    summary()
    #suggest for the user to double his budget after playing more than two rounds
    if rounds_counter>=1:
        message.color('red')
        while True:
            try:
                d =textinput("double your budget","to double your budget press 'y' else press 'n' ")
                if d!='y' and d!='n':
                    message.write("your answer should be 'y' or 'n'\n y =yes, n=no", move=False, align="center", font=("Arial", 27, "normal",'bold','italic'))
                    time.sleep(3)
                    clearscreen()
                    continue
            except Exception as x:
                message.write(x, move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
            if d=='y':
                budget*=2
                message.color('green')
                message.write(f"great choice!\nyour new budget is {current_budget()}$", move=False, align="center", font=("Arial", 27, "normal",'bold','italic'))
                time.sleep(3)
                clearscreen()
                break
            else:
                break
# choose winning turtle
    while True:
        chosen_turtle = textinput("choose your turtle", "pick t1 or t2 or t3 or t4")
        if chosen_turtle == 't1' or chosen_turtle == 't2' or chosen_turtle == 't3' or chosen_turtle == 't4':
            break
        else:
            message.color('red')
            message.write(
                "you have entered an invalid name\nReminder: the name of the turtle should be: t1 or t2 or t3 or t4",move=False, align="center", font=("Arial", 30, "normal",'bold','italic')
            )
            time.sleep(4)
            clearscreen()
# placing bet amount:
    while True:
        message.color('red')
        try:
            bet_amount = float(textinput("bet", "please enter betting amount"))
            if bet_amount < 15:
                message.write('cant place bet lower than 15$',move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
                time.sleep(3)
                clearscreen()

            elif bet_amount > current_budget():
                message.write(f"can't place bet higher than your current budget which is: {current_budget()}$",move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
                time.sleep(4)
                clearscreen()
            else:
                break
        except Exception as x:
            message.write(x,move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
            time.sleep(3)
            clearscreen()
    rounds_counter+=1
### check user's result
    ### first check for a draw:
    suspense.stop()
    while True:
        race_winner = create_race(chosen_turtle)  ### dictionary which contains the winning turtle name,colour and number of taken steps
        if check_draw(finished_race_info, race_winner):
            message.write('there has been a Draw!\nthe race will be recreated',move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
            time.sleep(5)
            clearscreen()
            continue  ### if there was a draw between the winning turtle and another turtle - repeat the race
        else:
            break
# check if the user won:
    if chosen_turtle == race_winner["name"]:
        crowd_applause.play(True)
        message.color('green')
        message.write(
            f"congrats! your turtle has won the race!\n\nwe have added {bet_amount * 3}$ to your budget!",
            move=False, align="center", font=("Arial", 30, "normal",'bold','italic')
        )
        time.sleep(5)
        crowd_applause.stop()
        clearscreen()
        budget+=bet_amount * 3
        wins_and_losses.append(bet_amount * 3)
    else:
        dissapointed_crowd.play(True)
        message.color('red')
        message.write(f"your turtle lost the race\n you have lost {bet_amount * 0.5}$ from your budget\n\nkeep trying!",
                      move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
        time.sleep(4)
        dissapointed_crowd.stop()
        clearscreen()
        budget-=bet_amount * 0.5
        wins_and_losses.append(-0.5 *bet_amount)
 # check bonus:
    if race_winner["steps"] >= 200:
        crowd_applause.play(True)
        message.color('green')
        message.write(
            f"BONUS: your turtle took: {race_winner['steps']} steps,\n\n we have added 10$ to your budget"
        ,move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
        time.sleep(4)
        crowd_applause.stop()
        clearscreen()
        budget+=10
        wins_and_losses.append(10)
 # make sure that the user still has enough money to play
    if (not enough_money_to_play()):
        message.color('red')
        message.write(f"you have now reached a budget less than 15 as you currently have:{current_budget()}$"
                      ,move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
        time.sleep(5)
        clearscreen()
        while True:
            want_to_play = textinput("continue playing?", "to continue-> y , to quit-> n")
            if (not want_to_play.lower() == 'y') and (not want_to_play.lower() == 'n'):
                message.write("invalid answer, please enter y or n",move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
                time.sleep(3)
                clearscreen()
            else:
                break

        if want_to_play.lower() == 'y':
            message.color('green')
            message.write("let's play again!",move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
            time.sleep(3)
            clearscreen()
            # initiate a new budget for the customer
            while True:
                message.color('red')
                message.write(f"REMINDER: your current budget should be larger than 15$\n it currently is: {current_budget()}$"
                              ,move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
                time.sleep(4)
                clearscreen()
                try:
                    deposit = (float(textinput("new deposit", "enter new deposit to continue")))
                    if deposit + current_budget() < 15:
                        message.write("your budget plus the added deposit total is  less than 15$"
                                      ,move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
                        time.sleep(4)
                        clearscreen()
                    else:
                        # initiate a new deposit for the customer
                        budget+=deposit
                        break
                except Exception as x:
                    message.write(x,move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
                    time.sleep(3)
                    clearscreen()
        else:
            message.color('black')
            message.write("thanks for patricipating, see you soon!",move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
            time.sleep(3)
            clearscreen()
            quit_game = True
    else:  # if the user does have enough money to play
        while True:
            another_round = textinput("one more round? ", "to continue type: y , to quit type: n ")
            if ((not another_round.lower() == 'y') and (not another_round.lower() == 'n')):
                message.color('red')
                message.write("invalid answer, please enter y or n ",move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
                time.sleep(3)
                clearscreen()
            else:
                break
        if another_round.lower() == 'y':
            message.color('green')
            message.write("good luck!",move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
            time.sleep(3)
            clearscreen()
        else:
            message.color('black')
            message.write("thanks for participating, see you soon!",move=False, align="center", font=("Arial", 30, "normal",'bold','italic'))
            time.sleep(3)
            clearscreen()
            quit_game = True
clearscreen()
#show the user his final summary
summary()
# gives the user gifts after finishing playing
message.write("your gifts are in the 'urls.txt' file\ntheir description is in the 'output.jsonl' file",move=False, align="center", font=("Arial",30, "normal",'bold','italic'))
time.sleep(4.5)
clearscreen()
# product_data = []
with open("urls.txt", 'r') as urllist:
    with open('output.jsonl', 'w') as outfile:
        for url in urllist.read().splitlines():
            data = scrape(url)
            if data is not None:
                json.dump(data, outfile)
                outfile.write("\n")
