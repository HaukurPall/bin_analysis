from collections import defaultdict
from pathlib import Path

from tqdm import tqdm

BIN_DATA = Path("/home/haukurpj/Resources/Data/DIM/DIM_2020.06_SHsnid.csv")

unique_lemmas = {}
non_unique_lemmas = defaultdict(list)
with open(BIN_DATA) as f:
    for line in tqdm(f):
        lemma, id, gen, fl, form, pos = line.strip().split(";")
        key = f"{form}-{pos}-{gen}"
        if key in unique_lemmas:
            if unique_lemmas[key] != lemma:
                non_unique_lemmas[form].append(
                    f"{gen}-{pos}={lemma} or {unique_lemmas[key]}"
                )
                # print(f"key={key}, lemma={lemma}, other_lemma={unique_lemmas[key]}")
        else:
            unique_lemmas[key] = lemma

for form, key_lemmas in non_unique_lemmas.items():
    print(f"form={form}, ambiguous={','.join(key_lemmas)}")
