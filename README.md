<h1 align="center">Xiwen 析文</h1>

<p align="center">
  <a href="https://github.com/essteer/xiwen/actions/workflows/test.yaml"><img src="https://github.com/essteer/xiwen/actions/workflows/test.yaml/badge.svg"></a>
  <a href="https://github.com/essteer/xiwen"><img src="https://img.shields.io/badge/Python-3.9_|_3.10_|_3.11_|_3.12-3776AB.svg?style=flat&logo=Python&logoColor=white"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json"></a>
  <a href="https://snyk.io/test/github/essteer/xiwen"><img src="https://snyk.io/test/github/essteer/xiwen/badge.svg?name=Snyk&style=flat&logo=Snyk"></a>
</p>

<p align="center">
A tool to scan HTML for Chinese characters.
</p>

## Overview 

Use Xiwen to scan websites for Chinese characters — hanzi — and:

- analyse the content by HSK grade
- identify character variants
- export character sets for further use

The analysis describes the breakdown by HSK grade (see below) and character lists can be exported for any combination of those levels, or less common hanzi beyond the HSK grades.

Data exports provide hanzi by HSK grade in traditional and simplified Chinese, their pinyin, count within the text, and character frequency.

## Who this is for

Mandarin learners can use Xiwen to determine the expected difficulty of an article or book relative to their current reading level, and create character lists for further study.

Instructors can use it to assess the suitability of reading materials for their students, and produce vocabulary lists.

## HSK

HSK — Hanyu Shuiping Kaoshi 汉语水平考试 — is a series of examinations designed to test Chinese language proficiency in simplified Chinese.

In its latest form the HSK consists of nine levels, and covers 3,000 simplified hanzi and 11,092 vocabulary items. The advanced levels — seven to nine — share 1,200 hanzi that are tested together.

To approximate a traditional hanzi version of the HSK, Xiwen maps the HSK hanzi to traditional Chinese equivalents. In most cases this is a one-to-one conversion, but in several cases there are two or more traditional hanzi that reflect distinct meanings of the single simplified character.

For example:

- "发": ["發", "髮"]
- "了": ["了", "瞭"]
- "面": ["面", "麵"]

Or even:

- "只": ["只", "衹", "隻"]
- "台": ["台", "檯", "臺", "颱"]

A list of these "polymaps" — not all of which relate to hanzi in the HSK — can be found in the Wikipedia article [Ambiguous character mappings](https://en.wikipedia.org/wiki/Ambiguities_in_Chinese_character_simplification).

This approach isn't perfect: obscure definitions implied by a distinct traditional hanzi may be far less frequent than the common conversion of a simplified hanzi.

The table below lists the number of simplified hanzi per grade, and the number of mappings to traditional equivalents.

| HSK Grade | Simp. Hanzi | Running Total | Trad. Hanzi Equivalents | Running Total |
| :-------: | :---------: | :-----------: | :---------------------: | :-----------: |
|    1    |     300     |      300      |           313           |      313      |
|    2    |     300     |      600      |           314           |      627      |
|    3    |     300     |      900      |           312           |      939      |
|    4    |     300     |     1200      |           316           |     1255      |
|    5    |     300     |     1500      |           310           |     1565      |
|    6    |     300     |     1800      |           310           |     1875      |
|   7-9   |    1200     |     3000      |          1214           |     3089      |

## Installation

### GitHub repo

[![](https://img.shields.io/badge/GitHub-xiwen-181717.svg?flat&logo=GitHub&logoColor=white)](https://github.com/essteer/xiwen)

Clone `xiwen` from GitHub for the full code, files used to generate the character lists and a test suite.

```console
$ git clone git@github.com:essteer/xiwen
```

Change into the `xiwen` directory then create and activate a virtual environment — the below example uses [Astral's](https://astral.sh/blog/uv) `uv`; substitute `pip` or use another package manager as needed — then install the `dev` dependencies:

![](https://img.shields.io/badge/Linux-FCC624.svg?style=flat&logo=Linux&logoColor=black)
![](https://img.shields.io/badge/macOS-000000.svg?style=flat&logo=Apple&logoColor=white)

```console
$ uv venv
$ source .venv/bin/activate
$ uv pip install -r requirements.txt
```

![](https://img.shields.io/badge/Windows-0078D4.svg?style=flat&logo=Windows&logoColor=white)

```console
$ uv venv
$ .venv\Scripts\activate
$ uv pip install -r requirements.txt
```

## Operation

### GitHub repo

[![](https://img.shields.io/badge/GitHub-xiwen-181717.svg?flat&logo=GitHub&logoColor=white)](https://github.com/essteer/xiwen)

To run `xiwen` as a CLI tool, navigate to the project root directory and run:

![](https://img.shields.io/badge/Linux-FCC624.svg?style=flat&logo=Linux&logoColor=black)
![](https://img.shields.io/badge/macOS-000000.svg?style=flat&logo=Apple&logoColor=white)

```console
$ source .venv/bin/activate
$ python3 -m main
```

![](https://img.shields.io/badge/Windows-0078D4.svg?style=flat&logo=Windows&logoColor=white)

```console
$ .venv\Scripts\activate
$ python -m main
```

The `src/resources/` directory contains `main.py`, which was used to create the dataset needed to run this program under `src/xiwen/assets/` by pairing simplified and traditional character sets with their pinyin, HSK grades, and character frequencies as identified in the MTSU dataset. The source data is kept under `src/resources/assets/`.

The functional program is contained in `src/xiwen/`. `interface.py` is the interactive component for the CLI tool. It receives user input and makes function calls to modules in `utils/`. Those files form the program's ETL pipeline including the following functions:

- break down text into individual hanzi (`extract.py`)
- sort hanzi as HSK-level simplified or traditional hanzi, or outliers (`transform.py`)
- determine the overall character variant of the text as simplified or traditional, or a mix (`analyse.py`)
- compute the grade-based and cumulative numbers of unique hanzi and total hanzi in the text (`analyse.py`)

Character sets can then be exported to CSV.

## Sources

This repo makes use of datasets of HSK vocabulary and character frequency lists in the public domain as indicated below - credit goes to those involved in their creation and distribution.

- Hanyu Shuiping Kaoshi (HSK) 3.0 character list: "hsk30-chars.csv", [hsk30](https://github.com/ivankra/hsk30), ivankra, GitHub

- Character frequency list: "CharFreq-Modern.csv", Da, Jun. 2004, [Chinese text computing](http://lingua.mtsu.edu/chinese-computing), Middle Tennessee State University

- Multiple character mappings: "[Ambiguous character mappings](https://en.wikipedia.org/wiki/Ambiguities_in_Chinese_character_simplification)", Wikipedia

- Simplified character set demo: "[Folding Beijing](https://web.archive.org/web/20160822161228/http://jessica-hjf.blog.163.com/blog/static/278128102015240444791/)" 《北京折叠》, Hao Jingfang 郝景芳, 2012

- Traditional character set demo: "Tao Te Ching" 《道德經》, Lao Tzu 老子, 400BC
