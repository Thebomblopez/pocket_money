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

# Recieve all cards that are repeated
def repeats(used_cards):
    used_cards = helpers.convert_vals(used_cards)
    used_cards.sort(key=itemgetter(0))
    
    counts = []
    for card in used_cards:
        if counts == []:
            counts.append([ card ])
            
        else:
            added = False
            for i in range(len(counts)):
                if counts[i][0][0] == card[0]:
                    counts[i].append(card)
                    added = True
                if i == len(counts) - 1 and added == False:
                    counts.append([ card ])
    
    repeats = [x for x in counts if len(x) >=2]
    
    used_cards = helpers.revert_vals(used_cards)
    
    if len(repeats) == 0:
        return used_cards[-1]
    return repeats

# Return any flushes
def flushes(used_cards):
    counts = []
    used_cards = helpers.convert_vals(used_cards)
    used_cards.sort(key=itemgetter(0))
    
    for card in used_cards:
        if counts == []:
            counts.append([ card ])
            print("Counts in first iter: ", counts)
        else:
            added = False
            for i in range(len(counts)):
                if counts[i][0][1] == card[1]:
                    counts[i].append(card)
                    added = True

                if i == len(counts) - 1 and added == False:
                    counts.append([ card ])
    
    flushes = [c for c in counts if len(c) >= 5]
    possibles = [c for c in counts if len(c) == 4]
    used_cards = helpers.revert_vals(used_cards)

    return  flushes, possibles 

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
    
    used_cards = helpers.revert_vals(used_cards)
      
    return straights

# Check card reapeats
def check_repeats(repeated_cards):
    # High Card
    if len(repeated_cards) == 2 and type(repeated_cards[0]) == str:
        return [ [ 1,repeated_cards[0]+' of '+repeated_cards[1] ], [ 2, repeated_cards[0], 3 ] ]
    # Three of a kind
    if len(repeated_cards) == 1 and len(repeated_cards[0]) == 3:
        return [ [ 4, repeated_cards[0][0][0] ], [ 8, repeated_cards[0][0][0], 1 ] ]
    # Pair
    if len(repeated_cards) == 1 and len(repeated_cards[0]) == 2:
        return [ [ 2,repeated_cards[0][0][0] ], [ 4, repeated_cards[0][0][0], 2 ] ]
    # Four of a kind
    if len(repeated_cards) == 1 and len(repeated_cards[0]) == 4:
        return [ [ 8,repeated_cards[0][0][0] ], None ]
    
    
    if len(repeated_cards) == 2:
        # Two Pairs
        if len(repeated_cards[0]) == 2 and len(repeated_cards[1]) == 2:
            return [ [ 3, repeated_cards[0][0][0]+" and "+ repeated_cards[1][0][0] ], [ 7, repeated_cards[1][0][0], 4 ] ] 
        # Full House
        if len(repeated_cards[0]) == 3 and len(repeated_cards[1]) == 2:
            return [ [ 7, repeated_cards[0][0][0]+"'s and two "+ repeated_cards[1][0][0] ], [ 8, repeated_cards[0][0][0], 1 ] ]
        # Full House
        if len(repeated_cards[1]) == 3 and len(repeated_cards[0]) == 2:
            return [ [ 7, "Three "+ repeated_cards[1][0][0]+"'s and two "+ repeated_cards[0][0][0] ], [ 8, repeated_cards[1][0][0], 1 ] ]
        # Two three of a kinds
        if len(repeated_cards[0]) == 3 and len(repeated_cards[1]) == 3:
            return [ [ 7, "Three "+ repeated_cards[1][0][0]+"'s and two "+ repeated_cards[0][0][0] ], [ 8, repeated_cards[1][0][0], 1 ] ]
        #Four of a kind
        if len(repeated_cards[0]) == 4:
            return [ [ 8, repeated_cards[0][0][0] ], None ]
        if len(repeated_cards[1]) == 4:
            return [ [ 8, repeated_cards[1][0][0] ], None ]
    if len(repeated_cards) == 3:
        # Two Pair
        if len(repeated_cards[1]) == 2 and len(repeated_cards[2]) == 2:
            return [ [  3, repeated_cards[1][0][0]+"'s and "+ repeated_cards[2][0][0] ], [ 7, repeated_cards[1][0][0], 4 ] ]
        # Full House
        if len(repeated_cards[1]) == 3 and len(repeated_cards[2]) == 2:
            return [ [ 7, "Three "+repeated_cards[1][0][0]+"'s and two "+ repeated_cards[2][0][0] ],  [ 8, repeated_cards[1][0][0], 1 ] ]
        # Full House
        if len(repeated_cards[2]) == 3 and len(repeated_cards[1]) == 3:
            return [ [ 7, "Three "+ repeated_cards[2][0][0]+"'s and two "+ repeated_cards[1][0][0]], [ 8, repeated_cards[2][0][0], 1 ] ] 

# Check Flush and prepare to add it to Completed Hands
def check_flushes(flush):
    if flush[0] == [] and len(flush[1][0]) > 0:
        return [ [ ], [ 6, "Of "+flush[1][0][0][1], 9 ] ]

    if flush[1] == [] and len(flush[0]) > 0:
        return [ [ 6, "Of " + flush[0][0][0][1] + " with " + flush[0][0][-1][0]+" high" ], [ ] ]


# Check Straights and prepare to add it to Comleted Hands
def check_straights(straights):
    return [ 5, straights[-1][-1][0] + " high" ]


