# 🧌 gmonsters_ner – Custom Polish Monster NER

This project is an exercise in training custom Named Entity Recognition (NER) model in Spacy.

It contains a model trained to detect monster names from the games Gothic, Gothic 2 and Gothic 2: Night of the Raven (e.g. *goblin*, *ścierwojadów*, *orkiem-szamanem*) in Polish forum-style texts.

Built using spaCy and trained on automatically annotated sentences from themodders.org forum.

👀 Note: model recognizes *inflected* Polish wordforms without lemmatization.

Base Spacy model: pl_core_news_md

# 🔍 Example

input:
```
Ścierwojady – tak nazywamy te wielkie ptaszyska – należy atakować jeden po drugim.
```
output:
```
[('Ścierwojady', 'MONSTER')]
```

# 🛠 How to use

```bash
pip install spacy
```

```python
import spacy
nlp = spacy.load("gmonsters_ner_0.1")

doc = nlp("A i na wszelki wypadek, gdyby nie chciał się pojawić ścierwojad i ten ork podaję na nich kody:")
print([(ent.text, ent.label_) for ent in doc.ents])
```

# 📊 Metrics

On the held-out test set:
- Precision: ~86%
- Recall: ~91%
- F1-score: ~89%

I could train the model for more epochs to achieve better scores, but I like it that currently it also recognizes novel monsters that were not annotated in the training and test datasets (see the note in next section). This drives the recall down. The downside is that it could also recognize false positives.

Ideally it would be better to drive precision up and keep recall at about 90%, but this is a toy project.

# 🖋️ How the annotations were created

1. Monster lemmas were taken from the games fan wikis ([1](https://gothic.fandom.com/pl/wiki/Bestiariusz_w_Gothic), [2](https://gothic.fandom.com/pl/wiki/Bestiariusz_w_Gothic_II), [2NOTR](https://gothic.fandom.com/pl/wiki/Bestiariusz_w_Gothic_II:_Noc_Kruka))
2. Lemmas were expanded to wordforms using a mixed approach:
    - [polimorf dictionary](https://zil.ipipan.waw.pl/PoliMorf): the most common monsters, found in the "small" subset
    - ChatGPT: all the other monsters
    - (something like an ML-based reversed lemmatizer would be the best for this task but I couldn't find it)
3. The annotations were created by marking the span of every wordform whenever it appeared in the paragraph.

👀 Note: the annotation is based on a list of monsters that already exist in the games, but the dataset is based on a forum about modifying the game, so it actually contains mentions of novel monsters.

# 📂 Contents

```bash
./corpus:
00_scrap.py  # Scrap text from forum
01_filter_corpus.py  # Filter the scrapped text to contain only paragraphs mentioning monsters
02_annotate_no_overlap.py  # Annotate the sentences to create train and test datasets

./corpus/themodders_forum_compact:
themodders.txt  # Scrapped contents from forum

./corpus/themodders_forum_monster_sentences_big:
monster_big_no_overlap_stats.csv  # Stats: which wordforms appear in each dataset split
monster_big_no_overlap_test.json  # Annotated test dataset
monster_big_no_overlap_train.json  # Annotated train dataset
themodders_monster_sentences_big.txt  # Filtered corpus with paragraphs mentioning monsters

./model:
train_0.1.ipynb  # Train the model
evaluate.ipynb  # Evaluate the model


./model/gmonsters_ner_0.1  # The resulting model
./model/gmonsters_ner_0.1/ner  # The custom NER pipeline that was created
./model/gmonsters_ner_0.1/*  # All the rest of the model (should be same as Spacy pl_core_news_md)

./monsters:
monsters_wordforms_big.txt  # Wordforms that were used to create annotations
monsters_wordforms_small.txt  # A subset of the "big" file
```

## 📜 License

This repository is licensed under the MIT License.  
You are free to use, modify, and distribute the code and trained model.

**Data Disclaimer**:  
The training data was derived from publicly available posts on themodders.org.  
If you are the copyright holder and have concerns about the inclusion of this data,  
please contact the repository maintainer to request removal or clarification.
