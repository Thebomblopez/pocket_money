from operator import itemgetter
import apps.poker_app.helpers as helpers 

#Dictionary of hands in ranked
Hands = {
    1: "High Card",
    2: "Pair",
    3: "Two Pairs",
    4: "Three of a Kind",
    5: "Straight",
    6: "Flush",
    7: "Full House",
    8: "Four of a Kind",
    9: "Straight Flush",
    10: "Royal Flush"
}

# Helper Variables
amount_suits = 13
amount_cards = 4

# Recieve All cards that are counted to an amount greater than 1
def value_repeats(used_cards):
    
    counts = []
    for card in used_cards:
        if counts == []:
            counts.append([card])
        else:
            added = False
            for arr in counts:
                if arr[0][0] == card[0]:
                    arr.append(card)
                    added = True
            if added == False:
                counts.append([card])
    repeats = [x for x in counts if len(x) >=2]
    return repeats

# Return any flushes
def check_flush(used_cards):
    counts = {}
    for card in used_cards:
        if card[1] in counts.keys():
            counts[card[1]] += 1
        else:
            counts[card[1]] = 1
    flushes = {}
    for k, v in counts.items():
        if v >= 5:
            flushes[k] = v
    return flushes

# Return Straights
def check_straights(used_cards):
    used_cards = helpers.convert_vals(used_cards)
    used_cards.sort(key=itemgetter(0))

    count = 1
    cards = []
    temp = ''
    straights = []
    
    for i in range(len(used_cards)):
        if cards == []:
            temp = used_cards[i]
            cards.append(temp)
        
        elif used_cards[i][0] == temp[0] + 1 and count == 5:
            cards = cards[1:]
            temp = used_cards[i]
            cards.append(temp)
            straights.append(cards)

        elif used_cards[i][0] == temp[0] + 1:
            temp = used_cards[i]
            cards.append(temp)
            count += 1
            if count == 5:
                straights.append(cards)
        
        elif used_cards[i][0] == temp[0]:
            cards.pop()
            temp = used_cards[i]
            cards.append(temp)
                
        else:
            count = 1
            temp = used_cards[i]
            cards = [temp]

    return straights

# Check card reapeats
def check_card_repeats(repeated_cards):
    if len(repeated_cards) == 1 and len(repeated_cards[0]) == 3:

        return "Three of a kind " + repeated_cards[0][0][0]+"'s"
    
    if len(repeated_cards) == 1 and len(repeated_cards[0]) == 2:
        return "Pair of " + repeated_cards[0][0][0]+"'s"

    if len(repeated_cards) == 1 and len(repeated_cards[0]) == 4:
        return "Four of a kind " + repeated_cards[0][0][0]+"'s"

    if len(repeated_cards) == 2:
        if len(repeated_cards[0]) == 2 and len(repeated_cards[1]) == 2:
            return "Two Pairs " + repeated_cards[0][0][0]+"'s"+" and"+ repeated_cards[1][0][0]+"'s"

        if len(repeated_cards[0]) == 3 and len(repeated_cards[1]) == 2:
            return "Full House Three" + repeated_cards[0][0][0]+"'s"+" and two "+ repeated_cards[1][0][0]+"'s"

        if len(repeated_cards[1]) == 3 and len(repeated_cards[1]) == 2:
            return "Full House Three" + repeated_cards[1][0][0]+"'s"+" and two "+ repeated_cards[0][0][0]+"'s"



