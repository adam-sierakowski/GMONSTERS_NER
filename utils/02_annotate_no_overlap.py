import json
import re
import csv
import random
from collections import defaultdict

def remove_overlaps(entities):
    entities = sorted(entities, key=lambda x: (x[0], -(x[1]-x[0])))
    non_overlapping = []
    for ent in entities:
        if not non_overlapping:
            non_overlapping.append(ent)
        else:
            last = non_overlapping[-1]
            if ent[0] < last[1]:
                continue  # overlap, keep longer or earlier one (already sorted)
            else:
                non_overlapping.append(ent)
    return non_overlapping

def main():
    # Load monster wordforms
    with open("../res/data/monsters/monsters_wordforms_big.txt", "r", encoding="utf-8") as f:
        monster_forms = set(line.strip().lower() for line in f if line.strip())

    # Load sentences
    with open("../res/data/dataset/themodders_forum_monster_sentences/themodders_monster_sentences.txt",
        "r", encoding="utf-8") as f:
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
            clean_entities = remove_overlaps(entities)
            data.append([sent, {"entities": clean_entities}])

    random.shuffle(data)
    split_idx = int(len(data) * 0.9)
    train_data = data[:split_idx]
    test_data = data[split_idx:]

    def update_counts(data_split, split_name):
        for sent, _ in data_split:
            lowered = sent.lower()
            for word in monster_forms:
                word_matches = re.findall(r"\b{}\b".format(re.escape(word)), lowered)
                wordform_stats[word][split_name] += len(word_matches)

    update_counts(train_data, "train")
    update_counts(test_data, "test")

    with open("../res/data/dataset/themodders_forum_monster_sentences/monster_big_train.json",
        "w", encoding="utf-8") as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)

    with open("../res/data/dataset/themodders_forum_monster_sentences/monster_big_test.json",
        "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    with open("../res/data/dataset/themodders_forum_monster_sentences/monster_big_stats.csv",
        "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["wordform", "train_count", "test_count"])
        for word, counts in sorted(wordform_stats.items()):
            writer.writerow([word, counts["train"], counts["test"]])

if __name__ == "__main__":
    main()