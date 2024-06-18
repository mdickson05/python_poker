# Pick the best hand(s) from a list of poker hands.
from pathlib import Path
import sys
class Card:
	def __init__(self, suit, num):
		self.suit = suit
		self.num = num
		self.rank_value = 0
		self.suit_value = 0
	def __str__(self):
		return str(self.num) + str(self.suit)
	def __iter__(self):
		yield self.suit
		yield self.rank
	def get_suit(self):
		return self.suit
	def get_num(self):
		return self.num
	def get_rank_value(self):
		return self.rank_value
	def get_suit_value(self):
		return self.suit_value
	def set_rank_value(self, in_rank):
		self.rank_value = in_rank
	def set_suit_value(self, in_rank):
		self.suit_value = in_rank
	def find_rank_value(self):
		ranking = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
		num = self.get_num()
		rank = ranking.index(num)
		self.set_rank_value(rank)
	def find_suit_value(self):
		ranking = ['s', 'h', 'd', 'c']
		suit = self.get_suit()
		rank = ranking.index(suit)
		self.set_suit_value(rank)
	def get_rank_map(self):
		rank_map = {
			"2": "Two",
			"3": "Three",
			"4": "Four",
			"5": "Five",
			"6": "Six",
			"7": "Seven",
			"8": "Eight",
			"9": "Nine",
			"T": "Ten",
			"J": "Jack",
			"Q": "Queen",
			"K": "King",
			"A": "Ace"
		}
		return rank_map
	def get_suit_map(self):
		suit_map = {
			"s": "Spades",
			"h": "Hearts",
			"d": "Diamonds",
			"c": "Clubs"
		}
		return suit_map
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
			rank_map = card.get_rank_map()
			suit_map = card.get_suit_map()
			card_string = rank_map[card.get_num()] + ' of ' + suit_map[card.get_suit()]
			hands.append(card_string)
		return ', '.join(hands)
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
	def generate_rank_list(self):
		cards = self.get_hand()
		cards.sort(key=lambda card: card.rank_value)
		self.set_rank_list(cards)
	def generate_suit_list(self):
		cards = self.get_hand()
		cards.sort(key=lambda card: card.get_suit_value())
		self.set_suit_list(cards)
	def get_all_rank_values(self):
		cards = self.get_rank_list()
		# get rank num @ position in sorted list
		first = cards[0].get_rank_value()
		second = cards[1].get_rank_value()
		third = cards[2].get_rank_value()
		fourth = cards[3].get_rank_value()
		fifth = cards[4].get_rank_value()
		return [first, second, third, fourth, fifth]
	def get_all_suit_values(self):
		cards = self.get_suit_list()
		# get suit num @ position
		first = cards[0].get_suit_value()
		second = cards[1].get_suit_value()
		third = cards[2].get_suit_value()
		fourth = cards[3].get_suit_value()
		fifth = cards[4].get_suit_value()
		return [first, second, third, fourth, fifth]
	def is_flush(self):
		suit_values = self.get_all_suit_values()
		first = suit_values[0]
		second = suit_values[1]
		third = suit_values[2]
		fourth = suit_values[3]
		fifth = suit_values[4]
		return first == second == third == fourth == fifth
	def is_straight(self):
		rank_values = self.get_all_rank_values()
		straight = False
		highest_rank = rank_values[4] # already sorted; last element = highest rank
		if highest_rank == 12: # i.e. highest_rank is an ACE
			# ACE wraps around; needs to be considered
			if 8 in rank_values and 9 in rank_values and 10 in rank_values and 11 in rank_values:
				# i.e. if T, J, Q and K appear
				straight = True
			elif 0 in rank_values and 1 in rank_values and 2 in rank_values and 3 in rank_values:
				# i.e. if 2,3,4 and 5 appear
				straight = True
		else:
			straight = self.walk()
		return straight
	def is_four_of_a_kind(self):
		rank_values = self.get_all_rank_values()
		first = rank_values[0]
		second = rank_values[1]
		third = rank_values[2]
		fourth = rank_values[3]
		fifth = rank_values[4]
		# check for x x x x y
		x_first = first == second == third == fourth
		# check for y x x x x 
		x_last = second == third == fourth == fifth
		# OR operator: only returns False if both elements are false, else True
		return x_first or x_last
	def is_full_house(self):
		rank_values = self.get_all_rank_values()
		first = rank_values[0]
		second = rank_values[1]
		third = rank_values[2]
		fourth = rank_values[3]
		fifth = rank_values[4]
		# check for x x x y y
		three_x = first == second and second == third and fourth == fifth
		# check for x x y y y
		three_y = first == second and third == fourth and fourth == fifth
		# OR operator: only returns False if both elements are false, else True
		return three_x or three_y

	def is_three_of_a_kind(self):
		# if we check four_of_kind & full house first, we can rule out some combinations for further tests
		if not (self.is_four_of_a_kind() or self.is_full_house()):
			# get rank @ position
			rank_values = self.get_all_rank_values()
			first = rank_values[0]
			second = rank_values[1]
			third = rank_values[2]
			fourth = rank_values[3]
			fifth = rank_values[4]
			# check x x x a b
			front = first == second and second == third 
			# check a x x x b
			middle = second == third and third == fourth
			# check a b x x x
			back = third == fourth and fourth == fifth
			return front or middle or back
		return False
	def is_two_pair(self):
		# same principle as three of kind: check for these first to rule out combinations
		if not (self.is_four_of_a_kind() or self.is_full_house() or self.is_three_of_a_kind()):
			rank_values = self.get_all_rank_values()
			first = rank_values[0]
			second = rank_values[1]
			third = rank_values[2]
			fourth = rank_values[3]
			fifth = rank_values[4]
			# check a a b b x
			back = first == second and third == fourth
			# check a a x b b
			middle = first == second and fourth == fifth
			# check x a a b b
			front = second == third and fourth == fifth
			return front or middle or back
		return False
			
	def is_one_pair(self):
		# same principle as three of kind: check for these first to rule out combinations
		if not (self.is_four_of_a_kind() or self.is_full_house() or 
			self.is_three_of_a_kind() or self.is_two_pair()):
			# get rank @ position
			rank_values = self.get_all_rank_values()
			first = rank_values[0]
			second = rank_values[1]
			third = rank_values[2]
			fourth = rank_values[3]
			fifth = rank_values[4]
			# check a a x y z
			pair_first = first == second
			# check x a a y z
			pair_front_mid = second == third
			# check x y a a z
			pair_back_mid = third == fourth
			# check x y z a a
			pair_last = fourth == fifth
			return pair_first or pair_front_mid or pair_back_mid or pair_last
		return False

	def walk(self):
	# if hand is "walkable", it means that next element in the list is the value of the previous + 1
	# i.e 3 = 2 + 1, etc.
		rank_values = self.get_all_rank_values()
		for i in range(len(rank_values) - 1):
			if (rank_values[i+1]) != (rank_values[i] + 1):
				return False
		return True
	
# Taken from tournament.py in mdickson05/50pythonpuzzles
def parse_input(cli_path):
	all_hands = []
	src = Path(__file__).parent
	relative_path = "input_files"
	relative_path += ("/" + cli_path)
	path = (src / relative_path).resolve()
	with path.open() as f:
		lines = f.readlines()
		for line in lines:
			cards_list = []
			line = line.strip()
			cards = line.split(";")
			for card_string in cards:
				rank = card_string[0]
				suit = card_string[1]
				card = Card(suit, rank)
				card.find_suit_value()
				card.find_rank_value()
				cards_list.append(card)
			hand = Hand(cards_list)
			hand.generate_suit_list() # generates suit list
			hand.generate_rank_list() # generates rank list
			all_hands.append(hand)
	return all_hands

def two_pair_value(hand):
	rank_values = hand.get_all_rank_values()
	first = rank_values[0]
	second = rank_values[1]
	third = rank_values[2]
	fourth = rank_values[3]
	fifth = rank_values[4]
	'''
	formula: 
	TWO_PAIRS + 14^2 * HIGH_PAIR_VAL + 14 * LOW_PAIR_VAL + UNMATCHED
	'''
	# x x y y a
	if first == second and third == fourth:
		value = (14*14*third + 14*first + fifth)
	# x x a y y
	elif first == second and fourth == fifth:
		value = (14*14*fourth + 14*first + third)
	# a x x y y
	else:
		value = (14*14*fourth + 14*second + first) 
	return value
def one_pair_value(hand):
	rank_values = hand.get_all_rank_values()
	first = rank_values[0]
	second = rank_values[1]
	third = rank_values[2]
	fourth = rank_values[3]
	fifth = rank_values[4]
	'''
	FORMULA:
		ONE_PAIR + 14^3*PairCard + 14^2*HighestCard + 14*MiddleCard 
		+ LowestCard
	'''
	# x x a b c
	if first == second:
		value = 14*14*14*first + third + 14*fourth + 14*14*fifth
	# a x x b c
	elif second == third:
		value = 14*14*14*second + first + 14*fourth + 14*14*fifth
	# a b x x c
	elif third == fourth:
		value = 14*14*14*third + first + 14*second + 14*14*fifth
	# a b c x x
	else:
		value = 14*14*14*fourth + first + 14*second + 14*14*third
	return value

def high_card_value(hand):
	rank_values = hand.get_all_rank_values()
	# get rank @ position
	first = rank_values[0]
	second = rank_values[1]
	third = rank_values[2]
	fourth = rank_values[3]
	fifth = rank_values[4]
	'''
	FORMULA:
		high_card_value = 14^4*Fifth + 14^3*Fourth + 14^2*Third + 14*Second
		+ first
	'''
	return 14*14*14*14*fifth + 14*14*14*fourth + 14*14*third + 14*second + first

# Only used when there is a draw on rankings
def suit_value_coefficient(hand):
	suit_values = hand.get_all_suit_values()
	# get rank @ position
	first = suit_values[0]
	second = suit_values[1]
	third = suit_values[2]
	fourth = suit_values[3]
	fifth = suit_values[4]
	'''
	FORMULA:
		suit_value = 14^4*Fifth + 14^3*Fourth + 14^2*Third + 14*Second
		+ first
	'''
	return 14*14*14*14*fifth + 14*14*14*fourth + 14*14*third + 14*second + first

def ranking_hands(hands):
	ranks = []
	winner = None
	# constants added for consistency and readability
	global ROYAL_FLUSH
	global STRAIGHT_FLUSH
	global FOUR_OF_A_KIND
	global FULL_HOUSE
	global FLUSH
	global STRAIGHT
	global THREE_OF_A_KIND
	global TWO_PAIR
	global ONE_PAIR

	ROYAL_FLUSH = 9000000
	STRAIGHT_FLUSH = 8000000
	FOUR_OF_A_KIND = 7000000
	FULL_HOUSE = 6000000
	FLUSH = 5000000
	STRAIGHT = 4000000
	THREE_OF_A_KIND = 3000000
	TWO_PAIR = 2000000
	ONE_PAIR = 1000000

	for hand in hands:
		ranks_list = hand.get_rank_list()
		high_card_rank = high_card_value(hand) # big number used to differentiate hands of same type
		set_rank = ranks_list[2].get_rank_value()
		suits_rank = suit_value_coefficient(hand) # used in case of draw!
		is_flush = hand.is_flush()
		is_straight = hand.is_straight()
		if is_flush and is_straight: # if straight flush...
			highest_rank = ranks_list[4].get_rank_value()
			if highest_rank == 12: # i.e. if highest rank is ACE
				value_of_hand = ROYAL_FLUSH # hand is royal flush; best possible hand.
			else:
				value_of_hand = STRAIGHT_FLUSH + high_card_rank
		elif hand.is_four_of_a_kind():
			value_of_hand = FOUR_OF_A_KIND + high_card_rank
		elif hand.is_full_house():
			value_of_hand = FULL_HOUSE + set_rank
		elif is_flush:
			value_of_hand = FLUSH + high_card_rank
		elif is_straight:
			value_of_hand = STRAIGHT + high_card_rank
		elif hand.is_three_of_a_kind():
			value_of_hand = THREE_OF_A_KIND + set_rank
		elif hand.is_two_pair():
			value_of_hand = TWO_PAIR + two_pair_value(hand)
		elif hand.is_one_pair():
			value_of_hand = ONE_PAIR + one_pair_value(hand)
		else:
			value_of_hand = high_card_rank
		ranking = (hand, value_of_hand, suits_rank)
		ranks.append(ranking)
	ranks.sort(key=lambda ranking: (ranking[1], ranking[2]),reverse=True)
	return ranks

# Straight from Stack Overflow: https://stackoverflow.com/a/20007730
def get_ordinal(n):
	if 11 <= (n % 100) <= 13:
	    suffix = 'th'
	else:
	    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
	return str(n) + suffix

def get_hand_value_as_string(value_of_hand):
	if value_of_hand == ROYAL_FLUSH:
		rank_string = "(Royal Flush!)"
	elif STRAIGHT_FLUSH <= value_of_hand < ROYAL_FLUSH:
		rank_string = "(Straight Flush)"
	elif FOUR_OF_A_KIND <= value_of_hand < STRAIGHT_FLUSH:
		rank_string = "(Four of a Kind)"
	elif FULL_HOUSE <= value_of_hand < FOUR_OF_A_KIND:
		rank_string = "(Full House)"
	elif FLUSH <= value_of_hand < FULL_HOUSE:
		rank_string = "(Flush)"
	elif STRAIGHT <= value_of_hand < FLUSH:
		rank_string = "(Straight)"
	elif THREE_OF_A_KIND <= value_of_hand < STRAIGHT:
		rank_string = "(Three of a Kind)"
	elif TWO_PAIR <= value_of_hand < THREE_OF_A_KIND:
		rank_string = "(Two Pair)"
	elif ONE_PAIR <= value_of_hand < TWO_PAIR:
		rank_string = "(One Pair)"
	else:
		rank_string = "(High Card)"
	return rank_string

try:
	path = sys.argv[1]
	hands_list = parse_input(path)
	ranking = ranking_hands(hands_list)
	winner = ranking[0]
	winner_hand = winner[0]
	hand_value_as_string = get_hand_value_as_string(winner[1])
	print('Winner is:', winner_hand, hand_value_as_string)
	print('Leaderboard:')
	for result in ranking:
		hand = result[0]
		value = get_hand_value_as_string(result[1])
		ordinal = get_ordinal(ranking.index(result) + 1)
		print(ordinal, 'place:', hand, value)
except IndexError:
	print('Error: path not entered properly. Please Try Again.')
