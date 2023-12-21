import json

from lab3 import *


def loging(encoded):
    with open(f"log.json", 'w') as json_file:
            json.dump(encoded, json_file, indent=4)

COUNT_OF_PLAYER = 6
LOG_VARIABLE = {}

def generate_deck():
    suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
    nominals = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    cards = []

    for suit in suits:
        for nominal in nominals:
            cards.append(suit + " " + nominal)
    return {i : cards[i - 2] for i in range(2, 54)}

def main():
    main_deck = generate_deck()
    deck_keys = list(main_deck.keys())
    random.shuffle(deck_keys)
    temp_deck = {key : main_deck[key] for key in deck_keys}

    p = generate_p()

    C = list()
    D = list()

    deck_keys = list(temp_deck.keys())
    LOG_VARIABLE["SHUFFLE"] = {}
    for i in range(COUNT_OF_PLAYER):
        LOG_VARIABLE["SHUFFLE"][i] = []
        c = get_coPrime(p - 1)
        d = extented_gcd(c, p - 1)[1]
        if d < 0:
            d += (p - 1)
        deck_keys = [rapid_pow(i, c, p) for i in deck_keys]
        random.shuffle(deck_keys)
        LOG_VARIABLE["SHUFFLE"][i].append({"deck" : deck_keys, "C" : c, "D" : d})
        C.append(c)
        D.append(d)
    loging(LOG_VARIABLE)

    hands = list()
    LOG_VARIABLE["DRAFT"] = {}
    LOG_VARIABLE["DRAFT"]["TABLE"] = []
    for i in range(COUNT_OF_PLAYER):
        LOG_VARIABLE["DRAFT"][i] = []
        hands.append([])
        for j in range(2):
            card = deck_keys[j]
            deck_keys.remove(card)
            hands[i].append(card)
        LOG_VARIABLE["DRAFT"][i].append({"hand" : hands[i]})

    table = deck_keys[:5]
    LOG_VARIABLE["DRAFT"]["TABLE"].append(table)
    loging(LOG_VARIABLE)

    for i in range(COUNT_OF_PLAYER):
        table = [rapid_pow(table[j], D[i], p) for j in range(len(table))]
    table = {key: temp_deck[key] for key in table}
    print(f"Cards on table: {list(table.values())}")

    for i in range(COUNT_OF_PLAYER):
        for j in range(COUNT_OF_PLAYER):
            if i != j:
                for m in range(2):
                    hands[i][m] = rapid_pow(hands[i][m], D[j], p)
        for m in range(2): 
            hands[i][m] = rapid_pow(hands[i][m], D[i], p)
    hands = [{key : temp_deck[key] for key in hand} for hand in hands]
    

    for i in range(COUNT_OF_PLAYER):
        print(f"Player {i + 1} has cards: {list(hands[i].values())}")



if __name__ == "__main__":
    main()