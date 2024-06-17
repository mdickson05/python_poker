# Pick the best hand(s) from a list of poker hands.
from pathlib import Path
class Card:
	def __init__(self, suit, num):
		self.suit = suit
		self.num = num
		self.num_rank = 0
		self.suit_rank = 0
	def __str__(self):
		return str(self.num) + str(self.suit)
	def __iter__(self):
		yield self.suit
		yield self.rank
	def get_suit(self):
		return self.suit
	def get_num(self):
		return self.num
	def get_num_rank(self):
		return self.num_rank
	def get_suit_rank(self):
		return self.suit_rank
	def set_num_rank(self, in_rank):
		self.num_rank = in_rank
	def set_suit_rank(self, in_rank):
		self.suit_rank = in_rank
	def find_num_rank(self):
		ranking = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
		num = self.get_num()
		rank = ranking.index(num)
		self.set_num_rank(rank)
	def find_suit_rank(self):
		ranking = ['s', 'h', 'd', 'c']
		suit = self.get_suit()
		rank = ranking.index(suit)
		self.set_suit_rank(rank)
class Hand:
	def __init__(self, cards):
		self.hand = cards
		self.rank_list = []
		self.suit_list = []
	def __iter__(self):
		return iter(self.hand)
	def __str__(self):
		hands = []
		for card in self.hand:
			hands.append(card.get_num() + card.get_suit())
		return ' '.join(hands)
	def get_hand(self):
		return self.hand
	def get_rank_list(self):
		return self.rank_list
	def get_suit_list(self):
		return self.suit_list
	def set_rank_list(self, in_list):
		self.rank_list = in_list
	def set_suit_list(self, in_list):
		self.suit_list = in_list
	def sort_by_rank(self):
		cards = self.get_hand()
		cards.sort(key=lambda card: card.num_rank)
		# sorted_hand = ';'.join(sorted_cards)
		self.set_rank_list(cards)
	def sort_by_suit(self):
		cards = self.get_hand()
		cards.sort(key=lambda card: card.get_suit_rank())
		self.set_suit_list(cards)
	def has_high_card(self):
		high_card = False
		ranks = self.get_rank_list()
		highest_rank = ranks[4]
		if 9 <= highest_rank <= 12: # i.e. if rank is between JACK and ACE 
			high_card = True
		return high_card
	def is_flush(self):
		flush = False
		cards = self.get_suit_list()
		lowest_suit = cards[0]
		highest_suit = cards[4]
		if lowest_suit == highest_suit:
			flush = True
		return flush
	def is_straight(self):
		cards = self.get_rank_list()
		straight = False
		highest_rank = cards[len(cards) - 1] # already sorted; last element = highest rank
		if highest_rank == 12: # i.e. highest_rank is an ACE
			# ACE wraps around; needs to be considered
			rank_list = []
			for card in cards:
				rank = card.get_num_rank(card)
				rank_list.append(rank)
			if 8 in rank_list and 9 in rank_list and 10 in rank_list and 11 in rank_list:
				# i.e. if T, J, Q and K appear
				straight = True
			elif 0 in rank_list and 1 in rank_list and 2 in rank_list and 3 in rank_list:
				# i.e. if 2,3,4 and 5 appear
				straight = True
		else:
			straight = self.walk(cards)
		return straight
	def is_four_of_a_kind(self):
		cards = self.get_rank_list()
		# get rank @ position
		first = cards[0].get_num_rank()
		second = cards[1].get_num_rank()
		third = cards[2].get_num_rank()
		fourth = cards[3].get_num_rank()
		fifth = cards[4].get_num_rank()
		# check for x x x x y
		x_first = first == second == third == fourth
		# check for y x x x x 
		x_last = second == third == fourth == fifth
		# OR operator: only returns False if both elements are false, else True
		return x_first or x_last
	def is_full_house(self):
		cards = self.get_rank_list()
		# get rank @ position
		first = cards[0].get_num_rank()
		second = cards[1].get_num_rank()
		third = cards[2].get_num_rank()
		fourth = cards[3].get_num_rank()
		fifth = cards[4].get_num_rank()
		# check for x x x y y
		three_x = first == second and second == third and fourth == fifth
		# check for x x y y y
		three_y = first == second and third == fourth and fourth == fifth
		# OR operator: only returns False if both elements are false, else True
		return three_x or three_y

	def is_three_of_a_kind(self):
		cards = self.get_rank_list()
		three_of_kind = True
		if self.is_four_of_a_kind() or self.is_full_house():
		# if we check for self first, we can rule out some combinations for further tests
			three_of_kind = False
		else:
			# get rank @ position
			first = cards[0].get_num_rank()
			second = cards[1].get_num_rank()
			third = cards[2].get_num_rank()
			fourth = cards[3].get_num_rank()
			fifth = cards[4].get_num_rank()
			# check x x x a b
			front = first == second and second == third 
			# check a x x x b
			middle = second == third and third == fourth
			# check a b x x x
			back = third == fourth and fourth == fifth

			if front or middle or back:
				three_of_kind = True
			else:
				three_of_kind = False
		return three_of_kind
	def is_two_pair(self):
		cards = self.get_rank_list()
		two_pair = True
		if self.is_four_of_kind() or self.is_full_house() or self.is_three_of_a_kind():
		# same principle as three of kind: check for these first to rule out combinations
			two_pair = False
		else:	
			# get rank @ position
			first = cards[0].get_num_rank()
			second = cards[1].get_num_rank()
			third = cards[2].get_num_rank()
			fourth = cards[3].get_num_rank()
			fifth = cards[4].get_num_rank()
			# check a a b b x
			back = first == second and third == fourth
			# check a a x b b
			middle = first == second and fourth == fifth
			# check x a a b b
			front = second == third and fourth == fifth
			if front or middle or back:
				two_pair = True
			else:
				two_pair = False
		return two_pair
			
	def is_one_pair(self):
		cards = self.get_rank_list()
		one_pair = True
		if (self.is_four_of_kind() or self.is_full_house() or 
			self.is_three_of_a_kind() or self_is_two_pair()):
		# same principle as three of kind: check for these first to rule out combinations
			one_pair = False
		else:	
			# get rank @ position
			first = cards[0].get_num_rank()
			second = cards[1].get_num_rank()
			third = cards[2].get_num_rank()
			fourth = cards[3].get_num_rank()
			fifth = cards[4].get_num_rank()
			# check a a x y z
			pair_first = first == second
			# check x a a y z
			pair_front_mid = second == third
			# check x y a a z
			pair_back_mid = third == fourth
			# check x y z a a
			pair_last = fourth == fifth
			if pair_first or pair_front_mid or pair_back_mid or pair_last:
				one_pair = True
			else:
				one_pair = False
		return one_pair

	def walk(self, cards):
	# if hand is "walkable", it means that next element in the list is the value of the previous + 1
	# i.e 3 = 2 + 1,etc.
		walkable = True
		rank = cards[0].get_num_rank() # start with lowest rank
		for card in cards[1:]:
			if card.get_num_rank() != rank + 1:
				walkable = False
				break # no point iterating if not walkable
			else:
				rank = card.get_num_rank()
		return walkable
	
# Taken from tournament.py in mdickson05/50pythonpuzzles
def parse_input():
	all_hands = []
	src = Path(__file__).parent
	relative_path = "input_files/poker.txt"
	path = (src / relative_path).resolve()
	with path.open() as f:
		lines = f.readlines()
		for line in lines:
			hand = []
			line = line.strip()
			cards = line.split(";")
			for card_string in cards:
				rank = card_string[0]
				suit = card_string[1]
				card = Card(suit, rank)
				card.find_suit_rank()
				card.find_num_rank()
				hand.append(card)
			hand_object = Hand(hand)
			# for card in hand_object:
				# print('suit:', card.get_suit_rank())
			all_hands.append(hand_object)
	return all_hands

def ranking_hands(hands):
	ranks = []
	winner = None
	for hand in hands:
		hand.sort_by_suit()
		hand.sort_by_rank()
		# print('Hand:')
		value_of_hand = 0 # undefined hand rank is 0
		# for card in hand:
			# print('Suit:', card.get_suit(), 'rank:', card.get_num_rank())
		is_flush = hand.is_flush()
		is_straight = hand.is_straight()
		if is_flush and is_straight: # if straight flush...
			value_of_hand = 2
			# 2nd best hand, will be winning unless royal flush occurs
			# As such, no break statement as not outright winner
			ranks = hand.get_rank_list()
			lowest_rank = rank[4] 
			if highest_rank == 12: # i.e. if highest rank is ACE
				winner = card
				break; # is royal flush; best possible hand, no other possible winner.
		elif hand.is_four_of_a_kind():
			value_of_hand = 3
		elif hand.is_full_house():
			value_of_hand = 4
		elif is_flush:
			value_of_hand = 5
		elif is_straight:
			value_of_hand = 6
		elif hand.is_three_of_a_kind():
			value_of_hand = 7
		elif hand.is_two_pair():
			value_of_hand = 8
		elif hand.is_one_pair():
			value_of_hand = 9
		elif hand.has_high_card():
			value_of_hand = 10
		else:
			value_of_hand = 11
		ranking = (hand, value_of_hand)
		ranks.append(ranking)
		# print('Card complete')
	ranks.sort(key=lambda ranking: ranking[1])
	winner = ranks[0]
	return winner

hands_list = parse_input()
# for hand in hands_list:	
	# print('Hand:')
	# for item in hand:
	#	print('Card:', item, 'Suit:', item.get_suit_rank(), 'Rank:', item.get_num_rank()) 
winner = ranking_hands(hands_list)
winner_hand = winner[0]
print('Winner is:', winner_hand)
