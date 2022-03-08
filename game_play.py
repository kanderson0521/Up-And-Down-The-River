import random  # used for random selection for first dealer
import game_objects as go  # import game classes

# Define global vars (lists to hold the game objects)
players = []
player_hands = []
rounds = []


def find_overall_winner():
    """ Finds the winner(s) at the end of the last round/end of game. Could create an overall game class to share
    objects and place this in as a game method. """
    # Get the max score and find all players with that score.
    max_score = max([player.score for player in players])
    overall_winners = [player.name for player in players if player.score == max_score]
    return overall_winners


def play_game():
    """ Iterate through each round object and prompt users to play the game """
    global players, player_hands, rounds
    deck = go.Deck()

    for ind, game_round in enumerate(rounds):
        if ind != 0:
            game_round.update_dealer_ind(players)  # First round dealer already chosen during setup
            print("The next round will begin.")
        game_round.set_dealer(players)
        game_round.set_up_trick_win_dict(players)
        game_round.set_player_order(players)
        round_card_count,dealer_name,round_trump  = game_round.deal_cards(deck, players, player_hands)
        print(f"\nTotal number of tricks for this round: {round_card_count}, the dealer is: "
              f"{dealer_name}.")
        input("Deck has been shuffled, press the Enter key to deal cards.")
        print(f"The trump suit for this round is {round_trump}")
        input("Press Enter to continue")
        print("The cards have been dealt.\n")
        game_round.place_bids(players, player_hands)
        print(f"Bids have been placed, there are {game_round.card_count} total tricks this round, try to win as many "
              f"tricks that you bid. Let's play!!!   ")
        for tricks in range(game_round.card_count):
            game_round.play_hands(players, player_hands)
            trick_winner = game_round.find_trick_winner(players)
            print(f"\nThe winner for this trick is {trick_winner}")
            game_round.set_player_order(players)
            game_round.clear_played_cards()
        round_winners = game_round.find_round_winners(players)
        if round_winners:
            print(f"The winner(s) for this round: {', '.join(round_winners)}")
        else:
            print("There were no winners for this round.")
    return


def setup_game():
    """ Game setup: grab player count and names. Determine number of tricks & rounds. Create game objects. """
    # set global variables
    global players, player_hands, rounds

    # get number of players
    while True:
        try:
            num_players = int(input("How many players? (3-7 only):   "))
        except ValueError:
            print("Enter integer only.")
        else:
            if 3 <= num_players <= 7:
                break
            else:
                print("Value out of range.")

    # Choose first dealer by random.
    dealer = random.randint(0, (num_players-1))

    # Create number of max cards for each hand based on num_players
    max_num_cards = None
    if num_players < 6:
        max_num_cards = 10
    elif num_players == 6:
        max_num_cards = 8
    elif num_players == 7:
        max_num_cards = 7

    # Create round objects and set the card deal count for each round (start at max -> 2 and back up)
    down_list = list(range(2, max_num_cards + 1))
    down_list.reverse()  # Returns None, must put after assignment
    up_list = list(range(3, max_num_cards + 1))
    deal_card_count_seq = down_list + up_list

    for num in deal_card_count_seq:
        rounds.append(go.GameRound(card_count=num))

    # Create object for each player and player hand after getting player name
    print("Enter player names, order of input determines position. Dealer will be randomly chosen.")
    for i in range(num_players):
        name = input("Enter player name:   ")
        position = i
        if position == dealer:
            dealer_ind = 1
        else:
            dealer_ind = 0
        # create player obj & add to players list
        p = go.Player(name, position, dealer_ind)
        players.append(p)
        # create player hand obj & add to hand list
        h = go.Hand(p.position)
        player_hands.append(h)
    return


if __name__ == '__main__':
    # Game rules found here: https://www.pagat.com/exact/ohhell.html
    view_rules = input("Would you like to see the game rules? (Y/N)   ")
    if view_rules in ("Y", "y"):
        with open('Rules.txt') as f:
            lines = f.read()
            print(lines)

    setup_game()
    play_game()
    winners = find_overall_winner()
    print(f"The winner(s) of the game: {', '.join(winners)} \nGame over...")
