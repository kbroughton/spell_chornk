import click
import re
import random
import json
import hashlib


@click.command()
@click.option('--num-changes', default=1, help='Number of words changed.')
@click.option('--only-changes', type=click.BOOL, default=False,
              help='Boolean, do not include the "data" in the output to save space')
@click.option('--text', prompt="Your text: ", help="Text to convert or file path beginning with '@'")
def chornk(num_changes, only_changes, text):
    """Simple program that changes random letters in a given number of words in a text"""
    if text[0] == '@':
        file = openFile(text[1::])
        if file is None:
            exit()
        else:
            text = file.read()
            file.close()

    words = re.findall(r'\b[A-Za-z]+\b', text)  # returns a list with all the words in the text

    new_text = text
    changes = [(None, None, None)] * num_changes
    for x in range(num_changes):
        has_upper = False
        rand = random.randint(0, len(words) - 1)
        word = words[rand]
        if word[0].isupper():
            word = word.lower()
            has_upper = True
        new_word = swap_random(word)
        if has_upper:
            new_word = new_word[0].upper() + new_word[1::]
        changes[x] = (text.find(words[rand]), words[rand], new_word)
        new_text = new_text.replace(words[rand], new_word)

    json_out = json.dumps({'meta': {'input_hash': hashlib.sha256(text.encode('utf-8')).hexdigest()}, 'data': new_text, 'changes': changes}, indent=4)
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
