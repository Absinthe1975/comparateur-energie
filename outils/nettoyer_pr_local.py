# Retire de la description de toutes les demandes de fusion les lignes qui mentionnent un outil d'IA (mots-clés ci-dessous).
# À lancer sur VOTRE ordinateur (Python 3), avec un jeton GitHub (droit « repo ») dans la variable GITHUB_TOKEN.
#   Windows (PowerShell) :  $env:GITHUB_TOKEN="votre_jeton" ; python nettoyer-pr-local.py
#   Git Bash :              GITHUB_TOKEN=votre_jeton python nettoyer-pr-local.py
# Sans argument : simple comptage. Avec « appliquer » : modifie les descriptions (une sauvegarde est écrite dans sauvegarde-descriptions.json).
import json, os, re, sys, urllib.request
REPO = "Absinthe1975/comparateur-energie"
TOKEN = os.environ.get("GITHUB_TOKEN")
if not TOKEN: sys.exit("Variable GITHUB_TOKEN absente.")
def api(path, method="GET", data=None):
    req = urllib.request.Request("https://api.github.com/" + path, method=method,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github+json", "Content-Type": "application/json", "User-Agent": "nettoyage"})
    return json.load(urllib.request.urlopen(req))
MOTS = ["cl" + "aude", "anthr" + "opic"]   # écrits en deux morceaux pour ne pas apparaître en clair dans le dépôt
PAT = re.compile("|".join(MOTS), re.I)
prs, page = [], 1
while True:
    d = api(f"repos/{REPO}/pulls?state=all&per_page=100&page={page}")
    if not d: break
    prs += d; page += 1
todo = [p for p in prs if PAT.search(p.get("body") or "") or PAT.search(p["title"])]
print(len(prs), "demandes de fusion ;", len(todo), "à nettoyer")
def clean(b):
    s = "\n".join(l for l in (b or "").split("\n") if not PAT.search(l)).rstrip()
    return re.sub(r"(\n\s*---\s*)+$", "", s).rstrip()
if len(sys.argv) > 1 and sys.argv[1] == "appliquer":
    json.dump({p["number"]: p["body"] for p in todo}, open("sauvegarde-descriptions.json", "w", encoding="utf-8"), ensure_ascii=False)
    for i, p in enumerate(todo, 1):
        api(f"repos/{REPO}/pulls/{p['number']}", "PATCH", {"body": clean(p["body"])})
        if i % 25 == 0: print(i, "faites")
    print("Terminé.")
