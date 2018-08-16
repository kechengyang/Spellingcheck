import re
from string import ascii_lowercase # All the lowercase letters

END = '$'  # The mark of the end of a world

class Trie:

    def __init__(self):
        self.trie = {}

    def get_words(self, text):
        """Transfer worlds into lowercase, and return a list"""
        return re.findall(r'\w+', text.lower())

    def add(self, word):
        """Add world into trie tree. node: current node, beginning with the root node; c: current letter; Traversal from the root node
            If the there is no c in node, then add c into node, finsh with an END mark
         """
        node = self.trie
        for c in word:
            if not c in node:
                node[c] = {}
            node = node[c]

        if not END in node:
            node[END] = 1
        else:
            node[END] += 1

    def make_trie(self, file):
        """Build trie based on lexicon file"""
        words = self.get_words(open(file).read())
        list(map(self.add, words))

    def check(self, word):
        """Check if the word is correct"""
        node = self.trie  # Node starts from the root node and traverses down (depth) step by step
        for c in word:
            if c not in node: # If there is no c in this layer's node, it means that the word definitely does not exist
                return False
            node = node[c]
        if END in node:
            return node[END]
        else:
            return 0
        # This layer has END to indicate that it is a complete word

    def fuzzy_words(self, word):
        """ word: entered word
            return: all possible fuzzy words 
        """
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)] # split words

        inserts = [L + c + R for L, R in splits for c in ascii_lowercase] # insert
        deletes = [L + R[1:] for L, R in splits if R] # delete
        replaces = [L + c + R[1:] for L, R in splits if R for c in ascii_lowercase] # replace
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1] # transpose
        # remove duplicates
        return set([word] + inserts + deletes + replaces + transposes)

    def fuzzy_check(self, word):
        """fuzzy check """
        a = ''
        words = self.fuzzy_words(word)
        count = 0
        for word in words:
            if self.check(word) > count:
                count = self.check(word)
                a = word
        return a

if __name__ == "__main__":
    # read file and build trie tree
    a = Trie()
    a.make_trie('corpus-challenge4.txt')
    
    while True:
        # get word entered
        word_input = []
        num = int(input("the number of input\n"))
        for i in range(num):
            word_input.append(input().lower())
        
        # spell check
        word_output = []
        for i in word_input:
            if a.check(i) == 0:
                word_output.append(a.fuzzy_check(i))
            else:
                word_output.append(i)
                
        # output corrected word
        print('\noutput')
        for i in word_output:
            print(i)
        print('\n')
