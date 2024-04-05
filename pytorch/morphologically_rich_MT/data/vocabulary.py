from .logger import Logger

class Vocabulary(Logger):

    def __init__(self, sentences, reserved_tokens, language, verbose, count=True):

        # sentences: List of all sentences in the set

        super().__init__(verbose)
        self.reserved_tokens = reserved_tokens
        self.language = language

        if count:
            self.tokens = {}
        
            for sentence in sentences:
                for token in sentence.split(' '):
                    self.add_token(token)
        
            self.sorted_tokens = sorted(self.tokens.keys(), key=lambda x: self.tokens[x], reverse=True)
            self.token_indices = {token: self.sorted_tokens.index(token) for token in self.sorted_tokens}
            self.sentences = sentences

    def restrict_vocabulary(self, new_vocab_size, unknown_token="UNK"):

        # in-place: delete vocabulary tokens based on new_vocab_size
        if len(self.token_indices) < new_vocab_size:
            self.print("Warning: Dataset vocabulary already below %d: %d tokens" % (new_vocab_size, len(self.token_indices)))
        else:
            prev_vocab_size = len(self.sorted_tokens)
            self.sorted_tokens = self.sorted_tokens[:new_vocab_size]
            self.tokens = {key: self.tokens[key] for key in self.sorted_tokens}
            
            # +1 in the counts of reserved_tokens ignored here
            for token in self.reserved_tokens:
                self.add_token(token)
                if not token in self.sorted_tokens:
                    self.sorted_tokens.append(token)

            self.token_indices = {token: self.sorted_tokens.index(token) for token in self.sorted_tokens}

            for idx in range(len(self.sentences)):
                new_tokens = []
                for token in self.sentences[idx].split(' '):
                    if not token in self.sorted_tokens:
                        new_tokens.append(unknown_token)
                        self.add_token(unknown_token)
                        self.remove_token(token)
                    else:
                        new_tokens.append(token)
                self.sentences[idx] = " ".join(new_tokens) 

            self.print("Reduced %s vocabulary size from %d to %d" % (self.language, prev_vocab_size, len(self.sorted_tokens)))
        
        self.sorted_tokens = sorted(self.tokens.keys(), key=lambda x: self.tokens[x], reverse=True)
        self.token_indices = {token: self.sorted_tokens.index(token) for token in self.sorted_tokens}
        
        return self.sentences

    def add_token(self, token):
        if not token in self.tokens:
            self.tokens[token] = 1
        else:
            self.tokens[token] += 1

    def remove_token(self, token):
        if not token in self.tokens:
            return
        else:
            del self.tokens[token]
