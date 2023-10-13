import random
import itertools
import argparse
from enum import Enum


class Rank(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

def generate_random_card(banned_cards):

    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['S', 'D', 'C', 'H']
    suit = random.choice([suit for suit in suits])
    rank = random.choice([rank for rank in ranks])
    card = (rank, suit)
    while card in banned_cards:
        suit = random.choice([suit for suit in suits])
        rank = random.choice([rank for rank in ranks])
        card = (rank, suit)
    return [rank, suit]
class Rank(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

def hand_value(hand):
    RANK_VALUES = '23456789TJQKA'
    RANK_DICT = {val: index for index, val in enumerate(RANK_VALUES)}
    ranks = ''.join(sorted([card[0] for card in hand], key=lambda r: RANK_DICT[r]))
    unique_ranks = ''.join(sorted(set(ranks), key=lambda r: ranks.index(r)))

    flush = all(card[1] == hand[0][1] for card in hand)
    straight = len(unique_ranks) == 5 and (
                RANK_DICT[unique_ranks[-1]] - RANK_DICT[unique_ranks[0]] == 4 or ranks == 'A2345')

    rank_counts = {rank: ranks.count(rank) for rank in unique_ranks}
    counts = list(rank_counts.values())
    rank_order = sorted(rank_counts, key=lambda r: (-counts[unique_ranks.index(r)], -RANK_DICT[r]))

    def get_rank_value(index):
        return RANK_DICT[rank_order[index]] if index < len(rank_order) else 0
    if flush and straight:
        return (Rank.ROYAL_FLUSH.value if ranks[-1] == 'A' else Rank.STRAIGHT_FLUSH.value, [get_rank_value(0)])
    if 4 in counts:
        return (Rank.FOUR_OF_A_KIND.value, [get_rank_value(0), get_rank_value(1)])
    if sorted(counts) == [2, 3]:
        return (Rank.FULL_HOUSE.value, [get_rank_value(0), get_rank_value(1)])
    if flush:
        return (Rank.FLUSH.value, [get_rank_value(i) for i in range(len(rank_order))])
    if straight:
        return (Rank.STRAIGHT.value, [get_rank_value(0)])
    if 3 in counts:
        return (Rank.THREE_OF_A_KIND.value, [get_rank_value(0), get_rank_value(1), get_rank_value(2)])
    if counts.count(2) == 2:
        return (Rank.TWO_PAIR.value, [get_rank_value(0), get_rank_value(1), get_rank_value(2)])
    if 2 in counts:
        return (Rank.PAIR.value, [get_rank_value(i) for i in range(4)])
    return (Rank.HIGH_CARD.value, [get_rank_value(i) for i in range(len(rank_order))])

def best_hand(cards):
    return max(itertools.combinations(cards, 5), key=hand_value)

def compare_hands(hand1, hand2, community_cards):
    best1, best2 = best_hand(hand1 + community_cards), best_hand(hand2 + community_cards)
    if hand_value(best1) > hand_value(best2):
        return "Hand1 wins"
    elif hand_value(best1) < hand_value(best2):
        return "Hand2 wins"
    else:
        return "It's a tie"

def __main__():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--hand1', type=str, default='ASAD', help='First hand')
    parser.add_argument('--hand2', type=str, default='2H7S', help='Second hand')
    parser.add_argument('--numruns', type=int, default=100000, help='Number of runs')
    args = parser.parse_args()
    hand1_win = 0
    hand_2_win = 0
    tie = 0
    hand1 = [args.hand1[:2], args.hand1[2:]]
    hand2 = [args.hand2[:2], args.hand2[2:]]
    for i in range(args.numruns):
        banned_cards = set()
        banned_cards.add((hand1[0], hand1[1]))
        banned_cards.add((hand2[0], hand2[1]))
        community_cards = []
        for _ in range(5):
            card1 = generate_random_card(banned_cards)
            banned_cards.add((card1[0], card1[1]))
            community_cards.append("".join(card1))
        s = compare_hands(hand1, hand2, community_cards)
        if s == "Hand1 wins":
            hand1_win += 1
        elif s == "Hand2 wins":
            hand_2_win += 1
        else:
            tie += 1
    print("Hand1 wins: ", hand1_win)
    print("Hand2 wins: ", hand_2_win)
    print("Tie: ", tie)
    print("Hand1 win rate: ", hand1_win / args.numruns)
    print("Hand2 win rate: ", hand_2_win / args.numruns)
    print("Tie rate: ", tie / args.numruns)

if __name__ == '__main__':
    __main__()

