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


def ShowAllBotAndCommunityCards(FrTableScreen):
    
    TxBotOneCardOne = Label(FrTableScreen, borderwidth=0)
    TxBotOneCardOne.place(x=70,y=50)
    TxBotOneCardTwo = Label(FrTableScreen, borderwidth=0)
    TxBotOneCardTwo.place(x=110,y=50)
    TxBotOneCardThree = Label(FrTableScreen, borderwidth=0)
    TxBotOneCardThree.place(x=150,y=50)
    TxBotOneCardFour = Label(FrTableScreen, borderwidth=0)
    TxBotOneCardFour.place(x=190,y=50)
    TxBotOneCardFive = Label(FrTableScreen, borderwidth=0)
    TxBotOneCardFive.place(x=230,y=50)

    TxBotTwoCardOne = Label(FrTableScreen, borderwidth=0)
    TxBotTwoCardOne.place(x=70,y=175)
    TxBotTwoCardTwo = Label(FrTableScreen, borderwidth=0)
    TxBotTwoCardTwo.place(x=110,y=175)
    TxBotTwoCardThree = Label(FrTableScreen, borderwidth=0)
    TxBotTwoCardThree.place(x=150,y=175)
    TxBotTwoCardFour = Label(FrTableScreen, borderwidth=0)
    TxBotTwoCardFour.place(x=190,y=175)
    TxBotTwoCardFive = Label(FrTableScreen, borderwidth=0)
    TxBotTwoCardFive.place(x=230,y=175)

    TxBotThreeCardOne = Label(FrTableScreen, borderwidth=0)
    TxBotThreeCardOne.place(x=70,y=300)
    TxBotThreeCardTwo = Label(FrTableScreen, borderwidth=0)
    TxBotThreeCardTwo.place(x=110,y=300)
    TxBotThreeCardThree = Label(FrTableScreen, borderwidth=0)
    TxBotThreeCardThree.place(x=150,y=300)
    TxBotThreeCardFour = Label(FrTableScreen, borderwidth=0)
    TxBotThreeCardFour.place(x=190,y=300)
    TxBotThreeCardFive = Label(FrTableScreen, borderwidth=0)
    TxBotThreeCardFive.place(x=230,y=300)

    botOneCards = [TxBotOneCardOne, TxBotOneCardTwo, TxBotOneCardThree, TxBotOneCardFour, TxBotOneCardFive]
    botTwoCards = [TxBotTwoCardOne, TxBotTwoCardTwo, TxBotTwoCardThree, TxBotTwoCardFour, TxBotTwoCardFive]
    botThreeCards = [TxBotThreeCardOne, TxBotThreeCardTwo, TxBotThreeCardThree, TxBotThreeCardFour, TxBotThreeCardFive]
    allBotCards = [botOneCards, botTwoCards, botThreeCards]

    for bot in range(3):
        for card in range(len(allBotHands[bot])): 
            
            cardImageFile = Image.open(f"Playing Cards/{allBotHands[bot][card]}")
            resizedCardImageFile = cardImageFile.resize((76, 109), Image.LANCZOS)
            actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
            allBotCards[bot][card].image = actualCardImage
            allBotCards[bot][card].config(image=actualCardImage)

    TxCommunityCardOne = Label(FrTableScreen, borderwidth=0)
    TxCommunityCardOne.place(x=505,y=50)

    TxCommunityCardTwo = Label(FrTableScreen, borderwidth=0)
    TxCommunityCardTwo.place(x=545,y=50)

    TxCommunityCardThree = Label(FrTableScreen, borderwidth=0)
    TxCommunityCardThree.place(x=595,y=50)

    allCommunityCards = [TxCommunityCardOne, TxCommunityCardTwo, TxCommunityCardThree]

    for card in range(3): 
        
        cardImageFile = Image.open(f"Playing Cards/{communityHand[card]}")
        resizedCardImageFile = cardImageFile.resize((76, 109), Image.LANCZOS)
        actualCardImage = ImageTk.PhotoImage(resizedCardImageFile)
        allCommunityCards[card].image = actualCardImage
        allCommunityCards[card].config(image=actualCardImage)

def GetResultOfGame():

    UpdateBotHandStrengthsList()
    
    winOrLoseList = [] 

    for bot in range(3):

        if (type(playerHandStrength) == tuple) and (type(botHandsStrengths[bot]) == tuple):
            if (playerHandStrength[0] > botHandsStrengths[bot][0]): 
                winOrLose = "win"
                winOrLoseList.append(winOrLose)
            elif (playerHandStrength[0] == botHandsStrengths[bot][0]): 
                if (playerHandStrength[1] > botHandsStrengths[bot][1]): 
                    winOrLose = "win"
                elif (playerHandStrength[1] == botHandsStrengths[bot][1]): 
                    winOrLose = "tie"
                elif (playerHandStrength[1] < botHandsStrengths[bot][1]): 
                    winOrLose = "lose"
                winOrLoseList.append(winOrLose)
            elif (playerHandStrength[0] < botHandsStrengths[bot][0]): 
                winOrLose = "lose"
                winOrLoseList.append(winOrLose)
        
        if (type(playerHandStrength) == tuple) and (type(botHandsStrengths[bot]) == int):
            if (playerHandStrength[0] > botHandsStrengths[bot]):
                winOrLose = "win"
            elif (playerHandStrength[0] == botHandsStrengths[bot]):
                winOrLose = "tie"
            elif (playerHandStrength[0] < botHandsStrengths[bot]):
                winOrLose = "lose"
            winOrLoseList.append(winOrLose)

        if (type(playerHandStrength) == int) and (type(botHandsStrengths[bot]) == tuple):
            if (playerHandStrength > botHandsStrengths[bot][0]): 
                winOrLose = "win"
            elif (playerHandStrength < botHandsStrengths[bot][0]): 
                winOrLose = "lose"
            winOrLoseList.append(winOrLose)

        if (type(playerHandStrength) == int) and (type(botHandsStrengths[bot]) == int):
            if (playerHandStrength > botHandsStrengths[bot]):
                winOrLose = "win"
            elif (playerHandStrength == botHandsStrengths[bot]):
                winOrLose = "tie"
            elif (playerHandStrength < botHandsStrengths[bot]):
                winOrLose = "lose"
            winOrLoseList.append(winOrLose)

    if "lose" in winOrLoseList:
        winOrLose = f"You lost :["
    elif "tie" in winOrLoseList:
        winOrLose = f"You tied and won {pot/2} coins! :|"
    elif "win" in winOrLoseList:
        winOrLose = f"You won {pot} coins! :]"
    
    return winOrLose


def ExecuteRoundEleven(FrTableScreen):
    
    ClearWindowOrFrame(FrTableScreen)
    DisplayCurrentRoundInstruction(FrTableScreen, False)

    BtRaise["state"] = "disabled"
    BtCall["state"] = "disabled"
    BtCheck["state"] = "disabled"
    BtCombine["state"] = "disabled"
    BtFold["state"] = "disabled"

    TxbotOne = Label(FrTableScreen, text="Bot 1", font=("Rockwell", 16), background="light grey")
    TxbotOne.place(x=10,y=50)
    TxbotTwo = Label(FrTableScreen, text="Bot 2", font=("Rockwell", 16), background="light grey")
    TxbotTwo.place(x=10,y=175)
    TxbotThree = Label(FrTableScreen, text="Bot 3", font=("Rockwell", 16), background="light grey")
    TxbotThree.place(x=10,y=300)
    TxCommunityHand = Label(FrTableScreen, text="Community cards", font=("Rockwell", 16), background="light grey")
    TxCommunityHand.place(x=320,y=50)

    PrintAllHands()
    ShowAllBotAndCommunityCards(FrTableScreen)

    winOrLose = GetResultOfGame()
    TxWinOrLose = Label(FrTableScreen, text=winOrLose, font=("Rockwell", 16), background="light grey")
    TxWinOrLose.place(x=10,y=420)

    UpdateAccStatsDB(winOrLose)

    BtLeave = Button(FrTableScreen, text="LEAVE\nGAME", font=("Rockwell", 16), borderwidth=0,
                    background="light grey", compound="c", image=pixel, height=70, width=70,
                    command=lambda:Leave())
    BtLeave.place(x=720,y=420)

def ExecuteRoundTen(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global firstTimeExecutingRoundTen, numOfPlayersMadeBetInThisRound, roundTenExecuted, previousRoundLastBet
    

    if firstTimeExecutingRoundTen: 
        numOfPlayersMadeBetInThisRound = 0
        BtRaise["state"] = "disabled"
        BtCall["state"] = "disabled"
        BtCheck["state"] = "disabled"
        BtCombine["state"] = "disabled"
        BtCombine.config(width=229) 
        BtFold["state"] = "normal" 
        BtContinue.destroy() 
        firstTimeExecutingRoundTen = False

    if whoseTurn != 0: 
        MakeBotBet(TxPot, FrScrollableText) 
        numOfPlayersMadeBetInThisRound += 1

    if whoseTurn == 0 and numOfPlayersMadeBetInThisRound != 4:
        playerCoins = GetPlayerCoins()
        if lastBet <= playerCoins:
            BtCall["state"] = "normal"
            BtRaise["state"] = "normal"
        if previousRoundLastBet == lastBet:
            BtCheck["state"] = "normal"
        DisplayCurrentRoundInstruction(FrTableScreen, True) 
        numOfPlayersMadeBetInThisRound += 1
        main.wait_variable(playerMadeDecision) 

    if numOfPlayersMadeBetInThisRound != 4 and whoseTurn != 0: 
        ExecuteRoundTen(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList) 
    elif numOfPlayersMadeBetInThisRound == 4: 
        previousRoundLastBet = lastBet
        roundTenExecuted = True

def ExecuteRoundNine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global BtContinue, roundNineExecuted, firstTimeExecutingRoundNine, numOfPlayersCombinedInThisRound
    
    
    if firstTimeExecutingRoundNine:
        BtRaise["state"] = "disabled"
        BtCall["state"] = "disabled"
        BtCheck["state"] = "disabled"
        BtCombine["state"] = "normal"

        BtCombine.config(width=109)
        
        BtContinue = Button(FrCommandPanel, text="CONTINUE", font=("Rockwell", 15), borderwidth=0,
                        background="light grey", compound="c", image=pixel, height=32, width=109,
                        command=lambda:[ClearWindowOrFrame(FrCommandPanelExtension),
                        IncreaseWhoseTurn(),
                        ExecuteRoundNine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)])
        BtContinue.place(x=128,y=107)

        numOfPlayersCombinedInThisRound = 0
        firstTimeExecutingRoundNine = False

    if numOfPlayersCombinedInThisRound == 4: 
        roundNineExecuted = True
        ExecuteGameSequence(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)

    elif numOfPlayersCombinedInThisRound < 4 and whoseTurn == 0: 
        DisplayCurrentRoundInstruction(FrTableScreen, True) 
        numOfPlayersCombinedInThisRound += 1

    elif numOfPlayersCombinedInThisRound < 4 and whoseTurn != 0: 
        MakeBotCombine(FrScrollableText) 
        numOfPlayersCombinedInThisRound += 1
        ExecuteRoundNine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)    
    
def ExecuteRoundEight(cardButtons, communityCardList):
    global roundEightExecuted

    

    GeneratePlayerCard(cardButtons) 
    GenerateCardForAllBots() 
    GenerateCommunityCard(communityCardList) 

    print("in round eight - given 5 cards to all")

    roundEightExecuted = True

def ExecuteRoundSeven(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global firstTimeExecutingRoundSeven, numOfPlayersMadeBetInThisRound, roundSevenExecuted, previousRoundLastBet
    

    if firstTimeExecutingRoundSeven: 
        numOfPlayersMadeBetInThisRound = 0
        BtRaise["state"] = "disabled"
        BtCall["state"] = "disabled"
        BtCheck["state"] = "disabled"
        BtCombine["state"] = "disabled"
        BtCombine.config(width=229) 
        BtFold["state"] = "normal" 
        BtContinue.destroy() 
        firstTimeExecutingRoundSeven = False

    if whoseTurn != 0: 
        MakeBotBet(TxPot, FrScrollableText) 
        numOfPlayersMadeBetInThisRound += 1

    if whoseTurn == 0 and numOfPlayersMadeBetInThisRound != 4:
        playerCoins = GetPlayerCoins()
        if lastBet <= playerCoins:
            BtCall["state"] = "normal"
            BtRaise["state"] = "normal"
        if previousRoundLastBet == lastBet:
            BtCheck["state"] = "normal"
        DisplayCurrentRoundInstruction(FrTableScreen, True) 
        numOfPlayersMadeBetInThisRound += 1
        main.wait_variable(playerMadeDecision) 

    if numOfPlayersMadeBetInThisRound != 4 and whoseTurn != 0: 
        ExecuteRoundSeven(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
    elif numOfPlayersMadeBetInThisRound == 4: 
        previousRoundLastBet = lastBet
        roundSevenExecuted = True

def ExecuteRoundSix(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    

    global BtContinue, roundSixExecuted, firstTimeExecutingRoundSix, numOfPlayersCombinedInThisRound

    if firstTimeExecutingRoundSix:
        BtRaise["state"] = "disabled"
        BtCall["state"] = "disabled"
        BtCheck["state"] = "disabled"
        BtCombine["state"] = "normal"

        BtCombine.config(width=109)
        
        BtContinue = Button(FrCommandPanel, text="CONTINUE", font=("Rockwell", 15), borderwidth=0,
                        background="light grey", compound="c", image=pixel, height=32, width=109,
                        command=lambda:[ClearWindowOrFrame(FrCommandPanelExtension),
                        UpdateFeedback("tried to combine", FrScrollableText, False, False),
                        IncreaseWhoseTurn(),
                        ExecuteRoundSix(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)])
        BtContinue.place(x=128,y=107)

        numOfPlayersCombinedInThisRound = 0
        firstTimeExecutingRoundSix = False

    if numOfPlayersCombinedInThisRound == 4: 
        roundSixExecuted = True
        ExecuteGameSequence(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)

    elif numOfPlayersCombinedInThisRound < 4 and whoseTurn == 0: 
        DisplayCurrentRoundInstruction(FrTableScreen, True) 
        numOfPlayersCombinedInThisRound += 1

    elif numOfPlayersCombinedInThisRound < 4 and whoseTurn != 0: 
        
        MakeBotCombine(FrScrollableText) 
        numOfPlayersCombinedInThisRound += 1
        ExecuteRoundSix(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)    
    
def ExecuteRoundFive(cardButtons, communityCardList):
    global roundFiveExecuted, communityHand
    

    GeneratePlayerCard(cardButtons) 
    GenerateCardForAllBots() 
    GenerateCommunityCard(communityCardList) 
    GenerateCommunityCard(communityCardList) 

    print("in round five - given 4 cards to all, 2 comm cards")
    PrintAllHands()

    roundFiveExecuted = True

def ExecuteRoundFour(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global firstTimeExecutingRoundFour, numOfPlayersMadeBetInThisRound, roundFourExecuted, BtRaise, BtCall, BtCheck, BtCombine, BtFold, previousRoundLastBet

    

    if firstTimeExecutingRoundFour:

        BtRaise = Button(FrCommandPanel, text="RAISE", font=("Rockwell", 15), borderwidth=0,
                        background="light grey", compound="c", image=pixel, height=32, width=229,
                        command=lambda:ShowRaiseMenu(TxPlayerCoins, TxPot, FrScrollableText, FrCommandPanelExtension))
        BtRaise.place(x=8,y=8)

        BtCall = Button(FrCommandPanel, text="CALL", font=("Rockwell", 15), borderwidth=0,
                        background="light grey", compound="c", image=pixel, height=32, width=109,
                        command=lambda:Call(TxPlayerCoins, TxPot, FrScrollableText, BtCall)) 
        BtCall.place(x=8,y=57)

        BtCheck = Button(FrCommandPanel, text="CHECK", font=("Rockwell", 15), borderwidth=0,
                        background="light grey", compound="c", image=pixel, height=32, width=109,
                        command=lambda:Check(FrScrollableText))
        BtCheck.place(x=128,y=57)

        BtCombine = Button(FrCommandPanel, text="COMBINE", font=("Rockwell", 15), borderwidth=0,
                            background="light grey", compound="c", image=pixel, height=32, width=229,
                            command=lambda:ShowCombineMenu(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList))
        BtCombine.place(x=8, y=107)

        BtFold = Button(FrCommandPanel, text="FOLD", font=("Rockwell", 15), borderwidth=0,
                        background="light grey", compound="c", image=pixel, height=32, width=229,
                        command=lambda:Fold(FrTableScreen))
        BtFold.place(x=8,y=156)

        BtCombine["state"] = "disabled"
        BtCheck["state"] = "disabled"

        numOfPlayersMadeBetInThisRound = 0
        firstTimeExecutingRoundFour = False 

    if whoseTurn != 0: 
        MakeBotBet(TxPot, FrScrollableText) 
        numOfPlayersMadeBetInThisRound += 1

    if whoseTurn == 0 and numOfPlayersMadeBetInThisRound != 4: 
        playerCoins = GetPlayerCoins()
        if lastBet <= playerCoins:
            BtCall["state"] = "normal"
            BtRaise["state"] = "normal"
        if previousRoundLastBet == lastBet:
            BtCheck["state"] = "normal"

        DisplayCurrentRoundInstruction(FrTableScreen, True) 
        numOfPlayersMadeBetInThisRound += 1
        main.wait_variable(playerMadeDecision) 

    if numOfPlayersMadeBetInThisRound != 4 and whoseTurn != 0: 
        ExecuteRoundFour(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
    elif numOfPlayersMadeBetInThisRound == 4: 
        previousRoundLastBet = lastBet
        roundFourExecuted = True

def ExecuteRoundThree():
    global roundThreeExecuted, botHandsStrengths, communityHand, allBotHands

    botHandsStrengths = []

    global roundThreeExecuted, botHandsStrengths, communityHand, allBotHands

    botHandsStrengths = []

    for hand in range(3):
        botHandStrength = CalculateHandStrength(allBotHands[hand]) 
        botHandsStrengths.append(botHandStrength) 


    roundThreeExecuted = True

def ExecuteRoundTwo(cardButtons):
    global roundTwoExecuted


    for x in range(3): 
        GeneratePlayerCard(cardButtons) 
        GenerateCardForAllBots() 

    print("in round two - given 3 cards to all")

    roundTwoExecuted = True

def ExecuteRoundOne(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global roundOneExecuted, whoseTurnInRoundOne, firstTimeExecutingRoundOne, numOfBetsMade, previousRoundLastBet, lastBet

    if firstTimeExecutingRoundOne:
        whoseTurnInRoundOne = whoseTurn
        numOfBetsMade = 0
        lastBet = 0
        previousRoundLastBet = ""
        firstTimeExecutingRoundOne = False

    if numOfBetsMade < 4 and whoseTurn != 0: 
        MakeBotBet(TxPot, FrScrollableText) 
        numOfBetsMade += 1 
        ExecuteRoundOne(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)


    elif numOfBetsMade < 4 and whoseTurn == 0:
        BtBetBlind = Button(FrCommandPanel, text="BET BLIND (10 COINS)",
                            compound="c", image=pixel, height=32, width=229,
                            font=("Rockwell", 13), borderwidth=0, background="light grey",
                            command=lambda:[DeductCoinsFromPlayer(10, TxPlayerCoins), 
                                            UpdatePot(10, TxPot), 
                                            UpdateFeedback(10, FrScrollableText, False, False), 
                                            IncreaseWhoseTurn(), 
                                            ExecuteRoundOne(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)])
        BtBetBlind.place(x=8,y=8) 
        numOfBetsMade += 1 

    elif numOfBetsMade == 4:
        previousRoundLastBet = lastBet
        roundOneExecuted = True
        ExecuteGameSequence(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)


def ResetMostGlobalValues():
    global pot, allBotHands, playerHand, communityHand, numOfCards, currentRound, dealer, whoseTurn, roundOneExecuted, roundTwoExecuted, roundThreeExecuted, roundFourExecuted
    global roundFiveExecuted, roundSixExecuted, roundSevenExecuted, roundEightExecuted, roundNineExecuted, roundTenExecuted, roundElevenExecuted, cardsList

    pot = 0

    allBotHands = [ [], [], [] ] 
    playerHand = []
    communityHand = []

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

    numOfCards = 51 
    cardsList = CreateListOfCards() 


def Leave():
    ResetMostGlobalValues()
    ClearWindowOrFrame(main)
    MakeWindowGameMenu()


def Fold(FrTableScreen):

    ClearWindowOrFrame(FrTableScreen)

    BtRaise["state"] = "disabled"
    BtCall["state"] = "disabled"
    BtCheck["state"] = "disabled"
    BtCombine["state"] = "disabled"
    BtFold["state"] = "disabled"
    try:
        BtContinue["state"] = "disabled"
    except:
        pass

    TxYouFolded = Label(FrTableScreen, text="You folded and lost.", font=("Rockwell", 16))
    TxYouFolded.place(x=10,y=10)

    UpdateAccStatsDB("lost")

    BtLeave = Button(FrTableScreen, text="LEAVE\nGAME", font=("Rockwell", 16), borderwidth=0,
                    background="light grey", compound="c", image=pixel, height=70, width=70,
                    command=lambda:Leave())
    BtLeave.place(x=10,y=40)


def UpdateBotHandStrengthsList():
    global botHandsStrengths, playerHandStrength
    botHandsStrengths = []


    for bot in range(3):
        tempList = communityHand.copy() 

        for card in range(len(allBotHands[bot])):
            tempList.append(allBotHands[bot][card]) 

        botHandStrength = CalculateHandStrength(tempList) 
        botHandsStrengths.append(botHandStrength) 
    

    print(f"strengths of all bots: {botHandsStrengths}")

    
    tempList = communityHand.copy() 
    for card in range(len(playerHand)):
        tempList.append(playerHand[card]) 
    
    playerHandStrength = CalculateHandStrength(tempList)
    

def IncreaseWhoseTurn():
    global whoseTurn 
   
    if whoseTurn == 3: 
        whoseTurn = 0 
    else: 
        whoseTurn +=1 


def UpdatePot(number, TxPot):
    global pot 

    pot += int(number) 
    TxPot.config(text=f"POT: {pot}") 


def UpdateFeedback(number, FrScrollableText, fold, combined):
    if fold: 
        if whoseTurn != 0: 
            Label(FrScrollableText, text=f"BOT {whoseTurn} FOLDED", font=("Rockwell", 10)).pack() 
        else: 
            Label(FrScrollableText, text=f"{accountUsername} FOLDED", font=("Rockwell", 10)).pack() 

    elif number == 0: 
        if whoseTurn != 0: 
            Label(FrScrollableText, text=f"BOT {whoseTurn} CHECKED", font=("Rockwell", 10)).pack() 
        else: 
            Label(FrScrollableText, text=f"{accountUsername} CHECKED", font=("Rockwell", 10)).pack() 

    elif not combined and number != "tried to combine": 
        if whoseTurn != 0: 
            Label(FrScrollableText, text=f"BOT {whoseTurn} PLACED BET OF {number}", font=("Rockwell", 10)).pack() 
        else: 
            Label(FrScrollableText, text=f"{accountUsername} PLACED BET OF {number}", font=("Rockwell", 10)).pack() 

    elif not combined and number == "tried to combine": 
        if whoseTurn != 0: 
            Label(FrScrollableText, text=f"BOT {whoseTurn} DIDN'T COMBINE", font=("Rockwell", 10)).pack() 
        else: 
            Label(FrScrollableText, text=f"{accountUsername} DIDN'T COMBINE", font=("Rockwell", 10)).pack() 

    elif combined: 
        if whoseTurn != 0: 
            Label(FrScrollableText, text=f"BOT {whoseTurn} COMBINED", font=("Rockwell", 10)).pack() 
        else: 
            Label(FrScrollableText, text=f"{accountUsername} COMBINED", font=("Rockwell", 10)).pack() 


def DisplayCurrentRoundInstruction(FrTableScreen, labelExists):
    global roundInstruction
   
    if not labelExists:
        roundInstruction = Label(FrTableScreen, text="", font=("Rockwell", 16), background="light grey")
        roundInstruction.place(x=10,y=10)

    if whoseTurn == 0: 
        if currentRound == 1:
            roundInstruction.config(text="First round of betting")

        elif currentRound == 4:
            roundInstruction.config(text="Second round of betting")

        elif currentRound == 6:
            roundInstruction.config(text="First combination round")

        elif currentRound == 7:
            roundInstruction.config(text="Third round of betting")

        elif currentRound == 9:
            roundInstruction.config(text="Second combination round")

        elif currentRound == 10:
            roundInstruction.config(text="Fourth round of betting")

    if currentRound == 11:
        roundInstruction.config(text="Showdown")


def ExecuteGameSequence(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList):
    global currentRound, firstTimeExecutingRoundOne, firstTimeExecutingRoundFour, firstTimeExecutingRoundSix, firstTimeExecutingRoundSeven, firstTimeExecutingRoundNine, firstTimeExecutingRoundTen

    if currentRound == 1: 
        firstTimeExecutingRoundOne = True
        if not roundOneExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, False)
            print("start of 'if not' roundOneExecuted:", roundOneExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundOne(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
            print("end of 'if not' roundOneExecuted:", roundOneExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundOneExecuted:
            print("start of 'if' roundOneExecuted:", roundOneExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1 
            print("end of 'if' roundOneExecuted:", roundOneExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")

    if currentRound == 2: 
        if not roundTwoExecuted:
            print("start of 'if not' roundTwoExecuted:", roundTwoExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundTwo(cardButtons)
            print("end of 'if not' roundTwoExecuted:", roundTwoExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundTwoExecuted:
            print("start of 'if' roundTwoExecuted:", roundTwoExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundTwoExecuted:", roundTwoExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
           
    if currentRound == 3: 
        if not roundThreeExecuted:
            print("start of 'if not' roundThreeExecuted:", roundThreeExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundThree()
            print("end of 'if not' roundThreeExecuted:", roundThreeExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundThreeExecuted:
            print("start of 'if' roundThreeExecuted:", roundThreeExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundThreeExecuted:", roundThreeExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
   
    if currentRound == 4: 
        firstTimeExecutingRoundFour = True
        if not roundFourExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, True)
            print("start of 'if not' roundFourExecuted:", roundFourExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundFour(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
            print("end of 'if not' roundFourExecuted:", roundFourExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundFourExecuted:
            print("start of 'if' roundFourExecuted:", roundFourExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            playerMadeDecision.set(False)
            print("end of 'if' roundFourExecuted:", roundFourExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
   
    if currentRound == 5: 
        if not roundFiveExecuted:
            print("start of 'if not' roundFiveExecuted:", roundFiveExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundFive(cardButtons, communityCardList)
            print("end of 'if not' roundFiveExecuted:", roundFiveExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundFiveExecuted:
            print("start of 'if' roundFiveExecuted:", roundFiveExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundFiveExecuted:", roundFiveExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
   
    if currentRound == 6: 
        firstTimeExecutingRoundSix = True
        if not roundSixExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, True)
            print("start of 'if not' roundSixExecuted:", roundSixExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundSix(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
            print("end of 'if not' roundSixExecuted:", roundSixExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundSixExecuted:
            print("start of 'if' roundSixExecuted:", roundSixExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundSixExecuted:", roundSixExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")

    if currentRound == 7: 
        firstTimeExecutingRoundSeven = True
        if not roundSevenExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, True)
            print("start of 'if not' roundSevenExecuted:", roundSevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundSeven(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
            print("end of 'if not' roundSevenExecuted:", roundSevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundSevenExecuted:
            print("start of 'if' roundSevenExecuted:", roundSevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            playerMadeDecision.set(False)
            print("end of 'if' roundSevenExecuted:", roundSevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")

    if currentRound == 8: 
        if not roundEightExecuted:
            print("start of 'if not' roundEightExecuted:", roundEightExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundEight(cardButtons, communityCardList)
            print("end of 'if not' roundEightExecuted:", roundEightExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundEightExecuted:
            print("start of 'if' roundEightExecuted:", roundEightExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundEightExecuted:", roundEightExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
   
    if currentRound == 9: 
        firstTimeExecutingRoundNine = True
        if not roundNineExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, True)
            print("start of 'if not' roundNineExecuted:", roundNineExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundNine(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
            print("end of 'if not' roundNineExecuted:", roundNineExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundNineExecuted:
            print("start of 'if' roundNineExecuted:", roundNineExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundNineExecuted:", roundNineExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
   
    if currentRound == 10: 
        firstTimeExecutingRoundTen = True
        if not roundTenExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, True)
            print("start of 'if not' roundTenExecuted:", roundTenExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundTen(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)
            print("end of 'if not' roundTenExecuted:", roundTenExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundTenExecuted:
            print("start of 'if' roundTenExecuted:", roundTenExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundTenExecuted:", roundTenExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")

    if currentRound == 11: 
        if not roundElevenExecuted:
            DisplayCurrentRoundInstruction(FrTableScreen, True)
            print("start of 'if not' roundElevenExecuted:", roundElevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            ExecuteRoundEleven(FrTableScreen)
            print("end of 'if not' roundElevenExecuted:", roundElevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")
        if roundElevenExecuted:
            print("start of 'if' roundElevenExecuted:", roundElevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn)
            currentRound += 1
            print("end of 'if' roundElevenExecuted:", roundElevenExecuted, "current round:", currentRound, "whose turn:", whoseTurn, "\n")


def MakeWindowGame():

    
    main.geometry("1050x700+480+200") 
    
    
    FrCardScreen = Frame(main, background="dark grey", width=800, height=200)
    FrCardScreen.place(x=0, y=500)

    FrTableScreen = Frame(main, width=800, height=500)
    FrTableScreen.place(x=0, y=0)

    FrCommandPanel = Frame(main, background="grey", width=250, height=200)
    FrCommandPanel.place(x=800, y=500)

    FrGameFeedback = Frame(main, width=250, height=500)
    FrGameFeedback.place(x=800, y=0)

    FrCommandPanelExtension = Frame(main, background="dark grey", width=135, height=200)
    FrCommandPanelExtension.place(x=665, y=500)
    
    
    CaTableScreen = Canvas(FrTableScreen, background="light grey", width=800, height=500)
    CaTableScreen.place(x=0, y=0)

    CaTableScreen.create_rectangle(100, 100, 700, 400,
                                outline="black", fill="dark green",
                                width=2)

    CaTableScreen.create_rectangle(50, 150, 100, 350,
                                outline="black", fill="
                                width=2)

    CaTableScreen.create_rectangle(300, 50, 500, 100,
                                outline="black", fill="
                                width=2)

    CaTableScreen.create_rectangle(700, 150, 750, 350,
                                outline="black", fill="
                                width=2)

    CaTableScreen.create_rectangle(300, 400, 500, 450,
                                outline="black", fill="
                                width=2)

    TxBot1Name = Label(FrTableScreen, text="BOT 1", font=("Rockwell", 10), background="
    TxBot1Name.place(x=55,y=240)

    TxBot2Name = Label(FrTableScreen, text="BOT 2", font=("Rockwell", 10), background="
    TxBot2Name.place(x=380,y=65)

    TxBot3Name = Label(FrTableScreen, text="BOT 3", font=("Rockwell", 10), background="
    TxBot3Name.place(x=705,y=240)

    TxPlayerName = Label(FrTableScreen, text=accountUsername, font=("Rockwell", 10), background="
    TxPlayerName.place(x=380,y=412)

    playerCoins = GetPlayerCoins()
    TxPlayerCoins = Label(FrTableScreen, text=accountUsername + "'s coins: " + str(playerCoins), font=("Rockwell", 16), background="light grey")
    TxPlayerCoins.place(x=297,y=460)

    TxPot = Label(FrTableScreen, text="POT: " + str(pot), font=("Rockwell", 10), background="dark green", foreground="white")
    TxPot.place(x=380,y=200)

    if dealer == 0:
        TxDealer = Label(FrTableScreen, text=" D ", font=("Rockwell", 20), background="grey")
        TxDealer.place(x=247,y=413)
    elif dealer == 1:
        TxDealer = Label(FrTableScreen, text=" D ", font=("Rockwell", 20), background="grey")
        TxDealer.place(x=49,y=364)
    elif dealer == 2:
        TxDealer = Label(FrTableScreen, text=" D ", font=("Rockwell", 20), background="grey")
        TxDealer.place(x=247,y=50)
    elif dealer == 3:
        TxDealer = Label(FrTableScreen, text=" D ", font=("Rockwell", 20), background="grey")
        TxDealer.place(x=711,y=364)
    
    
    BtCardOne = Button(FrCardScreen, borderwidth=0)
    BtCardOne.place(x=15,y=15)

    BtCardTwo = Button(FrCardScreen, borderwidth=0)
    BtCardTwo.place(x=145,y=15)

    BtCardThree = Button(FrCardScreen, borderwidth=0)
    BtCardThree.place(x=275,y=15)

    BtCardFour = Button(FrCardScreen, borderwidth=0)
    BtCardFour.place(x=405,y=15)

    BtCardFive = Button(FrCardScreen, borderwidth=0)
    BtCardFive.place(x=535,y=15)

    
    cardButtons = [BtCardOne, BtCardTwo, BtCardThree, BtCardFour, BtCardFive] 

    
    TxCommCardOne = Label(FrTableScreen, borderwidth=0)
    TxCommCardOne.place(x=310,y=230)

    TxCommCardTwo = Label(FrTableScreen, borderwidth=0)
    TxCommCardTwo.place(x=380,y=230)

    TxCommCardThree = Label(FrTableScreen, borderwidth=0)
    TxCommCardThree.place(x=450,y=230)

    
    communityCardList = [TxCommCardOne, TxCommCardTwo, TxCommCardThree] 

    
    CaGameFeedback = Canvas(FrGameFeedback, width=228, height=496) 
    scrollBar = Scrollbar(FrGameFeedback, orient="vertical", command=CaGameFeedback.yview) 
    FrScrollableText = Frame(CaGameFeedback) 

    FrScrollableText.bind("<Configure>", lambda e: CaGameFeedback.configure(scrollregion=CaGameFeedback.bbox("all")))
    
    CaGameFeedback.create_window((0, 0), window=FrScrollableText, anchor="nw") 
    CaGameFeedback.configure(yscrollcommand=scrollBar.set) 

    CaGameFeedback.pack(side=LEFT, fill=BOTH, expand=True)
    scrollBar.pack(side=RIGHT, fill="y")

    CaGameFeedback.update_idletasks() 
    CaGameFeedback.yview_moveto(1) 
    
    
    ExecuteGameSequence(FrTableScreen, FrCardScreen, FrCommandPanel, FrCommandPanelExtension, FrScrollableText, TxPlayerCoins, TxPot, cardButtons, communityCardList)


def MakeWindowGameMenu():

    
    main.geometry("215x215")
    
    
    TxGame = Label(main, text="GAME", font=("Rockwell", 18))
    TxGame.pack()

    
    BtPlay = Button(main, text="PLAY",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=195,
                    borderwidth=0, bg="light grey",
                    command=lambda:GameMenuToAnotherMenu(2))
    BtPlay.place(x=8, y=33)

    BtViewAccStats = Button(main, text="VIEW ACCOUNT\nSTATISTICS",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=60, width=195,
                    borderwidth=0, bg="light grey",
                    command=lambda:GameMenuToAnotherMenu(3))
    BtViewAccStats.place(x=8, y=70)

    BtHelp = Button(main, text="HELP",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=195,
                    borderwidth=0, bg="light grey",
                    command=lambda:GameMenuToAnotherMenu(1))
    BtHelp.place(x=8, y=142)

    BtBack = Button(main, text="BACK",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=195,
                    borderwidth=0, bg="light grey",
                    command=lambda:GameMenuToAnotherMenu(0))
    BtBack.place(x=8, y=179)
    

    if not loggedIn: 
        BtPlay["state"] = "disabled"
        BtViewAccStats["state"] = "disabled"


def MakeWindowAccountStats():

    
    main.geometry("400x230")
    

    statsDbName = (f"Stats({accountUsername}).db") 
    con = sqlite3.connect(statsDbName) 
    cursor = con.cursor() 
        
    
    cursor.execute(f"SELECT * FROM tblStats_{accountUsername}")
    records = cursor.fetchall()
    statsList = []

    for x in range(6):
        for row in records:
            statsList.append(row[x])
    cursor.close()
    
    statsList.pop(0) 

    
    TxStatsTitle = Label(main, text=f"{accountUsername}'s STATISTICS", font=("Rockwell", 18))
    TxStatsTitle.pack()

    TxCurrentMoney = Label(main, text=f"Current coins: {statsList[0]}", font=("Rockwell", 18))
    TxCurrentMoney.place(x=10, y=30)

    TxHandsWon = Label(main, text=f"Total hands won: {statsList[1]}", font=("Rockwell", 18))
    TxHandsWon.place(x=10, y=60)

    TxHandsLost = Label(main, text=f"Total hands lost: {statsList[2]}", font=("Rockwell", 18))
    TxHandsLost.place(x=10, y=90)

    TxLifetimeWinnings = Label(main, text=f"Lifetime winnings: {statsList[3]}", font=("Rockwell", 18))
    TxLifetimeWinnings.place(x=10, y=120)

    TxBiggestPotWon = Label(main, text=f"Biggest pot won: {statsList[4]}", font=("Rockwell", 18))
    TxBiggestPotWon.place(x=10, y=150)
    
    
    BtBack = Button(main, text="BACK",
                    font=("Rockwell", 18),
                    compound="c", image=pixel,
                    height=25, width=375,
                    borderwidth=0, bg="light grey",
                    command=lambda:[ClearWindowOrFrame(main),
                    MakeWindowGameMenu()])
    BtBack.place(x=10, y=190)


    def AccountCreatedMessage(BtBack, BtRegisterAccount):
    main.geometry("295x258")
    counter = 0
    BtBack["state"] = "disabled" 
    BtRegisterAccount["state"] = "disabled" 
    actualText = "ACCOUNT CREATED.\nRETURNING TO MAIN MENU IN 3..."
    TxFeedback = Label(main, text=actualText, font=("Rockwell", 10))
    TxFeedback.place(x=45, y=220)
    UpdateAccountCreatedMessage(counter, TxFeedback, actualText)