import click
import re
import random
import json
import hashlib


@click.command()
@click.option('--num-changes', default=3, help='Number of words changed.')
@click.option('--only-changes', type=click.BOOL, default=False,
              help='Boolean, do not include the "data" in the output to save space')
@click.option('--text', prompt="Your text: ", help="Text to convert or file path beginning with '@'")
@click.option('--swap-alg', default="sha256", help="Hash function to use for the input")
def chornk(num_changes, only_changes, text, swap_alg):
    """Simple program that changes a given number of words in a text. If the text has less words than the given number, there will be as many changes as words in the text"""
    hash_dic = {"sha256": hashlib.sha256(), "sha1": hashlib.sha1()}
    if(hash_dic.get(swap_alg) is None):
        print("Not a valid hash function")
    else:
        hash_f = hash_dic.get(swap_alg)

    with open("words.json", 'r') as f:
        spell_dic = json.load(f)

    if text[0] == '@':
        file = openFile(text[1::])
        if file is None:
            exit()
        else:
            text = file.read()
            file.close()

    print(spell_dic)

    words = re.findall(r'\b[A-Za-z]+\b', text)  # returns a list with all the words in the text
    print(words)

    new_text = text
    change_count = 0
    changes = []
    rand_used = []
    rand_changed = []

    for x in range(num_changes):
        has_upper = False
        while True:
            rand = random.randint(0, len(words) - 1)
            if rand not in rand_used or len(rand_used) >= len(words):
                break
        rand_used.append(rand)
        word = words[rand]
        print("1: " + word)
        if word[0].isupper():
            word = word.lower()
            has_upper = True
        if spell_dic.get(word) is not None:
            misspells = spell_dic.get(word)
            new_word = misspells[random.randint(0, len(misspells)-1)]
            print("1: " + new_word)
            if has_upper:
                new_word = new_word[0].upper() + new_word[1::]
            changes.append([text.find(words[rand]), words[rand], new_word])
            change_count += 1
            rand_changed.append(rand)
            new_text = new_text.replace(words[rand], new_word)
            print("1: " + new_text)
    
    if num_changes > change_count:
        rand_used = []
        for x in range(num_changes-change_count):
            has_upper = False
            if change_count == len(words):
                break
            while True:
                rand = random.randint(0, len(words) - 1)
                if (rand not in rand_used and rand not in rand_changed) or len(rand_used) >= len(words):
                    break
            rand_used.append(rand)
            word = words[rand]
            print("2: " + word)
            if word[0].isupper():
                word = word.lower()
                has_upper = True
            new_word = swap_random(word)
            if has_upper:
                new_word = new_word[0].upper() + new_word[1::]
                print("2: " + new_word)
            changes.append([text.find(words[rand]), words[rand], new_word])
            new_text = new_text.replace(words[rand], new_word)
            change_count += 1
            print("2: " + new_text)

    if only_changes:
        json_out = json.dumps({'data': new_text, 'changes': changes}, indent=None, separators=(",", ":"))
    else:
        hash_f.update(text.encode('utf-8'))
        json_out = json.dumps({'meta': {'input_hash': hash_f.hexdigest()}, 'data': new_text, 'changes': changes}, indent=None, separators=(",",":"))
    print(json_out)


def swap_random(string):
    """Swaps 2 random letters in a string"""
    characters = list(string)
    spot1 = random.randint(0, len(characters) - 1)
    while True:
        spot2 = random.randint(0, len(characters) - 1)
        if spot1 != spot2 or len(characters) == 1:
            break
    characters[spot1], characters[spot2] = characters[spot2], characters[spot1]
    return "".join(characters)


def openFile(fn):
    try:
        return open(fn, 'r')
    except IOError:
        print("Error: File does not appear to exist or the path is wrong.")
        return None


if __name__ == '__main__':
    chornk()
