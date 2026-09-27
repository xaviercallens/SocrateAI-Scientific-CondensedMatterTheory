# SocrateAI — Condensed Matter Theory : AdS/CMT

Deux volets, reliés par la **correspondance volume–frontière** :

1. **Théorie** — revue de littérature sur AdS/CMT et les isolants topologiques,
   corpus de 73 articles arXiv, et pipeline RAG branché sur le vector store
   Chroma d'AutoevolveAI (ANSE).
2. **Expérience** — programme « Garage Deep Tech » en 5 axes (matériel de
   récupération → données → TDA Gudhi → preuve Lean 4), revu de façon critique
   et préenregistré.

Les deux sont tenus par un même **protocole de rigueur** de type *elenchus* :
toute affirmation doit avoir été exposée à une manière précise d'échouer.

## Par où commencer

| Document | Contenu |
|---|---|
| [`docs/experimental_program.md`](docs/experimental_program.md) | **Revue critique du plan en 5 axes** : verdicts de faisabilité chiffrés, erreurs de physique, protocoles révisés, ordre d'exécution |
| [`docs/literature_review.md`](docs/literature_review.md) | Revue de littérature AdS/CMT ↔ isolants topologiques |
| [`docs/ryu_review.md`](docs/ryu_review.md) | **Le programme de Shinsei Ryu**, depuis son dossier arXiv complet (202 articles) |
| [`docs/contribution_map.md`](docs/contribution_map.md) | **Où votre expertise contribue** (Lean, GPU, Rust, HPC, Gudhi, IA) : trois projets classés |
| [`docs/assets/README.md`](docs/assets/README.md) | Actifs réutilisables de cette machine, vérifiés un par un |
| [`docs/rigor_protocol.md`](docs/rigor_protocol.md) | Protocole Elenchus : 5 portes, préenregistrement, verdicts |
| [`docs/safety.md`](docs/safety.md) | **À lire avant toute manipulation** : four à micro-ondes, lasers, eau |
| [`lean/README.md`](lean/README.md) | Échelle des objectifs Lean 4, T0 → T3 |
| `experiments/axis*/PREREGISTRATION.md` | Un préenregistrement par axe, à commiter **avant** toute acquisition |

---

## 1. Architecture

```
docs/
  literature_review.md       revue AdS/CMT ↔ isolants topologiques
  ryu_review.md              le programme de Shinsei Ryu (202 articles)
  contribution_map.md        expertise → contributions, trois projets classés
  experimental_program.md    revue critique du plan expérimental en 5 axes
  rigor_protocol.md          protocole Elenchus : portes, préenregistrement, verdicts
  safety.md                  sécurité : micro-ondes, lasers, eau
  assets/                    inventaire des actifs de la machine ; dossier arXiv de Ryu
tools/
  inventory_assets.py        inventaire en lecture seule des dépôts de la machine
  arxiv_author.py            dossier arXiv complet d'un auteur
experiments/
  axis1_topological_waves/   SSH 1D puis valley-Hall 2D, aquarium
  axis2_analogue_horizon/    superradiance sur vortex de vidange
  axis3_vortex/              vortex acoustique (ou hologramme en fourche)
  axis4_wave_chaos/          billard micro-ondes + VNA, loi de Weyl
  axis5_caustics/            caustiques, classification d'Arnold
lean/                        échelle des théorèmes, T0 → T3
corpus/
  seed_papers.py             liste (arxiv_id, pilier, fragment_de_titre_attendu)
  fetch_papers.py            API arXiv -> papers/meta, papers/pdf, papers/index.json
  ingest_chroma.py           découpage + embeddings -> collection adscmt_literature
  query_chroma.py            interrogation et vérification (--verify)
papers/                      métadonnées versionnées ; PDF régénérables (non versionnés)
mcp_adscmt_rag.py            serveur MCP exposant la recherche aux agents
config/mcp.json.example      configuration MCP à recopier en .mcp.json
```

### Deux garde-fous, hérités de la philosophie « fail closed » d'ANSE

**Contrôle d'identité à la récupération.** Chaque entrée de `seed_papers.py`
porte un fragment du titre attendu. `fetch_papers.py` refuse tout article dont
le titre réel arXiv ne contient pas ce fragment, et le signale au lieu de
l'indexer. Ce n'est pas théorique : la première passe a rejeté 6 identifiants
sur 36 — parmi eux, `1304.4926` supposé être « Cool horizons for entangled
black holes » est en réalité « Generalized gravitational entropy ». Plus tard,
elle a encore rejeté le titre d'Altland–Zirnbauer cité de mémoire. Sans ce
contrôle, ces articles faux seraient entrés dans le vector store, et rien ne
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
python3 corpus/ingest_chroma.py --dry-run            # découpage seul, aucune écriture
python3 corpus/ingest_chroma.py --abstracts-only --resume   # 73 chunks
python3 corpus/ingest_chroma.py --resume             # texte intégral, ~1500 chunks

# 3. Vérifier
python3 corpus/query_chroma.py --verify

# 4. Interroger
python3 corpus/query_chroma.py "why do topological insulators have edge states"
python3 corpus/query_chroma.py "strange metal transport" --pillar adscmt -n 3
```

**Contention GPU — à connaître avant de lancer.** L'Ollama de cette machine
partage une unique Tesla T4 avec les autres sessions SocrateAI. Mesuré le
2026-09-27 : GPU à 99 %, 13 Go de VRAM sur 15 occupés par
`Goedel-Prover-V2-8B` (le prouveur Lean de LeanMaster). Les requêtes
d'embedding attendent alors derrière le prouveur, et une seule peut prendre
plusieurs minutes. D'où :

- `--timeout 900` (par défaut) plutôt que les 120 s d'ANSE ;
- `--batch-size 4` (par défaut), pour que la progression soit enregistrée
  souvent ;
- **`--resume`**, qui saute les chunks déjà présents : une ingestion
  interrompue reprend là où elle s'est arrêtée au lieu de tout refaire.

Lancer les ~1500 chunks du texte intégral quand le prouveur est inactif
(`curl -s localhost:11434/api/ps` ne doit pas lister de prouveur).
`--abstracts-only` (73 chunks) donne un index utilisable bien plus tôt.

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
| `topology` | 13 | effet Hall de spin quantique, Altland–Zirnbauer, dix classes |
| `bridge` | 12 | anomalies, spectre d'intrication, code torique, semi-métaux holographiques |
| `experiment` | 3 | expériences de gravité analogue sur table (Hawking stimulé, superradiance) |
| `ryu` | 21 | travaux de Shinsei Ryu hors des piliers précédents (sélection sur 202) |

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
