import sys


def add(set: dict, num: str, word: str):
    if len(num) == 1:
        set[num] = word
        return

    if num[0] not in set:
        set[num[0]] = {}
    add(set[num[0]], num[1:], word)

def search(set: dict, num: str):
    if len(num) == 1:
        if isinstance(set[num], str):
            return set[num]
        else:
            return None
    if num[0] not in set:
        return None
    else:
        return search(set[num[0]], num[1:])



def main():
    if len(sys.argv) < 3:
        print("insufficient args number")
        return
    
    dim = int(sys.argv[1])

    tree = {}
    with open(sys.argv[2], encoding="utf_8") as f:
        import re
        r = re.compile("\d{5} \w*")
        for line in f:
            if r.match(line) is not None:
                add(tree, line[:5], line[6:-1])
    
    import requests
    r = requests.get("https://www.random.org/integers", {
        'num': 5*dim,
        'min': 1,
        'max': 6,
        'col': 5,
        'base': 10,
        'format': 'plain',
        'rnd': 'new'})

    if r.status_code != 200 :
        print(r.text)
        return
    
    res = r.text.replace('\t', '').split('\n')[:-1]
    for num in res:
        print(search(tree, num), end= " ")

    word_entropy = 12.9248 
    print("\nEntropy: ", round(dim*word_entropy, 2))

if __name__ == "__main__":
    main()

