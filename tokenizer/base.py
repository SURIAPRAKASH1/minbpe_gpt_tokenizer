def get_stats(ids: list):
    """
    get's ids (list of integers)  then creates dict of repetively occuring consective pair and thier count.
    Example : [5, 7, 2, 8, 5, 7] --> {(5, 7): 2, (7, 2): 1, (2, 8): 1, (8, 5): 1} like this nothing fancy
    """
    counts = {} 
    for pair in zip(ids, ids[1:]):
        counts[pair] = counts.get(pair, 0) + 1 
    return counts 


def merge(ids, pair, idx ):
    "any consective two ids that match the pair will repalced by idx"

    new_ids = []
    i = 0

    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
            new_ids.append(idx) 
            i += 2
        else:
            new_ids.append(ids[i]) 
            i += 1

    return new_ids 


class Tokenizer:
    """Base class for all tokenizer's to inherit"""

    def __init__(self) -> None:
      # rule for merging two tokens as single token (int, int) -> int
      self.merges = {}
      # regex pattern to splitting our text to desirable chunks      
      self.pattern = ''
      self.special_tokens = {}  # eg: {'<|endoftext|>' : 10000234}
      # default vocab size is 256 , no merges 
      self.vocab = self._build_vocab()   
    

    def train(self, text, vocab_size, verbose = False):
      # Tokenizer used to create our vocabulary from size of 256 to vocab_size
      raise NotImplementedError
    
    def encoder(self, text):
      # Tokenizer can takes bunch of text then gives tokens (integer representation) for that based on some rule
      raise NotImplementedError

    def decoder(self, ids):
      # Tokenizer can takes tokens (list of integers) then gives text 
      raise NotImplementedError

    def _build_vocab(self):
      # as default vocabulary start with some 0-256 and based on merges we build our desired vocab with vocab size
      vocab = {idx: bytes([idx]) for idx in range(256)}
      for (p0, p1), idx in self.merges.items():
        vocab[idx] = vocab[p0] + vocab[p1]
      for special, idx in self.special_tokens.items():
        vocab[idx] = special.encode('utf-8')
        
      return vocab
    
    def save(self):
      # Not yet
      pass

    def load(self):
      # Not yet
      pass 