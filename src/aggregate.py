"""Aggregate name by the repname."""
import argparse
import datetime

import progressbar
import zenhan
from pyknp import Jumanpp


def count_line(path):
    """

    :param path: path to input file
    :return: the line number of line

    """
    with open(path) as f:
        return len([_ for _ in f])


def load_file(path):
    """

    :param path: path to input file
    :return: data in the file

    """
    n_line = count_line(path)
    bar = progressbar.ProgressBar()
    with open(path) as f:
        return [word.strip() for word in bar(f, max_value=n_line)]


def preprocess_word(words):
    """

    :param words: a list of words to be preprocessed
    :return: preprocessed word

    """
    # TODO: convert Kansuji to Arabic numerals
    return [zenhan.h2z(word) for word in words]


def get_repname_set(words):
    """

    :param words: words in input file
    :return: a list of sets of representative names for the words

    """
    n_word = len(words)
    juman = Jumanpp()
    bar = progressbar.ProgressBar()
    repname_sets = []
    for word in bar(words, max_value=n_word):
        r = juman.analysis(word)
        # preserve ambiguity
        repname_set = [tuple(mrph.repnames().split('?')) if mrph.repnames() else mrph.midasi
                       for mrph in r.mrph_list()]
        repname_sets.append(expand_ambiguity(repname_set))
    return repname_sets


def expand_ambiguity(repname):
    """

    :param repname: a list of tuples which include the repname candidates for morphemes
    :return: a list of repname candidates for morphemes

    """
    def product_tuple(t1, t2):
        return tuple([_t1 + _t2 for _t1 in t1 for _t2 in t2])

    expanded_repname = tuple([''])
    for _repname in repname:
        expanded_repname = product_tuple(expanded_repname, _repname)
    return expanded_repname


def aggregate(words, repname_sets):
    """

    :param words: words in input file
    :param repname_sets: a list of sets of representative names for the words
    :return: words with aggregated ID

    """
    # TODO: Access ConceptNet to retrieve `Sysnonym` and `FormOf` of words
    # build a list of set to be merged
    repname_sets_to_merge = [set(repname_sets[0])]
    for repname_set in repname_sets[1:]:
        repname_set = set(repname_set)
        for i, repname_set_to_merge in enumerate(repname_sets_to_merge):
            if len(repname_set & repname_set_to_merge) > 0:
                repname_sets_to_merge[i] = repname_set | repname_set_to_merge
                break
        else:
            repname_sets_to_merge.append(repname_set)

    # assign IDs for each set
    repname2id = {}
    for i, repname_set in enumerate(repname_sets_to_merge):
        for repname in repname_set:
            repname2id[repname] = i

    # assign IDs to words
    word_with_id = []
    for word, repname_set in zip(words, repname_sets):
        repname = repname_set[0]
        word_with_id.append((word, repname2id[repname]))
    return word_with_id


def save(path, out):
    """

    :param path: path to output file
    :param out: words with ID

    """
    with open(path, 'w') as f:
        for word, id in out:
            f.write('{}\t{}\n'.format(word, id))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('IN', help='path to input file')
    parser.add_argument('OUT', help='path to output file')
    args = parser.parse_args()

    print('[{}] Loading data... '.format(datetime.datetime.now()))
    words = load_file(args.IN)
    words_prerprocessed = preprocess_word(words)

    print('[{}] Getting repname for data... '.format(datetime.datetime.now()))
    repname_sets = get_repname_set(words_prerprocessed)

    print('[{}] Aggregating words... '.format(datetime.datetime.now()))
    out = aggregate(words, repname_sets)
    save(args.OUT, out)


if __name__ == '__main__':
    main()
