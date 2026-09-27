# SocrateAI — Condensed Matter Theory : AdS/CMT

Corpus de recherche et pipeline RAG sur la **correspondance AdS/CMT** et la
**correspondance volume–frontière**, branché sur le vector store Chroma
d'AutoevolveAI (ANSE).

- **Revue de littérature** : [`docs/literature_review.md`](docs/literature_review.md)
- **Corpus** : 47 articles arXiv, métadonnées + PDF, définis dans
  [`corpus/seed_papers.py`](corpus/seed_papers.py)
- **Collection Chroma** : `adscmt_literature`, dans le store ANSE
  `~/AutoevolveAI/data/chroma`

---

## 1. Architecture

```
corpus/seed_papers.py    liste (arxiv_id, pilier, fragment_de_titre_attendu)
corpus/fetch_papers.py   API arXiv -> papers/meta/*.json, papers/pdf/*.pdf, papers/index.json
corpus/ingest_chroma.py  découpage + embeddings -> collection adscmt_literature
corpus/query_chroma.py   interrogation et vérification en ligne de commande
mcp_adscmt_rag.py        serveur MCP exposant la recherche aux agents
config/mcp.json.example  configuration MCP à recopier en .mcp.json
```

### Deux garde-fous, hérités de la philosophie « fail closed » d'ANSE

**Contrôle d'identité à la récupération.** Chaque entrée de `seed_papers.py`
porte un fragment du titre attendu. `fetch_papers.py` refuse tout article dont
le titre réel arXiv ne contient pas ce fragment, et le signale au lieu de
l'indexer. Ce n'est pas théorique : la première passe a rejeté 6 identifiants
sur 47 — parmi eux, `1304.4926` supposé être « Cool horizons for entangled
black holes » est en réalité « Generalized gravitational entropy ». Sans ce
contrôle, six articles faux seraient entrés dans le vector store, et rien ne
l'aurait signalé.

**Refus de l'embedding non sémantique.** ANSE embarque deux fonctions
d'embedding. `anse/memory/chroma_rag.py::FastDeterministicEmbeddingFunction`
construit des vecteurs 384-d par md5 sur des n-grammes de caractères ; la
documentation d'ANSE elle-même (`anse/memory/ollama_embeddings.py`) précise que
les plus proches voisins y sont des collisions de hash et non des sens voisins,
et qu'elle ne doit jamais servir de socle à une recherche présentée comme
sémantique. Ce pipeline utilise donc **`OllamaEmbeddingFunction`**
(`qwen3-embedding:0.6b`, 1024-d, vérifié en direct sur cet hôte), **importée
depuis ANSE** et non recopiée, pour qu'il n'existe qu'une seule définition. Si
Ollama est injoignable, l'ingestion s'arrête ; elle ne se rabat jamais sur la
fonction de hash, parce qu'une collection mélangeant les deux est
irrécupérable — les vecteurs ont la même forme et ne portent aucun marqueur.

---

## 2. Prérequis

```bash
# Ollama, avec le modèle d'embedding d'ANSE
ollama pull qwen3-embedding:0.6b
curl -s http://localhost:11434/api/tags | grep qwen3-embedding

# Dépendances Python
python3 -m pip install --user chromadb pypdf "mcp>=1.2" httpx
```

La collection doit rester en `1024-d`. `qwen3-embedding:0.6b` est la seule
source de vérité ; changer de modèle impose de recréer la collection.

---

## 3. Utilisation

```bash
# 1. Récupérer le corpus (métadonnées + PDF, ~54 Mo)
python3 corpus/fetch_papers.py
python3 corpus/fetch_papers.py --no-pdf     # métadonnées seules

# 2. Ingérer dans Chroma
python3 corpus/ingest_chroma.py --dry-run   # découpage seul, aucune écriture
python3 corpus/ingest_chroma.py             # ~1500 chunks
python3 corpus/ingest_chroma.py --abstracts-only   # rapide : 47 chunks

# 3. Vérifier
python3 corpus/query_chroma.py --verify

# 4. Interroger
python3 corpus/query_chroma.py "why do topological insulators have edge states"
python3 corpus/query_chroma.py "strange metal transport" --pillar adscmt -n 3
```

L'ingestion complète est **bornée par le CPU** : les embeddings passent par
Ollama un chunk à la fois. Compter plusieurs dizaines de minutes pour les
~1500 chunks. `--abstracts-only` donne un index utilisable en une minute.

`--verify` n'imprime pas seulement des statistiques : il vérifie que la
dimension vaut bien 1024 et lance six requêtes-sondes dont le résultat attendu
est un article précis, puis sort en code non nul si l'une échoue. Il peut donc
servir de porte dans un pipeline.

---

## 4. Configuration MCP

`.mcp.json` est un fichier protégé par Claude Code, il n'a donc pas été écrit
automatiquement. Pour l'activer :

```bash
cp config/mcp.json.example .mcp.json
```

Puis relancer Claude Code et approuver les serveurs.

### `adscmt-rag` — le serveur du corpus

Trois outils : `adscmt_search(query, n_results, pillar)`,
`adscmt_paper(arxiv_id)`, `adscmt_corpus_stats()`.

**Pourquoi un serveur maison plutôt que `chroma-mcp` seul.** `chroma-mcp`
atteint bien ce store (`--client-type persistent --data-dir ...`), mais n'offre
aucune option d'embedding Ollama : ses choix sont `default`, `cohere`,
`openai`, `jina`, `voyageai`, `roboflow`. Il interrogerait donc une collection
écrite en 1024-d avec son modèle par défaut en 384-d. Le serveur `adscmt-rag`
interroge avec **exactement** la fonction d'embedding utilisée à l'ingestion.

### `chroma-admin` — inspection générique

`chroma-mcp` est conservé pour l'administration : lister les collections,
compter, récupérer des documents par identifiant. Ces opérations ne passent pas
par l'embedding. En revanche, **`chroma_query_documents` sur
`adscmt_literature` échouera** sur une erreur de dimension (384 vs 1024) —
c'est un échec bruyant, pas un résultat silencieusement faux. Pour la recherche
sémantique, utiliser `adscmt-rag`.

### `leanmaster`

Serveur MCP du dépôt frère SocrateAI-Agora-LeanMaster, pour les théorèmes Lean 4
vérifiés par le noyau (réseaux, T-dualité, O(d,d), K3). Utile ici parce que la
classification en dix classes repose sur la périodicité de Bott et la
K-théorie, déjà partiellement formalisées de ce côté.

---

## 5. Le corpus

| Pilier | N | Contenu |
|---|---:|---|
| `holography` | 11 | AdS/CFT, entropie d'intrication holographique, codes QEC |
| `adscmt` | 13 | supraconducteurs holographiques, non-Fermi liquides, SYK |
| `topology` | 12 | effet Hall de spin quantique, classification en dix classes |
| `bridge` | 11 | anomalies, spectre d'intrication, semi-métaux holographiques |

Les PDF (`papers/pdf/`) ne sont pas versionnés — `corpus/fetch_papers.py` les
régénère à l'identique. Les métadonnées (`papers/meta/`, `papers/index.json`)
le sont.

---

## 6. Note de fond

La revue corrige un point du cadrage initial, et c'est important pour la suite :
les isolants topologiques et AdS/CFT ne sont **pas** le même énoncé de
correspondance volume–frontière. La direction de l'encodage s'inverse (volume →
frontière d'un côté, frontière → volume de l'autre), et la frontière
holographique n'est pas topologique — c'est une CFT fortement couplée, avec une
infinité de degrés de liberté locaux, là où une TQFT n'en a aucun.

Ce qui relie réellement les deux : l'écoulement d'anomalie (le seul mécanisme
littéralement identique des deux côtés), l'intrication comme langage commun, les
réalisations holographiques explicites de matière topologique, et la structure
de code correcteur quantique. Détails en
[§5 de la revue](docs/literature_review.md).

L'anecdote de départ sur Shinsei Ryu est exacte, et plus forte que présentée :
avec Takayanagi, il signe `hep-th/0603001` (entropie d'intrication
holographique) **et** `1001.0763` (« Topological Insulators and Superconductors
from D-branes »), qui réalise la table périodique dans la théorie des cordes.
C'est la jonction littérale des deux domaines, par les deux mêmes auteurs.
