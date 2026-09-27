# Shinsei Ryu : un programme de recherche entre holographie et matière topologique

**Source.** Le dossier arXiv complet de Shinsei Ryu, extrait par
[`tools/arxiv_author.py`](../tools/arxiv_author.py) et conservé dans
[`assets/ryu_arxiv.json`](assets/ryu_arxiv.json) : **202 articles, 2000–2026**,
filtrés sur l'auteur exact « Shinsei Ryu ». Répartition par catégorie primaire :
`cond-mat.str-el` 75, `cond-mat.mes-hall` 49, **`hep-th` 36**,
`cond-mat.stat-mech` 17, `quant-ph` 12, autres 13.

**Convention de citation.** `[CORPUS]` : l'article est dans `papers/index.json`,
récupéré et contrôlé par la porte d'identité, et interrogeable dans la
collection Chroma (pilier `ryu` ou autre). `[DOSSIER]` : l'article figure dans
les 202 entrées de `ryu_arxiv.json` (titre, auteurs, résumé), mais n'a pas été
téléchargé en texte intégral. Aucune référence de ce document n'est citée de
mémoire. Les jugements propres à cette revue sont marqués **[INTERPRÉTATION]**.

---

## 0. L'anecdote est exacte — et plus forte que prévu

Ryu signe, en premier auteur avec Takayanagi, la formule d'entropie
d'intrication holographique (`hep-th/0603001` [CORPUS]) ; il cosigne la
classification en dix classes (`0803.2786`, `0912.2157` [CORPUS]). Ce n'est
pas une coïncidence de carrière : 36 de ses articles sont en `hep-th`, et la
majorité de sa production en matière condensée porte sur la topologie et
l'intrication. **Il a passé vingt-cinq ans à construire, explicitement, les
ponts entre les deux domaines.**

Et un point de la revue principale doit être **nuancé** à la lumière de son
dossier. [`literature_review.md`](literature_review.md) §0 corrige le slogan
« la frontière encode le volume dans les deux cas » en rappelant qu'AdS/CFT
n'est pas topologique. Cette correction reste juste **pour AdS/CFT au sens
strict**. Mais Ryu et ses collaborateurs ont construit une **autre** forme de
dualité holographique — l'*exact holographic mapping*, fondé sur les réseaux de
tenseurs — dans laquelle l'intuition de départ devient un théorème précis :

> **Gu, Lee, Wen, Cho, Ryu (`1605.00570` [CORPUS])** : l'état de Hall anomal
> quantique en $(2+1)$ dimensions a pour **dual holographique un isolant
> topologique en $(3+1)$ dimensions**, vivant dans un espace hyperbolique. La
> topologie de la frontière est portée par le volume, et se lit dans
> l'intrication entre échelles.

C'est littéralement « la topologie de l'espace à $N-1$ dimensions dicte celle
de l'espace à $N$ dimensions » — mais dans un cadre (tenseurs, espace
hyperbolique discret, états libres) qui n'est **pas** la gravité dynamique
d'AdS/CFT. **[INTERPRÉTATION]** La formulation correcte de l'intuition de
départ est donc : *elle est vraie dans la dualité holographique par réseau de
tenseurs, démontrée pour des états de bandes libres ; elle n'est pas établie
dans AdS/CFT avec gravité dynamique.* L'écart entre les deux est un problème
ouvert réel, et c'est un bon endroit où contribuer (§5).

---

## 1. Le fil chronologique en treize thèmes

| Période | Thème | Articles clés |
|---|---|---|
| 2000–2003 | **Modes nuls de bord et symétrie chirale** | `cond-mat/0112197` [CORPUS], `cond-mat/0311595` [DOSSIER] |
| 2000–2013 | Fermions de Dirac désordonnés, transitions d'Anderson, modèles de réseau $\mathbb{Z}_2$ | `cond-mat/0107516`, `0705.1607`, `0912.2158`, `1111.3249` [DOSSIER] |
| 2006–2009 | **Entropie d'intrication holographique** | `hep-th/0603001`, `hep-th/0605073`, `0905.0932` [CORPUS] |
| 2007 | Invariant $\mathbb{Z}_2$ à N corps | `0708.1639` [CORPUS] |
| 2008–2015 | **Classification en dix classes** et ses extensions (réflexion, CPT, cristallin) | `0803.2786`, `0912.2157`, `1406.0307`, `1505.03535` [CORPUS] ; `0905.2029`, `1303.1843` [DOSSIER] |
| 2008–2011 | **Holographie appliquée** : désordre par répliques, effet Hall fractionnaire, supra/isolant | `0810.5394`, `0901.0924` [CORPUS] ; `0911.0962`, `1103.6068` [DOSSIER] |
| 2010 | **Isolants topologiques depuis la théorie des cordes** | `1001.0763`, `1007.4234` [CORPUS] |
| 2010–2017 | **Anomalies et réponses** (électromagnétique, gravitationnelle, thermique ; LSM) | `1010.0936`, `1705.03892` [CORPUS] ; `1211.0533`, `1611.09463` [DOSSIER] |
| 2012–2017 | Interactions et invariants topologiques à N corps ; transposée partielle | `1202.5805`, `1607.03896` [CORPUS] ; `1609.05970`, `1710.01886` [DOSSIER] |
| 2012–2021 | **Réseaux de tenseurs et géométrie holographique** (cMERA, EHM, réseaux aléatoires) | `1208.3469`, `1605.00570`, `1605.07199`, `2109.02649` [CORPUS] ; `1311.6095`, `1611.05877` [DOSSIER] |
| 2015–2023 | Négativité d'intrication, trempes de CFT, brouillage quantique | `1501.00568`, `1804.08637`, `2302.08009` [DOSSIER] |
| 2020–2026 | **Systèmes ouverts et non hermitiens**, SYK lindbladien, matrices aléatoires | `2112.13489`, `2202.02548`, `2212.00605` [CORPUS] ; `2411.11878`, `2609.00162` [DOSSIER] |
| 2023–2026 | **Phase de Berry supérieure, géométrie quantique, « magie »** | `2312.17318`, `2405.05327`, `2601.00761` [CORPUS] ; `2304.05356`, `2607.20624` [DOSSIER] |

---

## 2. Les quatre ponts qu'il a construits

### 2.1 Symétrie chirale → invariant d'enroulement → modes de bord (2001)

**Ryu & Hatsugai, `cond-mat/0112197` [CORPUS].** Pour un hamiltonien à
symétrie chirale (particule-trou), chaque hamiltonien de volume 1D définit une
**boucle** dans un espace de paramètres ; sa topologie, combinée à la symétrie
chirale, **décide de l'existence de modes de bord à énergie nulle**. Cadre
unifié pour les supraconducteurs gappés, les supraconducteurs $d$ et les rubans
de graphite.

C'est, sept ans avant la classification complète, la correspondance
volume–frontière dans sa forme la plus élémentaire — **et c'est exactement
l'énoncé de la cible Lean T2** de ce dépôt
([`lean/README.md`](../lean/README.md)), vérifié numériquement par
[`ssh_check.py`](../experiments/axis1_topological_waves/ssh_check.py), et
mesurable dans l'aquarium de l'axe 1.

### 2.2 K-théorie, D-branes, et la table périodique (2008–2010)

La classification en dix classes (`0803.2786`, `0912.2157`) révèle une
périodicité en dimension et en classe de symétrie, que Kitaev (`0901.2686`)
relie à la K-théorie. **Ryu & Takayanagi (`1001.0763`, `1007.4234` [CORPUS])**
observent que les charges de D-branes sont elles aussi classifiées par la
K-théorie, et établissent une **correspondance un-à-un** entre la classification
des isolants/supraconducteurs topologiques et les charges de paires de
D-branes. La réalisation en théorie des cordes arrive avec des interactions de
jauge, et le terme de Wess–Zumino y produit la réponse topologique.

### 2.3 Intrication, renormalisation et géométrie émergente (2006–2021)

- **RT** (`hep-th/0603001`, `hep-th/0605073`, revue `0905.0932`) : la géométrie
  du volume se lit dans l'intrication de la frontière.
- **Nozaki, Ryu, Takayanagi (`1208.3469` [CORPUS])** : une définition de la
  **métrique holographique** dans la direction d'échelle du cMERA, formulée
  uniquement en données de théorie des champs, calculée explicitement pour des
  bosons et fermions libres, et compatible avec AdS/CFT.
- **Wen, Cho, Lopes, Gu, Qi, Ryu (`1605.07199` [CORPUS])** : sous le flot de
  renormalisation par intrication d'un isolant de Chern, chaque couche porte un
  **flux de Berry non nul** émis depuis l'UV et transporté vers l'IR ; il est
  **obstrué** de construire l'état fondamental exact d'un isolant topologique à
  partir d'un état IR trivial.
- **Gu et al. (`1605.00570` [CORPUS])** : l'EHM envoie le Hall anomal en 2+1 d
  sur un isolant topologique en 3+1 d (§0).

### 2.4 Anomalies : la même équation des deux côtés (2010–2017)

**Ryu, Moore & Ludwig (`1010.0936` [CORPUS])** : réponses électromagnétique et
gravitationnelle, et anomalies, de toute la table périodique.
**Cho, Hsieh & Ryu (`1705.03892` [CORPUS])** : les états gapless imposés par le
théorème de Lieb–Schultz–Mattis et les bords des phases SPT d'une dimension
supérieure ont **la même théorie effective**, mais leurs anomalies jouent des
rôles différents — une distinction fine entre deux mécanismes de protection que
le slogan « volume–frontière » écrase.

---

## 3. La frontière actuelle (2020–2026)

Quatre directions dominent ses publications récentes. Elles sont importantes
ici parce qu'elles sont **nettement plus computationnelles** que ses travaux
antérieurs — et donc plus ouvertes à une contribution d'ingénierie.

1. **Topologie non hermitienne et systèmes ouverts.** Kawabata, Shiozaki & Ryu
   (`2202.02548` [CORPUS]) : les phases topologiques non hermitiennes 1D
   survivent aux interactions, avec un invariant donné par **l'enroulement du
   spectre complexe à N corps** sous un flux. Classification du chaos
   dissipatif par symétries (`2212.00605` [CORPUS]), dynamique lindbladienne
   de SYK (`2112.13489` [CORPUS]), statistiques de matrices aléatoires non
   hermitiennes (une demi-douzaine d'articles en 2025–2026 [DOSSIER]).
2. **Phase de Berry supérieure.** Ohyama & Ryu (`2405.05327` [CORPUS]) : une
   **connexion de Berry supérieure** pour des familles d'états produits de
   matrices, dont la structure mathématique sous-jacente est une **gerbe**.
   Extensions aux PEPS 2+1 d et aux variétés conformes de bord [DOSSIER].
3. **Géométrie quantique et bandes idéales.** Kruchkov & Ryu
   (`2312.17318` [CORPUS]) : pour une bande de Chern plate, la règle de somme
   de la conductivité longitudinale vaut $C\,\Delta e^2$ — l'invariant
   topologique sort d'une mesure **optique**, pas seulement du transport Hall.
4. **« Magie » (non-stabilisabilité).** Xiao & Ryu (`2601.00761` [CORPUS]) :
   calcul des entropies de Rényi de stabilisateur d'un état à $N$ qubits,
   coût moyen par chaîne de Pauli ramené de $O(2^N)$ à $O(N)$ par la
   **transformée de Walsh–Hadamard rapide**, plus un estimateur Monte-Carlo
   préconditionné par Clifford.

**[INTERPRÉTATION]** Le point 4 est un **article d'algorithmique**. Son cœur est
une transformée rapide et un échantillonneur — le genre de noyau où une
implémentation GPU et Rust soignée change l'échelle accessible d'un ou deux
ordres de grandeur. C'est le point d'entrée le plus direct pour votre profil
(voir [`contribution_map.md`](contribution_map.md)).

---

## 4. Ce que le dossier ne contient pas

Pour être complet et éviter de lui prêter ce qu'il n'a pas fait :

- **Aucun article de formalisation** (Lean, Coq, Isabelle) dans les 202
  entrées. La classification en dix classes, le théorème de Ryu–Hatsugai et
  les invariants à N corps n'ont, à notre connaissance du dossier, **jamais
  été vérifiés formellement** par lui. (Ce dossier ne dit rien des travaux
  d'autres groupes ; une recherche dédiée dans Mathlib et la littérature de
  formalisation est à faire avant d'affirmer une priorité.)
- **Aucun article expérimental** de sa main : ses travaux sont théoriques et
  numériques.
- **Aucun lien direct avec la gravité analogue** (axe 2 du programme
  expérimental).

---

## 5. Problèmes ouverts où une contribution est réaliste

Sélectionnés parce qu'ils sont **à la fois** ouverts dans ce dossier **et**
adaptés aux compétences listées dans
[`contribution_map.md`](contribution_map.md). **[INTERPRÉTATION]** pour
l'ensemble de la section.

1. **Formaliser Ryu–Hatsugai.** Le théorème de `cond-mat/0112197` en Lean 4 :
   premier résultat de matière topologique vérifié par le noyau, dans le
   pipeline à portes de LeanMaster. Point de départ déjà vérifié numériquement.
2. **Formaliser la périodicité de Bott de la table.** Mathlib possède les
   algèbres de Clifford ; la classification des dix classes se ramène au
   problème d'extension de Clifford (Kitaev `0901.2686`). Un énoncé T3, mais
   d'une valeur de référence durable.
3. **Échelle GPU pour la magie et les matrices aléatoires non hermitiennes.**
   Les algorithmes de `2601.00761` (Walsh–Hadamard + échantillonnage) et les
   diagonalisations massives de matrices aléatoires non hermitiennes se
   prêtent directement au GPU et au calcul distribué.
4. **Invariants à N corps non hermitiens à grande échelle.** L'invariant de
   `2202.02548` — enroulement du spectre complexe à N corps sous un flux —
   demande de diagonaliser des hamiltoniens non hermitiens en interaction sur
   une grille de flux : un calcul de diagonalisation exacte parallèle par
   nature.
5. **L'écart EHM ↔ AdS/CFT (§0).** Quand la dualité holographique par réseau de
   tenseurs (où la topologie passe à la dimension supérieure) admet-elle une
   limite avec gravité dynamique ? C'est le problème le plus profond de la
   liste, et le moins susceptible de céder à l'ingénierie seule.
