# latent space browser

Type a word and see, for each dimension of its embedding, the words that share
that axis-band but are otherwise most similar to it — plus the 10 nearest words
overall. English + Japanese live in one **aligned** space (ConceptNet
Numberbatch 300d), so `king` finds `王`, `国王`, `キング`.

**Live:** enable GitHub Pages (below), then visit the Pages URL.

Single static page: [`index.html`](index.html) + [`vectors.json`](vectors.json)
(9k words × 300d). No backend — everything runs in the browser.

## Run locally

```sh
python3 -m http.server 8017   # then open http://localhost:8017
```

## Deploy to GitHub Pages

1. Push this repo to GitHub.
2. Repo **Settings → Pages → Build and deployment → Source: Deploy from a branch**.
3. Branch: `main`, folder: `/ (root)`. Save.
4. Wait ~1 min; the site is at `https://<user>.github.io/<repo>/`.

`.nojekyll` is included so files are served as-is.

## Rebuild the data (optional)

`vectors.json` is committed, so you don't need this to deploy. To regenerate it,
merge English + Japanese from Numberbatch (uses `en_freq.txt` and `ja_freq.txt`,
the frequency word lists, both committed — top ~12k of each language):

```sh
curl -s https://conceptnet.s3.amazonaws.com/downloads/2019/numberbatch/numberbatch-19.08.txt.gz \
  | python3 build_ml.py
```
