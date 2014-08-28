Twice Challenge
---------------

##Word Jumble##

###Overview###
>Can you create a program to solve a word jumble? (More info here.) The program
> should accept a string as input, and then return a list of words that can be
> created using the submitted letters. For example, on the input "dog", the
> program should return a set of words including "god", "do", and "go".

###Usage###

jumble.py is a command line program that reads a line from stdin and returns a
list of anagrams as determined by the dictionary file (words.txt). Start by 
entering this command:
`python jumble.py`

By default jumble.py uses a recusrive algorithm to check all possible
permutations of the word. There is a `--better` flag that uses a modified 
algorithm. The modified algorith builds and checks the permutations and prunes
sub-permutations that are not valid beginnings to words. 

###Credits###
words.txt is a dictionary file from the [12dicts project](http://wordlist.aspell.net/12dicts-readme/)

###author###
Andrew Tamura
andrewtamura@gmail.com
http://www.andrewtamura.com
