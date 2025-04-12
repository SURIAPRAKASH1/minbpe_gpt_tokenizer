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


tummy_ids = [1, 3, 5, 8, 9, 2]
merges = merge(tummy_ids, [8, 9], 334)
print(merges)