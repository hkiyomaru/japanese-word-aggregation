# Japanese Name Aggregation

A simple command-line tool to aggregate Japanese words.
The aggregation is based on the representative name of words given by Juman++.

## Development Environment

- Python 3.6.0
- Juman++ (see https://github.com/ku-nlp/jumanpp)
- pyknp (see http://nlp.ist.i.kyoto-u.ac.jp/index.php?PyKNP)
- progressbar
- zenhan

## Getting Started

First, clone this repository.

```
$ git clone　https://github.com/kiyomaro927/name-aggregation.git
```

Then, enter the repository.

```
$ cd name-aggregation/
```

You can see a sample input file. Put one word per one line.

```
$ cat data/input.txt
こんにちは
こんにちわ
いぬ
犬
イヌ
ねこ
ネコ
猫
鰤大根
ぶり大根
1年生
１年生
一年生
```

Run the script for aggregation.

```
$ python src/aggregate.py data/input.txt data/output.txt
```

You'll get the result as a tab-separated file which includes original words and the IDs to aggregate.

```
$ cat data/output.txt
こんにちは      0
こんにちわ      1  # TODO: Access ConceptNet to retrieve `Sysnonym` and `FormOf` of words
いぬ    2
犬      2
イヌ    2
ねこ    3
ネコ    3
猫      3
鰤大根  4
ぶり大根        4
1年生   5
１年生  5
一年生  6  # TODO: Convert Kansuji to Arabic numerals
```

## Lisence

- MIT
