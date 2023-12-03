# Xiwen 析文

Xiwen is a CLI tool that scans text for Chinese characters (hanzi), and:

- identifies the character variant (simplified or traditional)
- analyses the content by HSK grade
- exports character sets for further use

The analysis describes the percentage of the content covered by each HSK grade(see below), and character lists can be exported for any combination of those levels, or more advanced hanzi not included in the grades.

Data exports provide the hanzi by HSK grade in traditional and simplified Chinese, their pinyin, count within the text, and character frequency.

## Who this is for

Mandarin learners can use Xiwen to determine the expected difficulty of an article or book relative to their current reading level, and create character lists for further study.

Instructors can use it to assess the suitability of reading materials for their students, and produce vocabulary lists.

## HSK

HSK (Hanyu Shuiping Kaoshi 汉语水平考试) is a series of examinations designed to test Chinese language proficiency in simplified Chinese.

In their latest form HSK consists of nine levels, and covers 3,000 simplified hanzi and 11,092 vocabulary items. The advanced levels (seven to nine) share 1,200 hanzi that are tested together.

To approximate a traditional hanzi version of the HSK, Xiwen maps the HSK hanzi to traditional Chinese equivalents. In most cases this is a one-to-one conversion, but in several cases there are two or more traditional hanzi that reflect distinct meanings of the single simplified character.

For example:

- "发": ["發", "髮"]
- "了": ["了", "瞭"]
- "面": ["面", "麵"]

Or even:

- "只": ["只", "衹", "隻"]
- "台": ["台", "檯", "臺", "颱"]

A list of these "polymaps" - not all of which relate to hanzi in the HSK - can be found on the Wikipedia article [Ambiguious character mappings](https://en.wikipedia.org/wiki/Ambiguities_in_Chinese_character_simplification).

This approach isn't perfect: obscure definitions implied by a distinct traditional hanzi may be far less frequent than the common conversion of a simplified hanzi.

The table below lists the number of simplified hanzi per grade, and the number of mappings to traditional equivalents.

| HSK Grade | No. Simplified Hanzi | Running Total | No. Traditional Hanzi Equivalents | Running Total |
| --------- | -------------------- | ------------- | --------------------------------- | ------------- |
| [1]       | 300                  | 300           | 313                               | 313           |
| [2]       | 300                  | 600           | 314                               | 627           |
| [3]       | 300                  | 900           | 312                               | 939           |
| [4]       | 300                  | 1200          | 316                               | 1255          |
| [5]       | 300                  | 1500          | 310                               | 1565          |
| [6]       | 300                  | 1800          | 310                               | 1875          |
| [7-9]     | 1200                 | 3000          | 1214                              | 3089          |

## Installation

Linux/macOS:

```python
git clone git@github.com:essteer/xiwen.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows:

```python
git clone git@github.com:essteer/xiwen.git
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Operation

Run `src/interface.py` from the virtual environment to launch, and follow the instructions as prompted: select a file on your device (.txt only for now) to process, or enter `D` for a demo as prompted at the main menu.

`src/prep.py` makes use of datasets in `data/input` to pair simplified and traditional character sets with their pinyin, HSK grades, and character frequencies as identified in the MTSU dataset.

The datasets needed to run Xiwen are included in the `data` folder. They're set up and ready to go out of the box, but you can run your own character lists through `prep.py` if needed.

`src/interface.py` is the interactive component. It receives your input and makes calls to functions in `src/utils/data_funcs.py`. Those functions then make call to `src/utils/hanzi_funcs.py` to:

- break down text into individual hanzi (`filter_text()`)
- sort hanzi as HSK-level simplified or traditional hanzi, or outliers (`partition_hanzi()`)
- determine the overall character variant of the text as simplified or traditional, or a mix (`identify()`)
- compute the grade-based and cumulative numbers of unique hanzi and total hanzi in the text (`get_stats()`)

Character sets can then be exported to .csv.

## Sources

This repo makes use of datasets of HSK vocabulary and character frequency lists in the public domain as indicated below - credit goes to those involved in their creation and distribution.

Hanyu Shuiping Kaoshi (HSK) 3.0 character list:
"hsk30-chars.csv", [hsk30](https://github.com/ivankra/hsk30), ivankra, GitHub

Character frequency list:
"CharFreq-Modern.csv", Da, Jun. 2004, [Chinese text computing](http://lingua.mtsu.edu/chinese-computing), Middle Tennessee State University

Multiple character mappings:
"[Ambiguious character mappings](https://en.wikipedia.org/wiki/Ambiguities_in_Chinese_character_simplification)", Wikipedia

Simplified character set demo:
"[Folding Beijing](https://web.archive.org/web/20160822161228/http://jessica-hjf.blog.163.com/blog/static/278128102015240444791/)" 《北京折叠》, Hao Jingfang 郝景芳, 2012

Traditional character set demo:
"Tao Te Ching" 《大的經》, Lao Tzu 老子, 400BC

## Planned upgrades

- File handling for .csv and .pdf file imports.
- URL handling to import text direct from webpages.
