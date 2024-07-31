from tkinter import * 
import sqlite3 
import os
from os.path import isfile 
from PIL import ImageTk,Image 
import random 


loggedIn = False

pot = 0

allBotHands = [ [], [], [] ] 
playerHand = []
communityHand = []

numOfCards = 51 

dealer = random.randint(0,3) 
if dealer == 3: 
    whoseTurn = 0 
else: 
    whoseTurn = dealer + 1 

currentRound = 1 
roundOneExecuted = False 
roundTwoExecuted = False
roundThreeExecuted = False
roundFourExecuted = False
roundFiveExecuted = False
roundSixExecuted = False
roundSevenExecuted = False
roundEightExecuted = False
roundNineExecuted = False
roundTenExecuted = False
roundElevenExecuted = False

showingRaiseMenu = False
showingCombineMenu = False

lastClickXTimer = 0
lastClickYTimer = 0

def SaveLastClickPosTimer(event):
    global lastClickXTimer, lastClickYTimer
    lastClickXTimer, lastClickYTimer = event.x, event.y

def DraggingTimer(event):
    draggedWidget= str(event.widget) 
    if draggedWidget[-9:] == "scrollbar" or draggedWidget[2:8] == "button": 
        pass 
    else: 
        x, y = event.x - lastClickXTimer + main.winfo_x(), event.y - lastClickYTimer + main.winfo_y()
        main.geometry("+%s+%s" % (x, y))


main = Tk()
main.overrideredirect(False)
main.geometry("200x157")
main.eval('tk::PlaceWindow . center') 
playerMadeDecision = BooleanVar(value=False) 


pixel = PhotoImage(width=1, height=1)

main.bind('<Button-1>', SaveLastClickPosTimer)
main.bind('<B1-Motion>', DraggingTimer)


def PrintAllHands():
    print()
    print(f"\nCommunity hand {communityHand}\n")
    for x in range(3):
        print(f"Bot {x+1} {allBotHands[x]}")
    print(f"\nPlayer {playerHand}")
    print(f"\nNumber of cards left in deck: {numOfCards}")

def Exit():
    main.destroy()

def ClearWindowOrFrame(windowOrFrame):
    for widget in windowOrFrame.winfo_children(): 
        widget.destroy() 

def MainMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    
    if n == 0:
        MakeWindowAccountMenu()
    elif n == 1:
        MakeWindowGameMenu()
    elif n == 2:
        SureYN()
    
def AccountMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowMainMenu()
    elif n == 1:
        MakeWindowRegisterMenu()
    elif n == 2:
        MakeWindowLogInMenu()
    elif n == 3:
        MakeWindowDelAccMenu()

def RegisterMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowAccountMenu()
    elif n == 1:
        MakeWindowMainMenu()

def LogInMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowAccountMenu()
    elif n == 1:
        MakeWindowMainMenu()

def AreYouSureMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowMainMenu()

def DelAccountMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowAccountMenu()

def GameMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowMainMenu()
    elif n == 1:
        MakeWindowHelpMenu()
    elif n == 2:
        MakeWindowGame()
    elif n == 3:
        MakeWindowAccountStats()

def HelpMenuToAnotherMenu(n):
    ClearWindowOrFrame(main)
    if n == 0:
        MakeWindowGameMenu()


def SureYN():

    main.geometry("200x70")
    
    TxAreYouSure = Label(main, text="ARE YOU SURE?", font=("Rockwell", 18))
    TxAreYouSure.pack()
    
    BtYes = Button(main, text="YES",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=82,
                    borderwidth=0, bg="light grey",
                    command=Exit)
    BtYes.place(x=8, y=33)

    BtNo = Button(main, text="NO",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=82,
                    borderwidth=0, bg="light grey",
                    command=lambda:AreYouSureMenuToAnotherMenu(0))
    BtNo.place(x=105, y=33)
    

def MakeWindowHelpMenu():

    main.geometry("460x520")
    
    FrHelp = Frame(main, width=430, height=450)
    FrHelp.place(x=10, y=10)

    CaHelp = Canvas(FrHelp, width=420, height=450)
    SbHelp = Scrollbar(FrHelp, orient="vertical", command=CaHelp.yview)
   
    FrScrollableHelpText = Frame(CaHelp)
    FrScrollableHelpText.bind("<Configure>", lambda e: CaHelp.configure(scrollregion=CaHelp.bbox("all")))
   
    CaHelp.create_window((0, 0), window=FrScrollableHelpText, anchor="nw")
    CaHelp.configure(yscrollcommand=SbHelp.set)
   
    CaHelp.pack(side=LEFT, fill=BOTH, expand=True)
    SbHelp.pack(side=RIGHT, fill="y")
    

    with open("HelpText.txt") as file:
        helpText = file.read()

    Label(FrScrollableHelpText, text=helpText, font=("Rockwell", 10), justify="left").pack()
    
    BtBack = Button(main, text="BACK",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=30, width=430,
                    borderwidth=0, bg="light grey",
                    command=lambda:HelpMenuToAnotherMenu(0))
    BtBack.place(x=13, y=475)
    

def CreateListOfCards():
    with open("ListOfCards.txt") as file:
        return file.read().splitlines()

def GetPlayerCoins():
    statsDbName = (f"Stats({accountUsername}).db")
    con = sqlite3.connect(statsDbName)
    cursor = con.cursor()

    cursor.execute(f"SELECT currentMoney FROM tblStats_{accountUsername}")
    for row in cursor:
        playerCoins = row[0]

    return playerCoins

def DeductCoinsFromPlayer(numberOfCoins, TxPlayerCoins):

    playerCoins = GetPlayerCoins()

    playerCoins -= numberOfCoins 
    TxPlayerCoins.config(text=f"{accountUsername}'s coins: {playerCoins}") 

    statsDbName = (f"Stats({accountUsername}).db") 
    con = sqlite3.connect(statsDbName) 
    cursor = con.cursor() 
    
    cursor.execute(f"UPDATE tblStats_{accountUsername} SET currentMoney = {playerCoins}")
    con.commit()