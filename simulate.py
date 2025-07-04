#some vibecoded bot to check some values
import time
from unittest.mock import patch
from games_and_tools import blackjack, googol

def clear_terminal():
    # \033[H setzt den Cursor oben links, \033[J löscht bis zum Ende
    print("\033[H\033[J", end="")
def run_simulation(rounds=100):
    start = time.time()
    """Run blackjack simulation for a given number of rounds and report stats"""
    wins = losses = ties = 0
    total_change = 0
    for i in range(1, rounds + 1):
        print(f"Runde {i} von {rounds}", end='\r')
        clear_terminal()
        # set fixed bet
        blackjack.bet = 10
        # record money before
        money_before = int(googol.display_money_value())

        # bot input logic
        def smart_input(prompt=""):
            prompt_lower = prompt.lower()
            # hit/stand decision
            if "hit" in prompt_lower and "stand" in prompt_lower:
                # get current scores
                player_score = blackjack.count_best_hand("player_1")
                upcard = blackjack.extract_card_value(blackjack.hand_dealer[0])
                # convert dealer upcard to numeric value
                if upcard == "A":
                    dealer_value = 11
                elif upcard in ("K", "Q", "J"):
                    dealer_value = 10
                else:
                    dealer_value = int(upcard)
                # basic strategy
                if player_score <= 11:
                    return 'h'
                elif player_score == 12:
                    return 'h' if dealer_value >= 7 else 's'
                elif player_score <= 16:
                    return 'h' if dealer_value >= 7 else 's'
                else:
                    return 's'
            # default Enter for all other prompts
            return ""

        # run one round with patched input and no sleep delays
        with patch('builtins.input', smart_input), patch('time.sleep', lambda x: None):
            blackjack.main_blackjack_classic()

        # record money after
        money_after = int(googol.display_money_value())
        change = money_after - money_before
        total_change += change
        if change > 0:
            wins += 1
        elif change < 0:
            losses += 1
        else:
            ties += 1
    
    # calculate expected value
    expected_value = total_change / rounds
    duration = time.time() - start
    # print summary
    print(f"Simulation complete: {rounds} rounds")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Ties: {ties}")
    print(f"Erwartungswert: {expected_value:.4f}")
    print(f"Total Money Change: {total_change}")
    print(f'duration: {duration}')


if __name__ == "__main__":
    x = int(input("Wie viel runs?:"))
    run_simulation(x)