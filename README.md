# Japanese Name Aggregation

A simple command-line tool to aggregate Japanese words.
The aggregation is based on Juman++[Morita+ 15] and ConceptNet5.5[Speer+ 17].

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
```

## Lisence

- MIT

## Reference

- Hajime Morita, Daisuke Kawahara, Sadao Kurohashi, "Morphological Analysis for Unsegmented Languages using Recurrent Neural Network Language Model", EMNLP, 2015.
- Robert Speer, Joshua Chin, Catherine Havasi, "ConceptNet 5.5: An Open Multilingual Graph of General Knowledge", AAAI, 2017.
