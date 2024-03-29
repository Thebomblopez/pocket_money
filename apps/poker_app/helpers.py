import apps.poker_app.iDent as id
import random 

# Cards and Suits
vals = ['2','3','4','5','6','7','8','9','10','jack','queen','king','ace']
suits = ['Spades','Hearts','Diamonds','Clubs']
# Create Deck
deck = []
for suit in suits:
    for val in vals:
        deck.append([val, suit])

# Remove previously added cards to session before adding more and setting new ones
def reset_used_hand(session):
    hand = session['hand_cards']
    used = session['used_cards']
    for card in hand:
        for used_card in used:
            if card == used_card:
                used.remove(used_card)
    return used

def reset_used_flop(session):
    flop = session['flop_cards']
    used = session['used_cards']
    for card in flop:
        for used_card in used:
            if card == used_card:
                used.remove(used_card)
    return used

def reset_used_turn(session):
    turn = session['turn_card']
    used = session['used_cards']
    if turn in used:
        used.remove(turn)
    return used

def reset_used_river(session):
    river = session['river_card']
    used = session['used_cards']
    if river in used:
        used.remove(river)
    return used

# set hand in session if none
def ishand(session):
    there = False
    for k,v in session.items():
        if k == 'hand_cards':
            there = True
    if there:
        return session["hand_cards"]
    else:
        return []

# set used in session if none
def is_used(session):
    there = False
    for k,v in session.items():
        if k == 'used_cards':
            there = True
    if there:
        return session["used_cards"]
    else:
        return []

# set flop in session if none
def is_flop(session):
    there = False
    for k,v in session.items():
        if k == 'flop_cards':
            there = True
    if there:
        return session["flop_cards"]
    else:
        return []

# set turn in session if none
def is_turn(session):
    there = False
    for k,v in session.items():
        if k == 'turn_card':
            there = True
    if there:
        return session["turn_card"]
    else:
        return []

# set river in session if none
def is_river(session):
    there = False
    for k,v in session.items():
        if k == 'river_card':
            there = True
    if there:
        return session["river_card"]
    else:
        return []

# Make sure there are no duplicate cards added
def is_duplicate_hand(input_form, used_cards):
    try:
        first_card = [ input_form['first_card_value'], input_form['first_card_suit'] ]
        second_card = [ input_form['second_card_value'], input_form['second_card_suit'] ]
        
        if first_card == second_card:
            return True
        
        if first_card in used_cards or second_card in used_cards:
            return True
        else:
            return False
    except:
        return True

def is_duplicate_flop(input_form, used_cards):
    try:
        first_card = [ input_form['first_card_value'], input_form['first_card_suit'] ]
        second_card = [ input_form['second_card_value'], input_form['second_card_suit'] ]
        third_card = [ input_form['third_card_value'], input_form['third_card_suit'] ]
        
        if first_card == second_card:
            return True

        elif first_card == third_card:
            return True
        
        elif second_card == third_card:
            return True
        
        elif (first_card[0] == None or first_card[1] == None) or (second_card[0] == None or second_card[1] == None) or (third_card[0] == None or third_card[1] == None):
            return True
        
        if first_card in used_cards or second_card in used_cards or third_card in used_cards:
            return True

        else:
            return False
    except:
        return True

def is_duplicate_turn(input_form, used_cards):
    try:
        turn_card = [ input_form['turn_card_value'], input_form['turn_card_suit'] ]
        if turn_card in used_cards:
            return True
        else:
            return False
    except:
        return True
    
def is_duplicate_river(input_form, used_cards):
    try:
        river_card = [ input_form['river_card_value'], input_form['river_card_suit'] ]
        if river_card in used_cards:
            return True
        else:
            return False
    except:
        return True

# Convert card values to Integers
def convert_vals(cards):
    for card in cards:
        try:
            card[0] = int(card[0]) - 2
        except:
            if card[0] == "jack":
                card[0] = 9
            elif card[0] == "queen":
                card[0] = 10

            elif card[0] == "king":
                card[0] = 11

            elif card[0] == "ace":
                card[0] = 12

    return cards

# Rever card values back to String
def revert_vals(cards):

    for card in cards:
        if card[0] < 9:
            card[0] += 2
            card[0] = str(card[0])
        
        elif card[0] == 9:
            card[0] = "jack"
        
        elif card[0] == 10:
            card[0] = "queen"
        
        elif card[0] == 11:
            card[0] = "king"

        elif card[0] == 12:
            card[0] = "ace"
    
    return cards

# Return the strongest of the complete hands
def strongest_hand(completed_hands):
    strongest = completed_hands[0]
    for hand in completed_hands:
        try:
            if hand[0] > strongest[0]:
                strongest = hand
        except:
            strongest = strongest 

    return id.Hands[strongest[0]] +" "+ strongest[1]

# Calculate Odds of possible hands after Flop
def flop_odds(possible_hands):
    strongest = possible_hands[0]
    for hand in possible_hands:
        if hand[0] > strongest[0]:
            strongest = hand
    return id.Hands[strongest[0]]+ " of "+ strongest[1]+"'s "+str(strongest[2]*4)+"% chance"

# Remove Nones
def remove_none(arr):
    for x in arr:
        if x == None:
            arr.remove(x)
    return arr

# Calculate Odds of possible hands after Turn
def turn_odds(possible_hands):
    strongest = possible_hands[0]
    for hand in possible_hands:
        if hand and hand[0] > strongest[0]:
            strongest = hand
            
    return id.Hands[strongest[0]]+ " of "+ strongest[1]+"'s "+str(strongest[2]*2)+"% chance"

# Return if Stronger Hand is Possible
def possibly_stronger(completed, possible):
    strongest = completed[0]
    validated = False
    for hand in completed:
        if hand[0] > strongest[0]:
            strongest = hand
    print("strongest from comleted", strongest)
    for hand in possible:
        if hand[0] > strongest[0]:
            validated = True
    return validated

# Random Card
def random_card(used_cards):
    card = random.choice(deck)
    while card in used_cards:
        card = random.choice(deck)
    return card



