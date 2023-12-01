# Xiwen 析文

Xiwen scans text for Chinese characters (hanzi), and:

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

The first six levels cover approximately 2,660 of the most frequently used hanzi, and around 5,000 vocabulary items (typically consisting of either one or two characters).

Xiwen maps the HSK hanzi to traditional Chinese equivalents, for use on either character variant.

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

## Usage

Run `src/interface.py` to launch, and follow the instructions as prompted: select a file on your device (.txt only for now) to process, or enter `D` for a demo as prompted at the main menu.

`src/prep.py` makes use of datasets in `data/input` to pair simplified and traditional character sets with their pinyin, HSK grades, and character frequencies as identified in the MTSU dataset.

The datasets needed to run Xiwen are included in the `data` folder. They're set up and ready to go out of the box, but you can run your own character lists through `prep.py` if needed.

`src/interface.py` is the interactive component. It receives your input and makes calls to functions in `src/utils/hanzi_funcs.py` to:

- break down text into individual hanzi (`filter_text()`)
- sort hanzi as HSK-level simplified or traditional hanzi, or outliers (`partition_hanzi()`)
- determine the overall character variant of the text as simplified or traditional, or a mix (`identify()`)
- compute the grade-based and cumulative numbers of unique hanzi and total hanzi in the text (`get_stats()`)

Character sets can then be exported to .csv.

## Sources

This repo makes use of datasets of HSK vocabulary and character frequency lists in the public domain as indicated below - my thanks to those involved in their creation and distribution.

Character frequency list:
"CharFreq-Modern.csv", Da, Jun. 2004, Chinese text computing, [http://lingua.mtsu.edu/chinese-computing](http://lingua.mtsu.edu/chinese-computing)

Hanyu Shuiping Kaoshi (HSK) vocabulary list:
"HSK 2013 Pleco.txt", alanmd, 2013, Pleco forums, [https://www.plecoforums.com/threads/new-hsk-levels-1-6.2950/](https://www.plecoforums.com/threads/new-hsk-levels-1-6.2950/)

Multiple character mappings:
"[Ambiguious character mappings](https://en.wikipedia.org/wiki/Ambiguities_in_Chinese_character_simplification)", Wikipedia

Simplified character set demo:
"[Folding Beijing](https://web.archive.org/web/20160822161228/http://jessica-hjf.blog.163.com/blog/static/278128102015240444791/)" 《北京折叠》, Hao Jingfang 郝景芳, 2012

Traditional character set demo:
"Tao Te Ching" 《大的經》, Lao Tzu 老子, 400BC

## Planned upgrades

- File handling for .csv and .pdf file imports.
- URL handling to import text direct from webpages.
- Expansion to cover the new HSK7-9 band introduced in 2021/2022.
