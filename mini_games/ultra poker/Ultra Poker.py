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


def UpdatePlayerCardButtonsWithList(cardButtons):

    
    for card in range(len(cardButtons)):
        cardButtons[card].image = ""
    

    
    for card in range(len(playerHand)): 
        cardImageFile = Image.open(f"Playing Cards/{playerHand[card]}")
        resizedCardImageFile = cardImageFile.resize((114, 164), Image.LANCZOS)
        actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
        cardButtons[card].image = actualCardImage
        cardButtons[card].config(image=actualCardImage)
    
def PlacePlayerCardImage(actualCardImage, cardButtons):
    

    if len(playerHand) == 1: 
        cardButtons[0].image = actualCardImage 
        cardButtons[0].config(image=actualCardImage) 
    elif len(playerHand) == 2: 
        cardButtons[1].image = actualCardImage
        cardButtons[1].config(image=actualCardImage) 
    elif len(playerHand) == 3: 
        cardButtons[2].image = actualCardImage
        cardButtons[2].config(image=actualCardImage) 
    elif len(playerHand) == 4: 
        cardButtons[3].image = actualCardImage
        cardButtons[3].config(image=actualCardImage) 
    elif len(playerHand) == 5: 
        cardButtons[4].image = actualCardImage
        cardButtons[4].config(image=actualCardImage) 

def GeneratePlayerCard(cardButtons):
    global numOfCards

    
    randomCardNum = random.randint(0, numOfCards)
    cardImagePNGtext = cardsList[randomCardNum]
    cardsList.pop(randomCardNum)
    numOfCards -= 1
    

    
    cardImageFile = Image.open(f"Playing Cards/{cardImagePNGtext}")
    resizedCardImageFile = cardImageFile.resize((114, 164), Image.LANCZOS)
    actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
    

    playerHand.append(cardImagePNGtext) 
    PlacePlayerCardImage(actualCardImage, cardButtons)

def GenerateCardForAllBots():
    global numOfCards, allBotHands

    
    for bot in range(3):
        if (currentRound == 2) or (currentRound > 2 and len(allBotHands[bot]) > 0): 
            randomCardNum = random.randint(0, numOfCards)
            cardImagePNGtext = cardsList[randomCardNum]
            cardsList.pop(randomCardNum)
            numOfCards -= 1
            allBotHands[bot].append(cardImagePNGtext) 

def GenerateCommunityCard(communityCardList):
    global numOfCards, communityHand

    
    randomCardNum = random.randint(0, numOfCards)
    cardImagePNGtext = cardsList[randomCardNum]
    cardsList.pop(randomCardNum)
    numOfCards -= 1
    

    
    cardImageFile = Image.open(f"Playing Cards/{cardImagePNGtext}")
    resizedCardImageFile = cardImageFile.resize((55, 83), Image.LANCZOS)
    actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
    

    communityHand.append(cardImagePNGtext) 

    if len(communityHand) == 1:
        communityCardList[0].image = actualCardImage
        communityCardList[0].config(image=actualCardImage)
    elif len(communityHand) == 2:
        communityCardList[1].image = actualCardImage
        communityCardList[1].config(image=actualCardImage)
    elif len(communityHand) == 3:
        communityCardList[2].image = actualCardImage
        communityCardList[2].config(image=actualCardImage)



def CheckForPairOrKinds(whatToCheckFor, botHand, pair, twoPair, threeOfAKind, fourOfAKind):

    botHandValues = MakeHandIntoListOfValues(botHand)
    print(f"bot hand values {botHandValues}")
    numberOfPairs = 0
    valuesOfPairs = []

    for value in range(14, 1, -1): 
        if botHandValues.count(value) == whatToCheckFor: 
            if whatToCheckFor == 2: 
                pair = True 
                valueOfPair = value 
                numberOfPairs += 1
                valuesOfPairs.append(value)
                if numberOfPairs == 2:
                    twoPair = True
                    valueOfTwoPair = max(valuesOfPairs)
            elif whatToCheckFor == 3:
                threeOfAKind = True
                valueOfThreeOfAKind = value
            elif whatToCheckFor == 4:
                fourOfAKind = True
                valueOfFourOfAKind = value
                
    
    if whatToCheckFor == 2 and pair and not twoPair: 
        return pair, valueOfPair 
    elif whatToCheckFor == 2 and twoPair: 
        return twoPair, valueOfTwoPair 
    elif whatToCheckFor == 3 and threeOfAKind: 
        return threeOfAKind, valueOfThreeOfAKind 
    elif whatToCheckFor == 4 and fourOfAKind: 
        return fourOfAKind, valueOfFourOfAKind 
    else:
        return False, 0

def IsStraight(hand): 

    handValues = MakeHandIntoListOfValues(hand) 
    handValuesSet = list(set(handValues))
    handValuesSet.sort() 
    sectionOfHandValues = []
    limit = 5
    if len(handValuesSet) >= limit:
        for x in range(limit - 1):
            sectionOfHandValues = handValuesSet[-5-x:len(handValuesSet)-x] 
            for i in range(limit - 1):
                if sectionOfHandValues[i] != sectionOfHandValues[i+1] - 1: 
                    return False
            return True 

def CheckForFlush(hand):
    botHandString = '\t'.join(hand) 

    numberOfDiamonds = botHandString.count("diamonds")
    numberOfHearts = botHandString.count("hearts")
    numberOfSpades = botHandString.count("spades")
    numberOfClubs = botHandString.count("clubs")

    if numberOfDiamonds >= 5:
        return True
    elif numberOfHearts >= 5:
        return True
    elif numberOfSpades >= 5:
        return True
    elif numberOfClubs >= 5:
        return True
    else:
        return False

def MakeHandIntoListOfValues(hand):
    handValues = [] 

    for card in range(len(hand)):
        valueOfCard = hand[card][0:2] 
        if valueOfCard[1] == "_": 
            valueOfCard = valueOfCard[0] 
        handValues.append(int(valueOfCard)) 

    return handValues  

def CalculateHandStrength(hand):

    royalFlush, straightFlush, fourOfAKind, fullHouse, flush, straight, threeOfAKind, twoPair, pair = False, False, False, False, False, False, False, False, False

    botHandString = '\t'.join(hand) 

    
    if IsStraight(hand):
        straight = True
    
           
    
    try:
        flush = CheckForFlush(hand) 
    except: 
        flush = False
    

    
    if flush and straight:
        
        if "10" in botHandString and "11" in botHandString and "12" in botHandString and "13" in botHandString and "14" in botHandString:
            return 10
        
        return 9
        
    if not straightFlush:

        
        fourOfAKind, valueOfFourOfAKind = CheckForPairOrKinds(4, hand, pair, twoPair, threeOfAKind, fourOfAKind)
        

        if fourOfAKind:
            return 8, valueOfFourOfAKind

    if not fourOfAKind:

        
        pair, valueOfPair = CheckForPairOrKinds(2, hand, pair, twoPair, threeOfAKind, fourOfAKind) 
        

        
        twoPair, valueOfTwoPair = CheckForPairOrKinds(2, hand, pair, twoPair, threeOfAKind, fourOfAKind) 
        

        
        threeOfAKind, valueOfThreeOfAKind = CheckForPairOrKinds(3, hand, pair, twoPair, threeOfAKind, fourOfAKind)
        

        
        if pair and threeOfAKind:
            return 7
        

        if flush:
            return 6

        if straight:
            return 5

        if threeOfAKind:
            return 4, valueOfThreeOfAKind
