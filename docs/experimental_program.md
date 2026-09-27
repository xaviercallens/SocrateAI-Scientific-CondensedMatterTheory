# Programme expérimental « Garage Deep Tech » — revue critique et plan révisé

**Objet.** Revue du plan en 5 axes reliant matériel de récupération, IA, TDA
(Gudhi) et formalisation Lean 4, sous l'angle : *qu'est-ce qui marchera
réellement, et qu'est-ce qui ne marchera pas ?*

**Méthode.** Chaque axe reçoit un verdict de faisabilité, les nombres qui le
justifient, les erreurs de physique à corriger, et un protocole révisé. Les
verdicts sont vérifiables : ils reposent sur des ordres de grandeur explicites,
pas sur une appréciation.

**Résumé des verdicts**

| Axe | Sujet | Verdict | Blocage principal |
|---|---|---|---|
| 5 | Caustiques / catastrophes | **Faisable, le meilleur** | aucun |
| 1 | Ondes topologiques | **Faisable, révisé** | mesure : caméra, pas panneaux solaires |
| 2 | Horizon analogue | **Faisable si reformulé** | Hawking spontané indétectable (~10⁻¹² K) |
| 4 | Chaos ondulatoire | **Faisable après pivot** | version optique impraticable ; passer au micro-ondes + VNA |
| 3 | Vortex optiques | **Bloqué tel quel** | lame spirale imprimée : 40–80× trop grossière |

Trois corrections transversales valent pour tout le programme et sont traitées
en §7 : les panneaux solaires ne sont pas des photodétecteurs utilisables, le
bloc optique des lecteurs CD/DVD est le meilleur composant récupérable et il est
sous-exploité, et l'ambition Lean 4 doit être échelonnée sous peine de tout
bloquer.

---

## 0. Une mise au point qui conditionne tout le reste

Le plan s'ouvre sur : « la topologie possède une propriété mathématique sublime :
elle est invariante d'échelle. Les équations qui protègent un électron quantique
ou qui courbent l'espace-temps s'appliquent avec la même rigueur aux ondes à la
surface de l'eau. »

**Ce qui est exact.** Les états de bord topologiques ne viennent pas de la
mécanique quantique. Ils viennent de la topologie du fibré de Bloch au-dessus
de la zone de Brillouin, et cette structure existe pour *toute* équation d'onde
linéaire dans un milieu périodique. C'est pourquoi les isolants topologiques
photoniques, phononiques, mécaniques et hydrodynamiques existent réellement et
sont publiés. Un réseau de piliers dans un aquarium peut authentiquement porter
un invariant topologique. **L'axe 1 repose sur de la physique solide.**

**Ce qui ne l'est pas, et c'est important pour la suite.** « Les équations qui
courbent l'espace-temps s'appliquent aux ondes à la surface de l'eau » est faux
tel quel. L'analogie de Unruh reproduit la **cinématique** — un champ se
propageant sur une métrique effective courbe — mais **pas la dynamique** :
l'écoulement d'eau n'obéit pas aux équations d'Einstein. Il n'y a pas de
constante de Newton, pas d'action d'Einstein–Hilbert, pas de rétroaction du
champ sur la géométrie. Unruh lui-même insiste sur ce point.

Conséquence opérationnelle : **l'axe 2 peut tester la diffusion de type Hawking
sur un horizon. Il ne peut rien dire sur la gravité quantique, ni sur
l'holographie.** Écrire le contraire dans un article le ferait rejeter d'emblée.

**Et un lien qu'il faut couper.** Ce programme expérimental touche le **pilier 3**
de la revue de littérature (topologie de bande à une particule). Il ne touche
**ni** le pilier 1 **ni** le pilier 2 (holographie, AdS/CMT). La raison est
nette : AdS/CMT porte sur des systèmes **fortement corrélés** sans
quasiparticules, dont le contenu physique est l'**intrication à N corps**. Les
ondes d'eau sont classiques et linéaires : aucune intrication, aucune
corrélation forte. Le dispositif ne peut donc pas sonder la correspondance
AdS/CMT. Il peut sonder, très bien, la correspondance volume–frontière au sens
de la théorie de bande. Ce sont deux choses différentes — c'est exactement la
distinction établie au §5 de [`literature_review.md`](literature_review.md).

C'est une limite de portée, pas une objection : la correspondance
volume–frontière à une particule est un sujet légitime, vérifiable sur
table, et formalisable en Lean. C'est même le seul des trois qui soit à la fois
expérimentalement accessible et formellement prouvable avec les moyens décrits.

---

## 1. Axe 1 — Aquarium topologique

**Verdict : faisable, avec deux corrections et un changement de métrologie.**

### 1.1 Les nombres

Ondes de gravité en eau profonde : $\omega^2 = gk$, donc
$\lambda = g/(2\pi f^2)$.

| $f$ | $\lambda$ |
|---|---|
| 3 Hz | 17 cm |
| 5 Hz | 6,2 cm |
| 7 Hz | 3,2 cm |
| 10 Hz | 1,6 cm |

La tension superficielle prend le dessus en dessous de la longueur capillaire
$\lambda_c = 2\pi\sqrt{\sigma/\rho g} \approx 1{,}7$ cm. **Il faut donc rester
au-dessus de ~3 cm**, soit $f \lesssim 7$ Hz.

Avec un pas de réseau $a \sim \lambda/2$ à $\lambda$, soit 3–8 cm, et le besoin
d'au moins 8–10 cellules pour qu'une structure de bande ait un sens :
**aquarium de 80–120 cm de long minimum**. Profondeur $h > \lambda/2 \approx 3$ cm
pour rester en eau profonde ; 8–10 cm est confortable.

**Les piliers doivent traverser la surface.** En eau profonde, le mouvement
décroît comme $e^{-kz}$ : à $h = 8$ cm et $\lambda = 6$ cm, $kh \approx 8$, et
l'amplitude au fond vaut $e^{-8} \approx 3\times10^{-4}$ de celle de surface.
Des piliers posés au fond, comme dans le plan initial, sont **invisibles** pour
l'onde. Il faut des cylindres émergents, ou bien passer en eau peu profonde
avec une topographie de fond — mais alors $\omega = k\sqrt{gh}$ et tout le
tableau ci-dessus change.

**Le risque sous-estimé, c'est l'amortissement.** Aux fréquences visées, la
dissipation n'est pas dominée par la viscosité de volume mais par la
**contamination de surface** : un film de tensioactif invisible rend la surface
inextensible et peut diviser la longueur d'atténuation par un ordre de grandeur.
Un aquarium rempli d'eau du robinet, non nettoyé, peut amortir l'onde en
20–30 cm — avant même d'avoir traversé le réseau. Nettoyage rigoureux (pas de
savon résiduel), eau déminéralisée, et écrémage de la surface avant chaque
mesure. C'est la première chose à vérifier, avant d'imprimer quoi que ce soit.

### 1.2 Erreur de physique à corriger : Chern ou SSH, pas les deux

Le plan demande de « démontrer que la matrice hamiltonienne possède un **Nombre
de Chern** non nul » à partir du **modèle SSH**. Ces deux énoncés sont
incompatibles :

- Le **SSH** est unidimensionnel. Son invariant est un **nombre d'enroulement**
  (phase de Zak), pas un nombre de Chern — lequel n'est défini qu'en 2D.
- Un réseau statique dans l'eau **préserve le renversement du temps**. Le nombre
  de Chern y est **nul par symétrie**. Aucun réseau de piliers immobiles ne peut
  avoir $C \neq 0$. Pour cela il faudrait briser T — rotation d'ensemble du
  bassin (force de Coriolis) ou écoulement circulant, ce qui est un tout autre
  dispositif.

**Ce qui est réellement atteignable, en deux étapes :**

**1a — Chaîne SSH (à faire en premier).** Attention : une simple rangée de
piliers dans un bassin ouvert n'est **pas** un système 1D — l'énergie fuit
latéralement. Il faut un **canal** de largeur $< \lambda/2$ (un seul mode
transverse) dont la section alterne étroit/large, ce qui réalise une chaîne de
résonateurs couplés à couplages alternés $v, w$. Un mur de domaine (là où
l'alternance s'inverse) porte un **mode localisé** protégé par la symétrie
chirale. Simple, peu de matériel, et c'est l'énoncé formalisable en Lean
(§8). À faire avant toute chose.

**La fréquence d'excitation se calcule, elle ne se choisit pas.** Le premier
gap de Bragg est à $k = \pi/a$ : pour une période de 8 cm, $\lambda = 16$ cm et
$f \approx 3{,}1$ Hz — pas 5 Hz. Le script
[`experiments/axis1_topological_waves/ssh_check.py`](../experiments/axis1_topological_waves/ssh_check.py)
est le premier artefact de l'axe : il vérifie numériquement l'énoncé SSH visé
en Lean et donne la fréquence de Bragg selon la période.

**1b — Réseau valley-Hall 2D.** Réseau nid d'abeille de piliers, avec inversion
brisée (deux diamètres de piliers différents). Ouvre un gap aux points de Dirac
K et K′, et un mur de domaine entre deux orientations opposées porte des modes
de bord.

**Honnêteté requise sur 1b :** ces modes sont protégés contre la rétrodiffusion
**inter-vallée uniquement**, donc seulement contre un désordre *lisse à l'échelle
du réseau*. Un pilier manquant est un diffuseur atomiquement abrupt : il
**mélange les vallées** et rétrodiffuse. L'affirmation du plan — « l'onde se
concentre sur les bords en ignorant les piliers manquants » — est donc
précisément le test qui risque d'échouer, et ce serait une vraie mesure. Il faut
le préenregistrer comme tel : *prédiction — la transmission chute d'un facteur
mesurable lorsqu'on retire un pilier ; l'ampleur de cette chute est le résultat.*

### 1.3 Métrologie : remplacer les panneaux solaires

Mesurer une surface d'eau avec des panneaux solaires ne donne **aucune
résolution spatiale** (un panneau = un pixel) et une bande passante médiocre.

**La bonne technique existe, elle est peu coûteuse et standard :
la Synthetic Schlieren de surface libre** (FS-SS, Moisy–Rabaud–Salsac 2009,
**[EXTERNE]**) :

1. Imprimer un motif de points aléatoires, le placer **sous** l'aquarium
   (fond transparent, rétroéclairé).
2. Caméra au-dessus, regardant à travers l'eau.
3. Les rides défléchissent les rayons : le motif paraît se déplacer.
4. Corrélation croisée image/référence → gradient de la surface → intégration →
   **champ de hauteur complet $\eta(x,y,t)$**, sensibilité de l'ordre du
   micromètre.

Coût : une feuille imprimée et un appareil photo. C'est un gain de plusieurs
ordres de grandeur en information par rapport à un capteur ponctuel.

**Générateur d'ondes.** Le moteur de lecteur CD est un BLDC optimisé pour
200–10 000 tr/min, mal adapté à 3–7 Hz stables. Un **moteur pas-à-pas** (de la
même imprimante 3D) piloté par microcontrôleur donne une fréquence verrouillée
au quartz — indispensable puisque toute l'analyse est en détection synchrone.

### 1.4 Analyse : ce que la TDA apporte, et ce qu'elle n'apporte pas

**Franchise nécessaire : l'homologie persistante n'est pas le bon outil pour
démontrer la localisation de bord.** Les observables correctes sont :

- **FFT 2D spatiale** du champ $\eta(x,y)$ → relation de dispersion mesurée →
  lecture directe du gap et des branches de bord ;
- **rapport de participation** et **longueur de décroissance** $\xi$ transverse
  au bord → la localisation, quantifiée ;
- **transmission** avec et sans défaut → la protection, quantifiée.

Ces trois mesures répondent à la question. La persistance ne le fait pas mieux.

**Là où Gudhi apporte vraiment quelque chose :** le suivi des **défauts de
phase** (vortex) du champ complexe reconstruit. Un vortex est une classe $H_1$
robuste, et le diagramme de persistance donne un critère de détection stable au
bruit, ce que le seuillage d'intensité ne donne pas. C'est un usage honnête de
la TDA — secondaire, mais réel. À utiliser pour ce qu'elle fait bien, plutôt
que de lui confier le résultat principal.

---

## 2. Axe 2 — Horizon analogue

**Verdict : faisable, à condition de reformuler complètement l'objectif de
mesure.**

### 2.1 Le blocage : le rayonnement de Hawking spontané est indétectable

Température de Hawking analogue :
$T_H = \hbar \kappa / 2\pi k_B$, avec $\kappa$ le gradient de vitesse à
l'horizon. Pour un écoulement de paillasse, $\kappa \sim 1\ \mathrm{s^{-1}}$ :

$$T_H \sim \frac{10^{-34}}{2\pi \times 1{,}38\times10^{-23}} \sim 10^{-12}\ \mathrm{K}$$

À comparer au bruit thermique et mécanique ambiant, à 300 K. **Quatorze ordres
de grandeur.** Aucun capteur, et certainement pas un panneau solaire, ne
franchira cet écart. Le plan — « capter les micro-fluctuations (l'analogue du
rayonnement de Hawking) » — ne peut pas aboutir tel qu'écrit.

### 2.2 Ce qui se mesure réellement, et qui a déjà été fait

L'expérience réalisable est la **diffusion Hawking stimulée**, c'est ce qu'ont
mesuré Weinfurtner *et al.* (`1008.1911`) dans un canal hydraulique, puis Euvé
*et al.* (`1511.08145`), et Torres *et al.* (`1612.06180`) sur un vortex de
vidange (superradiance). Les trois sont dans le corpus (pilier `experiment`).

Principe : au lieu d'attendre une émission spontanée, on **envoie** une onde
de surface à contre-courant vers l'horizon et on mesure le **rapport de
conversion** entre le mode sortant de norme positive et le mode de norme
négative. Ce rapport suit une loi thermique en $1/\omega$ dont on extrait une
température effective. Le signal est macroscopique et mesurable par la même
FS-SS que l'axe 1.

**Reformulation de l'objectif :** non pas « détecter le rayonnement de
Hawking », mais « mesurer le rapport de conversion de modes sur un horizon
acoustique et vérifier son caractère thermique ». C'est un résultat honnête,
reproductible, et déjà validé par la littérature — donc un bon banc d'essai.

### 2.3 Dispositif

Plus accessible que le canal hydraulique : le **vortex de vidange**. Un bac
cylindrique avec une bonde centrale et une alimentation tangentielle produit un
écoulement drainant-tournant stationnaire, doté à la fois d'un horizon et d'une
ergosphère. On y mesure la **superradiance** : une onde envoyée dans le sens de
la rotation ressort **amplifiée**. C'est spectaculaire, robuste, et cela ne
demande qu'une pompe et de l'impression 3D pour le profilé d'entrée.

### 2.4 Lean 4 : corriger la cible

Le plan propose de « formaliser l'équivalence entre l'équation de Navier–Stokes
linéarisée et l'équation des géodésiques d'Einstein ». Deux erreurs :

- **Navier–Stokes contient la viscosité**, qui détruit l'analogie. La métrique
  acoustique se dérive d'un écoulement **non visqueux, irrotationnel et
  barotrope** — c'est-à-dire d'**Euler**, pas de Navier–Stokes.
- Les perturbations obéissent à l'équation de **Klein–Gordon sans masse**
  $\Box_g \phi = 0$ dans la métrique acoustique, **pas** à l'équation des
  géodésiques (laquelle décrit une particule ponctuelle ; les géodésiques ne
  sortent qu'en limite eikonale).

**Énoncé correct, et formalisable :** *soit un écoulement irrotationnel,
non visqueux, barotrope ; alors les perturbations linéaires du potentiel de
vitesse satisfont $\partial_\mu(\sqrt{-g}\,g^{\mu\nu}\partial_\nu \phi) = 0$
avec $g_{\mu\nu}$ la métrique acoustique de Unruh.* C'est un calcul algébrique
fini, sans analyse difficile — un objectif Lean réaliste (niveau T2, §8).

---

## 3. Axe 3 — Vortex optiques

**Verdict : bloqué tel quel. Deux voies de contournement, dont une excellente.**

### 3.1 Le blocage, chiffré

Une lame de phase spirale de charge $\ell$ exige une hauteur totale :

$$h = \frac{\ell \lambda}{n-1}$$

Pour $\lambda = 650$ nm et $n = 1{,}5$ : $h = 1{,}3\ \mu\mathrm{m}$ par unité de
charge, avec une précision de forme de l'ordre de $\lambda/10 = 65$ nm.

Or une imprimante FDM a une hauteur de couche de 50–200 µm, une SLA de 25–50 µm.
**La structure entière à réaliser est 40 à 80 fois plus petite que la plus
petite marche imprimable**, et la rugosité de surface dépasse la hauteur totale
visée. Ce n'est pas une question de réglage : c'est un écart d'échelle
irréductible. **Une lame de phase spirale imprimée en 3D ne produira pas de
vortex optique.**

### 3.2 Voie A — l'hologramme en fourche (garde la lumière)

La méthode classique et peu coûteuse : imprimer sur **film transparent** un
**réseau en fourche** (le motif d'interférence entre une onde plane et une onde
hélicoïdale — une figure de franges avec une dislocation au centre). Une
imprimante laser à 1200 dpi donne des traits de ~21 µm ; avec un pas de réseau
de 50–100 µm, l'ordre $\pm1$ diffracté porte la charge topologique $\pm\ell$.

C'est la méthode historique de Bazhenov, Vasnetsov & Soskin (1990,
**[EXTERNE]**), et elle fonctionne
avec un pointeur laser. **Voie recommandée si l'optique est l'objectif.**

Variante supérieure si un vidéoprojecteur est disponible : sa **dalle LCD**,
extraite et placée entre polariseurs croisés, est un **SLM** — modulateur
spatial de lumière — pilotable en direct. On affiche l'hologramme en fourche à
l'écran et on change la charge topologique par logiciel. C'est ce que font les
laboratoires, avec du matériel de récupération.

### 3.3 Voie B — passer à l'acoustique (garde l'imprimante 3D)

L'obstacle est un rapport d'échelle entre $\lambda$ et la résolution
d'impression. Il disparaît si l'on change de $\lambda$ : à 3 kHz dans l'air,
$\lambda \approx 11$ cm.

**Mais une lame *transmissive* ne marche pas en acoustique.** L'impédance du
PLA ($\sim 3\times10^6$ Rayl) vaut environ $10^4$ fois celle de l'air
($\sim 413$ Rayl) : une plaque de 1 cm transmet environ −44 dB à 3 kHz (loi de
masse). Elle se comporte en **miroir**, pas en lame de phase. Deux montages qui
fonctionnent :

- **Surface hélicoïdale réfléchissante** imprimée : à la réflexion, le chemin
  est doublé, donc la hauteur totale vaut $\ell\lambda/2 \approx 5{,}5$ cm — très
  facile à imprimer.
- **Anneau de 4 à 8 petits haut-parleurs**, alimentés par une interface audio
  multicanal avec des déphasages $2\pi\ell n/N$. C'est le plus simple, et
  $\ell$ devient un **paramètre logiciel** : on passe de $\ell = 1$ à
  $\ell = -2$ sans rien refabriquer. **Montage recommandé.**

Le **vortex acoustique** porte exactement le même moment cinétique orbital, la
même singularité de phase, le même nombre d'enroulement quantifié. La mesure est
plus simple (un microphone déplacé sur une grille donne amplitude **et** phase,
ce qui est bien plus difficile en optique). Et le théorème Lean visé — le
nombre d'enroulement est un entier conservé — est **identique**.

**C'est la meilleure voie du point de vue coût/rigueur** : elle préserve
l'intégralité du contenu mathématique et supprime le blocage physique ;
l'imprimante 3D ne sert plus qu'aux supports, ou au réflecteur hélicoïdal.

### 3.4 Correction factuelle

Le plan attribue au CD un pas de piste de 0,74 µm. C'est celui du **DVD**. Pas
réels : **CD 1,6 µm, DVD 0,74 µm, Blu-ray 0,32 µm**. À $\lambda = 650$ nm, le
premier ordre sort à $\theta = \arcsin(\lambda/d)$, soit **24° pour un CD** et
**61° pour un DVD**. La différence est visible à l'œil et sert de vérification
du montage.

---

## 4. Axe 4 — Billards chaotiques

**Verdict : la version optique est impraticable. Le pivot micro-ondes est
excellent et bon marché.**

### 4.1 Pourquoi la version optique ne marche pas

- **Les morceaux de CD ne sont pas des miroirs.** La couche d'aluminium est
  réfléchissante, mais elle est **gravée d'un réseau de 1,6 µm** : elle
  *diffracte*. Un « billard tapissé de CD » disperse la lumière en ordres
  multiples à chaque rebond. Utiliser du **mylar aluminisé** ou des miroirs
  première surface.
- **Le chaos *ondulatoire* exige des modes résonants**, pas des rayons. Dans une
  cavité de 20 cm à $\lambda = 650$ nm, l'espacement des modes est de l'ordre de
  $\lambda^2/(2L) \sim 10^{-12}$ m — il faudrait un laser monomode accordable
  à la dizaine de MHz. Un laser de chantier n'en est pas un.
- On peut visualiser de belles **trajectoires de rayons** (fumée, fluorescéine),
  ce qui illustre le chaos classique. Mais la loi de Weyl et la statistique GOE,
  qui sont le cœur scientifique de l'axe, sont **ondulatoires** et resteront
  hors de portée.

### 4.2 Le pivot : billard micro-ondes

C'est l'expérience canonique du chaos ondulatoire (Stöckmann, Richter,
**[EXTERNE]**), et elle
devient accessible :

- La **carcasse du four** est une cavité métallique d'environ 30 × 30 cm.
  En insérant une plaque pour réduire la hauteur à $d = 8$ mm, seuls les modes
  TM₀ existent en dessous de $c/2d = 18{,}7$ GHz : la cavité est
  **rigoureusement bidimensionnelle**, et l'équation de Helmholtz y est celle
  d'un billard quantique. C'est l'usage le plus intelligent qu'on puisse faire
  de ce four — et il est **totalement passif : magnétron déposé, condensateur
  retiré**.
- Un **NanoVNA / LiteVNA** (~60–100 €, jusqu'à 6 GHz) et deux antennes fouet
  mesurent $S_{21}(f)$. Chaque résonance est un mode propre.
- Une pièce imprimée en 3D recouverte d'adhésif aluminium fait le diffuseur de
  **Sinaï** — et sa position est déplaçable, ce qui donne des familles de
  spectres.

**Nombre de modes accessibles.** Loi de Weyl $N(k) \simeq A k^2/4\pi$ ; avec
$A = 0{,}09\ \mathrm{m^2}$ et $f = 6$ GHz ($k = 126\ \mathrm{m^{-1}}$) :
$N \approx 113$ modes.

C'est **largement assez pour ajuster la loi de Weyl** (le terme dominant et la
correction de périmètre). C'est **juste à la limite pour la statistique
spectrale** : distinguer GOE de Poisson sur ~113 niveaux est possible mais
bruité. Deux remèdes : agrandir la cavité, ou moyenner sur plusieurs positions
du diffuseur. **À préenregistrer honnêtement : la loi de Weyl est l'objectif
principal, la statistique GOE l'objectif secondaire.**

### 4.3 L'amplituèdre : retirer cette référence

Le plan présente l'axe comme « l'équivalent expérimental macroscopique du calcul
d'une Matrice-S » à la manière de l'**amplituèdre**. Il faut retirer ce lien.

L'amplituèdre est une géométrie positive calculant les amplitudes de diffusion
de $\mathcal{N}=4$ super-Yang–Mills — une théorie de jauge supersymétrique,
planaire, à grand $N$. La matrice $S$ d'une cavité chaotique est décrite par la
**théorie des matrices aléatoires** (ensembles GOE/GUE de Wigner–Dyson). Ce sont
deux mathématiques différentes, sans énoncé reliant l'une à l'autre.

Le rapprochement est une métaphore. La garder dans un texte scientifique
coûterait la crédibilité de l'ensemble, y compris des axes solides. **La vraie
histoire — « la forme géométrique dicte le spectre », c'est-à-dire la loi de
Weyl et le problème de Kac (1966, **[EXTERNE]**) « peut-on entendre la forme
d'un tambour ? » — est
déjà excellente et, elle, exacte.**

### 4.4 Lean 4 : échelonner

Formaliser la **loi de Weyl** complète est un projet de recherche en
formalisation : elle demande l'analyse spectrale de l'opérateur de Laplace sur
un domaine irrégulier, une théorie que Mathlib ne possède pas aujourd'hui.

Objectif réaliste : prouver la **fonction de comptage pour un rectangle**, où
les valeurs propres sont explicites
($k^2_{mn} = \pi^2(m^2/a^2 + n^2/b^2)$), et établir l'asymptotique du terme
dominant $N(k) \sim Ak^2/4\pi$ par un comptage de points du réseau. C'est un
problème fini, difficile mais bordé — et c'est déjà un vrai théorème de la loi
de Weyl.

---

## 5. Axe 5 — Caustiques et théorie des catastrophes

**Verdict : le meilleur axe du programme. Le moins cher, le plus robuste, et
celui dont les mathématiques sont les plus exactement adaptées.**

Pourquoi il est solide, là où les autres demandent des corrections :

- **Le phénomène est générique, pas accordé.** Le théorème de Thom–Arnold dit
  que les caustiques d'une famille générique de fronts d'onde n'appartiennent,
  en dimension basse, qu'à une **liste finie** de types stables : pli ($A_2$),
  fronce ($A_3$), queue d'aronde ($A_4$), papillon ($A_5$), ombilics ($D_4^\pm$).
  On ne cherche pas un effet fragile : on vérifie une **classification**.
- **Le désordre est le sujet, pas le bruit.** Plus la lame est irrégulière,
  mieux la démonstration fonctionne — c'est précisément le point : la
  classification tient quand même. L'axe est donc à l'épreuve de la qualité de
  fabrication, ce qui est rare.
- **Pas de contrainte d'échelle.** Contrairement à l'axe 3, les structures utiles
  sont millimétriques à centimétriques : la résolution de l'imprimante convient
  largement.

**Une correction matérielle.** Une plaque imprimée en FDM n'est **pas
optiquement transparente** (interfaces entre couches, diffusion). Trois
solutions, par ordre de simplicité : (a) une surface d'eau légèrement ridée dans
l'aquarium de l'axe 1 — le caustique au fond de la piscine, littéralement ;
(b) du film plastique étiré sur un cadre ; (c) imprimer un **moule** et couler
de la résine transparente.

**Gudhi est ici pleinement à sa place**, plus que partout ailleurs dans le
programme : le squelette du réseau de caustiques est un **graphe**, et
l'homologie persistante en donne les nombres de Betti de façon stable au bruit
et au seuillage. Le suivi de $H_0$ et $H_1$ pendant qu'on déforme la lame fait
voir les **transitions de catastrophe** (une fronce qui naît ou disparaît) comme
des événements de naissance/mort dans le diagramme de persistance. C'est un
usage de la TDA à la fois naturel et non substituable.

**Lean 4.** La classification ADE complète des singularités simples est hors de
portée. Cible réaliste et néanmoins significative : prouver les **formes
normales** du pli et de la fronce par le théorème des fonctions implicites, et
que la caustique de la famille
$F(x,u) = \tfrac{x^4}{4} + \tfrac{u_2x^2}{2} + u_1x$ est bien la courbe
semi-cubique $4u_2^3 + 27u_1^2 = 0$ (paramétrée par $u_2 = -3x^2$,
$u_1 = 2x^3$). Attention à la normalisation : pour
$x^4 + u_2x^2 + u_1x$ sans les facteurs $1/4$ et $1/2$, la courbe devient
$8u_2^3 + 27u_1^2 = 0$ — vérifié numériquement, et c'est exactement le genre
d'écart qui fait échouer une preuve Lean ou pousse à affaiblir l'énoncé. C'est un calcul algébrique explicite,
donc atteignable.

---

## 6. Ordre d'exécution recommandé

Le plan traite les cinq axes comme parallèles. Ils ne le sont pas : ils
partagent une chaîne de mesure, et cette chaîne doit être validée une fois.

| Phase | Contenu | Pourquoi ici |
|---|---|---|
| **0** | Banc FS-SS : motif de points, caméra, reconstruction de $\eta(x,y,t)$ sur une onde plane connue | Aucune mesure des axes 1 et 2 n'a de sens avant que ce banc soit étalonné |
| **1** | **Axe 1a** — chaîne SSH 1D, mode de mur de domaine | Le plus simple ; valide réseau + métrologie + le premier théorème Lean |
| **2** | **Axe 5** — caustiques | Indépendant, très peu coûteux, résultat quasi garanti : entretient l'élan |
| **3** | **Axe 1b** — valley-Hall 2D, test au défaut | Le vrai résultat de l'axe 1 |
| **4** | **Axe 2** — vortex de vidange, superradiance | Réutilise le banc de la phase 0 |
| **5** | **Axe 4** — billard micro-ondes (après achat d'un VNA) | Chaîne de mesure disjointe |
| **6** | **Axe 3** — vortex acoustique ou hologramme en fourche | Le plus dépendant d'un choix de voie |

Commencer par l'axe 1a et l'axe 5 : ce sont les deux qui produisent un résultat
vérifiable au plus vite, et ils valident la chaîne complète
physique → données → TDA → Lean sur un cas facile avant de l'appliquer à un cas
difficile.

---

## 7. Les trois corrections transversales

### 7.1 Les panneaux solaires ne sont pas des photodétecteurs de mesure

Ils reviennent dans les cinq axes. Leurs limites sont structurelles :

- **Aucune résolution spatiale** : un panneau = un pixel. Or tous les objectifs
  du programme (modes de bord, caustiques, figures de billard, anneau de vortex)
  sont **spatiaux**.
- **Bande passante très faible** : la grande surface implique une grande
  capacité de jonction ; une cellule PV se comporte en intégrateur, utilisable
  à quelques dizaines de Hz au mieux.
- **Conçus pour la puissance, non pour le signal** : pas de polarisation
  inverse, courant d'obscurité élevé, linéarité médiocre.

**À utiliser à la place :**

| Besoin | Solution récupérée | Remarque |
|---|---|---|
| Champ 2D | webcam / appareil photo, mode RAW | de loin le meilleur rapport information/coût |
| Point rapide | photodiode d'une souris optique | bande passante kHz–MHz |
| Très rapide / position | **photodiode à quadrants d'un bloc optique CD** | MHz, et sensible à la position |
| Lumière très faible | phototransistor + amplificateur transimpédance | quelques euros |

Les panneaux solaires gardent un rôle utile : **alimenter** le montage.

### 7.2 Le bloc optique de lecteur CD/DVD est le meilleur composant disponible

C'est l'élément le plus sous-exploité du plan, qui n'en retient que le moteur et
le disque. Un bloc optique (OPU) contient, aligné en usine :

- une **diode laser** (780 nm sur CD, 650 nm sur DVD) ;
- une lentille de **collimation** et un réseau de diffraction 3 faisceaux ;
- un **cube séparateur polarisant** et une **lame quart d'onde** ;
- une lentille objective montée sur **bobines mobiles** (focalisation et suivi
  de piste), de course ~1 mm et de résolution **sub-micrométrique** ;
- une **lentille astigmate** et une **photodiode à quadrants** rapide.

L'ensemble astigmate + quadrants forme un **capteur de déplacement nanométrique**
prêt à l'emploi : c'est le signal d'erreur de focalisation, dont la pente
mesurée donne une résolution verticale de l'ordre de 10 nm sur une plage de
quelques µm. Soit, gratuitement : un profilomètre, un microscope à balayage
rudimentaire, ou le détecteur d'un interféromètre.

**Il vaut mieux consacrer une semaine à sortir un OPU et à en câbler le
quadrant qu'à essayer de faire d'un panneau solaire un capteur.**

### 7.3 Lean 4 : une échelle, sinon rien n'aboutit

Les cibles proposées — loi de Weyl, classification ADE, équivalence
Navier–Stokes/géodésiques — sont des projets de formalisation de plusieurs
années chacun. Les viser directement garantit qu'aucune ne sera atteinte.

L'échelle proposée en §8 découpe chaque axe en **T0 → T3**, de façon que chaque
niveau soit un théorème compilé et sans `sorry`, et que l'échec au niveau
suivant laisse quand même un acquis. Le dépôt frère
**SocrateAI-Scientific-Agora-LeanMaster** fournit déjà l'outillage
(portes de preuve, audit d'axiomes, interdiction des `sorry`) et des résultats
vérifiés sur les réseaux et la K-théorie : s'y brancher plutôt que repartir de
zéro.

---

## 8. Échelle des objectifs Lean 4

**Règle : un niveau n'est acquis que s'il compile, sans `sorry` et sans axiome
ajouté.** Le dépôt LeanMaster fournit la porte de vérification.

| Axe | T0 — définitions | T1 — théorème jouet | T2 — cible réaliste | T3 — ambition |
|---|---|---|---|---|
| **1 SSH** | hamiltonien SSH, symétrie chirale | le spectre est symétrique par rapport à 0 | **$\nu \in \{0,-1\}$ selon $\lvert v\rvert \gtrless \lvert w\rvert$ ; chaîne impaire : exactement un mode nul, $\psi_A(n)\propto(-v/w)^n$, au bord gauche ssi $\lvert w\rvert>\lvert v\rvert$** | demi-droite : $\dim\ker = \lvert\nu\rvert$ (indice de Toeplitz) ; dix classes |
| **2 Horizon** | écoulement barotrope, métrique acoustique | $g_{\mu\nu}$ est lorentzienne hors horizon | **perturbations $\Rightarrow \Box_g\phi = 0$** | spectre thermique de Hawking |
| **3 Vortex** | phase, indice d'enroulement | enroulement invariant par homotopie | **quantification entière par Stokes ; additivité des charges** | classification complète des faisceaux OAM |
| **4 Billard** | Laplacien de Dirichlet, comptage $N(k)$ | valeurs propres explicites du rectangle | **$N(k)\sim Ak^2/4\pi$ pour le rectangle** | loi de Weyl générale |
| **5 Caustiques** | famille génératrice, ensemble critique | le pli est stable | **forme normale de la fronce ; pour $\tfrac{x^4}{4}+\tfrac{u_2x^2}{2}+u_1x$, caustique $=\{4u_2^3+27u_1^2=0\}$** | classification ADE |

**Le T2 de l'axe 1 est le sommet scientifique du programme.** C'est la
correspondance volume–frontière sous sa forme la plus élémentaire : *le signe
d'un invariant du volume décide de quel côté de la chaîne vit le mode de bord.*
Il est démontrable en Lean, mesurable dans l'aquarium, et relié au §4 de
[`literature_review.md`](literature_review.md).

**Précision d'énoncé, vérifiée numériquement** par
[`ssh_check.py`](../experiments/axis1_topological_waves/ssh_check.py) : la
version naïve — « le nombre de modes de bord *exactement* nuls d'une chaîne
ouverte égale $\lvert\nu\rvert$ » — est **fausse** pour une chaîne paire, dont
le bloc de sous-réseau a $\det D = v^N \ne 0$ : les modes de bord y ont une
énergie $\sim (v/w)^N$, exponentiellement petite mais non nulle. La version
exacte et finie porte sur la **chaîne impaire**. L'égalité
$\dim\ker = \lvert\nu\rvert$ est vraie sur la **demi-droite** infinie (théorème
d'indice de Toeplitz), et relève de T3. Enfin, avec $h(k)=v+we^{-ik}$, le
contour est parcouru dans le sens horaire : $\nu = -1$, pas $+1$, quand
$\lvert w\rvert>\lvert v\rvert$.

---

## 9. Sécurité

Détail en [`safety.md`](safety.md). Les trois points non négociables :

1. **Four à micro-ondes.** Le condensateur haute tension retient une charge
   mortelle des semaines après débranchement. **Retirer et court-circuiter le
   condensateur, déposer le magnétron et le transformateur avant tout usage**,
   même pour n'utiliser que la carcasse. Une carcasse « inerte » ne l'est que
   si ces pièces sont physiquement sorties.
2. **Lasers.** Lunettes adaptées à la longueur d'onde et à la puissance. Les
   reflets spéculaires sur un CD sont des faisceaux à part entière : un disque
   diffracte en de multiples ordres, dans des directions inattendues. Travailler
   en faisceau horizontal, au-dessous du niveau des yeux, sur fond mat.
   **Traiter tout bloc optique comme émettant un faisceau infrarouge
   invisible** : la diode de lecture CD est à 780 nm, présente dans tout lecteur
   CD et dans la plupart des lecteurs combo DVD. Le réflexe de clignement ne
   protège pas.
3. **Eau et électricité.** Toute alimentation près de l'aquarium sur
   **différentiel 30 mA**, pompes en très basse tension, connexions au-dessus
   du niveau d'eau.
