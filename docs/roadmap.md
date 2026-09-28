# Feuille de route — AdS/CMT et travaux de Shinsei Ryu : théorie, numérique, observation, expérimentation

**Objet.** Un programme sur 12 mois qui fait avancer, de façon vérifiable,
une ligne de recherche établie (correspondance volume–frontière, spectres
d'intrication, SYK — le cœur du programme de Ryu), avec quatre pistes
couplées : **T** théorie et Lean 4, **N** numérique et GPU/HPC, **O**
observation (confrontation aux données publiées), **E** expérimentation en
laboratoire de garage. Chaque jalon a un critère d'arrêt.

**Répartition.** Vous : construction, mesures, décisions. Moi : énoncés,
preuves Lean, code numérique vérifié, références (toutes passées par la
porte d'identité du corpus), protocoles, nombres de conception, analyse des
données que vous produirez, relecture adverse. Je ne produis jamais une
« donnée expérimentale » : tout ce que je calcule est marqué simulation.

**Convention.** `[CORPUS]` = article dans `papers/index.json`, titre vérifié
contre arXiv. `[EXTERNE]` = référence hors corpus. Tiers Elenchus
`X < C < L < B < A` comme dans [`rigor_protocol.md`](rigor_protocol.md).

---

## État au 2026-09-27 — ce qui est livré, ce qui vient ensuite

### Livré

| Livrable | Où | Tier |
|---|---|---|
| **v0.1** : PoC spectres d'intrication + Gudhi, erratum de flou de taille finie | release `v0.1`, `experiments/poc_entanglement_tda/` | X (corrigé) |
| **Piste H, v1.0** : préprint *Logarithmic boundary depth and the conditioning of the discrete inverse conductance problem on hyperbolic lattices* | Zenodo [10.5281/zenodo.23000391](https://doi.org/10.5281/zenodo.23000391), `experiments/track_h_hyperbolic_network/paper/main.pdf` | X/B/L/C, par affirmation (grand livre) |
| Données et simulateur de la piste H | HF [dataset](https://huggingface.co/datasets/callensxavier/hyperbolic-resistor-networks), HF [simulateur](https://huggingface.co/callensxavier/hyperbolic-resistor-network-simulator) (code, sans poids) | — |
| Benchmark RC dans rusty-SUNDIALS | [rusty-SUNDIALS#62](https://github.com/xaviercallens/rusty-SUNDIALS/pull/62), fusionné (4ce8abb) | — |
| Grand livre Elenchus avec magasin de preuves adressé par contenu | `docs/elenchus/ledger.json`, `docs/elenchus/evidence/` | 19 affirmations |

**Résultats de la piste H (v1.0), en une ligne chacun.**
- **Conditionnement.** Il est polynomial sur $\{7,3\}$ ($\log_{10}\kappa=3{,}89$ à $N=847$, dans la bande préenregistrée) ; sur réseau plat, $\kappa$ n'est plus résolu en double précision dès $N\approx400$. Le mécanisme est la profondeur au bord : $O(\log N)$ contre $O(\sqrt N)$.
- **Identifiabilité.** Elle est exacte sur les deux géométries (rangs certifiés sur $\mathbb F_p$) : la différence tient au conditionnement.
- **Contrôles.** Contrôle à nombre de sondes égal : l'avantage persiste (métrique post hoc, déclarée comme telle). L'ordre est préservé pour la carte Neumann–Dirichlet.
- **H2.** La prédiction préenregistrée est **réfutée** à taille finie. En revanche $\lambda_{\min}\downarrow\lambda_0>0$ par monotonie de domaine, donc $\tau\le C/\lambda_0$ pour tout $N$.
- **Validation croisée.** Deux intégrateurs, SciPy et CVODE de rusty-SUNDIALS, s'accordent avec la solution exacte à $3\times10^{-8}$ près.

**Évaluation honnête.** C'est une contribution soignée, modeste et reproductible, un bon socle de légitimité, mais pas un résultat majeur. Un relecteur objectera trois points :
- le résultat est en partie prévisible une fois la profondeur $O(\log N)$ notée ;
- le résultat spectral applique des théorèmes connus (Dodziuk, Mohar, Häggström–Jonasson–Lyons) ;
- les preuves sont étroites : un seul pavage, tailles modérées, mesure linéarisée, aucune reconstruction effective, recherche de nouveauté ciblée et non systématique.

Les prochaines étapes visent précisément ces trois objections.

**Revue par les pairs (reçue le 2026-09-27).** Une revue de v1.0, enregistrée mot pour mot dans
`experiments/track_h_hyperbolic_network/paper/reviews/`, demande quatre choses : la loi plate au-delà de la double
précision, un test à conductances inhomogènes, la disparité de dimension du contrôle à sondes égales, et l'argument
topologique de la Proposition 1. Les quatre ont été préenregistrées (`PREREGISTRATION_3.md`) puis calculées pour
v1.1. Résultat notable : le contrôle à dimension égale a **réfuté notre propre prédiction** ; l'avantage à sondes et
dimension égales est au plus d'une demi-décade (et inversé à $N\approx112$). v1.0 est corrigé en ce sens dans v1.1,
publié comme nouvelle version Zenodo sous le même DOI de concept. Les régimes désordonnés confirment l'avantage
(l'écart s'élargit à 8,3 décades sous désordre log-uniforme sur deux décades). La loi plate au-delà de la double
précision, calculée en arithmétique de boules à 512 bits, suit la forme $e^{c\sqrt N}$ préenregistrée
($\log_{10}\kappa = 15{,}99$ à $N=421$, $16{,}54$ à $N=797$, à 0,4 décade des extrapolations ; une loi de puissance
manque de 2,7 décades ou plus) : la limitation (i) de v1.0 est levée.

### Prochaines étapes, par priorité

Chaque étape reprend la même discipline : préenregistrement commité *avant* le calcul, formes rivales énoncées, verdict au grand livre.

| # | Étape | Pourquoi (objection visée) | Livrable | Critère d'arrêt / de réfutation |
|---|---|---|---|---|
| **H-1** | Fusionner la PR #2 et publier la release `v1.0` sur GitHub | clôt la version publiée | tag `v1.0`, PDF attaché | — |
| **H-2** | **Loi d'échelle multi-pavages** : $\{8,3\}$, $\{5,4\}$, $\{p,q\}$ (le volet « plat au-delà de $N\approx400$ en précision étendue » est traité dans v1.1, `PREREGISTRATION_3.md` A) | « un seul pavage » | `PREREGISTRATION_4.md`, puis tableau $\log\kappa$ contre $(N, \text{taux de croissance du bord})$ | l'exposant local de $\kappa$ n'est **pas** ordonné par le taux de croissance du bord ⇒ le mécanisme « profondeur » est insuffisant, on l'écrit |
| **H-3** | **Reconstruction effective** : imagerie différentielle (localiser $\delta g$ sur quelques arêtes) avec bruit, hyperbolique contre plat | « mesure linéarisée seulement » | taux de localisation contre profondeur et bruit, seuils fixés d'avance | l'avantage hyperbolique disparaît en localisation ⇒ le résultat reste limité au conditionnement linéarisé |
| H-3a ✅ | Sous-hypothèse « un défaut de volume est un invariant topologique lisible au bord » (Gudhi, homologie persistante de la métrique de résistance) : **testée le 2026-09-28**, `PREREGISTRATION_5.md`, `TDA_RESULTS.md` | suggestion externe | grand livre H3-X-0001 | **échoue** pour un défaut profond sur les 4 réseaux ; un court-circuit près du bord n'est vu en $H_1$ que sur l'hyperbolique ; le nul (désordre global 50 %) était mal dimensionné (LL-A8). **Refait le 2026-09-28 contre du bruit de mesure** (`PREREGISTRATION_6.md`, H3-X-0002) : un défaut profond reste détectable jusqu'à ≥ 10× plus de bruit sur l'hyperbolique que sur le carré (N≈316), le budget de 3×10⁻⁴ du papier suffit sur les 4 réseaux, et la détection topologique est moins sensible que la métrique simple. **Prochain test décisif pour H-4 : nul à tolérance de composants (0,1 %, 1 %, 5 %)** — une vraie construction mesure sa propre ligne de base, et la tolérance en est une perturbation fixe |
| **H-4** | **Mesure physique RC** : $\{7,3\}$, $L=2$ ($N=112$, 140 résistances, 35 condensateurs sur les nœuds intérieurs, 77 nœuds de bord pilotés), plus témoin carré $R=6$ (200 résistances, 69 condensateurs), ESP32 en domaine temporel | « pas de donnée » ; c'est le vrai saut de légitimité | prédictions déjà écrites : $\tau=2{,}75\,RC$ contre $4{,}55\,RC$, raideur $14{,}9$ contre $35{,}4$ ; contrôles K1/K2 sur le circuit | écart $>20\,\%$ sur $\tau$ après correction des tolérances ⇒ modèle de circuit à revoir avant toute conclusion |
| **H-5** | **Avis d'un spécialiste** (problèmes inverses sur réseaux, p. ex. le groupe Borcea / Guevara Vasquez), puis arXiv (`math.NA` ou `math-ph`, parrainage nécessaire) et revue (*Inverse Problems*, *SIAM J. Appl. Math.*) | nouveauté non confirmée, pas de relecture | message de 5 lignes + lien DOI ; soumission | le spécialiste signale un antécédent ⇒ le citer et recentrer la contribution |
| **H-6** | **Lean 4** : Proposition 1 (monotonie de domaine) en dimension finie, et compilation de `lean/HyperbolicLogDepth.lean` avec la porte LeanMaster | transformer un tier C en A | fichier sans `sorry`, empreinte d'axiomes | énoncé affaibli pour compiler ⇒ refus |
| **H-7** | **rusty-SUNDIALS** : réparer la CI de `main` (4 jobs rouges avant #62), ajouter un argument de jacobien analytique au binding Python, benchmark à $N\sim10^3$–$10^4$ | synergie outillage ; coût du solveur en fonction de la géométrie | PR(s) rusty-SUNDIALS | — |
| **H-8** | Hygiène du grand livre : 5 empreintes anciennes sans blob (`SSH-L-0001`, `SSH-C-0001`, `POC-X-0001/0002`, `H0-X-0001`) | la porte stricte doit passer sans exception | blobs régénérés ou affirmations requalifiées | — |

**Ordre conseillé.** D'abord H-1, puis H-2 et H-3 en parallèle (numérique, quelques semaines). Ensuite H-4, l'expérience, qui peut démarrer dès maintenant côté achats. H-5 intervient quand H-2 ou H-3 a donné un résultat, pour arriver avec plus qu'un préprint. H-6 à H-8 se font au fil de l'eau.

**Ce qui ne change pas.** Le programme principal (M1–M9 ci-dessous : SYK, bassin SSH, Lean Ryu–Hatsugai) reste la voie vers le groupe de Ryu. La piste H est un socle parallèle, pas un substitut : elle ne teste pas AdS/CMT et ne doit jamais être présentée ainsi.

---

## 0. Stratégie de légitimité — ce qui compte vraiment

Vous voulez utiliser ce socle pour acquérir une légitimité, puis pivoter vers
un programme plus disruptif. C'est une stratégie saine. Voici, sans détour,
ce qui la fait réussir ou échouer dans cette communauté.

**Ce qui donne de la légitimité.**
1. **Reproduire un résultat connu, correctement, en public.** Un dépôt qui
   reproduit Fidkowski (`0909.2654`) ou Süsstrunk–Huber (`1503.06808`) avec
   contrôles, code et données, vaut plus qu'une idée neuve non vérifiée.
2. **Une contribution petite, vérifiable, utile à un groupe identifié.** Une
   formalisation Lean 4, vérifiée par le noyau, d'un théorème que ce groupe
   utilise (Ryu–Hatsugai, `cond-mat/0112197`) est **rare** dans ce domaine —
   à notre connaissance du dossier arXiv de Ryu (202 articles), aucun de ses
   résultats n'a été formalisé. C'est un artefact qu'un théoricien peut
   vérifier en une heure et citer. C'est le levier principal ici.
3. **La correction publique de ses propres erreurs.** Ce dépôt en contient
   déjà une : la prétendue absence de flou de taille finie (v0.1), fausse,
   corrigée par erratum ([`../experiments/poc_entanglement_tda/results.md`](../experiments/poc_entanglement_tda/results.md)).
   Un relecteur du domaine l'aurait attrapée en cinq minutes ; l'avoir
   attrapée soi-même, et documentée, est précisément ce qui distingue un
   travail crédible.

**Ce qui détruit la légitimité.**
- Relier le bassin d'eau à l'holographie. Le bassin teste la topologie de
  bande à une particule (pilier 3 de la revue), pas AdS/CMT. Chaque
  écrit doit le dire.
- Annoncer avant de mesurer. Le préenregistrement commité est la protection.
- Une seule affirmation surdimensionnée dans un premier article, et tout le
  reste est lu avec suspicion.

**Quand et comment contacter le groupe de Ryu.** Quand le jalon **M6**
(formalisation Lean de Ryu–Hatsugai, porte de LeanMaster passée) est atteint
— pas avant. Le message tient en trois lignes : « voici votre théorème,
vérifié par le noyau Lean 4, voici la seule hypothèse que nous avons dû
ajouter, voici où il est utilisé ». C'est concret, vérifiable, et cela
demande dix minutes de leur temps.

**Le pivot.** Une fois M6 et M4 (bassin) publiés, le socle est là. Le pivot
se fait en réutilisant *la même discipline* (préenregistrement, tiers,
grand livre) sur votre programme propre : c'est la discipline, plus que le
sujet, qui sera reconnue.

---

## 1. Le fil conducteur

Un seul énoncé physique traverse les quatre pistes :

> Pour une chaîne 1D à symétrie chirale (SSH), un invariant de volume (le
> nombre d'enroulement $\nu$) impose un mode de bord d'énergie nulle ; ce
> mode réapparaît comme un niveau à $\zeta=1/2$ du spectre d'intrication
> (Fidkowski `0909.2654`), et, dans une réalisation ondulatoire classique,
> comme un mode localisé mesurable dont la longueur de localisation vaut
> $\xi = 1/\ln(w/v)$.

Théorie : prouver $\nu \leftrightarrow$ mode (Lean). Numérique : $\xi$,
hybridation, spectres (fait, corrigé). Observation : ce que les réalisations
publiées (mécanique, acoustique, géophysique) ont mesuré. Expérience : le
mesurer dans l'eau, avec les nombres de conception issus du calcul.

Le frère fortement corrélé : le **SYK** et sa périodicité en $N \bmod 8$
(Fidkowski–Kitaev `0904.2197`, You–Ludwig–Xu `1602.06964`), observée ici
numériquement (100 % / 0 % de dégénérescence selon la classe, $N\le 24$).

---

## 2. Piste T — Théorie et Lean 4

| # | Objectif | Tier visé | État | Dépend de |
|---|---|---|---|---|
| **T1** | Ryu–Hatsugai / SSH : (a) chaîne impaire ouverte : noyau de dimension 1, profil $(-v/w)^n$ ; (b) $\nu\in\{0,1\}$ par `circleIntegral.integral_sub_inv_of_mem_ball` (pôle intérieur) et le théorème de Cauchy (pôle extérieur) ; (c) le côté du mode $\Leftrightarrow \nu$ | **A** | énoncé fixé ([`../lean/README.md`](../lean/README.md)), vérifié numériquement et en arithmétique exacte (`SSH-B-0001/2`) ; **`statement_lock.py` non encore passé** | LeanMaster, Mathlib |
| **T2** | La coupure symétrique : prouver que pour $\ell=L/2$ la réflexion + chiralité annule exactement l'hybridation (le fait derrière l'erratum). Petit lemme, **nouveau à notre connaissance** | **B** puis **A** | conjecture C, numérique X (`finite_size_scaling.py` S2) | T1(a) |
| **T3** | SYK : construire l'opérateur antiunitaire $T$ dans la représentation de Majorana et vérifier $T^2=\pm1$ selon $N\bmod 8$, en arithmétique **entière exacte** (les $\gamma_i$ sont des permutations signées : tout est exact) | **B** | motivé par `0904.2197`, `1602.06964` ; résultat numérique X (`POC-X-0002`) | rien |
| **T4** | Relation exacte de Fidkowski pour le projecteur SSH (spectre d'intrication = spectre de bord du hamiltonien aplati), cas libre | **L → B** | citation L | T1 |
| **T5** | Table périodique : classes de Clifford (`CliffordAlgebra` de Mathlib), périodicité de Bott | **A** (long) | ambition | T1, LeanMaster |

Références T : `cond-mat/0112197`, `0909.2654`, `0910.1811`, `0803.2786`,
`0912.2157`, `0901.2686`, `1505.03535`, `0904.2197`, `1602.06964`
[CORPUS].

---

## 3. Piste N — Numérique, GPU, HPC

| # | Objectif | Tier | État |
|---|---|---|---|
| **N1** | Scaling de taille finie du spectre d'intrication SSH ; nombres de conception $\xi$, cellules/côté | X | **fait, corrigé** (`finite_size_scaling.py`, 32 contrôles) |
| **N2** | = T3, moitié numérique : $T^2$ exact, $N=4\dots 32$ | B | à faire (jalon M1) |
| **N3** | SYK, classes $N\bmod 8\in\{2,6\}$ (nombre impair de paires : bipartition différente) ; $N$ jusqu'à 28 sur la T4 quand elle est libre (plafond `complex128` calculé : $N=28$) ; moyennes sur le désordre en parallèle parfait (Agora-Home / GCP) | X | à faire |
| **N4** | « Bassin virtuel » : résoudre l'équation d'onde linéaire 2D dans la **géométrie réelle** du canal (barrières partielles, profondeur), pour prédire le champ $\eta(x,y)$ que la caméra verra ; c'est la prédiction que l'axe 1a confronte, pas le modèle de liaisons fortes | X (simulation, jamais une donnée) | à faire, **avant** la découpe des pièces |
| **N5** | Moteur d'entropie de stabilisateur (Xiao–Ryu `2601.00761`) : transformée de Walsh–Hadamard vectorisée CPU, puis GPU ; reproduire une courbe à $N\le 20$ | X | à faire |
| **N6** | Non-hermitien : invariant à N corps de `2202.02548` (enroulement du spectre complexe sous flux), petites tailles | X | option |

**Contrainte matérielle.** Une seule T4 partagée, occupée par le prouveur
Lean d'une autre session lors de ce travail. Tout code GPU est écrit avec un
repli CPU et testé sur CPU d'abord.

---

## 4. Piste O — Observation : confronter aux données publiées

« Observation » ici = ce que d'autres ont mesuré, reproduit avant d'étendre.

| # | Cible | Ce qu'on reproduit | Usage |
|---|---|---|---|
| **O1** | Süsstrunk & Huber `1503.06808` (pendules couplés, isolant topologique mécanique) | le comptage de modes de bord et la robustesse aux défauts | gabarit pour la lecture de nos données d'axe 1 |
| **O2** | Yang *et al.* `1411.7100` (acoustique topologique) ; Souslov *et al.* `1802.09649` (fluides à viscosité impaire) | modes de bord chiraux en ondes classiques, profils spatiaux | ce à quoi ressemble « confirmation expérimentale » dans ce domaine |
| **O3** | Kane & Lubensky `1308.0554` (réseaux isostatiques) | modes de bord topologiques **mécaniques** — le plus proche parent conceptuel du SSH dans l'eau | sanity check du modèle de couplage |
| **O4** | Delplace, Marston & Venaille `1702.07583` (ondes équatoriales de Kelvin/Yanai) | l'origine topologique de deux ondes **observées** dans l'atmosphère et l'océan | une donnée d'observation réelle et publique (réanalyses) où la correspondance volume–frontière est déjà validée par la nature — option ambitieuse : refaire leur comptage sur des données publiques |
| **O5** | Weinfurtner `1008.1911`, Euvé `1511.08145`, Torres `1612.06180` | conversion de modes / superradiance mesurées | référence quantitative pour les verdicts de l'axe 2 |

---

## 5. Piste E — Expérimentation : commencer par l'axe 1a

Ordre : **1a (canal SSH) et 5 (caustiques) en parallèle**, puis 1b, 2, 4, 3
(justification : [`experimental_program.md`](experimental_program.md) §6).
Sécurité : [`safety.md`](safety.md), en particulier le différentiel 30 mA.

### 5.1 Ce que le canal SSH réalise

Un canal droit de largeur $W$ avec des **barrières transversales partielles**
(plaques émergentes percées d'une ouverture centrale $g$). Chaque
compartiment est un résonateur (mode de ballottement fondamental) ; le
couplage entre voisins passe par l'ouverture. Ouvertures alternées
$g_{\text{large}}$ / $g_{\text{étroite}}$ $\Rightarrow$ couplages alternés
$w > v$ : c'est la chaîne SSH. Le **mur de domaine** = deux ouvertures
étroites consécutives ; les deux extrémités se terminent par une ouverture
large vers la plage absorbante (terminaison « forte », pour qu'aucune
extrémité n'ait son propre mode — même construction que `D1`).

### 5.2 Nombres de conception (issus de `finite_size_scaling.py`, D1)

| $r=v/w$ visé | $\xi$ (cellules) | cellules/côté (99 %) | à construire (marge ×1,5) |
|---|---|---|---|
| 0,5 | 1,4 | 3 | 5 |
| **0,7** | **2,8** | **6** | **8–10** |
| 0,8 | 4,5 | 10 | 15 |

Cible **$r\approx0{,}7$** : localisé sur quelques cellules (visible), gap
$\Delta\propto|w-v|$ large (mesurable au-dessus de l'amortissement).
$r$ **se mesure**, il ne se choisit pas : le rapport des ouvertures n'est
qu'une première estimation ; la valeur réelle vient du gap et de $\xi$.

### 5.3 Fréquence, dimensions, régime

Compartiment de longueur $c$ : mode de ballottement $\lambda\approx 2c$,
$f\approx\sqrt{g\,k}/2\pi$ (eau profonde, $k=2\pi/\lambda$), avec correction
capillaire $\sigma k^3/\rho$ à ajouter dès que $\lambda\lesssim 5$ cm
($\lambda_c = 1{,}7$ cm).

| $c$ | période $a=2c$ | $\lambda$ | $f$ approx. | canal 2×9 cellules + mur | plages 2×20 cm |
|---|---|---|---|---|---|
| 4 cm | 8 cm | 8 cm | 3,1 Hz | 37 compartiments = 1,48 m | **≈ 1,9 m** |
| 5 cm | 10 cm | 10 cm | 2,8 Hz | 1,85 m | ≈ 2,3 m |

- Profondeur $h \ge \lambda/2$ (eau profonde) : **8–10 cm**.
- Largeur $W < \lambda/2$ pour un seul mode transverse : **$W\approx4$ cm**
  à $\lambda=8$ cm. Compromis : plus étroit = amortissement de paroi plus
  fort (couche limite $\delta=\sqrt{2\nu/\omega}\approx 0{,}3$ mm à 3 Hz ;
  atténuation estimée ~30 % sur 1,5 m — **à mesurer au jalon M2 avant de
  découper quoi que ce soit**).
- Le modèle de liaisons fortes est un **proxy** : la simulation 2D (N4)
  donne la vraie relation ouverture $\to$ couplage et la vraie fréquence
  de mi-gap. Ne pas fabriquer avant N4.

### 5.4 Nomenclature (matériel de récupération + peu d'achats)

| Élément | Solution | Note |
|---|---|---|
| Cuve | gouttière/canal en acrylique ou verre, ~2 m × 15 cm × 20 cm, ou deux cuves alignées | fond **transparent** pour la Schlieren ; ~60 L ⇒ support pour ≥ 80 kg, à niveau |
| Barrières | plaques acrylique 3 mm découpées (laser ou scie) ou PETG imprimé, hauteur $h+3$ cm, glissées dans un rail de base imprimé | 2 jeux d'ouverture ; **toutes émergentes** |
| Générateur | palette ou piston sur NEMA17 + Arduino/ESP32, fréquence verrouillée quartz, amplitude 1–3 mm | jamais le moteur de CD (vitesse instable à 3 Hz) |
| Absorbeurs | plages en mousse à cellules ouvertes ou grillage en pente douce (~10°), 20 cm | sans elles, ondes stationnaires ⇒ `INVALIDE` |
| Métrologie | **Schlieren synthétique de surface libre** (Moisy–Rabaud–Salsac 2009 [EXTERNE]) : motif de points aléatoires imprimé sous la cuve, panneau LED dessous, caméra (téléphone en RAW/exposition fixe, ≥ 30 fps) au-dessus | donne $\eta(x,y,t)$ complet ; sensibilité ~µm |
| Étalonnage | un objet de hauteur connue (lame de verre inclinée) pour la relation déplacement-de-motif → pente → hauteur | à refaire à chaque remplissage |
| Eau | déminéralisée ; **écrémer la surface** avant chaque mesure | la contamination de surface est la première cause d'amortissement excessif |
| Électricité | tout sur différentiel 30 mA ; pompe/moteur en TBTS | non négociable |

### 5.5 Modus operandi (chaque étape a un verdict avant la suivante)

0. **Amortissement à vide** (M2) : canal sans barrière, onde plane à $f$,
   mesurer la longueur d'atténuation $L_a$. **Critère d'arrêt :**
   $L_a < 10$ cellules $\Rightarrow$ changer d'échelle ($c$ plus grand) ou
   nettoyer l'eau, avant toute fabrication.
1. **Chaîne uniforme** (toutes ouvertures égales) : balayage 1,5–6 Hz,
   transmission ; pas de gap attendu (témoin).
2. **Chaîne SSH sans mur** : balayage ⇒ **gap** de transmission autour de
   $f_0$ ; $\Delta$ mesuré ⇒ estimation de $|w-v|$.
3. **Chaîne SSH avec mur** : excitation à $f_0$ (milieu du gap),
   $\eta(x)$ le long du canal ⇒ pic au mur, décroissance $\Rightarrow\xi$
   mesuré ; **signature chirale** : amplitude bien plus faible dans un
   compartiment sur deux (le mode vit sur un seul sous-réseau —
   [`finite_size_scaling.png`](../experiments/poc_entanglement_tda/figures/finite_size_scaling.png), droite).
4. **Comparaison** à la prédiction (N4 puis D1) : $\xi$ et $\Delta$ à 30 %
   près $\Rightarrow$ `CONFIRMÉ`. Sinon `RÉFUTÉ` ou `INVALIDE` selon les
   causes listées dans [`../experiments/axis1_topological_waves/PREREGISTRATION.md`](../experiments/axis1_topological_waves/PREREGISTRATION.md).
5. **Défaut** : retirer une barrière loin du mur ; le mode doit persister
   (protection par chiralité, pas par vallée : ici c'est un vrai test).

Chaque acquisition : un fichier vidéo brut, un JSON de paramètres, un hash ;
l'analyse est un script du dépôt, jamais un calcul à la main.

---

## 6. Jalons et critères d'arrêt (12 mois)

| Mois | Jalon | Livrable vérifiable | Critère d'arrêt |
|---|---|---|---|
| 1 | **M1** T3/N2 : $T^2$ exact pour SYK | script exact + rangée B au grand livre | aucun $T$ antiunitaire avec $T^2$ prédit trouvé ⇒ `POC-X-0002` reste X et on l'écrit |
| 1–2 | **M2** amortissement à vide (E, étape 0) | $L_a(f)$ mesuré, JSON + vidéo | $L_a<10$ cellules ⇒ redimensionner avant fabrication |
| 2 | **M3** N4 bassin virtuel | champ prédit pour la géométrie choisie, figure | l'ouverture ne donne pas $r\in[0{,}5;0{,}8]$ ⇒ revoir la géométrie |
| 2–3 | **M4a** Lean T1(a) : moitié finie, sans `sorry`, porte LeanMaster | fichier `.lean` + empreinte d'axiomes | énoncé affaibli pour compiler ⇒ refus (verrou d'énoncé) |
| 3–4 | **M5** canal SSH construit, étapes 1–5 | verdict `CONFIRMÉ/RÉFUTÉ/INVALIDE` de l'axe 1a | — un `RÉFUTÉ` propre est publiable |
| 4–6 | **M6** Lean T1(b,c) : enroulement + correspondance | théorème complet, tiers A | le pas de Cauchy (pôle extérieur) bloque ⇒ publier T1(a)+(c) conditionnel, dit tel quel |
| 6 | **M7** premier article (arXiv `cond-mat.mes-hall` + `physics.class-ph`) : *Kernel-verified bulk–boundary correspondence for the SSH chain, with a tabletop hydrodynamic realisation* | manuscrit, dépôt taggé, grand livre propre | — |
| 6–9 | **M8** N3, N5 (GPU si libre), O1–O3 reproductions | figures reproduites vs publiées | — |
| 9–12 | **M9** axes 5, 1b, 2 ; contact avec le groupe de Ryu après M6 | — | — |
| 12 | **Pivot** vers votre programme propre, même discipline | — | — |
| ✅ 0 | **MH** piste H v1.0 publiée (préprint + données + simulateur) | DOI 10.5281/zenodo.23000391 | fait le 2026-09-27 |
| 1–2 | **MH2/MH3** loi multi-pavages + imagerie différentielle | `PREREGISTRATION_3.md` puis résultats | voir H-2, H-3 |
| 2–4 | **MH4** mesure RC physique $\{7,3\}$ $L=2$ contre carré $R=6$ | $\tau$, raideur, K1/K2 mesurés | voir H-4 |
| 3–5 | **MH5** avis spécialiste puis soumission revue / arXiv | manuscrit v2 | voir H-5 |

---

## 6bis. Piste H — « Holographie analogique de garage » (évaluée séparément)

Le projet fusion proposé (réseau hyperbolique imprimé, laser dans la
carcasse du four, photodiodes solaires sur le pourtour, IA de reconstruction,
Gudhi, Lean) est évalué étape par étape dans
[`roadmap_holographie_analogique.md`](roadmap_holographie_analogique.md) :
ce qui est faux tel quel, ce qui est réel et déjà publié (holographie
discrète sur pavages hyperboliques, problèmes inverses sur réseaux), et le
protocole de remplacement qui garde l'objectif — *la frontière détermine le
volume* — sans les moyens qui ne peuvent pas marcher.

**Statut (2026-09-27).** La partie numérique de ce protocole de remplacement
est faite et publiée : préprint v1.0, DOI
[10.5281/zenodo.23000391](https://doi.org/10.5281/zenodo.23000391), code et
données dans [`../experiments/track_h_hyperbolic_network/`](../experiments/track_h_hyperbolic_network/).
Les étapes suivantes (H-2 à H-8) sont dans la section « État au 2026-09-27 »
en tête de ce document.

## 7. Ce que ce programme ne prétend pas

- Le bassin ne teste **pas** l'holographie. Il teste la correspondance
  volume–frontière de la théorie de bande (pilier 3). AdS/CMT est le
  contexte théorique (piliers 1–2), et le SYK en est le pont numérique.
- Le motif $N\bmod 8$ du SYK est **empirique** tant que M1 n'est pas
  atteint.
- Toute simulation (N4, N1) est marquée X et n'est jamais présentée comme
  une mesure.

---

## 8. Références par piste [CORPUS sauf mention]

**T.** Ryu & Hatsugai `cond-mat/0112197` · Fidkowski `0909.2654` ·
Pollmann, Berg, Turner, Oshikawa `0910.1811` · Schnyder–Ryu–Furusaki–Ludwig
`0803.2786`, `0912.2157` · Kitaev `0901.2686` · Chiu–Teo–Schnyder–Ryu
`1505.03535` · Fidkowski & Kitaev `0904.2197` · You, Ludwig, Xu
`1602.06964` · Peschel `cond-mat/0212631`.

**N.** Maldacena & Stanford `1604.07818` · Xiao & Ryu `2601.00761` ·
Kawabata, Shiozaki, Ryu `2202.02548` · Ryu et al. (SYK lindbladien)
`2112.13489` · Cotler et al. `1611.04650`.

**O.** Süsstrunk & Huber `1503.06808` · Yang et al. `1411.7100` · Kane &
Lubensky `1308.0554` · Souslov et al. `1802.09649` · Delplace, Marston,
Venaille `1702.07583` · Weinfurtner et al. `1008.1911` · Euvé et al.
`1511.08145` · Torres et al. `1612.06180`.

**E.** Moisy, Rabaud & Salsac, *Exp. Fluids* 46, 1021 (2009) [EXTERNE] —
Schlieren synthétique de surface libre.

**Contexte AdS/CMT.** Ryu & Takayanagi `hep-th/0603001` · Gu, Lee, Wen, Cho,
Ryu `1605.00570` · Nozaki, Ryu, Takayanagi `1208.3469` · Ryu & Takayanagi
`1001.0763` · Ryu, Moore, Ludwig `1010.0936` · Pastawski et al. `1503.06237`.
