from django.shortcuts import HttpResponse, redirect, render
import apps.poker_app.helpers as helpers
import apps.poker_app.iDent as id
from django.contrib import messages

# Create your views here.
# Hand Calculator page


def index(request):
    request.session["hand_cards"] = helpers.ishand(request.session)
    request.session["used_cards"] = helpers.is_used(request.session)
    request.session["flop_cards"] = helpers.is_flop(request.session)
    request.session["turn_card"] = helpers.is_turn(request.session)
    request.session["river_card"] = helpers.is_river(request.session)
    # print(request.session["used_cards"])

    return render(request, 'poker_app/hand_calculator.html', request.session)

# Clear Board
def clear_board(request):
    request.session.flush()
    return redirect('/')

# Add Hand cards to session
def submit_hand_cards(request):
    if helpers.is_duplicate_hand(request.POST, request.session['used_cards']):
        messages.error(request, 'Card used more than once or missing cards.')
        return redirect("/")

    request.session['used_cards'] = helpers.reset_used_hand(request.session)

    request.session['hand_cards'] = [
        [request.POST['first_card_value'], request.POST['first_card_suit']],
        [request.POST['second_card_value'], request.POST['second_card_suit']]
    ]

    request.session["used_cards"].append(
        [request.POST['first_card_value'], request.POST['first_card_suit']])
    request.session["used_cards"].append(
        [request.POST['second_card_value'], request.POST['second_card_suit']])

    return redirect('/')

# Add Flop cards to session
def submit_flopcards(request):
    if helpers.is_duplicate_flop(request.POST, request.session['used_cards']):
        messages.error(request, 'Card used more than once or missing cards.')
        return redirect("/")

    request.session['used_cards'] = helpers.reset_used_flop(request.session)

    request.session['flop_cards'] = [
        [request.POST['first_card_value'], request.POST['first_card_suit']],
        [request.POST['second_card_value'], request.POST['second_card_suit']],
        [request.POST['third_card_value'], request.POST['third_card_suit']]
    ]

    request.session["used_cards"].append(
        [request.POST['first_card_value'], request.POST['first_card_suit']])
    request.session["used_cards"].append(
        [request.POST['second_card_value'], request.POST['second_card_suit']])
    request.session["used_cards"].append(
        [request.POST['third_card_value'], request.POST['third_card_suit']])

    return redirect('/')

# Add Turn Card to session
def submit_turn_card(request):
    if helpers.is_duplicate_turn(request.POST, request.session['used_cards']):
        messages.error(request, 'Card used more than once or missing cards.')
        return redirect("/")

    request.session['used_cards'] = helpers.reset_used_turn(request.session)

    request.session['turn_card'] = [
        request.POST['turn_card_value'], request.POST['turn_card_suit']]
    request.session["used_cards"].append(
        [request.POST['turn_card_value'], request.POST['turn_card_suit']])

    return redirect('/')

# Add River Card to session
def submit_river_card(request):
    if helpers.is_duplicate_river(request.POST, request.session['used_cards']):
        messages.error(request, 'Card used more than once or missing cards.')
        return redirect("/")

    request.session['used_cards'] = helpers.reset_used_river(request.session)

    request.session['river_card'] = [
        request.POST['river_card_value'], request.POST['river_card_suit']]
    request.session["used_cards"].append(
        [request.POST['river_card_value'], request.POST['river_card_suit']])

    return redirect('/')

# Calculate Hand
def calculate_hand(request):
    completed_hands = []
    possible_hands = []

    # Check if there are any repeated card values
    repeated = id.repeats(request.session['used_cards'])
    # If there are repeated Values add the hand to completed Hands
    if len(repeated) > 0:
        checked = id.check_repeats(repeated)
        completed_hands.append(checked[0])
        possible_hands.append(checked[1])

    #  Check if there is a flush
    flush = id.flushes(request.session['used_cards'])
    print("Flushes: ", flush)
    # If there is a flush add it to completed hands
    if flush != ([], []):
        checked = id.check_flushes(flush)
        if checked[0] != []:
            completed_hands.append([checked[0][0], checked[0][1]])
        if checked[1] != []:
            possible_hands.append(checked[1])

    # Check for Straights
    straights = id.straights(request.session['used_cards'])
    print("Straights result: ", straights)
    # If there is a Straight add the strongest one to complete hands
    if straights != ([], []):
        checked = id.check_straights(straights)
        if checked[0] != []:
            completed_hands.append([checked[0][0], checked[0][1]])
        if checked[1] != []:
            possible_hands.append(checked[1])

    # Remove None vals from completed and possible hands
    possible_hands = helpers.remove_none(possible_hands)
    completed_hands = helpers.remove_none(completed_hands)

    if completed_hands != []:
        request.session['player_hand'] = helpers.strongest_hand(
            completed_hands)
    print("completed_hands: ", completed_hands)

    # Checking possible hands after the Flop
    if len(request.session['used_cards']) == 5 and possible_hands != [] and helpers.possibly_stronger(completed_hands, possible_hands):
        request.session['possible_hand'] = helpers.flop_odds(possible_hands)

    #  Check the possible hands after the Turn
    elif len(request.session['used_cards']) == 6 and possible_hands != [] and helpers.possibly_stronger(completed_hands, possible_hands):
        request.session['possible_hand'] = helpers.turn_odds(possible_hands)

    elif len(request.session['used_cards']) == 7 and possible_hands != [] and helpers.possibly_stronger(completed_hands, possible_hands):
        request.session['possible_hand'] = "Can Not Predict next card with Table Full."
    else:
        request.session['possible_hand'] = False

    return redirect('/')

# Random Hand
def random_hand(request):
    first_card = helpers.random_card(request.session['used_cards'])
    second_card = helpers.random_card(request.session['used_cards'])

    request.session['used_cards'] = helpers.reset_used_hand(request.session)

    request.session['hand_cards'] = [
        first_card,
        second_card ]
    
    request.session["used_cards"].append(
        first_card)
    request.session["used_cards"].append(
        second_card)
    
    return redirect("/")

# Random Flop
def random_flop(request):
    first_card = helpers.random_card(request.session['used_cards'])
    second_card = helpers.random_card(request.session['used_cards'])
    third_card = helpers.random_card(request.session['used_cards'])
    
    request.session['used_cards'] = helpers.reset_used_flop(request.session)

    request.session['flop_cards'] = [
        first_card,
        second_card,
        third_card
    ]

    request.session["used_cards"].append(
        first_card)
    request.session["used_cards"].append(
        second_card)
    request.session["used_cards"].append(
        third_card)    

    return redirect("/")

# Random Turn
def random_turn(request):
    turn_card = helpers.random_card(request.session['used_cards'])

    request.session['used_cards'] = helpers.reset_used_turn(request.session)    

    request.session['turn_card'] = turn_card

    request.session["used_cards"].append(
        turn_card)

    return redirect("/")

# Random River
def random_river(request):
    river_card = helpers.random_card(request.session['used_cards'])

    request.session['used_cards'] = helpers.reset_used_river(request.session)    

    request.session['river_card'] = river_card

    request.session["used_cards"].append(
        river_card)

    return redirect("/")

