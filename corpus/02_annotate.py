import json
import re
import csv
import random
from collections import defaultdict

# Load monster wordforms
# with open("../monsters/monsters_wordforms_small.txt", "r", encoding="utf-8") as f:
with open("../monsters/monsters_wordforms_big.txt", "r", encoding="utf-8") as f:
    monster_forms = set(line.strip().lower() for line in f if line.strip())

# Load sentences
# with open("themodders_forum_monster_sentences_small/themodders_monster_sentences_small.txt", "r", encoding="utf-8") as f:
with open("themodders_forum_monster_sentences_big/themodders_monster_sentences_big.txt", "r", encoding="utf-8") as f:
    sentences = [line.strip() for line in f if line.strip()]

data = []
wordform_stats = defaultdict(lambda: {"train": 0, "test": 0})

for sent in sentences:
    entities = []
    lowered = sent.lower()
    for word in monster_forms:
        for match in re.finditer(r"\b{}\b".format(re.escape(word)), lowered):
            start, end = match.span()
            entities.append([start, end, "MONSTER"])
    if entities:
        data.append([sent, {"entities": entities}])

random.shuffle(data)
split_idx = int(len(data) * 0.9)
train_data = data[:split_idx]
test_data = data[split_idx:]

# Count stats
def update_counts(data_split, split_name):
    for sent, _ in data_split:
        lowered = sent.lower()
        for word in monster_forms:
            if re.search(r"\b{}\b".format(re.escape(word)), lowered):
                wordform_stats[word][split_name] += len(re.findall(r"\b{}\b".format(re.escape(word)), lowered))

update_counts(train_data, "train")
update_counts(test_data, "test")

# Save JSONs
# with open("monster_small_train.json", "w", encoding="utf-8") as f:
with open("monster_big_train.json", "w", encoding="utf-8") as f:
    json.dump(train_data, f, ensure_ascii=False, indent=2)

# with open("monster_small_test.json", "w", encoding="utf-8") as f:
with open("monster_big_test.json", "w", encoding="utf-8") as f:
    json.dump(test_data, f, ensure_ascii=False, indent=2)

# Save stats CSV
# with open("monster_small_stats.csv", "w", newline="", encoding="utf-8") as f:
with open("monster_big_stats.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["wordform", "train_count", "test_count"])
    for word, counts in sorted(wordform_stats.items()):
        writer.writerow([word, counts["train"], counts["test"]])
