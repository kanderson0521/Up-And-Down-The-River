import pytest
import game_objects as go


"""
def test_player_list_creation(created_players, players):
    # A test to learn how to create objects
    player_list = created_players
    for player in player_list:
        assert player.name != 'Kelly'
    #assert len(players) == 5
"""


def test_deck(deck):
    """ Test deck was initialized correctly. """
    assert len(deck.cards) == 52  # Test for length
    assert len(deck.cards) == len(set(deck.cards))  # Test for no duplicate cards
    suit_counts = {}
    for card in deck.cards:
        if card.suit in suit_counts.keys():
            suit_counts[card.suit] += 1
        else:
            suit_counts[card.suit] = 1
    # ['\u2666', '\u2665', '\u2663', '\u2660']  -->  ["Clubs", "Diamonds", "Hearts", "Spades"]
    club = '\u2666'
    diamond = '\u2665'
    heart = '\u2663'
    spade = '\u2660'
    # Test for equal number of cards per suit
    assert suit_counts[club] == 13
    assert suit_counts[diamond] == 13
    assert suit_counts[heart] == 13
    assert suit_counts[spade] == 13


# Test card sequence used to deal cards for each round.
def test_create_deal_card_seq(created_players, players, created_round):
    """ Create players in length of 5, 6, and 7. Results should be 10 cards for 3-5, 8 cards for 6, and
    7 cards for 7."""
    correct_card_seq = {5: (['0', '1', '2', '3', '4'] * 5),
                        6: (['0', '1', '2', '3', '4', '5'] * 5),
                        7: (['0', '1', '2', '3', '4', '5', '6'] * 5)}  # Define correct values for card count = 5
    players_list = created_players  # Create players, returns a list of player objects
    game_round = created_round  # Create game round
    num_players = len(players_list)
    if num_players <= 5:
        total_cards, seq = go.GameRound.create_deal_card_seq(game_round, players_list)
        assert total_cards == 25
        assert seq == correct_card_seq[5]
    elif num_players == 6:
        total_cards, seq = go.GameRound.create_deal_card_seq(game_round, players_list)
        assert total_cards == 30
        assert seq == correct_card_seq[6]
    elif num_players == 7:
        total_cards, seq = go.GameRound.create_deal_card_seq(game_round, players_list)
        assert total_cards == 35
        assert seq == correct_card_seq[7]
    return


# Test scoring for each trick
def test_calc_trick_scores(card, created_round):
    """ Tests the scoring based on card suit and value. """
    # Define trump suit
    trump_suit = '\u2663'  # Hearts
    game_round = created_round  # Create a round obj to send to check pts val method
    game_round.trump = trump_suit
    first_played_card_suit = '\u2665'  # Diamond
    pts = []
    for card in card:
        pts.append(go.GameRound.card_pts_val(game_round, first_played_card_suit, card))
    assert pts[0] == 9  # 9 diamonds
    assert pts[1] == 102  # 2 hearts
    assert pts[2] == 0  # Ace clubs
    return


# Change dealer works correctly and goes in order from players list.
def test_change_dealer():

    return
