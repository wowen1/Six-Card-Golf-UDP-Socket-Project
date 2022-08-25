#Socket Group 7
#Lamanh Ngo
#William Owen

import sys
from socket import *
import random

#---PORT INFORMATION---
#Socket Project Group 7
#7 mod 2 = 1
#Port Range:
#Lower: ([7/2] * 1000) + 500 = 4000
#Upper: ([7/2] * 1000) + 999 = 4499
#[4000, 4499]
#Host Port = 4000

class Card:
    def __init__(self, suit, rank, faceUp =False):
        self.rank = rank
        self.faceUp = faceUp
        self.suit = suit

    def getValue(self):
        if self.faceUp:  
            return self.rank # dont really need the suit to add up 

    def setFaceUp(self):
        self.faceUp = True  #set as true because you're replacing a card and turning it face up

    def show(self):
        if(self.faceUp):
            print("{}{}".format(self.rank, self.suit),end=" ")
        else:
            print("***", end=" ")

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in ["S", "C", "D", "H"]:
            for v in range(1,14):
                self.cards.append(Card(s,v))

    def shuffle(self):
        for i in range(len(self.cards)-1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] =self.cards[r],self.cards[i]

    def show(self):
        for c in self.cards:
            c.show()

    def drawCard(self):
        return self.cards.pop()

    
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = [] 
        self.points = 0

    def draw(self, deck):   #draw 6x for each players
        self.hand.append(deck.drawCard())

    def showHand(self):
        for i in range(3):  #really just an array of 6 but displaying it as a 2x3 array
            self.hand[i].show()
        print()
        for i in range(3):
            self.hand[i+3].show()
        print()


class Game:
    def __init__(self, players):  #pass in a list of Player
        self.deck = Deck()
        self.deck.shuffle()
        self.discardPile = []
        self.discardPile.append(self.deck.cards.pop()) #Draw a single card into the discardPile
        self.discardPile[0].faceUp = True   #make the card face up
        self.playersArray = []
        for player in players:    #Add the amount of players into the playerArray
            self.playersArray.append(player)

     
    def drawHands(self):    #all players draw their hand
        for player in self.playersArray:
            for i in range(6):      #each players should have 6 cards
                player.draw(self.deck)
            player.hand[0].faceUp = True    #first and second card should be faced up
            player.hand[1].faceUp = True
        
    def drawFrDeck(self, playerTurn, indexOfHand): #playerTurn is index of who's turn it is
        if(not self.playersArray[playerTurn].hand[indexOfHand].faceUp): #facedup card cannot be discarded
            placeHolder = self.playersArray[playerTurn].hand[indexOfHand]   #hold the value of the card the player wants to replace
            drawnCard = self.deck.cards.pop()   #draw one card from the deck
            drawnCard.setFaceUp()
            #check to see if there's a duplicate already in player's hand
            dup = self.checkDup(playerTurn,drawnCard.rank)
            if(dup):
                if(self.handIdx < 3):   #if there's a dup within index 0-2
                   self.playersArray[playerTurn].hand[indexOfHand] = drawnCard  #place the card down in the original spot the player wanted to palce
                   self.swapCards(playerTurn,indexOfHand,self.handIdx+3)    #swap the cards so the duplicate cards are lined up
                else:
                    self.playersArray[playerTurn].hand[indexOfHand] = drawnCard
                    self.swapCards(playerTurn,indexOfHand,self.handIdx-3)
            else:
                self.playersArray[playerTurn].hand[indexOfHand] = drawnCard
            placeHolder.setFaceUp()
            self.discardPile.append(placeHolder)
        else:
            print("Cannot swap with an already faced up card")
        
    def drawFrDiscard(self, playerTurn, indexOfHand):#indexOfHand card cannot be faced up
        if(not self.playersArray[playerTurn].hand[indexOfHand].faceUp):
            placeHolder = self.playersArray[playerTurn].hand[indexOfHand]   #hold the value of the card the player wants to replace
            drawnCard = self.discardPile.pop()

            #now swap if it's a dup
            dup = self.checkDup(playerTurn,drawnCard.rank)
            if(dup):
                if(self.handIdx < 3):
                   self.playersArray[playerTurn].hand[indexOfHand] = drawnCard
                   self.swapCards(playerTurn,indexOfHand,self.handIdx+3)
                else:
                    self.playersArray[playerTurn].hand[indexOfHand] = drawnCard
                    self.swapCards(playerTurn,indexOfHand,self.handIdx-3)
            else:
                self.playersArray[playerTurn].hand[indexOfHand] = drawnCard
            placeHolder.setFaceUp()
            self.discardPile.append(placeHolder)
        else:
            print("Cannot swap with an already faced up card")

    def swapCards(self, playerTurn, index1, index2):    #swapping two cards
            placeHolder = self.playersArray[playerTurn].hand[index1]
            self.playersArray[playerTurn].hand[index1] = self.playersArray[playerTurn].hand[index2]
            self.playersArray[playerTurn].hand[index2] = placeHolder

    def countPoints(self, playerTurn):  #ima just assume that all cards are faced up                                         
        for i in range(6):
            if((i < 3 and self.playersArray[playerTurn].hand[i].rank == self.playersArray[playerTurn].hand[i+3].rank) 
            or (i >= 3 and self.playersArray[playerTurn].hand[i].rank == self.playersArray[playerTurn].hand[i-3].rank)): 
                print(self.playersArray[playerTurn].hand[i].rank, end=" ") 
                self.playersArray[playerTurn].points = self.playersArray[playerTurn].points + 0
                print(self.playersArray[playerTurn].points)
            elif(self.playersArray[playerTurn].hand[i].rank == 13):
                print(self.playersArray[playerTurn].hand[i].rank, end=" " )
                self.playersArray[playerTurn].points = self.playersArray[playerTurn].points + 0
                print(self.playersArray[playerTurn].points)
            elif(self.playersArray[playerTurn].hand[i].rank == 2):
                print(self.playersArray[playerTurn].hand[i].rank, end=" " )
                self.playersArray[playerTurn].points = self.playersArray[playerTurn].points - 2
                print(self.playersArray[playerTurn].points)
            elif(self.playersArray[playerTurn].hand[i].rank > 10):
                print(self.playersArray[playerTurn].hand[i].rank, end=" " )
                self.playersArray[playerTurn].points = self.playersArray[playerTurn].points + 10
                print(self.playersArray[playerTurn].points)
            else:
                print(self.playersArray[playerTurn].hand[i].rank, end=" " )
                self.playersArray[playerTurn].points = self.playersArray[playerTurn].points + self.playersArray[playerTurn].hand[i].rank
                print(self.playersArray[playerTurn].points)

    def showDiscardPile(self):
        for card in self.discardPile:
            card.show()
        print()

    def winner(self):
        min = self.playersArray[0].points
        self.winner = self.playersArray[0]
        for player in self.playersArray:
            if(min>player.points):
                min = player.points
                self.winner = player
        return self.winner

    def tradeCard(self,player1, player2, player1CardIdx, player2CardIdx):
        if((not self.playersArray[player1].hand[player1CardIdx].faceUp) and (not self.playersArray[player2].hand[player2CardIdx].faceUp)): #Both player cards has to be faced down
            #swap
            placeHolder = self.playersArray[player1].hand[player1CardIdx]
            self.playersArray[player1].hand[player1CardIdx] = self.playersArray[player2].hand[player2CardIdx]
            self.playersArray[player1].hand[player1CardIdx].setFaceUp() #turn it face up
            self.playersArray[player2].hand[player2CardIdx] = placeHolder
            self.playersArray[player2].hand[player2CardIdx].setFaceUp() #turn it face up
        else:
            print("Both cards must be faced down in order to steal")

    def checkDup(self,playerTurn,value):
        self.handIdx = 0
        for j in range(6):
            if((value == self.playersArray[playerTurn].hand[j].rank) and (self.playersArray[playerTurn].hand[j].faceUp)):
                self.handIdx = j
                return True
        return False


        


if __name__ == "__main__":

    #deck =Deck()
    #deck.shuffle()
    #deck.show()

    #card = deck.drawCard()
    #card.show()

    Brenda = Player("Brenda")
    #for i in range(6):
    #    Brenda.draw(deck)
    #Brenda.showHand()

    Flynn = Player("Flynn")
    playerList = []
    playerList.append(Brenda) 
    playerList.append(Flynn)

    game = Game(playerList)  #make the game
                    #has a shuffled deck and draw one in the discard pile
                    #1 player only 
    game.drawHands()    #all players draw 6 cards
    print("Show the init hand of player 1")
    game.playersArray[0].showHand()
    print("Show the init hand of player 2")
    game.playersArray[1].showHand()
    print()

    print("Player 1 draw from the deck with index 2")
    game.drawFrDeck(0,2)
    game.playersArray[0].showHand()
    print()

    print("Discard Pile")
    game.showDiscardPile()
    print()

    print("Player 2 draws from the discardPile with index 5")
    game.drawFrDiscard(1,5)
    game.playersArray[1].showHand()
    print()

    print("Discard Pile")
    game.showDiscardPile()
    print()

    print("Player 1 index 1 wants to steal player 2 index 5")
    game.tradeCard(0,1,4,4)
    game.playersArray[0].showHand()
    print()
    game.playersArray[1].showHand()
    print()

    # print("Player 1 draw from the discardPile with index 5")
    # game.drawFrDiscard(0,5)
    # game.playersArray[0].showHand()
    # print()

    # print("Discard Pile")
    # game.showDiscardPile()
    # print()

    # print("Player 2 draws from the deck with index 4")
    # game.drawFrDeck(1,4)
    # game.playersArray[1].showHand()
    # print()

    # print("Discard Pile")
    # game.showDiscardPile()
    # print()

    # print("Player 1 draw from the discardPile with index 4")
    # game.drawFrDiscard(0,4)
    # game.playersArray[0].showHand()
    # print()

    # print("Discard Pile")
    # game.showDiscardPile()
    # print()

    # print("Player 2 draws from the deck with index 3")
    # game.drawFrDeck(1,3)
    # game.playersArray[1].showHand()
    # print()

    # print("Discard Pile")
    # game.showDiscardPile()
    # print()

    # print("Player 1 draw from the deck with index 4")
    # game.drawFrDiscard(0,4)
    # print()

    # print("Player 1 draw from the deck with index 3")
    # game.drawFrDiscard(0,3)
    # game.playersArray[0].showHand()
    # print()

    # print("Discard Pile")
    # game.showDiscardPile()
    # print()

    # print("Player 2 draws from the discardPile with index 2")
    # game.drawFrDiscard(1,2)
    # game.playersArray[1].showHand()
    # print()

    # game.countPoints(0)

    # print()
    # game.countPoints(1)
    # print(f"{game.playersArray[0].name} has {game.playersArray[0].points}")
    # print(f"{game.playersArray[1].name} has {game.playersArray[1].points}")
    # print(f"The winner is {game.winner().name}")
        