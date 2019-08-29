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
def flushes(used_cards):
    counts = []
    used_cards = helpers.convert_vals(used_cards)
    used_cards.sort(key=itemgetter(0))
    used_cards.sort
    for card in used_cards:
        if counts == []:
            counts.append([card])
        else:
            added = False
            for arr in counts:
                if arr[0][1] == card[1]:
                    arr.append(card)
                    added = True
            if added == False:
                counts.append([card])
    
    flushes = [x for x in counts if len(x)>= 5]
    flushes = list(map(lambda x: helpers.revert_vals(x), flushes))

    return flushes

# Return Straights
def straights(used_cards):
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
        return [4, repeated_cards[0][0][0]+"'s"]
    
    if len(repeated_cards) == 1 and len(repeated_cards[0]) == 2:
        return [2,repeated_cards[0][0][0]+"'s"]

    if len(repeated_cards) == 1 and len(repeated_cards[0]) == 4:
        return [8,repeated_cards[0][0][0]+"'s"]

    if len(repeated_cards) == 2:
        if len(repeated_cards[0]) == 2 and len(repeated_cards[1]) == 2:
            return [3,repeated_cards[0][0][0]+"'s"+" and"+ repeated_cards[1][0][0]+"'s"]

        if len(repeated_cards[0]) == 3 and len(repeated_cards[1]) == 2:
            return [7,repeated_cards[0][0][0]+"'s"+" and two "+ repeated_cards[1][0][0]+"'s"]

        if len(repeated_cards[1]) == 3 and len(repeated_cards[1]) == 3:
            return [7, "Three "+ repeated_cards[1][0][0]+"'s"+" and two "+ repeated_cards[0][0][0]+"'s"]

# Check Flush and prepare to add it to Completed Hands
def check_flushes(flush):
    return [ 6, flush[-1][-1][1]+"'s", flush[-1][-1][0]+" high" ]

