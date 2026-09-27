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
Une rangée 1D de piliers à espacements alternés, comportant un mur de domaine où
l'alternance s'inverse, porte un mode localisé à la fréquence du milieu du gap,
absent d'une rangée à espacement uniforme.

### Observable
Amplitude de surface $|\eta(x)|$ le long de la chaîne, en détection synchrone à
la fréquence d'excitation, mesurée par FS-SS.
Grandeur dérivée : **longueur de localisation** $\xi$, par ajustement de
$|\eta(x)| \propto e^{-|x - x_0|/\xi}$ autour du mur.

### Protocole
- Aquarium ≥ 100 cm, profondeur 8 cm (eau profonde pour $\lambda \le 6$ cm).
- Piliers imprimés, diamètre 1,5 cm ; espacements alternés 3 / 5 cm ;
  ≥ 10 cellules de part et d'autre du mur.
- Excitation : moteur pas-à-pas piloté par microcontrôleur, $f = 5$ Hz
  ($\lambda \approx 6{,}2$ cm), verrouillée au quartz.
- Eau déminéralisée ; surface écrémée avant chaque acquisition.
- 5 répétitions ; chaîne uniforme (sans mur) comme témoin.

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
  briser l'inversion ; ≥ 8 cellules de chaque côté du mur.
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
