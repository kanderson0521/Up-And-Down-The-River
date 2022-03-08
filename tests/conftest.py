import pytest
import game_objects as go


# Define fixtures
@pytest.fixture
def players():
    """ Player factory to create multiple player objects """
    class PlayerFactory:
        def get(self, name, position, dealer_ind):
            player = go.Player(name, position, dealer_ind)
            return player
    return PlayerFactory()


@pytest.fixture(params=[5, 6, 7])
def created_players(players, request):
    """ Used to create dummy players using Player factory """
    player_list = []
    names = ['red', 'aram', 'dembe', 'mr kaplan', 'liz', 'dom', 'tom', 'samar']
    for i in range(request.param):
        player = players.get(name=names[i], position=i, dealer_ind=0)
        player_list.append(player)
    return player_list


@pytest.fixture(params=[5])
def created_round(request):
    """ Used to create dummy round objects """
    num_cards = request.param  # Create the card count as 5
    game_round = go.GameRound(card_count=num_cards)
    return game_round


@pytest.fixture()
def deck():
    deck = go.Deck()
    return deck


@pytest.fixture
def rounds():
    game_rounds = []
    return game_rounds


@pytest.fixture
def card():
    card_examples = ['\u26659', '\u26632', '\u2666A']
    cards = []
    for c in card_examples:
        card = go.Card(c[0], c[1])
        cards.append(card)
    return cards
