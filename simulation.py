import random

def betting_simulation(starting_bet, max_bets):
    money = 0
    bet = starting_bet
    wins = 0
    losses = 0
    
    for i in range(max_bets):
        result = random.choices([0, 1], weights=[2/3, 1/3])[0]
        
        if result == 1:
            money += bet
            wins += 1
            bet = starting_bet
        else:
            money -= bet
            losses += 1
            bet *= 3
        
        if money <= 0:
            break
        
    win_rate = wins / (wins + losses)
    
    return win_rate

win_rate = betting_simulation(0.10, 10000)
print("Win rate after 10000 bets:", win_rate)