import nltk
from nltk.tokenize import word_tokenize
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S

AP -> Adj | Adj AP
AdvP -> Adv | Adv AdvP
NP -> N | Det N | Det AP N | AP NP | N PP | Det N PP
PP -> P NP
VP -> V | V NP | V NP PP | V PP | Adv V | V Adv | VP Conj VP | VP AdvP | AdvP VP | V NP AdvP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # Tokenize
    tokens = word_tokenize(sentence)

    # Make Lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()

    # Remove if no alphabetic character in token
    for token in tokens[:]:
        if not any(char.isalpha() for char in token):
            tokens.remove(token)

    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    
    np_chunks = []

    # Search for NP chunks in tree
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            
            # Check if the NP contains other NP subtrees
            if not any(child.label() == 'NP' for child in subtree.subtrees(lambda t: t != subtree)):

                # Save NP chunk
                np_chunks.append(subtree)

    return np_chunks


if __name__ == "__main__":
    main()
