characterSheet = {}

with open('Character Sheet.txt') as f:
    next(f)
    next(f)
    for line in f:
        (key,val) = line.split('=')
        characterSheet[key[:-1]] = val[1:-1]