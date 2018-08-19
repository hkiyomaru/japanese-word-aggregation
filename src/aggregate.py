"""Aggregate words by Juman++ and ConceptNet."""
import argparse
import datetime
import itertools
import re
import requests
import string
import unicodedata

import progressbar
import zenhan
from pyknp import Jumanpp


class Word(object):

    _uid = itertools.count(0)

    def __init__(self, surface, p_surface, alias):
        self.surface = surface
        self.p_surface = p_surface
        self.alias = alias

        self.uid = next(self._uid)
        self.anc = [self.uid]  # ancestors


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
    :return: a list of Word instances

    """
    n_line = count_line(path)
    bar = progressbar.ProgressBar()
    with open(path) as f:
        words = [Word(word.strip(), None, None) for word in bar(f, max_value=n_line)]
    return words


def preprocess_word(words):
    """

    :param words: a list of Word instances
    :return: a list of Word instances with the preprocessed expressions

    """
    n_words = len(words)
    for i in range(n_words):
        word = words[i]
        # remove symbols
        preprocessed_word = unicodedata.normalize("NFKC", word.surface)
        table = str.maketrans("", "", string.punctuation + "「」、。・")
        preprocessed_word = preprocessed_word.translate(table)
        # convert to zenkaku
        preprocessed_word = zenhan.h2z(preprocessed_word)
        # register preprocessed word
        words[i].p_surface = preprocessed_word
        words[i].alias = [preprocessed_word]
    return words


def kansuji2arabic(kstring):
    """

    :param kstring: word which indicates a number
    :return: word represented by Arabic numerals

    """
    # https://qiita.com/cof/items/58ddf898db25db561a54
    tt_ksuji = str.maketrans('一二三四五六七八九〇壱弐参', '1234567890123')
    re_suji = re.compile(r'[十拾百千万億兆\d]+')
    re_kunit = re.compile(r'[十拾百千]|\d+')
    re_manshin = re.compile(r'[万億兆]|[^万億兆]+')
    TRANSUNIT = {
        '十': 10,
        '拾': 10,
        '百': 100,
        '千': 1000
    }
    TRANSMANS = {
        '万': 10000,
        '億': 100000000,
        '兆': 1000000000000
    }

    def _transvalue(sj, re_obj=re_kunit, transdic=TRANSUNIT):
        unit = 1
        result = 0
        for piece in reversed(re_obj.findall(sj)):
            if piece in transdic:
                if unit > 1:
                    result += unit
                unit = transdic[piece]
            else:
                val = int(piece) if piece.isdecimal() else _transvalue(piece)
                result += val * unit
                unit = 1

        if unit > 1:
            result += unit

        return result

    transuji = kstring.translate(tt_ksuji)
    for suji in sorted(set(re_suji.findall(transuji)), key=lambda s: len(s), reverse=True):
        if not suji.isdecimal():
            arabic = _transvalue(suji, re_manshin, TRANSMANS)
            arabic = str(arabic)
            transuji = transuji.replace(suji, arabic)

    return zenhan.h2z(transuji)


def append_repname(words):
    """

    :param words: a list of Word instances
    :return: a list of Word instances with preprocessed words
             with the representative expressions

    """
    n_word = len(words)
    juman = Jumanpp()
    bar = progressbar.ProgressBar()
    for i in bar(range(n_word), max_value=n_word):
        word = words[i]

        if word.uid != i:
            continue  # already merged

        repname_set = []
        r = juman.analysis(word.p_surface)
        for mrph in r.mrph_list():
            if mrph.bunrui == '数詞':
                repname_set.append([kansuji2arabic(mrph.midasi)])
            elif mrph.repnames() != '':
                repname_set.append(mrph.repnames().split('?'))
            else:
                repname_set.append([mrph.midasi])
        words[i].alias.extend(expand_ambiguity(repname_set))
    return words


def append_synonym_and_formof(words):
    """

    :param words: a list of Word instances
    :return: a list of Word instances with the relational words

    """
    n_word = len(words)
    bar = progressbar.ProgressBar()
    for i in bar(range(n_word), max_value=n_word):
        word = words[i]
        if word.uid != i:
            continue  # already merged

        nodes = []
        for _alias in word.alias:
            query = ''.join([mrph.split('/')[0] for mrph in _alias.split(' ')])
            nodes.extend(request_conceptnet(query, rels=['Synonym', 'FormOf']))
        words[i].alias.extend(nodes)
    return words


def expand_ambiguity(repname_set):
    """

    :param repname: a list of lists which include the repname candidates for morphemes
    :return: a list of repname candidates for morphemes

    """
    expanded_repname_set = ['']
    for repname in repname_set:
        expanded_repname_set = product_list(expanded_repname_set, repname)
    return expanded_repname_set


def product_list(t1, t2):
    return [(_t1 + ' ' + _t2).strip() for _t1 in t1 for _t2 in t2]


def request_conceptnet(query, rels):
    """

    :param query: a concept to request to ConceptNet
    :param rels: relations to filter edges
    :return: concepts to which the query is connected by rels

    """
    nodes = []
    url = 'http://api.conceptnet.io/c/ja/{}'.format(query)
    obj = requests.get(url).json()
    for edge in obj['edges']:
        if edge['rel']['label'] in rels:
            if edge['start']['language'] == 'ja' and edge['start']['label'] != query:
                nodes.append(edge['start']['label'])
            if edge['end']['language'] == 'ja' and edge['end']['label'] != query:
                nodes.append(edge['end']['label'])
    return nodes


def aggregate(words):
    """

    :param words: a list of Word instances
    :return: a list of Word instances with the updated IDs

    """
    n_words = len(words)
    bar = progressbar.ProgressBar()
    for i in bar(range(n_words), max_value=n_words):
        word = words[i]
        if word.uid != i:
            continue  # already merged

        for j in range(i+1, n_words):
            _word = words[j]
            if _word.uid != j:
                continue  # already merged

            if len(set(word.alias) & set(_word.alias)) > 0:
                words[i].alias = list(set(word.alias) | set(_word.alias))
                for k in words[j].anc:
                    words[k].uid = i
                    words[i].anc.append(k)
    return words


def postprocess_word(words):
    """

    :param words: a list of Word instances
    :return: a list of Word instances with the serialized IDs

    """
    n_words = len(words)

    uids = list(set([word.uid for word in words]))
    translator = {uid: i for i, uid in enumerate(uids)}
    bar = progressbar.ProgressBar()
    for i in bar(range(n_words), max_value=n_words):
        words[i].uid = translator[words[i].uid]
    return words


def save(path, words):
    """

    :param path: path to output file
    :param words: a list of Word instances

    """
    with open(path, 'w') as f:
        for word in words:
            f.write('{}\t{}\n'.format(word.surface, word.uid))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('IN', help='path to input file')
    parser.add_argument('OUT', help='path to output file')
    args = parser.parse_args()

    print('[{}] Loading data... '.format(datetime.datetime.now()))
    words = load_file(args.IN)
    print('[{}] Preprocessing data... '.format(datetime.datetime.now()))
    words = preprocess_word(words)
    print('[{}] Merging words... '.format(datetime.datetime.now()))
    words = aggregate(words)

    print('[{}] Getting representative expressions for data... '.format(datetime.datetime.now()))
    words = append_repname(words)
    print('[{}] Merging words... '.format(datetime.datetime.now()))
    words = aggregate(words)

    print('[{}] Getting relational words for data... '.format(datetime.datetime.now()))
    words = append_synonym_and_formof(words)
    print('[{}] Merging words... '.format(datetime.datetime.now()))
    words = aggregate(words)

    print('[{}] Postprocessing data... '.format(datetime.datetime.now()))
    words = postprocess_word(words)

    print('[{}] Writing the result... '.format(datetime.datetime.now()))
    save(args.OUT, words)


if __name__ == '__main__':
    main()
