with open("01_monsters_declined_gpt.txt", "r") as input_f, \
open("02_monsters_declined_deduplicated.txt", "w") as output_f:
    for line in input_f:
        deduplicated = "|".join(sorted(list(set(line.strip().split(";"))))).replace("||", "|")
        if deduplicated.startswith("|"):
            deduplicated = deduplicated[1:]
        output_f.write(deduplicated + "\n")