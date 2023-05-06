import sys
import argparse as arg
import requests
import re
import signal

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

def readNumbersFile(file) -> list:
    res = list()
    with file as f:
        for line in f:
            line = line.removesuffix('\n')
            res.append(line)
    return res

def generateNumbers(dim : int) -> list:

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
        return []
    
    return r.text.replace('\t', '').split('\n')[:-1]

def printEntropy(dim : int):
    word_entropy = 12.9248 
    print("Entropy: ", round(dim*word_entropy, 2))


def main():

    parser = arg.ArgumentParser()
    parser.add_argument("wordlist", type=arg.FileType("r", encoding="utf_8"))
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("-i", action="store_true")
    grp.add_argument("-g", type=int)
    grp.add_argument("-f", type=arg.FileType("w", encoding="utf_8"))
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    tree = {}
    with args.wordlist as f:
        r = re.compile("\d{5} \w*")
        for line in f:
            if r.match(line) is not None:
                add(tree, line[:5], line[6:-1])

    print("Word tree generated.")

    if args.f is not None:
        for num in readNumbersFile(args.f):
            print(search(tree, num))
        return

    if args.g is not None :
        for num in generateNumbers(args.g):
            print(search(tree, num), end= " ")
        return

    if args.i:
        i = 1
        while True:
            line = input()
            line = line.removesuffix('\n')
            res = search(tree, line)
            if res is not None:
                print(f"{i}. {res}", end = "\n")
                i+=1
            else:
                print("Not Found")

if __name__ == "__main__":
    main()

