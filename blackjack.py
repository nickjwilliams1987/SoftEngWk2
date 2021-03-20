import random

class card:
    """Holds details of a specific card"""
    def __init__(self, suit, number):
        self.suit = suit
        
        # Anything with a number over 10 is 10:
        if number > 10:
            self.number = 10
        else:
            self.number = number
        
        # Generate full string title of card
        suitsDict = {
            1:'Hearts',
            2:'Diamonds',
            3:'Clubs',
            4:'Spades'
        }
        
        if number == 1:
            cardTitle = 'Ace'
        elif number <= 10:
            cardTitle = str(number)
        elif number == 11:
            cardTitle = 'Jack'
        elif number == 12:
            cardTitle = 'Queen'
        elif number == 13:
            cardTitle = 'King'
        else:
            cardTitle = 'Unknown'
        
        self.name = '[' + cardTitle + ' of ' + suitsDict[suit] + ']'
    
    def __str__(self):
        return self.name
    
    def returnName(self):
        return self.name
    
    def returnNumber(self):
        return self.number

    
class deck:
    """Contains the full list of cards"""
    def __init__(self, totalDecks):
        """totalDecks is an integer of how many decks of 52 cards are needed"""
        self.cards = []
        
        for i in range(totalDecks):
            self.generateDeck()
            
        self.shuffle()
        
        
    def generateDeck(self):
        """Generates a single deck of 52 cards and adds them to the card list"""
        for suit in range(1,5):
            for number in range(1,14):
                self.cards.append(card(suit,number))
                
    def shuffle(self):
        """Shuffles all remaining cards"""
        random.shuffle(self.cards)
        
    def drawCard(self):
        """Returns a random card and removes it from the deck"""
        return self.cards.pop()
    
                
        
class player:
    """Player basic functions"""
    
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.type = 'Player'
        
    def draw(self, deck, cards=1):
        """Draws a new card from the deck and adds it to the player's hand"""
        for i in range(cards):
            self.hand.append(deck.drawCard())
        
    def getHand(self, hidden=False):
        """if hidden = True, hide the first card in the hand"""
        h = ''
        for card in self.hand:
            if hidden and card == self.hand[0]:
                h += '[x]'
            else:
                h += str(card)
        return h
    
    def printHand(self, hidden=False):
        """Prints the actual hand"""
        print(self.name + '\'s Hand: ' + self.getHand(hidden))
        
    def printValue(self):
        print(self.name + '\'s Hand Value: ' + str(self.totalValue()))

    def totalValue(self):
        """Returns the total value of the player's current hand"""
        value = 0
        for card in self.hand:
            value += card.returnNumber()
            
        return value
    
    
    def play(self, deck):
        """Looping sequence of play for player input"""
        stay = False
        while not stay:
            command = input('Draw a new card? (Y/N): ').upper()

            if command != 'Y' and command != 'N':
                print('Invalid command. Please try again.')
                
            elif command == 'Y': # Hit me! Draw a new card
                self.draw(deck)
                self.printHand()
                self.printValue()

                if self.totalValue() > 21:
                    print('\nBUST! Dealer wins.')
                    return False
                
            if command == 'N': # Stand
                print('Stand with a score of ' + str(self.totalValue()))
                return self.totalValue()
            
        

    
class dealer(player):
    """dealer object"""
    
    def __init__(self):
        player.__init__(self, 'Dealer')
        self.type = 'Dealer'
        
    def play(self, deck, playersScore):
        """A simple routine for the dealer to play the game"""
        print('\nDealer begins play')
        self.printHand()
        
        print('Total score: ' + str(self.totalValue()))
        
        # Keep drawing hands until the score is equal or greater than player's score
        while self.totalValue() < playersScore:
            self.draw(deck)
            print('Dealer drew ' + str(self.hand[-1]))
            print('Total score: ' + str(self.totalValue()))
            
        return self.totalValue()
        
    
    
def play():
    """Sequence of play"""
    
    deckObj = deck(1)
    dealerObj = dealer()
    
    playerName = input('Please enter your name: ')
    playerObj = player(playerName)
    
    # Draw cards
    playerObj.draw(deckObj,2)
    dealerObj.draw(deckObj,2)
    
    # Show hands
    dealerObj.printHand(True)
    playerObj.printHand()
    playerObj.printValue()
    
    # player
    playerScore = playerObj.play(deckObj)
    
    if not playerScore: #Player has bust (drawn over 21)
        return
    
    dealerScore = dealerObj.play(deckObj, playerScore)
    
    if dealerScore >= playerScore and dealerScore <= 21:
        print('\nDealer wins!')
    elif dealerScore > 21:
        print('BUST!\n\nPlayer wins!')
    else:
        print('\nPlayer wins!')



play()
    
