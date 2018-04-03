from enum import Enum
from urllib import request
import graph
import itertools
import pickle

class Tokenization(Enum):
    word = 1
    character = 2

class TwitterWriter(object):

    def __init__(self, level, tokenization=Tokenization.word):
        self.level = level
        self.tokenization = tokenization
        self.markov = graph.Markov()

    def output(self):
        state = self.markov.get_rand_state()
        for token in state.value:
            yield token
        while state is not None:
            if len(state.transitions) == 0:
                state = self.markov.get_rand_state()
            else:
                transition = state.get_next()
                yield transition.value
                state = transition.dest

    def learn_url(self, url):
        if self.tokenization == Tokenization.none:
            raise ValueError('Tokenization cannot be none')
        with request.urlopen(url) as f:
            self.train_iterable(f.read().decode('utf-8'))

    def learn_iterable(self, data):
        self.check_type(data)
        if self.tokenization == Tokenization.word:
            data = data.split()
        counts = {}
        prev_window = None
        # Window creation taken from Arthur Peters' final_tests.py
        win = list()
        for v in data:
            if len(win) < self.level:
                win.append(v)
            else:
                win.pop(0)
                win.append(v)
            if len(win) == self.level:
                window = tuple(win)
                # Populate dict mapping states to other states
                if prev_window is not None:
                    if prev_window in counts:
                        if window in counts[prev_window]:
                            curr_count = counts[prev_window][window]
                            counts[prev_window][window] = curr_count + 1
                        else:
                            counts[prev_window][window] = 1
                    else:
                        counts[prev_window] = {window: 1}
                if window not in counts:
                    counts[window] = {}
                prev_window = window
        # Add all the states to the Markov chain
        for state_val in counts:
            if state_val not in self.markov.states:
                state = graph.State(state_val)
                self.markov.add_state(state)
        # Add all the transitions between the states in the Markov chain
        for src_val in counts:
            for dest_val in counts[src_val]:
                src = self.markov.states[src_val]
                cnt = counts[src_val][dest_val]
                possible_tr = src.transitions.get(dest_val)
                if possible_tr is None:
                    dest = self.markov.states[dest_val]
                    tr = graph.Transition(dest, cnt, dest_val[-1])
                    src.add_transition(tr)
                else:
                    curr_count = possible_tr.count
                    possible_tr.count = curr_count + cnt

    def check_type(self, data):
        """Checks for correct data typing
        """
        if self.tokenization in (Tokenization.word, Tokenization.character):
            if not isinstance(data, str):
                raise TypeError('Data must be a string')