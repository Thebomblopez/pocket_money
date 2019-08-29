from django.shortcuts import HttpResponse, redirect, render
import apps.poker_app.helpers as helpers 
import apps.poker_app.iDent as id
from django.contrib import messages

# Create your views here.
# Hand Calculator page
def index(request):
    # request.session.flush()
    request.session["hand_cards"] = helpers.ishand(request.session)
    request.session["used_cards"] = helpers.is_used(request.session)
    request.session["flop_cards"] = helpers.is_flop(request.session)
    request.session["turn_card"] = helpers.is_turn(request.session)
    request.session["river_card"] = helpers.is_river(request.session)
    print(request.session["used_cards"])

    return render(request, 'poker_app/hand_calculator.html', request.session)

# Add Hand cards to session 
def submit_hand_cards(request):
    if helpers.is_duplicate_hand(request.POST, request.session['used_cards']):
        messages.error(request, 'Card used more than once or missing cards.')
        return redirect("/")

    request.session['used_cards'] = helpers.reset_used_hand(request.session)
    
    request.session['hand_cards'] = [
        [ request.POST['first_card_value'], request.POST['first_card_suit'] ],
        [ request.POST['second_card_value'], request.POST['second_card_suit'] ]
    ]
    
    request.session["used_cards"].append([ request.POST['first_card_value'], request.POST['first_card_suit'] ])
    request.session["used_cards"].append([ request.POST['second_card_value'], request.POST['second_card_suit'] ])

    return redirect('/')

# Add Flop cards to session
def submit_flopcards(request):
    if helpers.is_duplicate_flop(request.POST, request.session['used_cards']):
        messages.error(request, 'Card used more than once or missing cards.')
        return redirect("/")

    request.session['used_cards'] = helpers.reset_used_flop(request.session)
    
    request.session['flop_cards'] = [
        [ request.POST['first_card_value'], request.POST['first_card_suit'] ],
        [ request.POST['second_card_value'], request.POST['second_card_suit'] ],
        [ request.POST['third_card_value'], request.POST['third_card_suit'] ]
    ]

    request.session["used_cards"].append([ request.POST['first_card_value'], request.POST['first_card_suit'] ])
    request.session["used_cards"].append([ request.POST['second_card_value'], request.POST['second_card_suit'] ])
    request.session["used_cards"].append([ request.POST['third_card_value'], request.POST['third_card_suit'] ])
    
    return redirect('/')

# Add Turn Card to session
def submit_turn_card(request):
    if helpers.is_duplicate_turn(request.POST, request.session['used_cards']):
        messages.error(request, 'Card used more than once or missing cards.')
        return redirect("/")

    request.session['used_cards'] = helpers.reset_used_turn(request.session)

    request.session['turn_card'] = [ request.POST['turn_card_value'], request.POST['turn_card_suit'] ]
    request.session["used_cards"].append([ request.POST['turn_card_value'], request.POST['turn_card_suit'] ])
    
    return redirect('/')

# Add River Card to session
def submit_river_card(request):
    if helpers.is_duplicate_river(request.POST, request.session['used_cards']):
        messages.error(request, 'Card used more than once or missing cards.')
        return redirect("/")

    request.session['used_cards'] = helpers.reset_used_river(request.session)

    request.session['river_card'] = [ request.POST['river_card_value'], request.POST['river_card_suit'] ]
    request.session["used_cards"].append([ request.POST['river_card_value'], request.POST['river_card_suit'] ])

    return redirect('/')

# Calculate Hand
def calculate_hand(request):
    # print(request.session['used_cards'])
    repeated = id.value_repeats(request.session['used_cards'])
    print(repeated)
    print(id.check_card_repeats(repeated))
    
    # print("check_flush",id.check_flush(request.session['used_cards']))
    # print("check_straights",id.check_straights(request.session['used_cards']))

    return redirect('/')






