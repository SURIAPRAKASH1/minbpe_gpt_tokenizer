from .base import Tokenizer, get_stats, merge

class BaseTokenizer(Tokenizer):
  """
  the basic tokenizer with Byte-pair encoding algo
  IT DOESN'T HANDLE :
      1. special case tokens Eg: <|endoftext|> 
      2. regex pattern for text preprocessing nor vocab building
  """

  def __init__(self):
    super().__init__()
  
  def train(self, text, vocab_size, verbose = False):
    assert vocab_size >= 256
    num_merges = vocab_size - 256
    
    # change given text as raw tokens ranging from 0 - 255
    raw_tokens = list(map(int, text.encode('utf-8')))  
    ids = raw_tokens.copy()

    for i in range(num_merges):
      # get repetively occuring consective pair and thier counts
      stats = get_stats(ids)
      # get pair that occur mostly from consective pair
      pair = max(stats, key= stats.get) 
      # new token for that pair
      idx = 256 + i
      # then change all occurences of that pair to idx 
      ids = merge(ids, pair, idx) 
      # store those pair and thier idx
      self.merges[pair] = idx                                       #  used in encoder
      self.vocab[idx] = self.vocab[pair[0]] + self.vocab[pair[1]]   #  used in decoder

      if verbose:
        print(f"merge {i + 1}/{num_merges}: {pair} --> {idx} ({self.vocab[idx]} has {stats[pair]} occurencess)")

  def encoder(self, text):
    # first convert our text has raw tokens
    raw_tokens = list(map(int, text.encode('utf-8')))

    while len(raw_tokens) >= 2:
      # make our tokens as consective pair
      stats = get_stats(raw_tokens)
      # go from pair that occur least 
      pair = min(stats, key= lambda p: self.merges.get(p, float('inf')))
      # the pair not occur in merge then nothing else to merge
      if pair not in self.merges:
        break 

      # get the idx for that pair based on our tranined tokenizer
      idx = self.merges[pair]
      # change all those consective pair to idx
      raw_tokens = merge(raw_tokens, pair, idx)

    return raw_tokens

  def decoder(self, ids):
    # convert idx (tokens) as byte stream
    text_tokens = b"".join(bytes(self.vocab[id]) for id in ids)
    text = text_tokens.decode('utf-8', errors= "replace")
    return text 
  