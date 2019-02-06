"""
Hangman using a two classes
1 for logic and 1 for GUI
Widgets:root window,labels,Buttons, canvas
"""


import tkinter as tk
import random

#utility functions

#used to see if all chars in a word have been typed
#Thus you WIN when string_minus returns the empty string
def string_minus(s1,s2):
    """
    s1,s2:strings
    return:string consisting of letters in s1 not in s2
    string_minus("automobile","aom") ==> "utbile"
    string_minus("hola","lhaoxy") ==>""
    """
    diff=""
    for char in s1:
        if not(char in s2):
            diff=diff+char
    return diff

def make_display_word(word,letters_used):
    """
    word:str
    letters_used:str
    return:str - word, with underscores for letters
    that have not been used yet
    make_display_word ("automobile","aom") ==> "a __ __ o m o __ __ __ __"
    """
    display_word = ""
    for char in word:
        if char in letters_used:
            display_word += char+"  "
        else:
            display_word += "__  "
    return display_word





#logic part of game
#there should be NO GRAPHICS here.
class Hangman_game:

    def __init__(self):
    
        vocab = open("words.txt")
        self.words = list(vocab)
        
        self.start()

    def start(self):
        self.game_over = False
        self.body_parts_remaining = ["head","body","arm","arm","leg","leg"] #All the body parts
        self.body_parts_used = []
        
        self.word = random.choice(self.words).strip()
        #print(self.word)
        self.letters_used = ""
        self.message_string="" # to report a win or loss to player
        

    def make_display(self):
        """
        creates word with underscores for missing letters
        uses make_display_word, defined at top
        make_display_word ("automobile","aom") ==> "a __ __ o m o __ __ __"
        """
        return make_display_word(self.word,self.letters_used)

    def update_game(self,char):
        """
        THIS IS THE MOST IMPORTANT METHOD
        char:str - a single letter
        result:update letters_used,
        If char not in word update body_parts_used and
        body_parts_remaining (using the update_body_parts method)  
        """

        #DO NOTHING if letter has already been typed
        #or if the game is over
        if char in self.letters_used or self.game_over:
            pass #leave this pass here
        else:
            """
            update letters_used, also body parts information
            if necessary
            and check for the end of the game (win or loss)            
            
            """
            self.letters_used = self.letters_used + char
            if char not in self.word:
                self.update_body_parts()
                if self.body_parts_remaining == []:
                    self.lose_game()
            if char in self.word: 
                if string_minus(self.word, self.letters_used) == "":
                    self.win_game()
            
            
            
           #test in terminal
        #print(self.make_display())
        #print(self.body_parts_used)
        #print(self.message_string)
           
            
                
    def update_body_parts(self):
        """
        add the next body part to body_parts_used and remove it from
        body_parts_remaining
        """
        x = self.body_parts_remaining.pop(0)
        self.body_parts_used.append(x)
        
         
        
        
    def win_game(self):
        """
        result:notify player of win (on label2)
        and update the game_over attribute
        """
        self.game_over = True 
        self.message_string = self.message_string + "You Win!"
         
        
       
         

    def lose_game(self):
        """
        result:notify player of loss
        and display the word they failed to guess
        (by updating self.message_string)
        and update the game_over attribute
        """
        
        
        self.game_over = True 
        self.message_string = self.message_string + self.word + "\n" + "You Lose :("
      
        





        
#graphical layer
class Hangman_gui:
    """
    The graphical display part of
    Hangman
    """
    def __init__(self):
        """
        hangman_gui attributes:
        a root window, two labels, a button
        and a canvas
        label 1 will dislay the word
        label 2 displays "you won" or "you lost"
        """
        self.tkroot = tk.Tk()
        #The frame holding all the components
        self.tkroot.bind('<KeyPress>', self.onkeypress)
        labelfont= ('helvetica',12,'bold')
        
        self.label1 = tk.Label(self.tkroot)
        self.label2 = tk.Label(self.tkroot)
        self.label3 = tk.Label(self.tkroot)
        self.make_labels(labelfont)
        
        button = tk.Button(self.tkroot,text= "Restart")
        self.make_buttons(button)

        self.canvas = tk.Canvas(self.tkroot)
        self.make_canvas()
        
        self.tkroot.title("Hangman")
        self.tkroot.geometry("600x600+15+15")
        self.tkroot.focus()

        

        #create a hangman game object
        self.game = Hangman_game()        
        self.start()
        
        
    def start(self):
        self.game.start()
        #start the logic part, and then do the following:
        self.label1.config(text =  make_display_word(self.game.word,""))
        self.draw_scaffold() 
        self.tkroot.mainloop()
        
        
    def make_buttons(self,button):
        """
        configure restart button and pack it
        set its command function to self.restart
        """
        button.config(command = self.restart) 
        
        button.pack()
        
        
        


    def make_canvas(self):
        """
        configure and pack canvas
        """
        self.canvas.config(height = 100,width=125)
        
        
        
        self.canvas.pack(expand=True,fill='both')
        


    def draw_scaffold(self):
        self.canvas.create_rectangle(245, 5, 310, 20, fill="saddle brown")
        self.canvas.create_rectangle(230, 5, 250, 350, fill="saddle brown")
        self.canvas.create_rectangle(250, 350, 350, 335, fill="saddle brown")
        
            
        
    


        
    def draw_body_parts(self):
        """
        configure and pack body parts
        """

            
        if len(self.game.body_parts_used) >= 1:
            self.canvas.create_oval(259, 20, 337, 100)
        
        if len(self.game.body_parts_used) >= 2:
            self.canvas.create_oval(259, 20, 337, 100)
            self.canvas.create_rectangle(298, 100, 300, 200, width= 2)
            
        if len(self.game.body_parts_used) >= 3:
            self.canvas.create_oval(259, 20, 337, 100)
            self.canvas.create_rectangle(298, 100, 300, 200, width = 2)   
            self.canvas.create_line(301, 145, 321, 200, width= 2)
            
        if len(self.game.body_parts_used) >= 4:
            self.canvas.create_oval(259, 20, 337, 100)
            self.canvas.create_rectangle(298, 100, 300, 200, width = 2)   
            self.canvas.create_line(301, 145, 321, 200, width= 2)
            self.canvas.create_line(297, 145, 277, 200, width= 2)
            
        if len(self.game.body_parts_used) >= 5:
            self.canvas.create_oval(259, 20, 337, 100)
            self.canvas.create_rectangle(298, 100, 300, 200, width = 2)   
            self.canvas.create_line(301, 145, 321, 200, width= 2)
            self.canvas.create_line(297, 145, 277, 200, width= 2)
            self.canvas.create_line(301, 200, 321, 300, width= 3)

        if len(self.game.body_parts_used) >= 6:
            self.canvas.create_oval(259, 20, 337, 100)
            self.canvas.create_rectangle(298, 100, 300, 200, width = 2)   
            self.canvas.create_line(301, 145, 321, 200, width= 2)
            self.canvas.create_line(297, 145, 277, 200, width= 2)
            self.canvas.create_line(301, 200, 321, 300, width= 3)
            self.canvas.create_line(297, 200, 277, 300, width= 3)
                        

         
        
        

    def make_labels(self,fnt):
        """
        configure the necessary labels
        and pack them
        """
        self.label3.config(text = "Let's play Hangman!", bg= "DarkGoldenrod2", width= 20, height= 2) 
        self.label1.config(text= "Hangman", bg= "lightcoral" , width= 40, height= 5)
        self.label2.config(text= "Type in a character")
        
        self.label3.pack()
        self.label1.pack()
        self.label2.pack()
        
          
        
    def onkeypress(self,event):
        """
        define action carried out when user types a character
        it will be called self.onkeypress
        --grab the character typed by the user
        --update the logic game with the character typed by the user
        --update the texts on labels 1 and 2 
        display the word (by updating the text on label1)
        """
        ch = event.char  #get the character typed by the user
        self.game.update_game(ch)
        
        self.label1.config(text = make_display_word(self.game.word, self.game.letters_used))
        self.label2.config(text = self.game.message_string)

        
        
        self.draw_body_parts() 
                        
                  
            
                
        




        
    def restart(self):
        """
        restart the game
        change text displayed on labels
        clear the canvas
        using  self.canvas.delete("all")
        """
        
        self.canvas.delete("all")
        self.label2.config(text = "Type in a character")
        self.start()
        
        
        
        
          
#This starts everything. 
Hangman_gui()
#g= Hangman_game()

