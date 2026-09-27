# « Holographie analogique de garage » — évaluation et feuille de route de remplacement

**Objet.** Le projet fusion proposé (réseau hyperbolique imprimé en 3D,
éclats de CD comme « miroirs quantiques », laser dans la carcasse du four,
panneaux solaires en photodiodes sur le pourtour, IA reconstruisant
l'intérieur, Gudhi extrayant « des nombres de Betti ou un invariant de
Chern », Lean 4 prouvant un « isomorphisme volume–bord »), évalué étape par
étape, puis remplacé par un protocole qui **garde l'objectif** — *la
frontière détermine le volume, dans un système physique qu'on peut mesurer*
— avec des moyens qui fonctionnent et une littérature qui existe.

Toutes les références marquées `[CORPUS]` ont passé la porte d'identité
(`corpus/fetch_papers.py`, 94/94). Tiers Elenchus `X<C<L<B<A` comme dans
[`rigor_protocol.md`](rigor_protocol.md). Ce document complète
[`roadmap.md`](roadmap.md) (piste H) sans le remplacer.

---

## 0. Verdict en une page

| Étape proposée | Ce qui est affirmé | Statut | Remplacement |
|---|---|---|---|
| Cadrage | AdS/CFT = « théorème… vérité mathématique formelle absolue » | **Faux** : conjecture, extraordinairement testée, jamais démontrée | dire « conjecture » ; c'est déjà beaucoup |
| Cadrage | réseau Kagome dans l'eau ⇒ onde unidirectionnelle sur le bord | **Faux** sans brisure du renversement du temps ($C=0$ pour un réseau immobile) | bassin **tournant** (Coriolis) — Delplace–Marston–Venaille `1702.07583` |
| 1 | réseau hyperbolique imprimé = « géométrie exacte d'AdS » | **Réel**, et déjà réalisé sur table (`1802.09549`, `2109.01148`) | garder — mais en **circuit**, pas en optique |
| 1 | éclats de CD = « miroirs quantiques » | **Faux** : réseaux de diffraction, classiques | supprimer |
| 1 | laser dans la carcasse du four, « volume à $N$ dimensions » | **Impraticable** (modes optiques non résolubles, [`experimental_program.md`](experimental_program.md) §4.1) ; et c'est 2D | réseau de résistances / LC sur plaque |
| 2 | panneaux solaires = photodiodes ultrasensibles du bord | **Faux** (aucune résolution spatiale, bande passante nulle, §7.1) | nœuds de bord d'un circuit, lus par ADC / carte son |
| 2 | « on n'a pas le droit de regarder à l'intérieur » | **Juste** — c'est la bonne règle du jeu | garder telle quelle |
| 3 | l'IA reconstruit l'intérieur ⇒ « essence du principe holographique démontrée » | **Faux comme conclusion**, réel comme problème : c'est un **problème inverse sur réseau**, dont l'unicité est un **théorème** (Curtis–Morrow) | reconstruction exacte par le théorème ; l'IA notée contre elle |
| 4 | corrélation croisée des capteurs ≡ intrication de Ryu–Takayanagi | **Faux** : corrélations classiques ≠ entropie d'intrication ; aucune surface minimale n'en découle | corrélateur bord-à-bord et sa **loi de puissance** (`2005.12726`) |
| 4 | Gudhi révèle « nombres de Betti ou invariant de Chern » = nombre de trous imprimés | **Faux** trois fois (Betti ≠ Chern ≠ trous) | Gudhi comme détecteur de changement, avec témoins, Tier X |
| 5 | Lean prouve « l'isomorphisme strict » volume–bord sur le graphe | **Pas un théorème** tel qu'énoncé | formaliser Curtis–Morrow sur un petit réseau : *le* théorème « le bord détermine le volume » |

**Ce qui est bon dans le projet et qu'il faut garder :** l'intuition que
les réseaux hyperboliques sont un simulateur de table de l'holographie —
Boettcher, Gorshkov, Kollár & Maciejko l'écrivent en toutes lettres
(`2105.01087`) — et la règle « mesurer seulement le bord ».

---

## 1. Ce qui existe déjà, et que le projet redécouvre

- **Réseaux hyperboliques réalisés.** Kollár, Fitzpatrick & Houck
  (`1802.09549` [CORPUS]) : réseaux de résonateurs supraconducteurs formant
  des pavages réguliers d'un espace à courbure négative constante.
  Lenggenhager *et al.* (`2109.01148` [CORPUS], *Nat. Commun.* 2022) :
  **« Simulating hyperbolic space on a circuit board »** — un réseau
  électrique, les états propres du « tambour hyperbolique » mesurés, la
  propagation le long des géodésiques vérifiée. **C'est la plateforme de
  garage.**
- **Théorie de bande hyperbolique.** Maciejko & Rayan (`2008.05489`) :
  ondes de Bloch sans translations commutatives, moment cristallin sur une
  surface de Riemann de genre supérieur. Cristallographie : `2105.01087`.
- **Isolants topologiques hyperboliques.** Urwyler *et al.* (`2203.07292`,
  PRL 2022) : modèles de Haldane et Kane–Mele sur octogones ; **la
  correspondance volume–frontière y est mise en évidence** (densités
  d'états volume/bord, propagation de bord, robustesse au désordre).
- **Holographie discrète, testée.** Asaduzzaman, Catterall, Hubisz & Nelson
  (`2005.12726`, PRD 2020) : corrélateurs bord-à-bord d'un champ scalaire
  sur des pavages de $\mathbb{H}^2$ et $\mathbb{H}^3$ ; **la relation du
  continu entre masse du champ dans le volume et dimension d'échelle du
  corrélateur de bord survit à la discrétisation.** Brower *et al.*
  (`1912.07606`) : théorie des champs sur réseau en AdS$_2$. Basteiro,
  Di Giulio, Erdmenger & Karl (`2205.05693`, SciPost 2022) : chaînes de
  spins **apériodiques** obtenues du pavage par règle d'inflation, et
  reconstruction discrète du volume par réseau de tenseurs.
- **Le lien avec Ryu.** La cartographie holographique exacte de Gu, Lee,
  Wen, Cho & Ryu (`1605.00570`) et la métrique émergente du cMERA de Nozaki,
  Ryu & Takayanagi (`1208.3469`) sont les versions « réseau de tenseurs » du
  même programme ; les codes HaPPY (`1503.06237`) vivent sur un pavage
  hyperbolique ; revue : Jahn & Eisert (`2102.02619`).

Autrement dit : « les isolants topologiques comme simulateurs de
l'holographie » n'est pas une intuition à prouver dans une cave, c'est un
champ publié depuis 2019 — dans lequel on peut **entrer** avec le bon
montage.

---

## 2. La physique qu'on peut réellement mesurer sur le bord

Trois énoncés, chacun falsifiable, chacun avec sa littérature.

### 2.1 Le bord détermine le volume — comme théorème (problème inverse)

Sur un **réseau de résistances**, injecter un courant en un nœud du bord et
lire les potentiels des autres nœuds du bord donne la matrice de réponse
(Dirichlet-vers-Neumann). Pour un graphe **planaire circulaire critique**,
cette matrice **détermine toutes les conductances intérieures**, et un
algorithme explicite les reconstruit — Curtis, Ingerman & Morrow, *Linear
Algebra Appl.* 283 (1998) ; Colin de Verdière, *Comment. Math. Helv.* 69
(1994) ; livre Curtis & Morrow, *Inverse Problems for Electrical Networks*
(2000) **[EXTERNE]**. Hors de cette classe, l'unicité échoue : la
« reconstruction par IA » n'a de sens qu'avec ce théorème derrière.

**C'est exactement ce que l'étape 3 voulait, et l'étape 5 voulait prouver.**
Ce n'est pas l'holographie (pas de gravité, pas d'intrication) ; c'est un
énoncé précis, vrai, formalisable, et physiquement testable avec 100 € de
composants.

### 2.2 La signature holographique discrète — loi de puissance au bord

Sur un pavage de $\mathbb{H}^2$, le corrélateur bord-à-bord d'un champ de
masse $m$ décroît en loi de puissance de la distance **le long du bord**,
avec un exposant $2\Delta$ fixé par la relation AdS $\Delta(\Delta-1)=m^2$
(en unités de rayon) — et cela survit au réseau (`2005.12726`). Un réseau
de résistances réalise le cas **sans masse** (Laplacien) : $\Delta=1$,
prédiction fixe. Un réseau **LC** avec capacité vers la masse ajoute un
terme de masse réglable : on peut alors **balayer $m$ et mesurer $\Delta$**
— c'est le test de `2005.12726` sur table.

### 2.3 Le tambour hyperbolique — ordre spectral

Le classement des états propres du Laplacien est universellement différent
en géométrie hyperbolique et plate (`2109.01148`) ; mesurable avec les
mêmes nœuds de bord, en fréquence. Contrôle : le même circuit, recâblé en
pavage plat, ne le montre pas.

**Ce que ces trois énoncés ne sont pas :** une preuve du principe
holographique, ni de la gravité émergente. Ce sont ses **ombres
discrètes**, et c'est ainsi qu'il faut les nommer dans tout écrit.

---

## 3. Protocole de remplacement — Piste H

### H0 — Numérique (moi, semaines 1–2, Tier X)
Construire le graphe du pavage $\{7,3\}$ (et $\{8,3\}$) par inflation en
couches concentriques (règles de `2205.05693`), 3–5 couches (le nombre de
nœuds croît exponentiellement, et le bord reste une fraction finie du
total : c'est la signature hyperbolique, et la raison pour laquelle
quelques centaines de nœuds suffisent). Calculer : Laplacien, réponse de
bord, fonction de Green bord-à-bord, ordre spectral. Vérifier la loi de
puissance $\Delta=1$ sur ≥ 1 décade de distance de bord ; vérifier la
**recouvrabilité** Curtis–Morrow sur la matrice de réponse *simulée*
(reconstruire des conductances intérieures modifiées). **Critère d'arrêt :**
pas de loi de puissance sur une décade ⇒ disque trop petit ; reconstruction
impossible ⇒ la troncature n'est pas dans la classe critique, changer de
couche/de pavage. Rien ne se fabrique avant H0.

### H1a — Réseau de résistances (vous, mois 1–2)
- Nœuds : le graphe H0 (≈ 100–300 nœuds), résistances 1 % (une valeur
  nominale, plus un jeu « obstacle » différent), plaque perforée ou PCB
  (le pavage se dessine dans le disque de Poincaré ; la géométrie
  physique du câblage est sans importance, seule la **connectivité** compte —
  c'est le point qui rend le circuit supérieur à l'optique).
- Mesure : source de courant (ou tension + résistance série) sur un nœud
  de bord, lecture des potentiels de **tous** les nœuds de bord par
  multiplexeur (CD74HC4067) + ADC (ESP32/Arduino, 12 bits) ou multimètre
  USB. Répéter pour chaque nœud de bord ⇒ matrice de réponse $\Lambda$.
- Étalonnage : mesurer chaque résistance avant montage (la tolérance est
  la première source d'écart) ; comparer $\Lambda$ mesurée à $\Lambda$
  simulée avec les valeurs mesurées. **Critère d'arrêt :** écart > 10 %
  après étalonnage ⇒ contacts/câblage, corriger avant toute physique.
- Préenregistrement (avant la première mesure) : exposant du corrélateur
  de bord, $\Delta = 1 \pm 0{,}15$ ; témoin : le même nombre de nœuds en
  pavage **plat** (carré), qui doit donner une décroissance différente.

### H1b — « Le bord contient le volume » (ensemble, mois 2–3)
Modifier une ou deux résistances **intérieures** (les « obstacles »),
sans toucher au bord ; remesurer $\Lambda$ ; **reconstruire** les
conductances intérieures par l'algorithme de Curtis–Morrow, à partir du
bord seul ; comparer aux valeurs modifiées connues. Verdict préenregistré :
`CONFIRMÉ` si les résistances modifiées sont identifiées et leurs valeurs
retrouvées à 15 % ; `RÉFUTÉ` sinon ; `INVALIDE` si H1a n'a pas passé son
critère. **L'IA** (réseau appris de $\Lambda \to$ conductances) est
entraînée sur des $\Lambda$ simulées et **notée contre la reconstruction
exacte**, jamais l'inverse ; Tier X.

### H2 — Gudhi (mois 3, Tier X)
Homologie persistante sur la matrice de distance dérivée de $\Lambda$ (ou
des corrélations de bord), **avant/après** modification intérieure, avec
deux témoins : aucune modification (le diagramme doit être stable au bruit
de mesure) et modification aléatoire d'une résistance de **bord** (le
diagramme doit changer autrement). Ce que cela peut établir : que la
signature de bord change de façon détectable et robuste quand le volume
change. Ce que cela ne peut pas établir : un nombre de Chern, un nombre de
trous, une entropie d'intrication.

### H1c — Réseau LC : masse ↔ dimension (mois 4–6)
Remplacer les résistances par des inductances entre nœuds et une capacité
vers la masse par nœud (le « tambour hyperbolique » de `2109.01148`) ;
excitation par carte son ou générateur, lecture par carte son / NanoVNA.
Deux mesures : l'ordre spectral (§2.3) contre le témoin plat ; la loi de
puissance du corrélateur de bord en fonction de la « masse » (rapport
C/L) — **le test de `2005.12726` sur table.** Préenregistrer la relation
$\Delta(\Delta-1)=m^2$ avec sa barre d'erreur.

### H3 — Lean 4 (mois 3–9, Tier A visé)
Formaliser **Curtis–Morrow** pour un petit réseau planaire circulaire
critique (algèbre linéaire finie, Mathlib) : *la matrice de réponse de
bord détermine les conductances intérieures.* C'est l'énoncé « le bord
détermine le volume » sous sa forme vraie, et — à notre connaissance —
jamais formalisé. Porte : LeanMaster (`sorry`, axiomes, verrou d'énoncé).
Piège : ne pas définir « recouvrable » par « ce que l'algorithme renvoie ».

### H4 — Le bassin tournant (option, mois 6+)
La seule façon d'obtenir dans l'eau l'onde **unidirectionnelle** sur le
bord que le projet imaginait : un plateau tournant (Coriolis brise le
renversement du temps), ondes de Kelvin/Yanai — origine topologique
établie par `1702.07583` sur les ondes équatoriales de la Terre. C'est
l'axe 1c ; il demande un plateau tournant stable (platine de tourne-disque
lourde, ou moteur + réducteur) et la Schlieren embarquée.

---

## 4. Nomenclature (piste H, hors bassin)

| Élément | Solution | Coût indicatif |
|---|---|---|
| Réseau H1a | 150–300 résistances 1 % (deux valeurs), plaque perforée/PCB, fils | 15–30 € |
| Mesure | ESP32 (ADC 12 bits) + 2–3 multiplexeurs CD74HC4067, ou multimètre USB | 15–25 € |
| Source | régulateur de tension + résistance série (source de courant approx.) | 5 € |
| Réseau H1c | inductances (mH) + condensateurs (nF), carte son USB ou NanoVNA | 40–80 € |
| Logiciel | scripts du dépôt (H0), reconstruction Curtis–Morrow, Gudhi | 0 |

Sécurité : basse tension continue ; aucun des dangers du bassin, du laser
ou du four. **Le four et le laser ne servent à rien dans cette piste.**

---

## 5. Jalons

| Mois | Jalon | Livrable | Critère d'arrêt |
|---|---|---|---|
| 0,5 | **H0** graphe, Green, recouvrabilité simulée | scripts + figures, Tier X | pas de loi de puissance sur 1 décade / non recouvrable |
| 1–2 | **H1a** matrice de réponse mesurée | JSON + comparaison à la simulation | écart > 10 % après étalonnage |
| 2–3 | **H1b** reconstruction depuis le bord | verdict préenregistré | — un `RÉFUTÉ` propre est un résultat |
| 3 | **H2** Gudhi avec témoins | diagrammes + témoins | témoins non discriminants ⇒ méthode inutile ici, on le dit |
| 4–6 | **H1c** masse ↔ dimension | courbe $\Delta(m)$ vs `2005.12726` | — |
| 3–9 | **H3** Curtis–Morrow en Lean | théorème, porte LeanMaster | énoncé affaibli ⇒ refus |
| 6+ | **H4** bassin tournant | option | — |

Article visé (mois ~7) : *Boundary determines bulk on a tabletop
hyperbolic resistor network: exact inverse reconstruction, discrete
holographic scaling, and a kernel-verified recoverability theorem.* Trois
énoncés, trois tiers (B, X, A), aucun mot sur la gravité quantique.

---

## 6. Références

**Pavages hyperboliques et holographie discrète [CORPUS].** Kollár,
Fitzpatrick, Houck `1802.09549` · Boettcher, Bienias, Belyansky, Kollár
`1910.12318` · Maciejko & Rayan `2008.05489` · Boettcher, Gorshkov, Kollár,
Maciejko `2105.01087` · Lenggenhager *et al.* `2109.01148` · Urwyler,
Lenggenhager, Boettcher, Thomale `2203.07292` · Asaduzzaman, Catterall,
Hubisz, Nelson `2005.12726` · Brower, Cogburn, Fitzpatrick, Howarth
`1912.07606` · Basteiro, Di Giulio, Erdmenger, Karl `2205.05693` · Jahn &
Eisert `2102.02619`.

**Holographie et Ryu [CORPUS].** Ryu & Takayanagi `hep-th/0603001` · Gu,
Lee, Wen, Cho, Ryu `1605.00570` · Nozaki, Ryu, Takayanagi `1208.3469` ·
Pastawski, Yoshida, Harlow, Preskill `1503.06237`.

**Ondes chirales classiques [CORPUS].** Delplace, Marston, Venaille
`1702.07583` · Souslov, Dasbiswas, Fruchart `1802.09649`.

**Problèmes inverses sur réseaux [EXTERNE].** Curtis, Ingerman & Morrow,
*Circular planar graphs and resistor networks*, Linear Algebra Appl. 283,
115 (1998) · Colin de Verdière, *Réseaux électriques planaires I*, Comment.
Math. Helv. 69, 351 (1994) · Curtis & Morrow, *Inverse Problems for
Electrical Networks*, World Scientific (2000).
