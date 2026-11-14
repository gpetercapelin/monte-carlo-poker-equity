# Validation: AA vs KK preflop should give ~82% equity for AA
# Same Monte Carlo logic as poker_equity.py, simplified to one fixed opponent hand.
import random
from treys import Evaluator, Deck, Card

evaluator = Evaluator()

hand = [Card.new("As"), Card.new("Ah")]
opp_hand = [Card.new("Ks"), Card.new("Kh")]

record_results = []
for i in range(10000):
    deck = Deck()
    for card in hand + opp_hand:
        deck.cards.remove(card)

    board = deck.draw(5)
    my_score = evaluator.evaluate(board, hand)
    opp_score = evaluator.evaluate(board, opp_hand)

    if my_score < opp_score:
        record_results.append(1)
    elif my_score > opp_score:
        record_results.append(0)
    else:
        record_results.append(0.5)

equity = sum(record_results) / len(record_results)
print(f"AA vs KK preflop equity: {equity*100:.2f} % (expected ~82 %)")