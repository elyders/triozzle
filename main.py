import numpy as np
from js import document, setInterval, clearInterval
import time
from datetime import datetime, timedelta
import asyncio
from pyodide.ffi import to_js
import pyclip as pc

# global variables
guess_list = [0 for i in range(3)]
game_result = "??"
start_time = 0.0
end_time = 0.0
game_status = "loading"
game_type = 'daily'
total_rounds = 10
curr_round = 0
round_times = [0 for i in range(total_rounds)]
errors_allowed = 3
num_of_errors = errors_allowed
error_penalty = 5
random_seed = time.gmtime()
current_date = datetime.now()
rng_seed = int(current_date.year + current_date.month + current_date.day + 17)
rng = np.random.default_rng(rng_seed)
timerVal = 0
intervalId = 0
timerElement = Element("timer")

#################################################
async def main():
    # Setup game: create grid, game_result, buttons,  etc...
    setup_game()
    
    main = document.getElementById("main")
    main.style.display = "inline"

#################################################
def update_timer(timerElement):
    global timerVal

    timerVal += .1
    timerElement.write(round(timerVal,2))

#################################################
def reset_page():
    document.getElementById("endOverlay").style.width = "0";

    startBtn = document.getElementById("startOverlay")
    startBtn.style.display = "flex"

    grid = document.getElementById("grid")
    grid.style.display = "none"

    gamebartop = document.getElementById("gamebartop")
    gamebartop.style.display = "none"

    gamebarbottom = document.getElementById("gamebarbottom")
    gamebarbottom.style.display = "none"

#################################################
def setup_game():
    global game_status
    global curr_round
    global num_of_errors
    global timerElement

    game_status = "setting"
    
    # Loop thru every row/column combo and hide each btn
    # Rows are 1-10; Columns are 0-9
    rows_cols = 10
    for rowid in range(1,rows_cols+1):
        for colid in range(0,rows_cols):
            btn = Element(f"btn{rowid}{colid}")
            btn.remove_class("btn_shown")	
            btn.add_class("btn_hidden")	

    game_status = "waiting"
    curr_round = 0
    num_of_errors = 0
    timerElement.write(0.0)
    

#################################################
def crt_grid():
    numcells = 100
    rows_cols = 10
    
    grid = document.getElementById("grid")
    grid.style.display = "none"
    
    # Loop thru every row/column combo and get a random integer for each btn
    # Rows are 1-10; Columns are 0-9
    for rowid in range(1,rows_cols+1):
        for colid in range(0,rows_cols):
            btnElement = Element(f"btn{rowid}{colid}")
            btnElement.remove_class("btn_chosen")	
            btnElement.remove_class("btn_shown")	
            #btnElement.add_class("btn_hidden")	

            # Create random value (0-9) for btn
            cell_num = rng.integers(0, 10)
            btnElement.write(f"{cell_num}")
            #btnElement.write(f"{rowid}{colid}") # For testing only

#################################################
def crt_game_result(numcells):
    # Create the game_result from any 3 cells in the grid
    rows_cols = np.round(np.sqrt(numcells)).astype(int)
    rowdirection = None
    coldirection = None
    
    # Rows are 1-10; Columns are 0-9
    cellrow1 = rng.integers(1, rows_cols + 1)
    cellcol1 = rng.integers(0, rows_cols)
    handle_msg(0,f"Result:{cellrow1},{cellcol1}")

    # middle cell in 3x3 grid can't be part of the game_result
    # 10  11  12
    # 20 x21x 22
    # 30  31  32
    if rows_cols == 3 and cellrow1 == 2 and cellcol1 == 1:
        cellrow1 += rng.choice([-1, 1]) # move 1 row up or down
        cellcol1 += rng.choice([-1, 1]) # move 1 column left or right
        handle_msg(0,["Changed:",cellrow1,cellcol1])
    
    # Get the row/column direction for next cell (-1=move up/left; 0=same row/column; 1=move down/right)
    # Handle the corners: The 4 cells that make up a corner can only move away from corner
    if cellrow1 <= 2 and cellcol1 <= 1:
        # top left corner can only move down or right
        coldirection = rng.choice([1, 0])
        if coldirection == 0: # if column is not moving, row must move
            rowdirection = 1
        else:
            rowdirection = rng.choice([1, 0])
    elif cellrow1 >= rows_cols - 1 and cellcol1 <= 1:
        # bottom left corner can only move up or right
        coldirection = rng.choice([1, 0])
        if coldirection == 0: # if column is not moving, row must move
            rowdirection = -1
        else:
            rowdirection = rng.choice([-1, 0])
    elif cellrow1 <= 2 and cellcol1 >= rows_cols - 2:
        # top right corner can only move down or left
        coldirection = rng.choice([-1, 0])
        if coldirection == 0: # if column is not moving, row must move
            rowdirection = 1
        else:
            rowdirection = rng.choice([1, 0])
    elif cellrow1 >= rows_cols - 1 and cellcol1 >= rows_cols - 2:
        # bottom right corner can only move up or left
        coldirection = rng.choice([-1, 0])
        if coldirection == 0: # if column is not moving, row must move
            rowdirection = -1
        else:
            rowdirection = rng.choice([-1, 0])
    # Handle some of 3x3 grid options separately
    elif rows_cols == 3:
        # Left cell can only move right
        if cellrow1 == 2 and cellcol1 == 0:
            coldirection = 1
            rowdirection = 0
        # Top cell can only move down
        elif cellrow1 == 1 and cellcol1 == 1:
            coldirection = 0
            rowdirection = 1
        # Bottom cell can only move up
        elif cellrow1 == 3 and cellcol1 == 1:
            coldirection = 0
            rowdirection = -1
        # Right cell can only move left
        elif cellrow1 == 2 and cellcol1 == 2:
            coldirection = -1
            rowdirection = 0
    else:
        # if at last 2 columns, can only move to left/center (-1/0)
        if cellcol1 >= rows_cols - 2:
            coldirection = rng.choice([-1, 0])
        # if at first 2 columns, can only move to right/center (0/1)
        elif cellcol1 <= 2:
            coldirection = rng.choice([0, 1])
        else: # Otherwise, column can move any direction
            coldirection = rng.integers(-1, 1)

        # if column direction is center(coldirection=0)...
        if coldirection == 0:
            #... and cell is in last 2 columns, next cell must be to the left(1)
            if cellrow1 <= 2:
                rowdirection = 1
            #... and cell is in first 2 columns, next cell must be to the right(-1)
            elif cellrow1 >= rows_cols - 1:
                rowdirection = -1
            else: # ... row can't be center also, can only move left or right
                rowdirection = rng.choice([-1, 1])
        # If at top 2 rows, must move center or down
        elif cellrow1 <= 2:
            rowdirection = rng.choice([0, 1])
        # If at bottom 2 rows, must move center or up
        elif coldirection == -1 and cellrow1 >= rows_cols - 1:
            rowdirection = rng.choice([-1, 0])
        else: # row can mnove in any direction
            rowdirection = rng.integers(-1, 1)
    
    handle_msg(0,["Direction:",coldirection,rowdirection])

    cellrow2 = cellrow1 + rowdirection
    cellcol2 = cellcol1 + coldirection
    handle_msg(0,[cellrow2,cellcol2])

    cellrow3 = cellrow2 + rowdirection
    cellcol3 = cellcol2 + coldirection
    handle_msg(0,[cellrow3,cellcol3])
    
    try:
        Element(f"btn{cellrow1}{cellcol1}").add_class("btn_result")
        Element(f"btn{cellrow2}{cellcol2}").add_class("btn_result")
        Element(f"btn{cellrow3}{cellcol3}").add_class("btn_result")
    except:
        handle_msg(2,"An exception occurred assigning btn_result to cells")
        return -1
    
    # Now calculate game_result from chosen cells
    #if gLevel == 0:
    plus_minus = rng.choice([-1, 1])
    chosenValue1 = int(document.getElementById(f"btn{cellrow1}{cellcol1}").innerHTML)
    chosenValue2 = int(document.getElementById(f"btn{cellrow2}{cellcol2}").innerHTML)
    chosenValue3 = int(document.getElementById(f"btn{cellrow3}{cellcol3}").innerHTML)
    game_result = chosenValue1 * chosenValue2 + (chosenValue3 * plus_minus)
    handle_msg(0,["Chosen:",chosenValue1,"*",chosenValue2,plus_minus,chosenValue3,"=",game_result])

    
    return game_result

#################################################
def reset_header():
    global timerElement

    game_resultElement = Element("game_result")
    game_resultElement.write("??")

    roundElement = Element("curr_round")
    roundElement.write("0")

    errElement = Element("num_of_errors")
    errElement.write("0")

    timerElement.write(0.0)
#################################################
def start_game(type):
    global start_time
    global game_status
    global curr_round
    global game_result
    global intervalId
    global timerElement
    global timerVal
    global rng
    global game_type

    if type == 'practice':
        game_type = type
        rng = np.random.default_rng()

    handle_msg(0,f"Seed:{rng_seed}")

    curr_round += 1
    if curr_round > total_rounds:
        game_status = "winner"
        end_game()
    else:
        crt_grid()
        game_result = crt_game_result(100)
        if game_result == -999:
            handle_msg(2,"ERROR in crt_game_result")
        elif game_status == "waiting":
            reset_header()

        #startBtn = Element("startOverlay")
        #startBtn.add_class("btn_hidden")
        startBtn = document.getElementById("startOverlay")
        startBtn.style.display = "none"

        grid = document.getElementById("grid")
        grid.style.display = "grid"

        gamebartop = document.getElementById("gamebartop")
        gamebartop.style.display = "grid"

        gamebarbottom = document.getElementById("gamebarbottom")
        gamebarbottom.style.display = "grid"

        # Loop thru every row/column combo and show each btn
        # Rows are 1-10; Columns are 0-9
        rows_cols = 10
        for rowid in range(1,rows_cols+1):
            for colid in range(0,rows_cols):
                btn = Element(f"btn{rowid}{colid}")
                btn.remove_class("btn_hidden")	
                btn.add_class("btn_shown")	

        game_resultElement = Element("game_result")
        game_resultElement.write(f"{game_result}")

        # Get starting time so we can compare it to ending time for round
        start_time = time.time()
        handle_msg(0,f"Start:{start_time}")

        roundElement = Element("curr_round")
        roundElement.write(f"{curr_round}")

        game_status = "playing"
        handle_msg(0,f'{game_status}')

        # stop and reset timer
        js.clearInterval(intervalId);
        timerVal = 0
        intervalId = setInterval(to_js(lambda: update_timer(timerElement)),100)

#################################################
def end_game():
    global game_status
    global game_type

    # stop timer
    js.clearInterval(intervalId);
    
    # Loop thru every row/column combo and hide each btn
    # Rows are 1-10; Columns are 0-9
    rows_cols = 10
    for rowid in range(1,rows_cols+1):
        for colid in range(0,rows_cols):
            btn = Element(f"btn{rowid}{colid}")
            btn.add_class("btn_hidden")
            btn.remove_class("btn_shown")
    
    # Set end title based on game_type
    if game_type == 'daily':
        document.getElementById("endTitle").innerHTML = "Triozzle Daily Challenge"
    else:
        document.getElementById("endTitle").innerHTML = "Triozzle Practice"

    # Show player's final score
    handle_msg(0,f"game_status:{game_status}")
    if game_status == "winner":
        document.getElementById("endScore").innerHTML = "Score: " + str(get_score())

        # Show num of seconds for each round
        timesTxt = ""
        for i in range(len(round_times)):
            timesTxt += f"Round {i}: " + str(round_times[i]) + "<br>"

        document.getElementById("endTimes").innerHTML = timesTxt

    elif game_status == "loser":
        document.getElementById("endScore").innerHTML = "Better luck next time"
        if game_type == 'daily':
            document.getElementById("endTimes").innerHTML = "You can try again tomorrow"
        else:
            document.getElementById("endTimes").innerHTML = "Keep practicing!"
          

    # Get current date/time
    current_time = time.gmtime()
    current_datetime = datetime(*current_time[:6])  # Convert time.struct_time to datetime object

    # Add one day to the current datetime
    next_day_datetime = current_datetime + timedelta(days=1)
    next_day_time = next_day_datetime.timetuple()

    document.getElementById("endDateTime").innerHTML = time.strftime("%B %d, %Y %H:%M:%S",current_time)
    document.getElementById("nextgameDateTime").innerHTML = "Next Game: " + time.strftime("%B %d, %Y 00:00:00",next_day_time)
    document.getElementById("endOverlay").style.width = "100%";

#################################################
def btn_click(id):
    global end_time
    handle_msg(0,[id," clicked!"])
    
    end_time = time.time()
    global guess_list
    
    btn = Element(f"btn{id}")
    btn.add_class("btn_chosen")

    handle_msg(0,["Guess: ",guess_list])
    
    # See if they clicked on an existing guess. If so, unchoose it:
    if id == guess_list[0]:
        # Unchoose 1st guess and make 2nd guess 1st guess or clear out 1st guess
        btn.remove_class("btn_chosen")
        if guess_list[1] != 0:
            guess_list[0] = guess_list[1]
            guess_list[1] = 0
        else:
            guess_list[0] = 0
    elif id == guess_list[1]:
        # Unchoose 2nd guess
        btn.remove_class("btn_chosen")
        guess_list[1] = 0
    else:
        # See which guess this is: 1st, 2nd or 3rd
        if guess_list[0] == 0:
            guess_list[0] = id
        elif guess_list[1] == 0:
            # Check that their 2nd guess is valid: should be adjacent to 1st guess
            if abs(guess_list[0] - id) not in {10, 1, 11, 9}:
                handle_msg(0,f"Invalid guess:{guess_list[0]} {id}")
                btn.remove_class("btn_chosen")
            else:
                guess_list[1] = id
        elif guess_list[2] == 0:
            # Check that their 3rd guess is valid: should be in same direction 2nd guess is from 1st guess
            if (guess_list[0] - guess_list[1]) != (guess_list[1] - id):
                handle_msg(0,f"Invalid guess:{guess_list[1]} {id}")
                btn.remove_class("btn_chosen")
            else:
                # Assign var and check guess against game_result
                guess_list[2] = id
                handle_msg(0,["Guess: ",guess_list])
                check_guess()

    handle_msg(0,["Guess: ",guess_list])

#################################################
def check_guess():
    global guess_list
    global round_times
    global curr_round
    global end_time
    global start_time
    global intervalId
    global timerElement
    global timerVal

    game_resultInt = int(document.getElementById("game_result").innerHTML)
    guessInt1 = int(document.getElementById(f"btn{guess_list[0]}").innerHTML)
    guessInt2 = int(document.getElementById(f"btn{guess_list[1]}").innerHTML)
    guessInt3 = int(document.getElementById(f"btn{guess_list[2]}").innerHTML)

    guessIntPlus = guessInt1 * guessInt2 + guessInt3
    guessIntMinus = guessInt1 * guessInt2 - guessInt3
    if guessIntPlus == game_resultInt or guessIntMinus == game_resultInt:
        handle_msg(0,f"CORRECT guess! {guessIntPlus} or {guessIntMinus} = {game_resultInt}")
        correctGuess=True
        round_times[curr_round-1] = round(end_time - start_time,3)
    else:
        handle_msg(0,f"WRONG guess! {guessIntPlus} or {guessIntMinus} != {game_resultInt}")
        correctGuess=False
    
    reset_guess()
    update_header(correctGuess)

#################################################
def reset_guess():
    handle_msg(0,"Reset Guess")

    global guess_list

    guessElement = Element(f"btn{guess_list[0]}")
    guessElement.remove_class("btn_chosen")
    guessElement = Element(f"btn{guess_list[1]}")
    guessElement.remove_class("btn_chosen")
    guessElement = Element(f"btn{guess_list[2]}")
    guessElement.remove_class("btn_chosen")
    
    guess_list[0] = 0
    guess_list[1] = 0
    guess_list[2] = 0
    handle_msg(0,["Guess: ",guess_list])

#################################################
def update_header(correct):
    global start_time
    global num_of_errors
    global errors_allowed
    global game_status
    global game_type

    if correct:
        start_game(game_type)
    else:
        num_of_errors += 1
        if num_of_errors > errors_allowed:
            game_status = "loser"
            end_game()
        else:
            errorsElement = Element("num_of_errors")
            errorsElement.write(f"{num_of_errors}")


#################################################
# Get final score
def get_score():
    global num_of_errors
    global error_penalty
    global round_times
    
    score = 0
    # Sum all round times together
    for round_time in round_times:
        score += round_time
    
    # Add penalties for errors
    score += error_penalty * num_of_errors

    return round(score,3)

#################################################
def handle_msg(msg_type, msg_text):
    # msg_type:
    #	0=normal debug msg that can be ignored in prod;
    #	1=warning msg that should be looked at;
    #	2+=error occurred that will cause app to fail
    if msg_type > 1:
        # This is a true error, so always show msg
        print(msg_text)
    else:
        # Store these in a debug file once app in production ready
        x = 1
        #print(msg_text)

#################################################
def copyResults():
    copyText = document.getElementById("endScore").innerHTML
    pc.copy(copyText)

#################################################

pyscript.run_until_complete(main())
