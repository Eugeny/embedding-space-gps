import gzip, json, sys, re
# common english words (word list only) from the earlier GloVe build
common_en = set(json.load(open("vectors.glove.json"))["words"])

# common japanese words from a local frequency list, pure Japanese script, keep freq rank
ja_ok = re.compile(r"^[぀-ヿ一-龯々ー]+$")
hira = re.compile(r"^[぀-ゟ]$")   # single hiragana = particle, skip
ja_rank, want_ja = {}, set()
for line in open("ja_freq.txt", encoding="utf-8"):
    w = line.split(" ")[0]
    if ja_ok.match(w) and not hira.match(w) and w not in ja_rank:
        ja_rank[w] = len(ja_rank); want_ja.add(w)
        if len(want_ja) >= 6000: break

EN_MAX = 5000
en_re = re.compile(r"[a-z]+$")
en_w, en_v, ja_w, ja_v = [], [], [], []
gz = gzip.GzipFile(fileobj=sys.stdin.buffer)
dim = int(gz.readline().split()[1])
for raw in gz:
    line = raw.decode("utf-8", "ignore")
    sp = line.find(" ")
    parts = line[:sp].split("/")            # ['', 'c', 'en', 'king']
    if len(parts) < 4:
        continue
    lang, word = parts[2], parts[3]
    if lang == "en":
        if len(en_w) < EN_MAX and word in common_en and en_re.match(word):
            en_w.append(word); en_v.append([round(float(x), 4) for x in line[sp+1:].split()])
    elif lang == "ja":
        if word in want_ja:
            ja_w.append(word); ja_v.append([round(float(x), 4) for x in line[sp+1:].split()])
    elif lang > "ja":                        # past the ja block
        break

# order japanese by frequency rank
order = sorted(range(len(ja_w)), key=lambda k: ja_rank[ja_w[k]])
ja_w = [ja_w[k] for k in order]; ja_v = [ja_v[k] for k in order]

words = en_w + ja_w
vecs = en_v + ja_v
langs = ["en"] * len(en_w) + ["ja"] * len(ja_w)
json.dump({"dim": dim, "words": words, "langs": langs, "vecs": vecs},
          open("vectors.json", "w"), separators=(",", ":"), ensure_ascii=False)
print("en", len(en_w), "ja", len(ja_w), "dim", dim)
