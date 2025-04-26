import re

with open("../monsters/02_monsters_declined_deduplicated.txt", "r") as patterns_file:
    stats = []
    for line in patterns_file:
        pattern = r"\b(" + line.strip() + r")\b"
        stats.append({"pattern": pattern, "count": 0})

with open("themodders_monster_sentences.txt", "r") as input_f:
    for line in input_f:
        for row in stats:
            if count := re.findall(row["pattern"], line, flags=re.IGNORECASE):
                row["count"] += len(count)

import pandas as pd

df = pd.DataFrame.from_dict(stats)
df.to_csv("03_stats.csv")