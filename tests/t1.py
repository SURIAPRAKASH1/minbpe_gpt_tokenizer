if __name__ == '__main__':
    from ..tokenizer.basic import BaseTokenizer
    tokenizer =  BaseTokenizer()
    text = "aaabdaaabac"
    tokenizer.train(text, 256 + 3)
    print(tokenizer.encoder(text))
    print(tokenizer.decoder(tokenizer.encoder(text)))