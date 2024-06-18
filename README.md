# Python Poker
The idea for this project came from https://exercism.org/tracks/python/exercises/poker.
Furthermore, I would not have been able to complete it without this fantastic guide: http://www.cs.emory.edu/~cheung/Courses/170/Syllabus/10/pokerCheck.html
### Using the Program
1. Put your `<file>`.txt files in input_files
2. Run the command: `python poker.py <file>`
### Formatting
Pretty straight forward idea. The program takes in a text file of five poker cards, and picks the best hand. The rules for formatting are:
- (A)ce, (K)ing, (Q)ueen, (J)ack, (T)en, or numbers 2-9 for the first char. This represents the rank
- (s)pade, (h)earts, (d)iamond and (c)lub for the second char. This represents the suit
- All cards within a hand are separated by ";", and all hands are separated by a line.
### Test cases
There are a couple of provided test cases:
- all_cases will test all different hands (i.e. royal flush, straight flush => high card, one example of each)
- boundary_cases will test all hand classification boundaries (e.g. highest value one-pair vs lowest value two-pair)
- suit_comparison_cases will test identically ranked hands with different suits for all different hands (e.g. one-pair of 4s with clubs vs with diamonds)
