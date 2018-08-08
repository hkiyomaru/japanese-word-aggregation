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
いぬ
犬
イヌ
ねこ
ネコ
猫
鰤大根
ぶり大根
1年生
一年生
１年生
```

Run the script for aggregation.

```
$ python src/aggregate.py data/input.txt data/output.txt
```

You'll get the result as a tab-separated file which includes original words and the IDs to aggregate.

```
$ cat data/output.txt
こんにちは	0
いぬ	1
犬	1
イヌ	1
ねこ	2
ネコ	2
猫	2
鰤大根	3
ぶり大根	3
1年生	4
一年生	4
１年生	4
```

## Lisence

- MIT
