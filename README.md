# Monte Carlo Poker Equity Simulator

Estimates your Texas Hold'em hand equity against multiple opponents using Monte Carlo simulation, then turns it into a decision with pot odds, expected value and Kelly-criterion bet sizing.

## How it works
- Opponents are modelled by player type: tight (15%), TAG (25%), LAG (40%), whale (60%) of starting hands.
- Each iteration deals opponent hands first, then completes the board, accounting for card removal and split pots.
- Works on any street: preflop, flop, turn or river.

## Example
```
Your hand: [K♣],[T♣]
Flop: [Q♠],[K♦],[2♣]
With 2 opponents (Opponents: `opponent_types = [3, 4]` (one LAG, one whale), pot = 1000, call = 100):
Flop odds are: 65.76 %
Optimal Bankroll Bet (Kelly): 62.34 %
Pot odds: 9.09 % -> CALL
Expected Value (EV): 623.38
```

**Validation:** AA vs KK preflop gives ≈ 82% equity, matching the known value.

## Usage
```
pip install -r requirements.txt
python3 poker_equity.py
```
Set your hand, board cards, pot, call and opponent types in the variables section.

## Work in progress/ Future work
- Convergence plot (law of large numbers): running equity estimate vs. number of iterations
- CLT plot: histogram of equity estimates from many repeated 10,000-iteration runs
- Input validation (wrong hand size, duplicate cards)
- Position-aware ranges
- Game-theory-based bet sizing

## Credits
Hand evaluation uses [treys](https://github.com/ihendley/treys) (MIT License).