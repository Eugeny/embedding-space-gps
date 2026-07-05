import gzip, json, sys, re
# common words from frequency lists (local), pure-script, keeping frequency rank
EN_MAX, JA_MAX = 12000, 12000

def load_freq(path, ok, skip=None, cap=None):
    rank = {}
    for line in open(path, encoding="utf-8"):
        w = line.split(" ")[0]
        if ok.match(w) and (skip is None or not skip.match(w)) and w not in rank:
            rank[w] = len(rank)
            if cap and len(rank) >= cap: break
    return rank

en_rank = load_freq("en_freq.txt", re.compile(r"^[a-z]+$"), cap=EN_MAX * 3)
ja_rank = load_freq("ja_freq.txt", re.compile(r"^[぀-ヿ一-龯々ー]+$"),
                    skip=re.compile(r"^[぀-ゟ]$"), cap=JA_MAX * 3)
want_en, want_ja = set(en_rank), set(ja_rank)

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
    if lang == "en" and word in want_en:      # collect ALL matches (block is alphabetical)
        en_w.append(word); en_v.append([round(float(x), 3) for x in line[sp+1:].split()])
    elif lang == "ja" and word in want_ja:
        ja_w.append(word); ja_v.append([round(float(x), 3) for x in line[sp+1:].split()])
    elif lang > "ja":                          # scanned past the ja block
        break

# keep the most frequent MAX that actually exist in Numberbatch (rank order)
def top_by_rank(ws, vs, rank, cap):
    idx = sorted(range(len(ws)), key=lambda k: rank[ws[k]])[:cap]
    return [ws[k] for k in idx], [vs[k] for k in idx]
en_w, en_v = top_by_rank(en_w, en_v, en_rank, EN_MAX)
ja_w, ja_v = top_by_rank(ja_w, ja_v, ja_rank, JA_MAX)

json.dump({"dim": dim, "words": en_w + ja_w, "vecs": en_v + ja_v,
           "langs": ["en"] * len(en_w) + ["ja"] * len(ja_w)},
          open("vectors.json", "w"), separators=(",", ":"), ensure_ascii=False)
print("en", len(en_w), "ja", len(ja_w), "dim", dim)
