#Monte Carlo poker equity simulator, with pot odds, EV and Kelly Criterion
import random
import itertools
import numpy as np
from treys import Evaluator, Deck, Card

evaluator = Evaluator()

#OPPONENT RANGES (built with AI assistance)
suits = 'shdc'

def pairs(ranks):
    return [[Card.new(r+s1), Card.new(r+s2)] for r in ranks.split() for s1, s2 in itertools.combinations(suits, 2)]

def suited(combos):
    return [[Card.new(c[0]+s), Card.new(c[1]+s)] for c in combos.split() for s in suits]

def offsuit(combos):
    return [[Card.new(c[0]+s1), Card.new(c[1]+s2)] for c in combos.split() for s1 in suits for s2 in suits if s1 != s2]

# 1. Tight (15%)
top_15 = pairs("A K Q J T 9 8 7") + \
         suited("AK AQ AJ AT A9 A8 A7 KQ KJ KT K9 QJ QT JT") + \
         offsuit("AK AQ AJ AT KQ KJ KT QJ")

# 2. TAG (25%)
top_25 = top_15 + \
         pairs("6 5") + \
         suited("A6 A5 A4 A3 A2 K8 K7 Q9 Q8 J9 J8 T9 T8 98") + \
         offsuit("QT JT")

# 3. LAG (40%)
top_40 = top_25 + \
         pairs("4 3 2") + \
         suited("Q7 Q6 Q5 J7 T7 97 96 87 86 76 75 65 54") + \
         offsuit("A9 A8 K9 Q9 J9 T9")

# 4. Whale (60%)
top_60 = top_40 + \
         suited("K6 K5 K4 K3 K2 Q4 Q3 Q2 J6 J5 J4 J3 J2 T6 T5 T4 95 85 84 74 64 53 43") + \
         offsuit("A7 A6 A5 A4 A3 A2 K8 K7 K6 K5 Q8 Q7 J8 J7 T8 T7 98 97 87")

ranges = [top_15, top_25, top_40, top_60]


#VARIABLES
hand = [
    Card.new("Kc"),
    Card.new("Tc")
]

#board cards already dealt: 0 = preflop, 3 = flop, 4 = turn, 5 = river
dealt_cards = [
    Card.new("Qs"),
    Card.new("Kd"),
    Card.new("2c")
]

pot = 1000

call = 100

#types:
# 1: tight. top 15% hands
# 2: tight-aggressive (TAG) standard. top 25% hands
# 3: loose-aggressive (LAG). top 40% hands
# 4: whale. top 60% hands
opponent_types = [3, 4]
#just add the number of each opponent's personality, and that takes into account how many opponents there are


print("Your hand:")
Card.print_pretty_cards(hand)

playing_position = ""
if len(dealt_cards) == 0:
    playing_position = "Preflop"
elif len(dealt_cards) == 3:
    playing_position = "Flop"
elif len(dealt_cards) == 4:
    playing_position = "Turn"
elif len(dealt_cards) == 5:
    playing_position = "River"


#MONTE CARLO SIMULATION
record_results = []
for i in range(10000):
    deck = Deck()
    for card in hand:
        deck.cards.remove(card)
    for card in dealt_cards:
        deck.cards.remove(card)

    #1. deal the opponents FIRST (real order: their cards are dealt preflop, before the board)
    opp_hands = []
    for current_type in opponent_types:
        opp_range = ranges[current_type-1]

        available_hands = []
        for h in opp_range:
            # h[0] is the first card, h[1] is the second card
            if h[0] in deck.cards and h[1] in deck.cards:
                available_hands.append(h)

        opp_hand = random.choice(available_hands)
        #take their cards out of the deck, so no other opponent or the board can get them
        for card in opp_hand:
            deck.cards.remove(card)
        opp_hands.append(opp_hand)

    #2. THEN complete the board with what is left
    board = dealt_cards + deck.draw(5-len(dealt_cards))

    #3. compare, evaluating our hand only once
    #LOWER SCORE, stronger hand
    my_score = evaluator.evaluate(board, hand)
    opp_scores = [evaluator.evaluate(board, opp_hand) for opp_hand in opp_hands]
    best_opp = min(opp_scores)

    if my_score < best_opp:
        winstatus = 1
    elif my_score > best_opp:
        winstatus = 0
    else:
        #split pot: 1 opponent ties -> 1/2, 2 opponents tie -> 1/3, etc.
        ties = opp_scores.count(my_score)
        winstatus = 1/(ties+1)

    record_results.append(winstatus)

average_wins = np.average(record_results)

print(f"{playing_position}")
Card.print_pretty_cards(dealt_cards)
print(f"With {len(opponent_types)} opponents, your {playing_position} odds are: {average_wins*100:.2f} %")


#KELLY CRITERION, EV AND POT ODDS
b = pot/call
p = average_wins
q = 1 - p

kelly_fraction = (b * p - q) / b
#if negative, do not bet (set to 0)
kelly_fraction = max(0, kelly_fraction)

EV = average_wins*pot - (1-average_wins)*call

pot_odds = call/(pot+call)

#pot odds = the p where EV is zero. If our equity p is higher than the pot odds,
#Kelly is positive (> 0) and we should bet.
#Kelly then gives the percentage of our stack to bet.
print(f"Optimal Bankroll Bet (Kelly): {kelly_fraction * 100:.2f} %")
print(f"Pot odds: {pot_odds*100:.2f} % -> {'CALL' if average_wins > pot_odds else 'FOLD'}")
print(f"Expected Value (EV): {EV:.2f}")