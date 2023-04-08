
def add(set, num, word):
    if len(num) == 1:
        set[num] = word
        return

    if num[0] not in set:
        set[num[0]] = {}
    add(set[num[0]], num[1:], word)

def search(set, num):
    if len(num) == 1:
        return set[num]
    if num[0] not in set:
        return None
    else:
        return search(set[num[0]], num[1:])


tree = {}
with open("wordlist.txt", encoding="utf_8") as f:
    import re
    r = re.compile("\d{5} \w*")
    for line in f:
        if r.match(line) is not None:
            add(tree, line[:5], line[6:-1])


with open("numberlist.txt") as f:
    for line in f:
        print(search(tree, line[:-1]), end= " ")

