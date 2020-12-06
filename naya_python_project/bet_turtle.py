from turtle import *
from random import randint
from pathlib import Path

chosen_turtle = ""  # the turtle which the user bets on
bet_amount = 0  # the betting amount
guessed_steps = 0  # gussed number of steps of the winning turtle
finished_race_info = []  # as the name suggest, info about the race

### colours:
RED = '\u001b[31m'  # the colour red (will be used for printing errors)
BLUE = '\u001b[34m'  # colour presented when the user wins
RESET = '\u001b[0m'  # RESET returns the colour to default
BOLD = '\u001b[1m'
UNDERLINE = '\u001b[4m'


def create_race() -> dict:
    "function that creates the race and returns a dictionary which contains all the infromation about the winning turtle"

    # create a pen to write the lanes of the race track
    lanes_pen = Turtle()
    lanes_pen.speed(0)
    lanes_pen.penup()
    lanes_pen.goto(-150, 150)

    # creating the race track which consists of 15 vertical lanes (0-14)

    for lane_numb in range(14 + 1):
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

        # creating the first racing turtle
    t1 = Turtle()
    t1.color('green')
    t1.shape('turtle')

    # move turtle number 1 to the starting point of the race which is (-160 , y1)
    t1.penup()
    t1.goto(-160, 110)
    t1.pendown()

    # introduce turtle 1 : turn the turtle by 360 degrees (doesnt change nothing - just a cool way to introduce the turtle)
    for turn in range(36):
        t1.right(10)

    # create turtle number 2
    t2 = Turtle()
    t2.color('purple')
    t2.shape('turtle')

    # moving turtle number 2 to its starting point(-160,y2<y1)
    t2.penup()
    t2.goto(-160, 75)
    t2.pendown()

    # introduce turtle 2
    for turn in range(72):
        t2.left(5)

    # create turtle number 3
    t3 = Turtle()
    t3.shape('turtle')
    t3.color('blue')

    # moving turtle 3 to its starting point(-160,y3<y2)
    t3.penup()
    t3.goto(-160, 40)
    t3.pendown()

    # introduce turtle 3
    for turn in range(60):
        t3.right(6)
    # create turtle 4
    t4 = Turtle()
    t4.shape('turtle')
    t4.color('orange')
    # moving turtle 4 to its starting point(-160,y4<y3)
    t4.penup()
    t4.goto(-160, 5)
    t4.pendown()

    # introduce turtle 4
    for turn in range(30):
        t4.left(12)
    # create a list of steps for each turtle
    turtle_step_counter = [0, 0, 0, 0]
    turtle_names = ["t1", "t2", "t3", "t4"]
    turtle_colors = ["green", "purple", "blue", "orange"]

    ### initiate the race by moving each turtle x steps , where x is a random number between 1 and 5
    # after each time the turtle moves forward- save its number of steps to the step-counter list
    for time in range(100):
        t1_steps = randint(1, 5)
        t1.forward(t1_steps)
        turtle_step_counter[0] += t1_steps
        t2_steps = randint(1, 5)
        t2.forward(t2_steps)
        turtle_step_counter[1] += t2_steps
        t3_steps = randint(1, 5)
        t3.forward(t3_steps)
        turtle_step_counter[2] += t3_steps
        t4_steps = randint(1, 5)
        t4.forward(t4_steps)
        turtle_step_counter[3] += t4_steps

    global finished_race_info  # i want to use the variable outside the method thus 'global'
    finished_race_info = list(zip(turtle_step_counter, turtle_names, turtle_colors))

    #clear the screen from the prevoius race:
    clearscreen()

    #return winner info
    return (
    {"name": max(finished_race_info)[1], "color": max(finished_race_info)[2], "steps": max(finished_race_info)[0]})


def check_draw(l: list, d: dict) -> bool:
    "functions that checks if there was a draw between the winning turtle and a different turtle and re-creates the race"
    to_return = False
    for steps, turtle_name, turtle_color in l:
        if d["steps"] == steps and d["name"] != turtle_name:
            colour_print_manyarguments("there was a Draw! the race will be re-created!", RED, BOLD, UNDERLINE)
            to_return = True

    return to_return


def current_budget() -> int:
    "function that returns the current budget of the user"
    sum = 0
    with open(filepath) as f_in:
        for line in f_in.readlines():
            line = line.strip()
            # since there is not direct int value of lateral with base - number, then we need to strip the - from the string and do it ourselves
            if '-' in line:
                line = line[1:]
                sum -= (float(line))
            else:
                sum += (float(line))
    return sum


# function that checks if the user still has enough money to play
def enough_money_to_play() -> bool:
    "function that check if the user still has enough money to play(minimum 15$), returns True or False"

    if current_budget() < 15:
        return False
    else:
        return True


def colour_print(text: str = "", effect: str = "") -> None:
    """
    print a given `string` by adding a given effect to it

    :param text: inputed string to be printed
    :param effect: string that represents the effect to be made to 'text'

    """
    output_string = "{0}{1}{2}".format(effect, text,
                                       RESET)  # the RESET is added to make sure that after each call we change the colour
    print(output_string)


def colour_print_manyarguments(text: str = "", *effects) -> None:
    """
    print a given  `str` by adding effect/effects on it
    :param text: string given as an input to the function
    :param effects: string\strings given as input to make effects on the text string

    """
    effects_string = " ".join(effects)
    output_string = "{0}{1}{2}".format(effects_string, text, RESET)
    print(output_string)


def smiley(s: str) -> None:
    "display happy/sad smiley when user wins/loses"

#initiate turtle and draw the smiley eyes:

    smiles = Turtle()
    smiles.penup()
    smiles.goto(-75,150)
    smiles.pendown()
    smiles.circle(10)     #eye one

    smiles.penup()
    smiles.goto(75,150)
    smiles.pendown()
    smiles.circle(10)     #eye two

    if s=='happy':
        smiles.penup()
        smiles.goto(0,0)
        smiles.pendown()
        smiles.circle(100,90)   #right smile

        smiles.penup()
        smiles.setheading(180) # <-- look West
        smiles.goto(0,0)
        smiles.pendown()
        smiles.circle(-100,90)

    elif s=='sad':
        smiles.penup()
        smiles.goto(0,50)
        smiles.pendown()
        smiles.circle(-100,90)

        smiles.penup()
        smiles.setheading(180)
        smiles.goto(0,50)
        smiles.pendown()
        smiles.circle(100,90)
    clearscreen()


# create a file which contains the user's winning and losses plus his initial budget (100$ gift)
# we will update the money amount according to the user's winning or losses

filepath = Path('.') / 'budget.txt'

# let the user enter his initial budget, it should be greater than 15$- the minimum entry for each round
while True:
    try:
        starting_budget=float(input("please enter your initial budget -- it should be equal to or larger than 15$   "))
        if starting_budget<15:
            print("you have entered a budget less than 15")
        else:
            break
    except Exception as x:
        print(x)


with open(filepath, 'w') as f:
    print(f"{starting_budget}", file=f)  # start with granting the user free 100$



# start interacting with the user
print("""
welcome to the turtle race betting, carefully read the instructions, then place your bet.\n
we have added 100$ to your budget as you initial starting amount\n
the minimum entry amount for each round is 15$\n
in this race four turtles 't1','t2','t3','t4' participate, pick your winner\n
if you choose correctly - we will triple your winnings, however if you lose, then you will lose 50% of the entered amount
""")

quit_game = False
while not (quit_game):
    # show the user his current budget
    print(f"your current budget is: {current_budget()}$")
    print()

    # choose winning turtle
    while True:
        chosen_turtle = textinput("choose your turtle", "pick t1 or t2 or t3 or t4")
        if chosen_turtle == 't1' or chosen_turtle == 't2' or chosen_turtle == 't3' or chosen_turtle == 't4':
            break
        else:
            colour_print(
                "you have entered an invalid name\nReminder: the name of the turtle should be: t1 or t2 or t3 or t4",
                RED)

    # placing bet amount:
    while True:
        try:
            bet_amount = float(textinput("bet", "please enter betting amount"))
            if bet_amount < 15:
                colour_print('cant place bet lower than 15$', RED)

            elif bet_amount > current_budget():
                colour_print(f"cant place bet higher than your current budget which is:{current_budget()}", RED)

            else:
                break
        except Exception as x:
            colour_print(x, RED)

    ### check user's result

    ### first check for a draw:
    while True:
        race_winner = create_race()  ### dictionary which contains the winning turtle name,colour and number of taken steps
        if check_draw(finished_race_info, race_winner):
            continue  ### if there was a draw between the winning turtle and another turtle - repeat the race
        else:
            break

    # check if the user won:
    if chosen_turtle == race_winner["name"]:
        colour_print_manyarguments(
            f"congrats! you have guessed the winning turtle correctly!\nyou have added {bet_amount * 3}$ to your budget!",
            BLUE, BOLD, UNDERLINE)
        smiley('happy')
        with open(filepath, 'a') as f_append:
            print(f"{bet_amount * 3}", file=f_append)
        print(f"your current budget is: {current_budget()}$")
        print()
    else:
        print(f"you have not guessed the winning turtle correctly\n you lost {bet_amount * 0.5}$\nkeep trying!")
        smiley('sad')
        with open(filepath, 'a') as f_append:
            print(f"{-(bet_amount * 0.5)}", file=f_append)
        print(f"your current budget is: {current_budget()}$")
        print()

    # check bonus:
    if race_winner["steps"] > 400:
        colour_print_manyarguments(
            f"BONUS: your turtle took: {race_winner['steps']} steps,\n we have added 10$ to your budget", BLUE, BOLD,
            UNDERLINE)

        with open(filepath, 'a') as fapp:
            print("10", file=fapp)
        print(f"your current budget is: {current_budget()}$")
        print()

    # make sure that the user still has enough money to play
    if (not enough_money_to_play()):
        colour_print(f"you have now reached a budget less than 15 as you currently have:{current_budget()}",RED)
        while True:
            want_to_play = textinput("continue playing?", "to continue-> y , to quit-> n")
            if (not want_to_play.lower() == 'y') and (not want_to_play.lower() == 'n'):
                colour_print("invalid answer, please enter y or n", RED)
            else:
                break

        if want_to_play.lower() == 'y':
            print("let's play again!")
            # initiate a new budget for the customer
            while True:
                colour_print(f"REMINDER: your current budget should be larger than 15$, it currently is: {current_budget()}",RED)
                try:
                    deposit = int(float(textinput("new deposit", "enter new deposit to continue")))
                    if deposit + current_budget() < 15:
                        colour_print("your budget plus the added deposit total is  less than 15$", RED)
                    else:
                        # initiate a new deposit for the customer
                        with open(filepath, 'a') as f_new:
                            print(f"{deposit}", file=f_new)
                            break

                except Exception as x:
                    colour_print(x, RED)

        else:
            print("thanks for patricipating, see you soon!")
            quit_game = True

    else:  # if the user does have enough money to play
        while True:
            another_round = textinput("one more round? ", "to continue type: y , to quit type: n ")
            if ((not another_round.lower() == 'y') and (not another_round.lower() == 'n')):
                colour_print("invalid answer, please enter y or n ", RED)

            else:
                break
        if another_round.lower() == 'y':
            print("good luck!")
        else:
            print("thanks for participating, see you soon!")
            quit_game = True
colour_print_manyarguments(f"you have finished the game with a budget of {current_budget()}$",BOLD)