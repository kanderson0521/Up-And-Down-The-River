import random  # used for shuffle

class Player:
    def __init__(self, player_name, position, dealer_ind):
        self.name = player_name
        self.position = position
        self.score = 0
        self.dealer_ind = dealer_ind
        pass


class Card:
    suits = ['\u2666', '\u2665', '\u2663', '\u2660']  # ["Clubs", "Diamonds", "Hearts", "Spades"]
    card_values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    card_value_score = {}  # Create a dict holding the points for the card value
    counter = 2
    for card in card_values:
        card_value_score[card] = counter
        counter += 1

    def __init__(self, suit=0, val=0):
        self.suit = suit
        self.value = val
        self.pts = Card.card_value_score[self.value]

    def __str__(self):
        # str rep of card to print card suit and value to screen
        return f"{self.suit}{self.value}"


class Deck(Card):
    def __init__(self):
        # initialize the deck with 52 cards & shuffle
        self.cards = []
        for suit in Card.suits:
            for val in Card.card_values:
                card = Card(suit, val)
                self.cards.append(card)
        self.shuffle()

    def __str__(self):
        # returns str rep of deck instead of calling to print each card separately
        str_c = []
        for card in self.cards:
            str_c.append(str(card))
        return ' '.join(str_c)

    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)


class Hand(Deck):
    """ Represents the cards in a players hand for each round """
    def __init__(self, player_int):
        self.cards = []
        self.player = player_int
        pass

    def play_card(self, ind):
        # Remove specified card
        del self.cards[ind]
        pass


class GameRound:
    """ Holds actions for each round & stores data from each round """
    def __init__(self, card_count):
        self.card_count = card_count  # aka trick count
        self.dealer_ind = None  # stores the dealer player list ind for that round
        self.dealer_name = None  # used to display the dealer name for that round
        self.trump = None  # stores the round trump card
        self.first_round_player_name = None  # used to display the name of the first round player
        self.player_order = None  # stores player order for playing cards and placing bid in the beginning
        self.player_bids = {}  # saves the trick bids for that trick
        self.played_cards = []  # saves cards played in a trick to calc scores and determine winner, clears every trick
        self.player_trick_wins = {}  # saves player list ind to list of who won that trick
        self.trick_winner_inds = []  # saves player list ind to list of who won that trick,
        # preserves order of wins for finding the order of the next trick
        self.trick_first_player = None  # used to display the name of the winner of the trick
        self.trick_first_player_name = None  # used to display the name of the first to play card
        self.round_winners = []  # stores the winners for each round

    def set_dealer(self, players):
        """ Finds the player index with the dealer indicator equal to 1 and updates round attributes. """
        dealer_index = [index for index, item in enumerate(players) if item.dealer_ind == 1][0]
        self.dealer_ind = dealer_index
        self.dealer_name = players[dealer_index].name
        return

    def set_player_order(self, players):
        """ Set player order for playing cards. If it's the beginning of the round, create order based on starting with
        player after dealer, else the last trick winner."""
        player_indices = [ind for ind, val in enumerate(players)]
        if not len(self.trick_winner_inds) and self.dealer_ind != len(player_indices):
            player_order = player_indices[self.dealer_ind+1:] + player_indices[:self.dealer_ind+1]
        elif not len(self.trick_winner_inds) and self.dealer_ind == len(player_indices):
            player_order = player_indices
        elif len(self.trick_winner_inds):
            max_win_ind = self.trick_winner_inds[-1]
            if max_win_ind == 0:
                player_order = player_indices
            else:
                player_order = player_indices[max_win_ind:] + player_indices[:max_win_ind]
        else:
            player_order = None

        self.player_order = player_order
        return

    def set_up_trick_win_dict(self, players):
        for i, v in enumerate(players):
            self.player_trick_wins[i] = 0
        return

    def create_deal_card_seq(self, players):
        """ Create sequence based on player count and card count to determine index split of deck. """
        seq = []
        total_cards = len(players) * self.card_count  # Total cards needed to take from the deck
        for i in range(len(players)):
            seq.append(str(i))
        seq = seq * round((total_cards / len(players)))
        return total_cards, seq

    def split_deck_by_seq(self, len_players, deck, seq):
        """ Splits deck by sequence created in function above. """
        player_hand_list = []  # Pull cards from deck matching seq index and split into player hands
        for i in range(len_players):
            card_ind_list = [ind for ind, val in enumerate(seq) if int(val) == i]  # get the indices to grab from deck
            card_list = [val for ind, val in enumerate(deck.cards) if ind in card_ind_list]  # grab cards with indices
            player_hand_list.append(card_list)
        return player_hand_list

    def assign_hands(self, player_hands, player_hand_list):
        counter = 0
        for num in self.player_order:
            player_hands[num].cards = player_hand_list[counter]
            counter += 1
        return

    def deal_cards(self, deck, players, player_hands):
        """ Function to call the deck split and dealing methods. Determine deck split based on player count and total
        cards to be dealt then split the deck based on this sequence and then hand out to players based on player
        order. """
        deck.shuffle()
        total_cards, seq = self.create_deal_card_seq(players)  # Get deck split sequence based on card count and players
        player_hand_list = self.split_deck_by_seq(len(players), deck, seq)  # Split deck by seq to make hands
        self.assign_hands(player_hands, player_hand_list)  # Assign hands based on player_order
        self.trump = deck.cards[total_cards].suit  # Show trump suit from top card in leftover deck.
        return self.card_count, players[self.dealer_ind].name, self.trump

    def place_bids(self, players, player_hands):
        """ Each player, in player order, will guess # of tricks they think they will win based on their cards
        & the trump suit. """
        self.first_round_player_name = [player.name for ind, player in enumerate(players) if ind == self.player_order[0]][0]
        input(f"\nTime to place player bids, starting with player {self.first_round_player_name}")
        current_bid_total = 0
        for num in self.player_order:
            current_player = players[num]
            current_hand = player_hands[num]
            print(f"\nBelow are your cards, {current_player.name}")
            print(f"{current_hand}")
            print(f"The trump suit is {self.trump}")
            while True:
                try:
                    bid = int(input("How many tricks do you think you will win?   "))
                except ValueError:
                    print("Enter integer only.")
                else:
                    if num == self.player_order[-1] and bid + current_bid_total == self.card_count:
                        print("Cannot place final bid that equals number of tricks, total bids are {}, "
                              "you cannot bid {}.".format(current_bid_total,
                                                          (self.card_count - current_bid_total)))
                    else:
                        break
            self.player_bids[num] = bid  # Num is the same as Player ind
            current_bid_total += bid
        return

    def check_card_suit_played(self, hand):
        """ Check if player has the suit led in a trick in their hand. A player must follow the suit of the first card
        laid in a trick, if they do not have that suit they can play any card. """
        list_of_suits = [card.suit for card in hand.cards if card.suit == self.played_cards[0].suit]
        if list_of_suits:
            has_suit_ind = 1
        else:
            has_suit_ind = 0
        return has_suit_ind

    def play_hands(self, players, player_hands):
        """ Iterate through players, show their hand and ask them what card to play by selecting the number next to
         their card """
        # Have the play_game function iterate through the players and figure this out then
        self.trick_first_player_name = players[self.player_order[0]].name
        print(f"Player {self.trick_first_player_name} will go first.\n")
        for num in self.player_order:
            if num == self.player_order[0]:
                print("----------------------------------------- ")
            else:
                print("\n-------------- Next Player -------------- ")
            current_player = players[num]
            current_hand = player_hands[num]
            print(f"\n{current_player.name}, here are your cards:")
            for i in range(len(current_hand)):
                print(f"{i+1}: {current_hand.cards[i]}")
            if num != self.player_order[0]:
                if len(self.played_cards) > 1:
                    played_cards_str = [str(card) for card in self.played_cards]
                    played_cards_str = ' '.join(played_cards_str)
                    print(f"Here are the cards other players have played: {played_cards_str}")
                else:
                    print(f"Here are the cards other players have played: {self.played_cards[0]}  ")
            print(f"The trump suit is {self.trump}. Your bid: {self.player_bids[num]}. Your wins: "
                  f"{self.player_trick_wins[num]}. ")
            # Catch errors for incorrect card choices and must match first player suit if they have one on hand.
            while True:
                try:
                    # Changed index to start at 1 instead of 0 for better UX, will need to convert back later
                    play_card = int(input("Which card would you like to play? "
                                          "Please enter the number next to your card.   "))
                except ValueError:
                    print("Enter integer only. You must type the number next to the card you want to play.")
                else:
                    if play_card < 1 or play_card > len(current_hand.cards):  # Less than the len of their hand + 1
                        print("You must type the number next to the card you want to play.")
                    elif len(self.played_cards) and current_hand.cards[play_card - 1].suit != self.played_cards[0].suit \
                            and self.check_card_suit_played(current_hand) == 1:
                        print(f"You must play a card with the {self.played_cards[0].suit} suit.")
                    else:
                        break
            play_card_index = play_card - 1  # Convert back to index num
            play_card = current_hand.cards[play_card_index]  # Str rep of card to display to other players
            current_hand.play_card(play_card_index)  # Remove played card from their hand
            self.played_cards.append(play_card)
        return

    def card_pts_val(self, first_played_suit, card):
        """ Calculates the points by each card in trick. If suit is trump, add 100 points plus the card pts value.
         If the card suit is not trump or matching the suit of the first card played, it will have a score of 0 since
         it cannot win. """
        pts = 0
        if card.suit == self.trump:
            pts += 100
        if card.suit == first_played_suit or card.suit == self.trump:
            pts += card.pts
        elif card.suit != first_played_suit and card.suit != self.trump:
            pts = 0
        return pts

    def find_trick_winner(self, players):
        """ Finds the winner of the trick and appends their index to the trick_winner_ind list for the round """
        first_card_played_suit = self.played_cards[0].suit
        card_scores = []
        for card in self.played_cards:
            pts = self.card_pts_val(first_card_played_suit, card)
            card_scores.append(pts)

        # Determine highest score and find the player with that score
        max_score = max(card_scores)
        winner_ind = [ind for ind, val in enumerate(card_scores) if val == max_score][0]
        players_list_ind = self.player_order[winner_ind]  # Convert from player order to player index
        player_winner_name = players[players_list_ind].name
        self.player_trick_wins[players_list_ind] += 1
        self.trick_winner_inds.append(players_list_ind)
        return player_winner_name

    def find_round_winners(self, players):
        """ Finds the winners based on bid placed and tricks won at the end of a round. """
        print('\nCalculating this rounds winners...')
        for ind, player in enumerate(players):
            wins = self.player_trick_wins[ind]  # Get player win count
            bid = self.player_bids[ind]  # Get player bid
            if wins == bid:
                score = wins + 10
                player.score += score
                self.round_winners.append(ind)
        winner_names = [player.name for ind, player in enumerate(players) if ind in self.round_winners]
        return winner_names

    def clear_played_cards(self):
        """ Clear the played card list for the next trick. """
        self.played_cards = []
        return

    def update_dealer_ind(self, players):
        """ Sets the next dealer for the new round, changes previous dealer's ind to 0. """
        dealer_ind = [index for index, item in enumerate(players) if item.dealer_ind == 1][0]
        players[dealer_ind].dealer_ind = 0  # Reset last dealers ind to 0
        if dealer_ind == (len(players)-1):
            new_dealer_ind = 0
        else:
            new_dealer_ind = dealer_ind + 1
        players[new_dealer_ind].dealer_ind = 1  # Set the new dealer's indicator
        return
