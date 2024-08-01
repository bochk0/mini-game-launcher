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

        if twoPair:
            return 3, valueOfTwoPair

        if pair:
            return 2, valueOfPair

    
    if not royalFlush and not straightFlush and not straight and not flush and not fourOfAKind and not fullHouse and not threeOfAKind and not twoPair and not pair:
        return 1
    

def Call(TxPlayerCoins, TxPot, FrScrollableText, button):
    playerMadeDecision.set(True)

    DeductCoinsFromPlayer(lastBet, TxPlayerCoins)
    UpdatePot(lastBet, TxPot)
    UpdateFeedback(lastBet, FrScrollableText, False, False)
    IncreaseWhoseTurn()

    button["state"] = "disabled"

def Check(FrScrollableText):
    playerMadeDecision.set(True)
    BtCheck["state"] = "disabled"
    UpdateFeedback(0, FrScrollableText, False, False)
    IncreaseWhoseTurn() 

def CommitRaise(EnRaise, TxPlayerCoins, TxPot, FrScrollableText, FrCommandPanelExtension):
    global lastBet

    raiseValue = EnRaise.get()
    if raiseValue == "": 
        raiseValue = 0
    raiseValue = int(raiseValue) 
    print(f"player attempted to raise by: {raiseValue}")

    playerCoins = GetPlayerCoins()
    if playerCoins >= raiseValue and raiseValue > lastBet:
        lastBet = raiseValue
        DeductCoinsFromPlayer(raiseValue, TxPlayerCoins)
        UpdatePot(raiseValue, TxPot),
        UpdateFeedback(raiseValue, FrScrollableText, False, False)
        ClearWindowOrFrame(FrCommandPanelExtension)
        IncreaseWhoseTurn()
        playerMadeDecision.set(True)

def ShowRaiseMenu(TxPlayerCoins, TxPot, FrScrollableText, FrCommandPanelExtension):

    BtCloseRaiseMenu = Button(FrCommandPanelExtension, text="CANCEL RAISE", font=("Rockwell", 10),
                        compound="c", image=pixel, height=50, width=108, borderwidth=0, 
                        command=lambda:ClearWindowOrFrame(FrCommandPanelExtension))
    BtCloseRaiseMenu.place(x=5,y=130)

    TxRaiseBy = Label(FrCommandPanelExtension, text="RAISE BET BY", font=("Rockwell", 12), background="dark grey")
    TxRaiseBy.place(x=5,y=5)

    EnRaise = Entry(FrCommandPanelExtension, width=18)
    EnRaise.place(x=5,y=30)

    BtCommitRaise = Button(FrCommandPanelExtension, text="COMMIT RAISE", font=("Rockwell", 10),
                        compound="c", image=pixel, height=50, width=108, borderwidth=0, 
                        command=lambda:CommitRaise(EnRaise, TxPlayerCoins, TxPot, FrScrollableText, FrCommandPanelExtension))
    BtCommitRaise.place(x=5,y=60)


def ReturnPercentageInteger():
    integer = random.randint(1,100)
    return integer

def CalculateNextBotBet():

    previousBotChecked = False
    if previousRoundLastBet == lastBet: 
        previousBotChecked = True

    if len(allBotHands[whoseTurn - 1]) == 0:
        return -2 

    botHandStrength = botHandsStrengths[whoseTurn - 1] 
    if type(botHandStrength) == tuple: 
        
        
        botHandStrength = botHandStrength[0] 

    if botHandStrength == 1: 
        chance = ReturnPercentageInteger()
        if chance >= 25: 
            print(f"bot {whoseTurn} with strength {botHandStrength} CALLED with chance {chance}") 
            return 1.0 
        else: 
            if previousBotChecked: 
                print(f"bot {whoseTurn} with strength {botHandStrength} CHECKED with chance {chance}") 
                return 0 
            else:
                print(f"bot {whoseTurn} with strength {botHandStrength} FOLDED with chance {chance}") 
                return -1 
        
    elif botHandStrength == 2:
        chance = ReturnPercentageInteger()
        if chance >= 30: 
            print(f"bot {whoseTurn} with strength {botHandStrength} CALLED with chance {chance}") 
            return 1.0 
        else: 
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 1.2x with chance {chance}") 
            return 1.2 

    elif botHandStrength == 3:
        chance = ReturnPercentageInteger()
        if chance >= 35: 
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 1.5x with chance {chance}") 
            return 1.5
        else: 
            print(f"bot {whoseTurn}with strength {botHandStrength} RAISED by 2.0x with chance {chance}") 
            return 2.0 

    elif botHandStrength == 4:
        chance = ReturnPercentageInteger()
        if chance >= 30: 
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 2.5x with chance {chance}") 
            return 2.5
        else: 
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 2.0x with chance {chance}") 
            return 2.0 
    
    elif botHandStrength == 5:
        chance = ReturnPercentageInteger()
        if chance >= 25: 
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 3.0x with chance {chance}") 
            return 3.0 
        else: 
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 2.5x with chance {chance}") 
            return 2.5 
    
    elif botHandStrength == 6:
        chance = ReturnPercentageInteger()
        if chance >= 20: 
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 3.5x with chance {chance}") 
            return 3.5 
        else: 
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 3.0x with chance {chance}") 
            return 3.0 

    elif botHandStrength == 7:
        chance = ReturnPercentageInteger()
        if chance >= 15: 
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 4.0x with chance {chance}") 
            return 4.0
        else: 
            print(f"bot {whoseTurn} with strength {botHandStrength} RAISED by 3.5x with chance {chance}") 
            return 3.5 
    

def MakeBotBet(TxPot, FrScrollableText):
    global lastBet

    if currentRound == 1:
        UpdatePot(10, TxPot)
        UpdateFeedback(10, FrScrollableText, False, False)
        IncreaseWhoseTurn() 
        lastBet = 10
    else:
        UpdateBotHandStrengthsList() 
        nextBetMultiplier = CalculateNextBotBet() 
        if nextBetMultiplier == 0:
            print(f"bot: {whoseTurn - 1} checked")
        if not len(allBotHands[whoseTurn - 1]) == 0: 
            if nextBetMultiplier == 1.0: 
                UpdatePot(lastBet, TxPot)
                UpdateFeedback(lastBet, FrScrollableText, False, False)
            elif nextBetMultiplier == -1: 
                allBotHands[whoseTurn - 1].clear() 
                UpdateFeedback(lastBet, FrScrollableText, True, False)
            elif nextBetMultiplier == -2:
                print(f"no bet made by bot {whoseTurn - 1}, nextbetmultiplier = -2") 
            elif nextBetMultiplier == 0: 
                UpdateFeedback(0, FrScrollableText, False, False)
            else: 
                UpdatePot(round(lastBet * nextBetMultiplier, 0), TxPot)
                UpdateFeedback(round(lastBet * nextBetMultiplier, 0), FrScrollableText, False, False)
                lastBet = round(lastBet * nextBetMultiplier, 0)
        IncreaseWhoseTurn()


def GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard):

    if "spades" in firstChosenCard:
        firstChosenCardSuit = "spades"
    elif "clubs" in firstChosenCard:
        firstChosenCardSuit = "clubs"
    elif "hearts" in firstChosenCard:
        firstChosenCardSuit = "hearts"
    elif "diamonds" in firstChosenCard:
        firstChosenCardSuit = "diamonds"

    if "spades" in secondChosenCard:
        secondChosenCardSuit = "spades"
    elif "clubs" in secondChosenCard:
        secondChosenCardSuit = "clubs"
    elif "hearts" in secondChosenCard:
        secondChosenCardSuit = "hearts"
    elif "diamonds" in secondChosenCard:
        secondChosenCardSuit = "diamonds"

    return firstChosenCardSuit, secondChosenCardSuit
    def CommitCombine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, 
                TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global showingCombineMenu, roundSixExecuted

    playerHand.remove(firstChosenCard) 
    playerHand.remove(secondChosenCard) 
    playerHand.append(cardImagePNGtext) 

    cardButtons[cardTwo].image = "" 

    
    cardImageFile = Image.open(f"Playing Cards/{cardImagePNGtext}")
    resizedCardImageFile = cardImageFile.resize((114, 164), Image.LANCZOS)
    actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
    

    
    cardButtons[cardOne].image = actualCardImage
    cardButtons[cardOne].config(image=actualCardImage)
    

    UpdatePlayerCardButtonsWithList(cardButtons)

    ClearWindowOrFrame(FrCommandPanelExtension)
    showingCombineMenu = False

    print("PLAYER combined cards")
    IncreaseWhoseTurn()
    if currentRound == 6:
        ExecuteRoundSix(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, 
                        TxPlayerCoins, TxPot, cardButtons, communityCardList)
    elif currentRound == 9:
        ExecuteRoundNine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, 
                        TxPlayerCoins, TxPot, cardButtons, communityCardList)

def SelectTwoCardsToCombine(EnCardOne, EnCardTwo, EnOperation, TxResultCard, BtCommitCombine):
    global cardImagePNGtext, cardOne, cardTwo, firstChosenCard, secondChosenCard

    cardOne = EnCardOne.get()
    cardOne = int(cardOne) - 1
    cardTwo = EnCardTwo.get()
    cardTwo = int(cardTwo) - 1
    operation = EnOperation.get()

    firstChosenCard = playerHand[cardOne]
    secondChosenCard = playerHand[cardTwo]

    firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

    valuesInPlayerHand = MakeHandIntoListOfValues(playerHand)
    biggerCardOfTheTwo = max(valuesInPlayerHand[cardOne], valuesInPlayerHand[cardTwo])
    smallerCardOfTheTwo = min(valuesInPlayerHand[cardOne], valuesInPlayerHand[cardTwo])

    if operation == "+" and valuesInPlayerHand[cardOne] + valuesInPlayerHand[cardTwo] < 15:
        number = valuesInPlayerHand[cardOne] + valuesInPlayerHand[cardTwo]

    elif operation == "-" and biggerCardOfTheTwo - smallerCardOfTheTwo > 0:
        number = biggerCardOfTheTwo - smallerCardOfTheTwo

    elif operation == "*" and valuesInPlayerHand[cardOne] * valuesInPlayerHand[cardTwo] < 15:
        number = valuesInPlayerHand[cardOne] * valuesInPlayerHand[cardTwo]

    elif operation == "/" and str((biggerCardOfTheTwo / smallerCardOfTheTwo))[-2:] == ".0":
        number = round(biggerCardOfTheTwo / smallerCardOfTheTwo)

    try: 
        if valuesInPlayerHand[cardOne] >= valuesInPlayerHand[cardTwo]: 
            
            cardImagePNGtext = f"{number}_of_{firstChosenCardSuit}.png" 
            
        elif valuesInPlayerHand[cardOne] <= valuesInPlayerHand[cardTwo]: 
            cardImagePNGtext = f"{number}_of_{secondChosenCardSuit}.png" 

        
        cardImageFile = Image.open(f"Playing Cards/{cardImagePNGtext}")
        resizedCardImageFile = cardImageFile.resize((45, 70), Image.LANCZOS)
        actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
        

        
        TxResultCard.image = actualCardImage
        TxResultCard.config(image=actualCardImage)
        
        BtCommitCombine["state"] = "normal"
    except: 
        print("error occurred creating image for result card")
        BtCommitCombine["state"] = "disabled"

def ShowCombineMenu(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, 
                    TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global showingCombineMenu

    if showingCombineMenu:
        ClearWindowOrFrame(FrCommandPanelExtension)
        showingCombineMenu = False
    else:   
        showingCombineMenu = True

        TxResult = Label(FrCommandPanelExtension, text="RESULT", font=("Rockwell", 12), background="dark grey")
        TxResult.place(x=30,y=75)

        TxCardOne = Label(FrCommandPanelExtension, text="CARD 1", font=("Rockwell", 8), background="dark grey")
        TxCardOne.place(x=15,y=5)

        TxCardTwo = Label(FrCommandPanelExtension, text="CARD 2", font=("Rockwell", 8), background="dark grey")
        TxCardTwo.place(x=85,y=5)

        TxOperation = Label(FrCommandPanelExtension, text="MATH OPERATION", font=("Rockwell", 8), background="dark grey")
        TxOperation.place(x=15,y=30)
        
        EnCardOne = Entry(FrCommandPanelExtension, width=2)
        EnCardOne.place(x=0,y=5)
        
        EnCardTwo = Entry(FrCommandPanelExtension, width=2)
        EnCardTwo.place(x=70,y=5)

        EnOperation = Entry(FrCommandPanelExtension, width=2)
        EnOperation.place(x=0,y=30)

        TxResultCard = Label(FrCommandPanelExtension, borderwidth=0)
        TxResultCard.place(x=40,y=100)

        BtCheckCombination = Button(FrCommandPanelExtension, text="CHECK COMBINATION", font=("Rockwell", 9),
                            compound="c", image=pixel, height=15, width=130, borderwidth=0, 
                            command=lambda:SelectTwoCardsToCombine(EnCardOne, EnCardTwo, EnOperation, TxResultCard, BtCommitCombine))
        BtCheckCombination.place(x=0,y=55)

        BtCommitCombine = Button(FrCommandPanelExtension, text="COMBINE", font=("Rockwell", 10),
                            compound="c", image=pixel, height=15, width=115, borderwidth=0, 
                            command=lambda:CommitCombine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, 
                                                        FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList))
        BtCommitCombine.place(x=0,y=175)
        BtCommitCombine["state"] = "disabled" 


def TryCombiningIntoFourOfAKind(botHandValues, valueOfPairOrKind):
    
    newCardCreated = False

    currentBotHand = allBotHands[whoseTurn - 1]
    print(f"before removing targets trying to combine into 4 of a kind: {botHandValues}\n current bot hand {currentBotHand}")
    target = valueOfPairOrKind 

    if len(communityHand) == 3:

        if (botHandValues[0] == target and botHandValues[1] == target and botHandValues[2] == target): 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            situation = 1

        elif (botHandValues[0] == target and botHandValues[1] == target): 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] 
            currentBotHand.pop(botHandValues.index(target)) 
            botHandValues.remove(target) 
            situation = 2

        elif (botHandValues[1] == target and botHandValues[2] == target): 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] 
            currentBotHand.pop(botHandValues.index(target)) 
            botHandValues.remove(target) 
            situation = 2

        elif (botHandValues[0] == target and botHandValues[2] == target): 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] 
            currentBotHand.pop(botHandValues.index(target)) 
            botHandValues.remove(target) 
            situation = 2

        elif botHandValues.index(target) == 0 or botHandValues.index(target) == 1 or botHandValues.index(target) == 2: 
            
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] 
            currentBotHand.pop(botHandValues.index(target)) 
            currentBotHand.pop(botHandValues.index(target)) 
            botHandValues.remove(target) 
            botHandValues.remove(target) 
            situation = 3
        
        elif botHandValues.index(target) > 2: 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] 
            currentBotHand.pop(botHandValues.index(target)) 
            currentBotHand.pop(botHandValues.index(target)) 
            currentBotHand.pop(botHandValues.index(target)) 
            botHandValues.remove(target) 
            botHandValues.remove(target) 
            botHandValues.remove(target) 
            situation = 4

    elif len(communityHand) == 2:

        if botHandValues[0] == target and botHandValues[1] == target: 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] 
            currentBotHand.pop(botHandValues.index(target)) 
            botHandValues.remove(target) 
            situation = 2
            
    elif botHandValues.index(target) == 0 or botHandValues.index(target) == 1: 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] 
            currentBotHand.pop(botHandValues.index(target)) 
            currentBotHand.pop(botHandValues.index(target)) 
            botHandValues.remove(target) 
            botHandValues.remove(target) 
            situation = 3

    print(f"situation: {situation}. after removing targets trying to combine into 4 of a kind: {botHandValues}\n current bot hand {currentBotHand}")

    for index in range(len(botHandValues)): 
        firstChosenCard = currentBotHand[index - 1] 
        secondChosenCard = currentBotHand[index] 

        print(botHandValues[index - 1], botHandValues[index], index)
        
        if botHandValues[index - 1] + botHandValues[index] == target: 

            firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

            print(f"{botHandValues[index - 1]} of {firstChosenCardSuit} + {botHandValues[index]} of {secondChosenCardSuit} = {target}")

            if botHandValues[index - 1] >= botHandValues[index]: 
                print(f"{target}_of_{firstChosenCardSuit}.png = resulting card") 
                resultingCard = f"{target}_of_{firstChosenCardSuit}.png"

                print(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")

                currentBotHand.remove(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")

                currentBotHand.append(resultingCard)  

                if situation == 2: 
                    currentBotHand.append(targetInCurrentBotHand) 
                elif situation == 3: 
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                elif situation == 4:
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)

                newCardCreated = True
                break

            elif botHandValues[index - 1] <= botHandValues[index]: 
                print(f"{target}_of_{secondChosenCardSuit}.png = resulting card") 
                resultingCard = f"{target}_of_{secondChosenCardSuit}.png"

                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index-1]}_of_{firstChosenCardSuit}.png") 
                currentBotHand.append(resultingCard) 

                if situation == 2:
                    currentBotHand.append(targetInCurrentBotHand) 
                elif situation == 3:
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                elif situation == 4:
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                    
                newCardCreated = True
                break

        elif botHandValues[index - 1] * botHandValues[index] == target:
            firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

            print(f"{botHandValues[index - 1]} of {firstChosenCardSuit} * {botHandValues[index]} of {secondChosenCardSuit} = {target}")

            if botHandValues[index - 1] >= botHandValues[index]: 
                print(f"{target}_of_{firstChosenCardSuit}.png = resulting card") 
                resultingCard = f"{target}_of_{firstChosenCardSuit}.png"

                currentBotHand.remove(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                currentBotHand.append(resultingCard)  

                if situation == 2: 
                    currentBotHand.append(targetInCurrentBotHand) 
                elif situation == 3: 
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                elif situation == 4:
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)
                    
                newCardCreated = True
                break


    if not newCardCreated and situation == 2: 
        currentBotHand.append(targetInCurrentBotHand) 
        
        
    elif not newCardCreated and situation == 3:
        currentBotHand.append(targetInCurrentBotHand)
        currentBotHand.append(targetInCurrentBotHand)

    return newCardCreated

def TryCombiningIntoThreeOfAKind(botHandValues, valueOfPairOrKind):
    
    newCardCreated = False

    currentBotHand = allBotHands[whoseTurn - 1]
    print(f"before removing target trying to combine into 3 of a kind: {botHandValues}\n current bot hand {currentBotHand}")
    target = valueOfPairOrKind 

    if len(communityHand) == 3:

        if (botHandValues[0] == target and botHandValues[1] == target): 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            situation = 1

        elif (botHandValues[1] == target and botHandValues[2] == target): 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            situation = 1

        elif (botHandValues[0] == target and botHandValues[2] == target): 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            situation = 1

        elif botHandValues.index(target) == 0 or botHandValues.index(target) == 1 or botHandValues.index(target) == 2: 
            
            botHandValues.remove(target) 
            botHandValues.pop(0) 
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target) - 1] 
            currentBotHand.pop(botHandValues.index(target) - 1) 
            botHandValues.remove(target) 
            botHandValues.pop(0) 
            situation = 2

        elif botHandValues.index(target) > 1: 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] 
            currentBotHand.pop(botHandValues.index(target)) 
            currentBotHand.pop(botHandValues.index(target)) 
            botHandValues.remove(target) 
            botHandValues.remove(target) 
            situation = 3

    elif len(communityHand) == 2:

        if botHandValues[0] == target and botHandValues[1] == target: 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            situation = 1

        elif botHandValues.index(target) == 0 or botHandValues.index(target) == 1: 
            botHandValues.remove(target) 
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target) - 1] 
            currentBotHand.pop(botHandValues.index(target) - 1) 
            botHandValues.remove(target) 
            botHandValues.pop(0) 
            situation = 2

        elif botHandValues.index(target) > 1: 
            botHandValues.pop(0) 
            botHandValues.pop(0) 
            targetInCurrentBotHand = currentBotHand[botHandValues.index(target)] 
            currentBotHand.pop(botHandValues.index(target)) 
            currentBotHand.pop(botHandValues.index(target)) 
            botHandValues.remove(target) 
            botHandValues.remove(target) 
            situation = 3

    print(f"situation: {situation}. after removing target trying to combine into 3 of a kind: {botHandValues}\n current bot hand {currentBotHand}")

    for index in range(len(botHandValues)): 
        firstChosenCard = currentBotHand[index - 1] 
        secondChosenCard = currentBotHand[index] 

        print(botHandValues[index - 1], botHandValues[index], index)
        
        if botHandValues[index - 1] + botHandValues[index] == target: 

            firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

            print(f"{botHandValues[index - 1]} of {firstChosenCardSuit} + {botHandValues[index]} of {secondChosenCardSuit} = {target}")

            if botHandValues[index - 1] >= botHandValues[index]: 
                print(f"{target}_of_{firstChosenCardSuit}.png = resulting card") 
                resultingCard = f"{target}_of_{firstChosenCardSuit}.png"

                print(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")

                currentBotHand.remove(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                currentBotHand.append(resultingCard)  

                if situation == 2: 
                    currentBotHand.append(targetInCurrentBotHand) 
                elif situation == 3: 
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)

                newCardCreated = True
                break

            elif botHandValues[index - 1] <= botHandValues[index]: 
                print(f"{target}_of_{secondChosenCardSuit}.png = resulting card") 
                resultingCard = f"{target}_of_{secondChosenCardSuit}.png"

                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index-1]}_of_{firstChosenCardSuit}.png")
                currentBotHand.append(resultingCard) 

                if situation == 2:
                    currentBotHand.append(targetInCurrentBotHand) 
                elif situation == 3:
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)

                newCardCreated = True
                break

        elif botHandValues[index - 1] * botHandValues[index] == target:
            firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

            print(f"{botHandValues[index - 1]} of {firstChosenCardSuit} * {botHandValues[index]} of {secondChosenCardSuit} = {target}")

            if botHandValues[index - 1] >= botHandValues[index]: 
                print(f"{target}_of_{firstChosenCardSuit}.png = resulting card") 
                resultingCard = f"{target}_of_{firstChosenCardSuit}.png"

                currentBotHand.remove(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                currentBotHand.append(resultingCard)  

                if situation == 2: 
                    currentBotHand.append(targetInCurrentBotHand) 
                elif situation == 3: 
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)

                newCardCreated = True
                break

            elif botHandValues[index - 1] <= botHandValues[index]: 
                print(f"{target}_of_{secondChosenCardSuit}.png = resulting card") 
                resultingCard = f"{target}_of_{secondChosenCardSuit}.png"

                currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                currentBotHand.remove(f"{botHandValues[index-1]}_of_{firstChosenCardSuit}.png")
                currentBotHand.append(resultingCard) 

                if situation == 2: 
                    currentBotHand.append(targetInCurrentBotHand) 
                elif situation == 3: 
                    currentBotHand.append(targetInCurrentBotHand)
                    currentBotHand.append(targetInCurrentBotHand)

                newCardCreated = True
                break

    if not newCardCreated and situation == 2: 
        currentBotHand.append(targetInCurrentBotHand) 
        
        
    elif not newCardCreated and situation == 3:
        currentBotHand.append(targetInCurrentBotHand)
        currentBotHand.append(targetInCurrentBotHand)

    return newCardCreated

def TryCombiningIntoPair(botHandValues):


    newCardCreated = False

    currentBotHand = allBotHands[whoseTurn - 1]

    target = max(botHandValues) 

    if botHandValues.index(target) == 0 or botHandValues.index(target) == 1: 
        botHandValues.remove(target) 
        botHandValues.pop(0) 
        if len(communityHand) == 3: 
            botHandValues.pop(0) 
        situation = 1

    elif botHandValues.index(target) > 1: 
        if len(communityHand) == 3: 
            botHandValues.pop(0) 
        targetInCurrentBotHand = currentBotHand[botHandValues.index(target) - 2] 
        currentBotHand.pop(botHandValues.index(target) - 2) 
        botHandValues.remove(target) 
        botHandValues.pop(0) 
        botHandValues.pop(0) 
        situation = 2

    
    if len(botHandValues) != 1:
        for index in range(len(botHandValues)): 
            firstChosenCard = currentBotHand[index - 1] 
            secondChosenCard = currentBotHand[index] 


            if botHandValues[index - 1] + botHandValues[index] == target: 

                firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

            
                if botHandValues[index - 1] >= botHandValues[index]: 
                    
                    resultingCard = f"{target}_of_{firstChosenCardSuit}.png"

                    currentBotHand.remove(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")
                    currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                    currentBotHand.append(resultingCard)  

                    if situation == 2:
                        currentBotHand.append(targetInCurrentBotHand) 

                    newCardCreated = True
                    break

                elif botHandValues[index - 1] <= botHandValues[index]: 
                    
                    resultingCard = f"{target}_of_{secondChosenCardSuit}.png"

                    currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                    currentBotHand.remove(f"{botHandValues[index-1]}_of_{firstChosenCardSuit}.png")
                    currentBotHand.append(resultingCard) 

                    if situation == 2:
                        currentBotHand.append(targetInCurrentBotHand) 
                        
                    newCardCreated = True
                    break

            elif botHandValues[index - 1] * botHandValues[index] == target:
                firstChosenCardSuit, secondChosenCardSuit = GetSuitOfCardOneAndTwo(firstChosenCard, secondChosenCard)

                

                if botHandValues[index - 1] >= botHandValues[index]: 
                    
                    resultingCard = f"{target}_of_{firstChosenCardSuit}.png"

                    currentBotHand.remove(f"{botHandValues[index - 1]}_of_{firstChosenCardSuit}.png")
                    currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")

                    currentBotHand.append(resultingCard)  

                    if situation == 2:
                        currentBotHand.append(targetInCurrentBotHand) 
                        
                    newCardCreated = True
                    break

                elif botHandValues[index - 1] <= botHandValues[index]: 
                    
                    resultingCard = f"{target}_of_{secondChosenCardSuit}.png"

                    currentBotHand.remove(f"{botHandValues[index]}_of_{secondChosenCardSuit}.png")
                    currentBotHand.remove(f"{botHandValues[index-1]}_of_{firstChosenCardSuit}.png")

                    currentBotHand.append(resultingCard) 

                    if situation == 2:
                        currentBotHand.append(targetInCurrentBotHand) 
                        
                    newCardCreated = True
                    break

    if not newCardCreated and situation == 2: 
        currentBotHand.append(targetInCurrentBotHand) 

    return newCardCreated

def DecideWhichCombinationToMake(tempList, FrScrollableText):

    
    botHandStrength = CalculateHandStrength(tempList)
    if type(botHandStrength) == tuple: 
        
        
        valueOfPairOrKind = botHandStrength[1]
        botHandStrength = botHandStrength[0]

    botHandValues = MakeHandIntoListOfValues(tempList)

    

    if botHandStrength == 1: 
        isNewCardCreated = TryCombiningIntoPair(botHandValues)
    elif botHandStrength == 2: 
        isNewCardCreated = TryCombiningIntoThreeOfAKind(botHandValues, valueOfPairOrKind)
    elif botHandStrength == 4: 
        isNewCardCreated = TryCombiningIntoFourOfAKind(botHandValues, valueOfPairOrKind)

    try:
        UpdateFeedback("tried to combine", FrScrollableText, False, isNewCardCreated)
    except:
        UpdateFeedback("tried to combine", FrScrollableText, False, False)
