#Author - Gurshmeer Singh

import random


class Card:
 #initiating the class
 Suits = {'C': 0, 'D': 1, 'H': 2, 'S': 3}
 Ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

 def __init__(self, rank,suit):
  if rank not in self.Ranks or suit not in self.Suits:
   raise ValueError("Invalid rank or suit")
  self.rank = rank
  self.suit = suit

 def get_rank(self):
  return self.rank
 def get_suit(self):
  return self.suit

 def __repr__(self):
  return f"Card(rank='{self.rank}',suit='{self.suit}')"

 def __str__(self):
  return self.__repr__()

 def __eq__(self, other):
  #comparing the cards to each other
  return self.rank == other.rank and self.suit == other.suit

 def __lt__(self, other):
   if self.rank == other.rank:
    return self.Suits[self.suit] < self.Suits[other.suit]
   return self.Ranks[self.rank] < self.Ranks[other.rank]

 def __le__(self, other):
   return self.__lt__(other) or self.__eq__(other)

 def __gt__(self, other):
   return not self.__le__(other)

 def __ge__(self, other):
   return not self.__lt__(other)

 def __ne__(self, other):
   return not self.__eq__(other)


class Deck :
 def __init__(self):
  Suits = {'C': 0, 'D': 1, 'H': 2, 'S': 3}
  Ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

  self.cards = []
  for rank in Ranks:
     for suit in Suits:
      self.cards.append(Card(rank,suit))

 def __len__(self):
        return len(self.cards)

 def __repr__(self):
        return f"Deck({self.cards})"

 def __str__(self):
  deck = ''
  for card in self.cards:
   deck += str(card) + ','
  return deck
 def shuffle(self):

       random.shuffle(self.cards)
 def draw(self):
       if self.cards :
        return self.cards.pop(0)


class Pile:
 def __init__(self,cards=None):
  if cards is None:
   cards = []
  self.cards = cards
 def draw_card(self):
  if self.cards :
       return self.cards.pop(0)
  else:
     return None
 def add_cards(self,cards):
  if type(cards) != list:
   cards = [cards]
  self.cards += cards
 def pile_size(self):
  return len(self.cards)
 def find_highest(self):
  highest = None
  for card in self.cards:
   if highest is None or card> highest:
    highest = card
  return highest

 def most_common_suit(self):
  suit_counts = {}
  for card in self.cards:
   suit_counts[card.suit] = suit_counts.get(card.suit,0) +1
  max_count = 0
  most_common = None
  for suit, count in suit_counts.items():
   if count > max_count:
    max_count = count
    most_common = suit
   elif count == max_count:
    most_common = None
  return most_common

 def get_pile(self):
  return self.cards

 def __str__(self):
  pile = ''
  for card in self.cards:
   pile += str(card) + ','
  return pile


class Game:
  def __init__(self):
   deck = Deck()
   deck.shuffle()
   self.player_draw_pile = Pile(deck.cards[:26])
   self.computer_draw_pile = Pile(deck.cards[26:])
   self.player_win_pile = Pile()
   self.computer_win_pile = Pile()
   self.peace_offerings = {'p':0,'c':0}
  def start_game(self,rounds):
   for i in range (rounds):
    if not self.player_draw_pile.pile_size() or not self.computer_draw_pile.pile_size():
     break
    p_card = self.player_draw_pile.draw_card()
    computer_card = self.computer_draw_pile.draw_card()
    print(f"Player plays {p_card}, Computer plays {computer_card}")

    if p_card > computer_card:
     self.player_win_pile.add_cards([p_card, computer_card])
    elif p_card < computer_card:
     self.computer_win_pile.add_cards([p_card, computer_card])
    else:
     self.go_to_war([p_card, computer_card])
  def go_to_war(self, pot):
   if self.player_draw_pile.pile_size() < 4 or self.computer_draw_pile.pile_size() < 4:
    return

   for x in range(3):  # Burn three cards
    pot.append(self.player_draw_pile.draw_card())
    pot.append(self.computer_draw_pile.draw_card())

   player_faceoff = self.player_draw_pile.draw_card()
   computer_faceoff = self.computer_draw_pile.draw_card()
   pot.extend([player_faceoff, computer_faceoff])
   if player_faceoff > computer_faceoff:
    self.player_win_pile.add_cards(pot)
   elif computer_faceoff > player_faceoff:
    self.computer_win_pile.add_cards(pot)
   else:
    self.go_to_war(pot)

  def print_winner(self):
   # Determine the winner
   if len(self.player_win_pile.cards) > len(self.computer_win_pile.cards):
    print("Player wins!")
    return "p"  # Player wins
   elif len(self.computer_win_pile.cards) > len(self.player_win_pile.cards):
    print("Computer wins!")
    return "c"  # Computer wins
   else:
     print("It's a tie!")
     return "t"  # Tie

  def summary(self, result):
   print(f"Game Over! Winner: {'Player' if result == 'p' else 'Computer' if result == 'c' else 'Tie'}")
   print(f"Peace offerings - Player: {self.peace_offerings['p']}, Computer: {self.peace_offerings['c']}")
   print(f"Player's highest card: {self.player_win_pile.find_highest()}")
   print(f"Player's most common suit: {self.player_win_pile.most_common_suit()}")
   print(f"Player's win pile: {self.player_win_pile}")
	

if __name__ == "__main__":
    game = Game()
    game.start_game(26)
    result = game.print_winner()
    game.summary(result)