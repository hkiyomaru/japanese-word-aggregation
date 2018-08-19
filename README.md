# Japanese Word Aggregation

A simple command-line tool to aggregate Japanese words.
The aggregation is based on Juman++[Morita+ 15] and ConceptNet5.5[Speer+ 17].

## Development Environment

- Python 3.6.0
- Juman++ (see https://github.com/ku-nlp/jumanpp)
- pyknp (see http://nlp.ist.i.kyoto-u.ac.jp/index.php?PyKNP)
- progressbar
- zenhan
- and their dependencies

## Getting Started

First, clone this repository.

```
$ git clone　https://github.com/kiyomaro927/japanese-word-aggregation.git
```

Then, enter the repository.

```
$ cd japanese-word-aggregation/
```

You can see a sample input file which includes one word per one line.

```
$ cat data/input.txt
こんにちは
こんにちわ
こんにちは。
こんにちは!
こんにちは！
いぬ
犬
イヌ
鰤大根
ぶり大根
父
お父さん
父親
1年生
１年生
一年生
12月
１２月
十二月
1万円
１万円
10000円
１００００円
```

Run the script for aggregation.

```
$ python src/aggregate.py data/input.txt data/output.txt
```

You'll get the result as a tab-separated file which includes original words and the IDs to aggregate.

```
$ cat data/output.txt
こんにちは	0
こんにちわ	0
こんにちは。	0
こんにちは!	0
こんにちは！	0
いぬ	1
犬	1
イヌ	1
鰤大根	2
ぶり大根	2
父	3
お父さん	3
父親	3
1年生	4
１年生	4
一年生	4
12月	5
１２月	5
十二月	5
1万円	6
１万円	6
10000円	6
１００００円	6
```

## Lisence

- MIT

## Reference

- Hajime Morita, Daisuke Kawahara, Sadao Kurohashi, "Morphological Analysis for Unsegmented Languages using Recurrent Neural Network Language Model", EMNLP, 2015.
- Robert Speer, Joshua Chin, Catherine Havasi, "ConceptNet 5.5: An Open Multilingual Graph of General Knowledge", AAAI, 2017.
