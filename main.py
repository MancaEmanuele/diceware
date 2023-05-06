import sys
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

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    if len(sys.argv) < 2:
        print("insufficient args number")
        return

    tree = {}
    with open(sys.argv[1], encoding="utf_8") as f:
        import re
        r = re.compile("\d{5} \w*")
        for line in f:
            if r.match(line) is not None:
                add(tree, line[:5], line[6:-1])

    print("Word tree generated.")

    i = 0
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

