# Python Poker
The idea for this project came from https://exercism.org/tracks/python/exercises/poker.
Furthermore, I would not have been able to complete it without this fantastic guide: http://www.cs.emory.edu/~cheung/Courses/170/Syllabus/10/pokerCheck.html
### Formatting
Pretty straight forward idea. The program takes in a text file of five poker cards, and picks the best hand. The rules for formatting are:
- (A)ce, (K)ing, (Q)ueen, (J)ack, (T)en, or numbers 2-9 for the first char. This represents the rank
- (s)pade, (h)earts, (d)iamond and (c)lub for the second char. This represents the suit
- All cards within a hand are separated by ";", and all hands are separated by a line.
- Note: Jokers are not included... yet ;)
### TO-DO list:
- Convert the winning result to the full string (i.e. Th becomes Ten of Hearts)
- Show what the winning hand actually was
- Clean up some redundant code
- Tidy up the variable naming
- Maybe have a 'results leaderboard' as opposed to just a single winner?
