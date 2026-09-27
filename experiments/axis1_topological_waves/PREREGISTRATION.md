# Axe 1 — Ondes de surface topologiques

> À compléter et **commiter avant toute acquisition**. L'horodatage git fait foi.
> Protocole : [`../../docs/rigor_protocol.md`](../../docs/rigor_protocol.md).
> Analyse critique : [`../../docs/experimental_program.md`](../../docs/experimental_program.md) §1.

Deux expériences distinctes, préenregistrées séparément. **1a doit être terminée
avant que 1b commence** : 1a valide le réseau, la métrologie et le premier
théorème Lean sur le cas le plus simple.

---

## 1a — Chaîne SSH : mode de mur de domaine

### Affirmation
Un canal étroit dont la section alterne (résonateurs couplés à couplages
alternés $v$, $w$), comportant un mur de domaine où l'alternance s'inverse,
porte un mode localisé à la fréquence du milieu du gap, absent d'un canal à
section uniforme.

### Observable
Amplitude de surface $|\eta(x)|$ le long de la chaîne, en détection synchrone à
la fréquence d'excitation, mesurée par FS-SS.
Grandeur dérivée : **longueur de localisation** $\xi$, par ajustement de
$|\eta(x)| \propto e^{-|x - x_0|/\xi}$ autour du mur.

### Protocole — valeurs **provisoires**
Les nombres ci-dessous sont provisoires jusqu'à ce qu'un calcul de bandes du
canal (matrice de transfert) les fixe. Ce calcul doit être commité **avant**
de verrouiller ce préenregistrement. Premier artefact déjà disponible :
[`ssh_check.py`](ssh_check.py), qui vérifie l'énoncé SSH et donne la fréquence
de Bragg selon la période.

- Aquarium ≥ 100 cm ; profondeur $h$ telle que $h > \lambda/2$ (eau profonde).
- **Canal** de largeur $< \lambda/2$ (un seul mode transverse), parois
  imprimées, sections alternées étroit/large ; ≥ 10 cellules de part et
  d'autre du mur. Une rangée de piliers dans le bassin ouvert **ne convient
  pas** : l'énergie fuit latéralement.
- **Toutes les parois et tous les obstacles traversent la surface.** En eau
  profonde, l'amplitude au fond vaut $e^{-kh}$ — à $kh \approx 8$, $3\times10^{-4}$ :
  un obstacle posé au fond est invisible.
- Période du canal $a = 8$ cm → premier gap de Bragg à $\lambda = 2a = 16$ cm,
  **$f \approx 3{,}1$ Hz** (`ssh_check.py`), donc $h \ge 8$ cm. La fréquence au
  milieu du gap sera fixée par le calcul de bandes.
- Excitation : moteur pas-à-pas piloté par microcontrôleur, verrouillé au
  quartz.
- Eau déminéralisée ; surface écrémée avant chaque acquisition.
- 5 répétitions ; canal uniforme (sans mur) comme témoin.

### Prédiction
Un pic d'amplitude au mur de domaine, avec $\xi$ entre 1 et 3 pas de réseau
(3–15 cm), et un rapport pic/fond $\ge 3$.
Le témoin uniforme ne présente aucun pic ($< 1{,}3$).

### Hypothèse nulle
Aucune localisation : $|\eta(x)|$ décroît de façon monotone depuis la source,
sans structure au mur, et le profil est indiscernable du témoin.

### Critère de réfutation
Rapport pic/fond $< 1{,}5$, ou $\xi$ non distinguable de la longueur
d'atténuation visqueuse mesurée sans réseau.

### Analyses prévues
Détection synchrone à $f$ ; ajustement exponentiel de $\xi$ ; test de Welch
entre configurations mur et témoin.

### Causes d'échec connues (→ `INVALIDE`, non `RÉFUTÉ`)
- **Amortissement de surface** : si l'onde est atténuée de plus de 50 % avant
  d'atteindre le mur, rien n'est mesuré. **À vérifier en premier**, sans réseau.
- Ondes stationnaires sur les parois : absorbeurs en biseau aux extrémités.
- Régime capillaire si $\lambda < 1{,}7$ cm : rester à $f \le 7$ Hz.
- Obstacles ne traversant pas la surface : invisibles en eau profonde.
- Dérive de fréquence du générateur : à enregistrer en continu.

---

## 1b — Réseau valley-Hall 2D : test au défaut

### Affirmation
Un réseau nid d'abeille de piliers à inversion brisée ouvre un gap aux points de
Dirac ; un mur de domaine entre deux orientations opposées guide l'onde, et la
transmission reste élevée lorsqu'un pilier est retiré du guide.

### Observable
Transmission $T = P_{\text{sortie}}/P_{\text{entrée}}$ le long du mur de
domaine, dans le gap, avec et sans pilier retiré.
Accessoirement : relation de dispersion par FFT 2D spatio-temporelle de
$\eta(x,y,t)$.

### Protocole
- Nid d'abeille, pas $a = 5$ cm, deux diamètres de piliers (1,0 et 2,0 cm) pour
  briser l'inversion ; ≥ 8 cellules de chaque côté du mur. **Piliers émergents**
  (traversant la surface), pour la même raison qu'en 1a.
- Balayage $f$ de 3 à 7 Hz par pas de 0,25 Hz pour localiser le gap.
- Trois configurations : guide intact ; **un** pilier retiré du guide ; guide
  trivial de contrôle (même géométrie, pilier unique — pas de topologie).
- 5 répétitions par configuration.

### Prédiction
Gap observable (transmission chutant d'un facteur $\ge 5$ hors du mur de
domaine). Sur le mur, $T$ élevée dans le gap. **Avec un pilier retiré, $T$
diminue de moins de 30 %.**

### Hypothèse nulle
Le retrait d'un pilier fait chuter $T$ autant que dans le guide trivial : aucune
protection.

### Critère de réfutation
Chute de $T$ supérieure à 50 %, ou indiscernable de celle du guide trivial.

### Note d'honnêteté — c'est ici que ça peut casser, légitimement
Les modes valley-Hall ne sont protégés que contre la diffusion **conservant la
vallée**, donc contre un désordre lisse à l'échelle du réseau. **Un pilier
manquant est un diffuseur abrupt qui mélange les vallées et rétrodiffuse.**
La prédiction « moins de 30 % » est donc un pari, pas une certitude : c'est
exactement le test qui a une vraie chance d'échouer.

**Une réfutation ici est un résultat, pas un échec** — elle mesure
quantitativement la limite de la protection de vallée, ce qui est plus
intéressant qu'une confirmation. Elle ne doit en aucun cas être reclassée en
`INVALIDE` après coup : le seuil de 30 % est fixé maintenant.

### Ce que cette expérience ne montre pas
Rien sur AdS/CMT. Les ondes d'eau sont classiques et linéaires : ni intrication,
ni corrélations fortes. Le résultat porte sur la topologie de bande à une
particule (pilier 3 de la revue), pas sur l'holographie.
