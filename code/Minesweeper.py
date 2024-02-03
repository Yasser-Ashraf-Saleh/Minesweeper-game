from tkinter import *
import time
import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


window = Tk()
window.geometry("423x469")
window.resizable(width = False, height = False)

window.title("Minesweeper V 1.0")

# Loading background and mine images (Ensure files exist to avoid errors)

background_image= PhotoImage(file = "1111-02.JPEG")
background_label = Label(window, image = background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
mine_image = PhotoImage(file = "MiNE.JPEG")

# Setup buttons for game options
button1 = Button(text = "New Game", width = 20, height = 2, font=("Moon", 10, 'bold'), relief = GROOVE, borderwidth = 4)
button2 = Button(text = "Highscores", width = 20, height = 2, font=("Moon", 10, 'bold'), relief = GROOVE, borderwidth = 4)
button5 = Button(text = "Help", width = 20, height = 2, font=("Moon", 10, 'bold'), relief = GROOVE, borderwidth = 4)
button6 = Button(text = "Exit", width = 20, height = 2, font=("Moon", 10, 'bold'), relief = GROOVE, borderwidth = 4)

# Position buttons on the window
button1.place(relx=.5, rely=0.40, anchor="c")
button2.place(relx=.5, rely=0.52, anchor="c")
button5.place(relx=.5, rely=0.64, anchor="c")
button6.place(relx=.5, rely=0.76, anchor="c")

n = (0,0,0) # Initial difficulty level (will be set later)
# Display help message on Help button click
def help_message(event):
    button5.configure(relief = SUNKEN)
    tk.messagebox.showinfo('Help', 'Welcome to Minesweeper !! \n \nThe rule of the game is simple, the number on a block shows the number of mines adjacent to it and you have to flag all the mines. If you find the mine, you can open unopened squares around it, opening more areas. \n \nYou can start by clicking at any random place, but generally it is better to start at the middle. \n \nMark all the mines that are downright OBVIOUS. Such as eight ONEs surrounding an unopened square. Next start finding the mines around other numbers. \n \nFinding the mines in 1 blocks helps a lot, because it opens many squares and good hints to 2s and 3s. \n \nThe game completes when you have opened all the safe blocks not when you have flagged every mine. \n \nHave fun!!')
button5.bind("<Button-1>", help_message)

# Placeholder for combined_hells function; intended to initialize game based on difficulty

def combined_hells(event):
    global n 
    global rows
    global cols
    global mines
    global buttons
    buttons = []
    # Calls an undefined function `diificulty_level`, should be corrected
    n = diificulty_level()


buttons = []
DAMAGE = []
opened_list = []
flaged_list = []
opened_buttons =[]
# Play the game based on the difficulty level chosen by the player
def play_game(n):
    # Setup game window, initialize board, place mines, and prepare event bindings
    # Start the Tkinter main loop to begin the game
    mines = n[0]
    rows = n[1]
    cols = n[2]
    global root
    global buttons
    global opened_list
    global DAMAGE
    global flaged_list
    global opened_buttons

    start_time = time.clock() # Deprecated in Python 3.8, consider using time.perf_counter() or time.process_time()
    root = Tk()
    root.resizable(width = False, height = False)
    frame = Frame(root)
    frame.pack()
    lower_frame = Frame(root)
    lower_frame.pack(side=BOTTOM)
    # Create the grid of buttons for the game board
    def create_grid(rows,cols):
        for row in range (rows):
            buttons.append([])  
            for col in range (cols):
                    b = Button(frame,background='#b3b3b3', width=2, command=lambda row=row,col=col: clickOn(row,col))
                    b.bind("<Button-3>", lambda e, row=row, col=col:onRightClick(row, col))
                    b.bind("<Button-2>", lambda e, row=row, col=col:onMiddleClick(row, col))
                    b.grid(row=row+1, column=col, sticky=N+W+S+E)
                    buttons[row].append(b)
        return buttons
        # Define additional game logic here, such as clickOn, onRightClick, onMiddleClick, and helper functions
    # Function to handle left-click on a button (game tile)
    def clickOn(row,col):
    # Check if the clicked tile is a mine, an adjacent tile, or needs to open surrounding tiles
    # Implement game logic to handle these scenarios, updating the game state accordingly
        count = 0
        global opend_list
        if (row,col) not in opened_buttons:
                opened_buttons.append((row,col))
        if is_flaged(row,col)==False:
            for i in get_surroundings(row,col):
                    if i in DAMAGE:
                        count+=1
            if count !=0 and (row,col) not in DAMAGE :
                set_numbers(count,row,col)
            elif (row,col) in DAMAGE:
                    buttons[row][col].configure(background='red')
                    gameover()
                
            else:
                    buttons[row][col].configure(background='white', command = lambda row=row,col=col: clickOn(row,col))
                    opened_list.append((row,col))
                    auto_click(row,col)
            if is_win()== True:
                open_all()
                tk.messagebox.showinfo('Minesweeper','WHAT A HERO !!\nCONGRATS FAWZY \nYou took: \n'+str(time.clock()-start_time)+'  seconds')
                answer = tk.messagebox.askquestion('Minesweeper','Do you want to play again?')
                if answer == 'yes':
                    restart_game()
                    
                else:
                    root.destroy()


 # Function to restart the game with the same settings   
    def restart_game():
    # Reset the game state, clear the board, and reinitialize the game with the same difficulty settings
        global buttons
        global opened_list
        global DAMAGE
        global flaged_list
        global opened_buttons
        buttons = []
        buttons = create_grid(rows,cols)
        DAMAGE = create_mines(mines,rows,cols)
        opened_list = []
        flaged_list = []
        opened_buttons =[]
    
    n = Button(lower_frame,background='#b3b3b3', width=20, text='Restart Game',command= restart_game)
    n.pack(side=BOTTOM)
    # Function to create mines on the game board

    def create_mines(mines,rows,cols):
    # Randomly place the specified number of mines on the board
    # Ensure no duplicates and that the placement is consistent with the game's difficulty level
        mines_list = []
        while True: 
            x= random.randint(0, rows-1)
            y= random.randint(0, cols-1)
            if (x,y)not in mines_list:
                mines_list.append((x,y))
            if len(mines_list)== mines:
                return mines_list
    DAMAGE = create_mines(mines,rows,cols)
    def is_locked(row,col):
        global locked_list
        for i in locked_list:
            if i ==(row,col):
                return True
        return False
    def get_surroundings(row,col):
            l=[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row,col+1),(row+1,col-1),(row+1,col),(row+1,col+1)]
            return l
    
    def is_flaged(row,col):
        if (row,col)in flaged_list:
            return True
        return False
    
            
    def open_all():
        for row in range (rows):
            for col in range (cols):
                for h in get_surroundings(row,col):
                    count = get_count(h)
                    if h[0]>=0 and h[1]<cols and h[0]<rows and h[1]>=0:
                        count = get_count(h)
                        if count !=0 and (h[0],h[1]) not in DAMAGE :
                            set_numbers(count,h[0],h[1])
                        elif (h[0],h[1]) in DAMAGE:
                            buttons[h[0]][h[1]].configure(background='red', command = lambda row=h[0],col=h[1]: clickOn(h[0],h[1]))
                    
                        else:
                            buttons[h[0]][h[1]].configure(background='white', command = lambda row=h[0],col=h[1]: clickOn(h[0],h[1]))
                    
    
    def gameover():
        open_all()
        tk.messagebox.showinfo('Minesweeper','YOU DIED')
        answer = tk.messagebox.askquestion('Minesweeper','Do you want to play again?')
    
        if answer == 'yes':
            restart_game()
            
        else:
            root.destroy()
            
        
   # Function to handle right-click on a button (game tile) for flagging potential mines     
    def onRightClick(row, col):
    #    photo = PhotoImage(file='gh')
    #    buttons[row][col].configure(image = photo, command = lambda row=row,col=col: clickOn(row,col))
    # Toggle a flag on the tile to mark or unmark a potential mine
    # Update the display and game state to reflect the change
        if (row,col) not in opened_buttons:
            buttons[row][col].configure(background = 'green')
            flaged_list.append((row,col))
        if is_win()== True:
            open_all()
            tk.messagebox.showinfo('Minesweeper','WHAT A HERO !!\n CONGRATS FAWZY \n YOU TOOK \n'+str(time.clock()-start_time)+' seconds')
            answer = tk.messagebox.askquestion('Minesweeper','Do you want to play again?')
            if answer == 'yes':
                restart_game()
                
            else:
                root.destroy()
# Function to handle middle-click on a button (game tile), possibly to open all surrounding tiles

    def onMiddleClick(row, col):
    # Implement logic to open all surrounding tiles if the number of flags matches adjacent mines
    # Ensure this action only occurs for tiles that logically should open surrounding tiles

        buttons[row][col].configure(background = 'gray')
        flaged_list.remove((row,col))
    def is_opend(row,col):
        if (row,col) in opened_list:
            return True
        else:
            return False
    
    def get_count(i):
        count = 0
        for k in get_surroundings(i[0],i[1]):
            if k in DAMAGE:
                count+=1
        return count
    def auto_click(row,col) :
        global opened_buttons
        global opened_list
        for i in range (10):
            for i in range (row,-1,-1):
                for j in range (col,cols):
                    if is_opend(i,j):
                        for h in get_surroundings(i,j):
                            if h[0]>=0 and h[1]<cols and h[0]<rows and h[1]>=0:
                                count = get_count(h)
                                if count !=0 and (h[0],h[1]) not in DAMAGE :
                                        set_numbers(count,h[0],h[1])
                                        if (h[0],h[1]) not in opened_buttons:
                                            opened_buttons.append((h[0],h[1]))
                    
                                else:
                                    buttons[h[0]][h[1]].configure(background='white', command = lambda row=h[0],col=h[1]: clickOn(h[0],h[1]))
                                    opened_list.append((h[0],h[1]))
                                    if (h[0],h[1]) not in opened_buttons:
                                        opened_buttons.append((h[0],h[1]))
                for j in range (col-1,-1,-1):
                    if is_opend(i,j):
                        for h in get_surroundings(i,j):
                            if h[0]>=0 and h[1]<cols and h[0]<rows and h[1]>=0:
                                count = get_count(h)
                                if count !=0 and (h[0],h[1]) not in DAMAGE :
                                        set_numbers(count,h[0],h[1])
                                        if (h[0],h[1]) not in opened_buttons:
                                            opened_buttons.append((h[0],h[1]))                         
                    
                                else:
                                    buttons[h[0]][h[1]].configure(background='white', command = lambda row=h[0],col=h[1]: clickOn(h[0],h[1]))
                                    opened_list.append((h[0],h[1]))
                                    if (h[0],h[1]) not in opened_buttons:
                                        opened_buttons.append((h[0],h[1]))        
            for i in range (row+1,rows):
                for j in range (col,cols):
                    if is_opend(i,j):
                        for h in get_surroundings(i,j):
                            if h[0]>=0 and h[1]<cols and h[0]<rows and h[1]>=0:
                                count = get_count(h)
                                if count !=0 and (h[0],h[1]) not in DAMAGE :
                                        set_numbers(count,h[0],h[1])
                                        if (h[0],h[1]) not in opened_buttons:
                                            opened_buttons.append((h[0],h[1]))                            
                                else:
                                    buttons[h[0]][h[1]].configure(background='white', command = lambda row=h[0],col=h[1]: clickOn(h[0],h[1]))
                                    opened_list.append((h[0],h[1]))
                                    if (h[0],h[1]) not in opened_buttons:
                                        opened_buttons.append((h[0],h[1]))
                for j in range (col-1,-1,-1):
                    if is_opend(i,j):
                        for h in get_surroundings(i,j):
                            if h[0]>=0 and h[1]<cols and h[0]<rows and h[1]>=0:
                                count = get_count(h)
                                if count !=0 and (h[0],h[1]) not in DAMAGE :
                                        set_numbers(count,h[0],h[1])
                                        if (h[0],h[1]) not in opened_buttons:
                                            opened_buttons.append((h[0],h[1]))
                                else:
                                    buttons[h[0]][h[1]].configure(background='white', command = lambda row=h[0],col=h[1]: clickOn(h[0],h[1]))
                                    opened_list.append((h[0],h[1]))
                                    if (h[0],h[1]) not in opened_buttons:
                                        opened_buttons.append((h[0],h[1]))
    def is_win(): # Function to check if the game has been won or lost
     # Determine win condition (all non-mine tiles opened or all mines flagged)
    # Check game state and provide feedback to the player       
        count = 0
        for i in flaged_list:
            if i in DAMAGE:
                count+=1
        if count==mines or len(opened_buttons)==(cols*rows)-mines:
            return True
        else:
            return False
    buttons = create_grid(rows,cols)
    root.mainloop()
        








# Custom difficulty level setup by the user
def difficulty_level_custom():
    # Function definitions for handling custom difficulty settings
    # Consider adding validation for user inputs to ensure game can start with reasonable settings
    global n
#    global root
#    root.destroy()
    def call():
        global n
        n = (int(mines_entry.get()),int(rows_entry.get()),int(cols_entry.get()))
        
    def destroy():
        root1.destroy()
    root1= Tk()
    upper_frame = Frame(root1)
    upper_frame.pack()
    label1 = Label(upper_frame, text='custom level')
    label1.pack()
    down_frame = Frame(root1)
    down_frame.pack(side=BOTTOM)    
    mines_entry= Entry(down_frame)  
    rows_entry = Entry(down_frame)
    cols_entry = Entry(down_frame)
    mines_num = Label(down_frame,text = 'set number of mines')
    rows_num = Label(down_frame,text = 'set number of rows')
    cols_num = Label(down_frame,text = 'set number of cols')
    SETTER = Checkbutton(down_frame, text = 'SET',command = call)
    Start = Button(down_frame, text= ' start game ' , command = destroy)
    Start.grid(row=4,columnspan=2)
    SETTER.grid(row=3,columnspan= 2)
    mines_num.grid(row=0,column=0)
    rows_num.grid(row=1,column=0)
    cols_num.grid(row=2,column=0)
    mines_entry.grid(row=0,column=1)
    rows_entry.grid(row=1,column=1)  
    cols_entry.grid(row=2,column=1)
    root1.mainloop()
    return n


def diificulty_level():
    # Actual implementation of difficulty level selection should go here
    def easy():
        global n
        n = (7,10,8)
        return n
    def hard():
        global n
        n = (30,20,15)
        return n
    def medium():
        global n 
        n = (15,14,11)
        return n
    def expert():
        global n 
        n =(100,25,20)
    def destrooy ():
        global window
        root2.destroy()
        play_game(n)
        
        
    root2 = Tk()
    upper_framee = Frame(root2)
    label = Label(upper_framee,text = 'level setter')
    upper_framee.pack()
    lower_framee = Frame(root2)
    easy_button = Checkbutton(lower_framee, text= 'Patric star' , fg = 'blue' , command = easy)
    medium_button = Checkbutton(lower_framee, text= 'e**(-(x**2))' , fg = 'green' , command = medium)
    hard_button = Checkbutton(lower_framee, text= 'Tyrion Lannister' , fg = 'red' , command = hard)
    expert_button = Checkbutton(lower_framee, text= ' SEVEN HELLS' , fg = 'red' , command = expert)
    easy_button.grid(row = 0 , columnspan = 3)
    medium_button.grid(row = 1 , columnspan = 3)
    hard_button.grid(row = 2 , columnspan = 3)
    expert_button.grid(row = 3 , columnspan = 3)

    starter = Button(lower_framee, text= 'lets go',command= destrooy)
    starter.grid(row = 6, columnspan = 5)
    lower_framee.pack(side= BOTTOM)
    h = Button(lower_framee, text='custom',command= difficulty_level_custom)
    h.grid(row = 5, columnspan = 5)

    lower_framee.pack(side= BOTTOM)

    root2.mainloop()
    return n
# Update button appearances based on the number of adjacent mines

def set_numbers(counts,row,col):
    # Define the appearance of buttons based on the count of adjacent mines
    if counts==1:
        buttons[row][col].configure(foreground = '#22b573', font = ('Helvetica 9 bold'), background='#f2f2f2',text=str(counts), command = lambda row=row,col=col: clickOn(row,col))
    elif counts ==2:
        buttons[row][col].configure(foreground = '#29abe2', font = ('Helvetica 9 bold'), background='#f2f2f2',text=str(counts), command = lambda row=row,col=col: clickOn(row,col))
    elif counts ==3:
        buttons[row][col].configure(foreground = '#c1272d', font = ('Helvetica 9 bold'), background='#f2f2f2',text=str(counts), command = lambda row=row,col=col: clickOn(row,col))
    elif counts ==4:
        buttons[row][col].configure(foreground = '#f7931e', font = ('Helvetica 9 bold'), background='#f2f2f2',text=str(counts), command = lambda row=row,col=col: clickOn(row,col))
    elif counts ==5:
        buttons[row][col].configure(foreground = '#1b1464', font = ('Helvetica 9 bold'), background='#f2f2f2',text=str(counts), command = lambda row=row,col=col: clickOn(row,col))
    elif counts ==6:
        buttons[row][col].configure(foreground = '#662d91', font = ('Helvetica 9 bold'), background='#f2f2f2',text=str(counts), command = lambda row=row,col=col: clickOn(row,col))
    elif counts ==7:
        buttons[row][col].configure(foreground = '#8c6239', font = ('Helvetica 9 bold'), background='#f2f2f2',text=str(counts), command = lambda row=row,col=col: clickOn(row,col))
    elif counts ==8:
        buttons[row][col].configure(foreground = '#1a1a1a', font = ('Helvetica 9 bold'), background='#f2f2f2',text=str(counts), command = lambda row=row,col=col: clickOn(row,col))
# Bind the New Game button to the combined_hells function to start game setup
    
button1.bind("<Button-1>", combined_hells)



window.mainloop()
#
#
