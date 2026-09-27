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
