from enum import Enum
from urllib import request
import graph

class Tokenization(Enum):
    word = 1
    character = 2

class TwitterWriter(object):

    def __init__(self, level, tokenization=Tokenization.word):
        # How many tokens to save in each state
        self.level = level
        # Tokenize by word or character
        self.tokenization = tokenization
        # Creats empty Markov chain
        self.markov = graph.Markov()

    def output(self):
        """ Outputs tokens by randomly traversing the Markov chain
        """
        state = self.markov.get_rand_state()
        # Yields all the tokens in the first state
        for token in state.value:
            yield token
        while state is not None:
            if len(state.transitions) == 0:
                # Gets a new starting state if prior state has no outgoing edges
                state = self.markov.get_rand_state()
            else:
                # Randomly gets the next state and yields the changing token
                transition = state.get_next()
                yield transition.value
                state = transition.dest

    def learn_url(self, url):
        """ Creates the Markov chain from a URL
        """
        with request.urlopen(url) as f:
            self.learn_iterable(f.read().decode('utf-8'))

    def learn_iterable(self, data):
        """ Creats the Markov chain by going through the data and computing
        probabilities
        """
        if self.tokenization in (Tokenization.word, Tokenization.character):
            if not isinstance(data, str):
                raise TypeError('Data must be a string')
        if self.tokenization == Tokenization.word:
            data = data.split()
        prev_window = None
        # Code for converting data to win used was taken from Arthur Peters
        win = list()
        for v in data:
            if len(win) < self.level:
                win.append(v)
            else:
                win.pop(0)
                win.append(v)
            if len(win) == self.level:
                # Creates tuples of elements in data for each Markov state
                window = tuple(win)
                # Checks if not at the first window in the data
                if prev_window is not None:
                    prev_st = self.markov.states[prev_window]
                    # Checks if there's an edge between previous and current
                    if window in prev_st.transitions:
                        tr = prev_st.transitions[window]
                        # Increments number of times current is after previous
                        tr.count += 1
                    else:
                        if window not in self.markov.states:
                            # Makes state for window if not already a state
                            curr_st = graph.State(window)
                            self.markov.add_state(curr_st)
                        st = self.markov.states[window]
                        # Adds edge between previous and current states
                        tr = graph.Transition(st, 1, window[-1])
                        prev_st.add_transition(tr)
                else:
                    # Makes state from the first window in the data
                    st = graph.State(window)
                    self.markov.add_state(st)
                prev_window = window
