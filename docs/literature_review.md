# AdS/CMT et correspondance volume–frontière — revue de littérature

**Corpus** : 49 articles arXiv, téléchargés et vérifiés (titre réel confronté au titre
attendu pour chaque identifiant), indexés dans `papers/index.json`.
**Date de la revue** : 2026-09-27.
**Portée** : dualité holographique, ses applications à la matière condensée, la
classification des isolants topologiques, et les mécanismes qui relient
réellement les deux.

**Statut des citations** (voir [`rigor_protocol.md`](rigor_protocol.md) §4).
Toute référence donnée avec un identifiant arXiv est dans le corpus et a passé
le contrôle d'identité. Trois références sont citées **hors corpus**, parce
qu'elles sont antérieures à arXiv ou n'y figurent pas, et sont marquées
**[EXTERNE]** dans le texte : Callan & Harvey (1985), Jackiw (1985) et
Teitelboim (1983). Les jugements propres à cette revue, qui ne sont pas des
résultats de la littérature, sont marqués **[INTERPRÉTATION]**.

---

## 0. Résumé exécutif, et une correction au cadrage initial

L'intuition de départ — « dans les deux cas, la dynamique de l'espace à $N$
dimensions est intégralement encodée et dictée par la topologie de l'espace à
$N-1$ dimensions » — pointe vers quelque chose de réel, mais la formulation
fusionne deux correspondances qui sont **structurellement différentes**. Il vaut
la peine de les séparer avant de construire un programme de recherche dessus,
parce que presque tout ce qui suit en dépend.

**Trois écarts précis :**

1. **Les deux correspondances n'ont pas la même forme logique.**
   Dans un isolant topologique, c'est une **implication à sens unique, portant
   sur des données de basse énergie** : un invariant discret du volume *impose*
   l'existence de modes de bord protégés (Kane & Mele, `cond-mat/0506581` ;
   Hasan & Kane, `1002.3895`). Le bord ne permet pas, en retour, de reconstruire
   le volume.
   En AdS/CFT, c'est une **équivalence exacte entre deux théories complètes** :
   la fonction de partition de la frontière *égale* celle du volume
   (Gubser–Klebanov–Polyakov, `hep-th/9802109` ; Witten, `hep-th/9802150`).
   Aucun des deux côtés n'est plus fondamental que l'autre.
   Le slogan « $N-1$ dicte $N$ » ne décrit donc correctement ni l'un ni
   l'autre : trop fort pour les isolants topologiques (où rien n'est
   « intégralement encodé »), mal orienté pour AdS/CFT (où l'encodage va dans
   les deux sens).

2. **La frontière holographique n'est *pas* topologique.**
   Le dual de $\mathrm{AdS}_5\times S^5$ est $\mathcal{N}=4$ super-Yang–Mills :
   une théorie de jauge conforme, fortement couplée, à grand $N$, avec un
   continuum d'opérateurs locaux et une infinité de degrés de liberté locaux.
   Une TQFT, par définition, n'a *aucun* degré de liberté local. Ce qui encode
   la géométrie du volume n'est pas un invariant topologique : c'est la
   structure d'**intrication** et le contenu en opérateurs (Ryu & Takayanagi,
   `hep-th/0603001` ; Van Raamsdonk, `1005.3035`).

3. **Dans un isolant topologique, le volume garde sa propre dynamique.**
   Il n'est pas « encodé » dans son bord : c'est un isolant gappé avec ses
   propres bandes. Ce que l'invariant fixe, c'est une **obstruction** — il
   interdit de gapper le bord sans briser la symétrie protectrice. C'est une
   contrainte discrète, pas un encodage intégral.

**Ce qui relie réellement les deux mondes** — et c'est plus intéressant que le
slogan — tient en quatre mécanismes, documentés en §5 :

- **l'écoulement d'anomalie** (anomaly inflow), seul et unique mécanisme qui
  soit littéralement la même équation des deux côtés ;
- **l'intrication comme langage commun**, où Shinsei Ryu apparaît effectivement
  des deux côtés — l'anecdote est exacte, et elle est même plus forte que
  suggéré ;
- **les réalisations holographiques explicites de matière topologique** ;
- **le codage correcteur quantique**, l'unification structurelle la plus
  profonde des deux.

Une dernière mise au point, sur « le domaine le plus actif de la physique
théorique » : AdS/CMT a été extrêmement actif entre 2008 et 2016. Depuis, le
centre de gravité s'est déplacé vers SYK, l'information quantique et le
paradoxe de l'information des trous noirs. Le sujet est mature et fertile, pas
en pointe de la mode — ce qui, pour construire un programme de recherche, est
plutôt un avantage : les fondations sont stabilisées.

---

## 1. Le corpus

| Pilier | Articles | Contenu |
|---|---:|---|
| `holography` | 11 | AdS/CFT, entropie d'intrication holographique, codes |
| `adscmt` | 13 | supraconducteurs holographiques, non-Fermi liquides, SYK |
| `topology` | 13 | effet Hall de spin quantique, classes d'Altland–Zirnbauer, classification en dix classes |
| `bridge` | 12 | anomalies, spectre d'intrication, code torique, semi-métaux holographiques |

Chaque entrée de `papers/index.json` porte : `arxiv_id`, titre réel,
auteurs, année, catégorie primaire, DOI, `journal_ref`, pilier, et le chemin du
PDF local.

---

## 2. Pilier 1 — La dualité holographique

**La conjecture.** Maldacena (`hep-th/9711200`) observe que les branes D3 de la
théorie des cordes de type IIB admettent deux descriptions limites — une théorie
de jauge sur leur volume d'univers, une géométrie proche de l'horizon — et
propose qu'elles soient exactement équivalentes : $\mathcal{N}=4$ SYM en $3+1$
dimensions **est** la théorie IIB sur $\mathrm{AdS}_5\times S^5$. Le
dictionnaire quantitatif est fourni presque simultanément par Gubser, Klebanov
& Polyakov (`hep-th/9802109`) et Witten (`hep-th/9802150`) : la fonction de
partition de la frontière égale l'action gravitationnelle sur-couche du volume,
les conditions au bord des champs du volume jouant le rôle de sources pour les
opérateurs de la frontière.

Le point crucial pour la matière condensée : le couplage de la frontière est
$\lambda = g^2 N$, et la gravité classique dans le volume correspond à
$\lambda \to \infty$. **La dualité est forte–faible.** Elle rend calculable un
régime fortement couplé où la théorie des perturbations et le Monte-Carlo
quantique échouent tous les deux — c'est là toute sa valeur d'usage, et aussi la
raison pour laquelle elle est difficile à falsifier.

**La dimension manquante est une échelle.** La coordonnée radiale de AdS est
l'échelle du groupe de renormalisation de la frontière. « Volume $N$-dimensionnel
depuis une frontière à $N-1$ dimensions » signifie : *la trajectoire RG complète
de la théorie de frontière, géométrisée.*

**L'entropie d'intrication.** Ryu & Takayanagi (`hep-th/0603001`) proposent que
l'entropie d'intrication d'une région $A$ de la frontière soit l'aire de la
surface minimale du volume qui s'appuie sur $\partial A$, divisée par $4G_N$.
Généralisée au cas covariant par Hubeny, Rangamani & Takayanagi (`0705.0016`),
puis **dérivée** — et non plus postulée — par Lewkowycz & Maldacena
(`1304.4926`). Van Raamsdonk (`1005.3035`) en tire la conséquence radicale :
désintriquer deux moitiés de la frontière *déchire* l'espace-temps du volume.
La connectivité géométrique est faite d'intrication. Maldacena & Susskind
(`1306.0533`) poussent jusqu'à ER = EPR.

**La structure du code.** Swingle (`0905.1317`) remarque que le réseau de
tenseurs MERA a la géométrie d'une tranche hyperbolique, ce qui suggère que la
carte frontière→volume est un circuit de renormalisation. Pastawski, Yoshida,
Harlow & Preskill (`1503.06237`) précisent : c'est un **code correcteur
quantique**. L'information du volume est encodée de façon redondante et
non-locale dans la frontière — d'où sa robustesse à l'effacement d'une région.
Retenir ce point : il revient en §5.4.

---

## 3. Pilier 2 — AdS/CMT

**Le pari.** Les métaux étranges, les cuprates au-dessus de $T_c$ et les points
critiques quantiques sont fortement couplés et sans quasiparticules. Ce sont
précisément les conditions où la gravité classique est le bon outil dual. La
stratégie AdS/CMT est donc : construire dans le volume la géométrie la plus
simple qui porte les bonnes symétries et les bonnes charges, puis lire ce
qu'elle prédit pour la frontière.

**Le premier succès, et le plus solide.** Kovtun, Son & Starinets
(`hep-th/0405231`) calculent $\eta/s = 1/4\pi$ pour tout plasma holographique, et
conjecturent que c'est une borne universelle. Le plasma quark-gluon du RHIC s'en
approche. C'est le résultat holographique qui a le mieux survécu au contact de
l'expérience.

**Supraconducteurs holographiques.** Gubser (`0801.2977`) montre qu'un scalaire
chargé se condense spontanément près d'un horizon de trou noir chargé : la
symétrie $U(1)$ est brisée sous une température critique. Hartnoll, Herzog &
Horowitz en font un modèle complet (`0803.3295`, puis `0810.1563`), avec un gap
$\omega_g/T_c \approx 8$ — à comparer à $3.5$ pour BCS, valeur effectivement plus
proche de ce qu'on mesure dans les cuprates. Le mécanisme est purement
gravitationnel : instabilité de superradiance près de l'horizon. Aucun appariement
de paires de Cooper n'intervient.

**Surfaces de Fermi sans quasiparticules.** Cubrovic, Zaanen & Schalm
(`0904.1993`) et Faulkner, Liu, McGreevy & Vegh (`0907.2694`) étudient les
fermions holographiques chargés. Le résultat central : la région
$\mathrm{AdS}_2 \times \mathbb{R}^2$ proche de l'horizon d'un trou noir extrémal
contrôle l'infrarouge et confère à l'opérateur fermionique une **dimension
d'échelle anormale et continûment variable** $\nu$. Selon $\nu$, on obtient un
liquide de Fermi, un liquide de Fermi marginal, ou un non-Fermi liquide — le
liquide de Fermi marginal, postulé phénoménologiquement pour les cuprates,
*émerge* ici d'une géométrie. C'est le résultat conceptuellement le plus fort
d'AdS/CMT.

**Transport.** Hartnoll (`1405.3651`) propose une borne inférieure universelle sur
la diffusivité dans les métaux incohérents, où la quantité de contrôle est la
diffusion et non le libre parcours moyen — ce qui explique la résistivité
linéaire en $T$ sans invoquer de quasiparticules.

**SYK, ou comment le pari se resserre.** La chaîne va de Sachdev & Ye
(`cond-mat/9212030`, un aimant de Heisenberg aléatoire, solvable, sans ordre) à
Sachdev (`1506.05111`, l'entropie résiduelle de ce modèle *est* l'entropie de
Bekenstein–Hawking d'un trou noir extrémal $\mathrm{AdS}_2$), puis à Maldacena &
Stanford (`1604.07818`). Le modèle SYK est un système quantique à $N$ fermions
en couplage aléatoire à quatre corps, **résoluble**, sans quasiparticules, qui
sature la borne au chaos et dont l'infrarouge est gouverné par le mode
Schwarzien — exactement la gravité de Jackiw–Teitelboim **[EXTERNE]** en
$\mathrm{AdS}_2$.

SYK change la nature de l'argument. Ailleurs en AdS/CMT, on postule un dual
gravitationnel et on espère. Ici, on part d'un hamiltonien de matière condensée
écrit explicitement, et la gravité en sort. C'est la réalisation la plus
contrôlée de l'ensemble du programme.

**Les revues.** Hartnoll (`0903.3246`), McGreevy (`0909.0518`) et Iqbal, Liu &
Mezei (`1110.3814`) sont les trois portes d'entrée pédagogiques ; Hartnoll,
Lucas & Sachdev (`1612.07324`) est le traité de référence.

**Limite honnête du programme.** Les duals gravitationnels utilisés en AdS/CMT
sont « bottom-up » : on écrit une action dans le volume avec les bons champs,
sans savoir si elle provient d'une véritable compactification de cordes, ni
quelle théorie de frontière elle décrit exactement. Les modèles ont aussi une
entropie résiduelle à température nulle et une invariance translationnelle
parfaite, deux propriétés qu'aucun matériau ne possède. AdS/CMT a produit des
*mécanismes* et des *bornes* robustes ; il n'a pas produit de prédiction
quantitative vérifiée sur un composé nommé.

---

## 4. Pilier 3 — Isolants topologiques

**L'invariant.** Kane & Mele (`cond-mat/0506581`) montrent qu'avec la symétrie de
renversement du temps, les isolants bidimensionnels se répartissent en **deux**
classes distinguées par un invariant $\mathbb{Z}_2$ — et que la classe non
triviale porte obligatoirement une paire de Kramers de modes de bord
hélicoïdaux. Bernevig, Hughes & Zhang (`cond-mat/0611399`) prédisent la
réalisation dans les puits quantiques HgTe/CdTe ; Fu, Kane & Mele
(`cond-mat/0607699`) étendent à trois dimensions ; Fu & Kane
(`cond-mat/0611341`) donnent la formule des parités qui rend l'invariant
calculable en pratique.

**Pourquoi le bord est protégé.** L'invariant est une propriété globale du fibré
de Bloch sur la zone de Brillouin. Il ne peut changer sans fermeture du gap.
À une interface avec le vide (trivial), il *doit* changer — donc le gap *doit*
se fermer là. Les modes de bord ne sont pas ajoutés à la main : ils sont la
conséquence forcée d'un changement d'invariant. Le renversement du temps
interdit la rétrodiffusion, d'où une conduction de bord sans dissipation.

**La classification complète.** Schnyder, Ryu, Furusaki & Ludwig (`0803.2786`),
puis Kitaev (`0901.2686`) par K-théorie, et Ryu, Schnyder, Furusaki & Ludwig
(`0912.2157`), établissent la « **table périodique** » : les dix classes de
symétrie d'Altland–Zirnbauer (`cond-mat/9602137` ; générées par les symétries antiunitaires de
renversement du temps et particule-trou, plus la symétrie chirale) admettent en
chaque dimension spatiale un groupe de classification qui vaut
$0$, $\mathbb{Z}$ ou $\mathbb{Z}_2$, avec une périodicité de Bott en dimension
(2 pour les classes complexes, 8 pour les réelles). C'est un résultat de
classification exhaustif — rare en matière condensée. Chiu, Teo, Schnyder & Ryu
(`1505.03535`) l'étendent aux symétries cristallines.

**La réponse électromagnétique.** Qi, Hughes & Zhang (`0802.3537`) montrent que
la physique d'un isolant topologique 3D se résume à un terme
$\theta$ : $S_\theta = \frac{\theta}{2\pi}\frac{\alpha}{2\pi}\int E\cdot B$, avec
$\theta = \pi$ dans la phase non triviale et $0$ dans la phase triviale. Ce
terme est une dérivée totale : il ne change rien dans le volume, mais laisse un
terme de Chern–Simons de niveau demi-entier sur le bord. **Toute la physique
observable du terme topologique du volume vit sur la frontière.** C'est le
prototype exact de l'écoulement d'anomalie (§5.1).

Kitaev (`cond-mat/0010440`) fournit l'exemple unidimensionnel canonique :
une chaîne supraconductrice $p$-onde dont la phase non triviale porte des
fermions de Majorana non appariés à ses extrémités. Les revues de synthèse sont
Hasan & Kane (`1002.3895`) et Qi & Zhang (`1008.2026`).

---

## 5. Pilier 4 — Ce qui relie réellement les deux mondes

### 5.1 L'écoulement d'anomalie : le seul mécanisme littéralement identique

Une théorie de champs en $d$ dimensions peut porter une **anomalie** : une
symétrie classique que la quantification ne préserve pas. Une anomalie de jauge
rend une théorie incohérente *isolément*. La résolution de Callan–Harvey
(1985, **[EXTERNE]**) :
la théorie anomale vit sur le bord d'un volume en $d+1$ dimensions dont le terme
topologique produit exactement le flux compensateur. L'ensemble est cohérent ;
ni l'une ni l'autre moitié ne l'est.

C'est **exactement** le contenu du terme $\theta$ de Qi–Hughes–Zhang
(`0802.3537`) : le Chern–Simons de niveau demi-entier du bord est anomal seul, et
le volume 3D le sauve. C'est **aussi** le contenu de l'anomalie holographique :
le terme de Chern–Simons dans le volume AdS reproduit l'anomalie de la théorie
de frontière, et Landsteiner (`1610.04413`) en déduit le transport induit par
anomalie — effet Hall chiral, effet magnétique chiral — de manière identique en
holographie et en matière condensée.

Ryu, Moore & Ludwig (`1010.0936`) sont l'article-charnière : ils calculent les
réponses électromagnétique **et gravitationnelle** des isolants et
supraconducteurs topologiques et montrent que la table périodique entière
s'organise par les anomalies de ses théories de bord. Wang, Qi & Zhang
(`1011.0586`) étendent aux réponses thermiques des supraconducteurs
topologiques en interaction.

**Verdict.** L'écoulement d'anomalie est une correspondance volume–frontière
exacte, et c'est bien la même mathématique des deux côtés. Mais il faut noter
ce qu'il n'est pas : ce n'est *pas* AdS/CFT. L'écoulement d'anomalie relie une
théorie de bord à un volume **topologique** (sans degré de liberté local) ;
AdS/CFT relie une théorie de bord à un volume **gravitationnel dynamique**. Les
confondre est précisément l'erreur du cadrage initial.

### 5.2 L'intrication comme langage commun — et le rôle de Shinsei Ryu

L'anecdote est exacte, et elle est plus forte que présentée. Ryu ne fait pas
seulement les deux sujets : il a écrit des deux côtés l'article qui traduit la
topologie en intrication.

- Côté gravité : Ryu & Takayanagi (`hep-th/0603001`) — la géométrie du volume
  se lit dans l'intrication de la frontière.
- Côté matière condensée : Ryu, Schnyder, Furusaki & Ludwig (`0912.2157`) — la
  table périodique.

Et le pont est construit des deux côtés à la fois :

- Kitaev & Preskill (`hep-th/0510092`) et Levin & Wen (`cond-mat/0510613`)
  isolent, indépendamment et simultanément, l'**entropie d'intrication
  topologique** $-\gamma$ : le terme sous-dominant, constant, de
  $S_A = \alpha L - \gamma$, avec $\gamma = \log \mathcal{D}$ où $\mathcal{D}$
  est la dimension quantique totale. Un ordre topologique devient ainsi
  détectable dans une seule fonction d'onde, sans passer par la réponse.
- Li & Haldane (`0805.0332`) montrent que le **spectre** d'intrication, et non
  seulement son entropie, contient l'information physique : le spectre du
  hamiltonien d'intrication d'une moitié du système reproduit le spectre des
  états de bord.
- Qi, Katsura & Ludwig (`1103.5437`) en font un **théorème** pour une large
  classe de systèmes : spectre d'intrication $\Leftrightarrow$ spectre de bord.

Le parallèle formel est net : couper le système en deux et lire le spectre de la
matrice densité réduite fait apparaître, dans les deux domaines, la physique de
la frontière. RT et Li–Haldane sont la même opération — tracer sur une région —
appliquée à deux objets différents.

**Nuance à ne pas effacer.** C'est un parallèle structurel profond, pas une
identité. Dans RT, la coupure produit une *géométrie* ; dans Li–Haldane, elle
produit un *spectre de hamiltonien de bord*. Il n'existe pas aujourd'hui de
théorème qui les unifie.

### 5.3 La matière topologique réalisée *dans* l'holographie

Ici, le lien cesse d'être analogique : la matière topologique est construite à
l'intérieur de la théorie des cordes et de l'holographie.

- **Ryu & Takayanagi, `1001.0763`** — « Topological Insulators and
  Superconductors from D-branes ». Les mêmes deux auteurs que la formule
  d'entropie holographique réalisent la classification en dix classes au moyen
  de systèmes de D-branes, la table périodique découlant de la théorie des
  cordes sur les branes. C'est la jonction littérale entre les piliers 1 et 3 —
  et la meilleure justification de l'anecdote de départ.
- **Witten, `1510.07698`** — trois leçons qui relient phases topologiques de la
  matière, anomalies et théorie des champs topologique, écrites par un physicien
  des cordes à destination de la matière condensée.
- **Landsteiner, Liu & Sun (`1511.05505`, revue `1911.07978`)** — un
  **semi-métal de Weyl holographique**. Le modèle gravitationnel subit une
  transition de phase quantique entre une phase topologique et une phase
  triviale, diagnostiquée par la conductivité de Hall anomale, qui joue le rôle
  d'ordre topologique. La transition est **fortement couplée** : elle n'a pas de
  description en quasiparticules. C'est ce qu'AdS/CMT peut faire et que la
  théorie des bandes ne peut pas — la théorie des bandes suppose des
  quasiparticules dès le départ.

### 5.4 Codes correcteurs quantiques : l'unification structurelle la plus profonde

**[INTERPRÉTATION]** C'est, à mon sens, le lien le plus solide et le moins
exploité du corpus. Les deux faits ci-dessous sont établis ; leur
rapprochement en un seul phénomène est un jugement de cette revue, pas un
théorème.

- L'ordre topologique **est** un code correcteur quantique. Le code torique de
  Kitaev (`quant-ph/9707021`) est simultanément un modèle de matière
  topologiquement ordonnée et un code : l'information logique est stockée dans
  des degrés de liberté globaux, inaccessibles à toute mesure locale — d'où sa
  protection. C'est exactement ce que mesure $\gamma$ (`hep-th/0510092`,
  `cond-mat/0510613`).
- L'holographie **est** un code correcteur quantique. Pastawski, Yoshida,
  Harlow & Preskill (`1503.06237`) : un opérateur du volume admet plusieurs
  représentations sur la frontière, et l'information du volume survit à
  l'effacement d'une région de frontière.

Dans les deux cas, la même structure : *de l'information encodée de façon
redondante et non locale, protégée parce qu'aucune opération locale ne peut y
accéder.* La non-localité de l'ordre topologique et la redondance holographique
sont deux instances d'un même phénomène. C'est là que je dirigerais l'effort si
l'objectif est une unification conceptuelle plutôt qu'un calcul.

---

## 6. Synthèse : deux correspondances, une famille

| | Isolant topologique | AdS/CFT |
|---|---|---|
| Forme logique | implication : invariant du volume ⇒ modes de bord | équivalence exacte : $Z_{\text{frontière}} = Z_{\text{volume}}$ |
| Nature du volume | gappé, topologique, **sans** d.d.l. local | gravitationnel, **dynamique** |
| Nature de la frontière | modes gapless protégés | CFT fortement couplée, grand $N$ |
| Ce qui est encodé | une obstruction discrète | la trajectoire RG complète |
| Invariant de contrôle | $\mathbb{Z}$, $\mathbb{Z}_2$ (K-théorie) | aucun — intrication et opérateurs |
| Exactitude | théorème (à symétrie fixée) | conjecture, très fortement étayée |
| Mécanisme partagé | écoulement d'anomalie, intrication, structure de code |

La formulation défendable est donc :

> Les deux domaines instancient une même famille de correspondances
> volume–frontière, dont le membre commun exact est l'écoulement d'anomalie, et
> dont le langage commun est l'intrication. Ils ne sont pas le même énoncé :
> l'un est une implication sur des données de basse énergie, l'autre une
> équivalence exacte entre théories complètes.

---

## 7. Questions ouvertes et pistes de travail

1. **Rendre précis le lien « code »** (§5.4). Existe-t-il un énoncé qui contienne
   à la fois le code torique et les codes HaPPY comme cas limites ? La
   dimension quantique totale $\mathcal{D}$ et la redondance holographique
   devraient être deux faces d'une même quantité.
2. **Une table périodique holographique.** `1001.0763` réalise les dix classes
   par des D-branes ; `1911.07978` construit des semi-métaux holographiques.
   Peut-on classifier les phases topologiques **fortement couplées** — sans
   théorie des bandes — par des données gravitationnelles ? La théorie des
   bandes présuppose des quasiparticules ; l'holographie non. C'est le trou le
   plus net dans la littérature actuelle.
3. **SYK et matière topologique.** SYK est le seul cas où la gravité *émerge*
   d'un hamiltonien explicite. Existe-t-il une variante de SYK à ordre
   topologique, dont le dual porterait un terme $\theta$ ?
4. **Spectre d'intrication et géométrie.** Unifier Li–Haldane (`0805.0332`) /
   Qi–Katsura–Ludwig (`1103.5437`) avec Ryu–Takayanagi (`hep-th/0603001`) :
   quand le hamiltonien d'intrication *est-il* une géométrie de volume ?
   Lewkowycz–Maldacena (`1304.4926`) fournit la technique (méthode des
   répliques) utilisable des deux côtés.
5. **Falsifiabilité.** Le point faible d'AdS/CMT reste l'absence de prédiction
   quantitative vérifiée sur un matériau nommé. Le transport induit par anomalie
   (`1610.04413`) dans les semi-métaux de Dirac et de Weyl est le candidat le
   plus sérieux, parce qu'il est fixé par l'anomalie et donc insensible aux
   détails du modèle.

---

## 8. Ordre de lecture conseillé

**Entrée (1 semaine).** McGreevy `0909.0518` → Hartnoll `0903.3246` →
Hasan & Kane `1002.3895`.

**Cœur (1 mois).** Maldacena `hep-th/9711200` → Witten `hep-th/9802150` →
Ryu–Takayanagi `hep-th/0603001` → Qi–Hughes–Zhang `0802.3537` →
Schnyder–Ryu–Furusaki–Ludwig `0803.2786` → Faulkner et al. `0907.2694`.

**Le pont (l'essentiel).** Ryu–Moore–Ludwig `1010.0936` →
Ryu–Takayanagi `1001.0763` → Qi–Katsura–Ludwig `1103.5437` →
Pastawski et al. `1503.06237` → Landsteiner et al. `1911.07978`.

**Référence permanente.** Hartnoll–Lucas–Sachdev `1612.07324` ;
Chiu–Teo–Schnyder–Ryu `1505.03535`.

---

## 9. Bibliographie

Voir `papers/index.json` pour les 49 entrées avec auteurs complets, DOI,
`journal_ref` et chemins des PDF. La liste des identifiants et de leur pilier
est dans `corpus/seed_papers.py`, avec pour chacun le fragment de titre servant
de contrôle d'identité à la récupération.
