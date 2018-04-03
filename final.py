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
                if prev_window is not None:
                    if prev_window in self.markov.states:
                        if window in self.markov.states[prev_window].transitions:
                            prev_st = self.markov.states[prev_window]
                            curr_count = prev_st.transitions[window].count
                            prev_st.transitions[window].count = curr_count + 1
                        else:
                            prev_st = self.markov.states[prev_window]
                            curr_st = graph.State(window)
                            self.markov.add_state(curr_st)
                            tr = graph.Transition(curr_st, 1, window[-1])
                            prev_st.add_transition(tr)
                else:
                    st = graph.State(window)
                    self.markov.add_state(st)
                prev_window = window

    def check_type(self, data):
        """Checks for correct data typing
        """
        if self.tokenization in (Tokenization.word, Tokenization.character):
            if not isinstance(data, str):
                raise TypeError('Data must be a string')
