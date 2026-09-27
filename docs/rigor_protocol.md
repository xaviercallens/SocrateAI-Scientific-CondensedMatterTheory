# Protocole de rigueur — Elenchus

> **Statut d'accès.** Le dépôt `xaviercallens/SocrateAI-Scientific-Elenchus`
> renvoie 404 en accès non authentifié, et aucune copie locale n'existe sur
> cette machine (`~` et `/mnt/disks/disk-socrateai-local-1/...` vérifiés). Les
> commandes d'accès authentifié (`gh`, `git ls-remote`) sont refusées par le
> mode de permission de cette session. **Le protocole ci-dessous est donc
> reconstruit depuis les principes, et non importé du dépôt.** Dès que le dépôt
> sera accessible, il faudra confronter ce document au protocole réel et
> l'aligner : noms des portes, schéma des verdicts, format des artefacts.
> Voir la section « Entrées manquantes » du rapport de session.

L'*elenchos* (ἔλεγχος) est la réfutation socratique : on n'établit pas une thèse
en l'appuyant, on la teste en cherchant ce qui la contredit. Appliqué ici, cela
donne une règle unique, dont tout le reste découle :

> **Une affirmation n'a de valeur que si elle a été exposée à une manière
> précise d'échouer, et qu'elle n'a pas échoué.**

Ce protocole a deux usages dans ce dépôt : la **revue de littérature** (§4) et
le **programme expérimental** (§2–§3).

---

## 1. Les cinq portes

Toute affirmation portée par ce dépôt doit franchir cinq portes. Chacune peut
échouer, et un échec est enregistré, pas contourné.

| Porte | Question | Échec typique |
|---|---|---|
| **G1 — Identité** | La source est-elle bien celle qu'on croit ? | citer `1304.4926` comme « Cool horizons » alors que c'est « Generalized gravitational entropy » |
| **G2 — Opérationnalisation** | L'affirmation est-elle liée à une mesure, avec un seuil chiffré ? | « l'onde ignore les défauts » au lieu de « la transmission chute de moins de 10 % » |
| **G3 — Falsifiabilité** | Quel résultat réfuterait l'affirmation ? | aucune issue imaginable ne compte comme un échec |
| **G4 — Producteur ≠ vérificateur** | Celui qui vérifie est-il distinct de celui qui a produit ? | l'auteur du code d'analyse décide seul que le pic est réel |
| **G5 — Traçabilité** | Peut-on remonter de l'affirmation à l'artefact brut ? | une figure sans les données ni le script qui la génèrent |

**G1 est déjà automatisée** dans ce dépôt : `corpus/fetch_papers.py` refuse tout
article dont le titre arXiv réel ne contient pas le fragment attendu déclaré
dans `corpus/seed_papers.py`. Ce n'est pas une précaution théorique — la
première passe a rejeté **6 identifiants sur 36**. Sans cette porte, six
articles faux seraient entrés dans le vector store, sans aucun signal.

---

## 2. Préenregistrement

**Règle : aucune donnée n'est acquise avant que le fichier
`PREREGISTRATION.md` de l'axe soit écrit et commité.** L'horodatage git est la
preuve d'antériorité. C'est la seule protection réelle contre le HARKing
(*Hypothesizing After the Results are Known*), qui est la façon dont un
programme honnête produit néanmoins des résultats faux.

Chaque `experiments/axis*/PREREGISTRATION.md` contient :

```
## Affirmation            l'énoncé physique, en une phrase
## Observable             la grandeur mesurée, avec son unité
## Protocole              montage, échantillonnage, nombre de répétitions
## Prédiction             valeur attendue AVEC barre d'incertitude
## Hypothèse nulle        ce qu'on observerait si l'affirmation est fausse
## Critère de réfutation  le seuil chiffré qui fait échouer l'affirmation
## Analyses prévues       fixées d'avance ; toute autre est exploratoire
## Causes d'échec connues ce qui peut casser l'expérience sans rien dire de la physique
```

Le champ **Critère de réfutation** est celui qui compte. S'il ne peut pas être
rempli avec un nombre, l'expérience n'est pas prête.

---

## 3. Verdicts

À l'issue d'une campagne, l'affirmation reçoit **exactement un** verdict :

| Verdict | Sens |
|---|---|
| `CONFIRMÉ` | prédiction vérifiée dans les barres, critère de réfutation non déclenché |
| `RÉFUTÉ` | critère de réfutation déclenché — **résultat publiable** |
| `NON CONCLUANT` | incertitude trop large pour trancher ; dire quelle amélioration trancherait |
| `INVALIDE` | une cause d'échec connue s'est produite ; l'expérience n'a pas testé l'affirmation |

`RÉFUTÉ` et `INVALIDE` ne sont pas interchangeables, et la confusion des deux
est la faute méthodologique la plus fréquente. Une onde amortie avant d'entrer
dans le réseau (§1.1 du programme expérimental) rend le résultat `INVALIDE` :
elle ne réfute rien, elle n'a rien mesuré.

**Un verdict `NON CONCLUANT` est un résultat acceptable. Un verdict absent ne
l'est pas.**

---

## 4. Application à la revue de littérature

Les mêmes portes s'appliquent aux affirmations théoriques. Trois catégories, à
distinguer explicitement dans le texte :

- **`[CORPUS]`** — l'article est dans `papers/index.json`, récupéré et vérifié
  par G1. C'est le cas par défaut, et il doit le rester.
- **`[EXTERNE]`** — référence réelle mais hors corpus, par exemple parce qu'elle
  est antérieure à arXiv (Callan–Harvey 1985, Altland–Zirnbauer 1997,
  Thouless–Kohmoto–Nightingale–den Nijs 1982). **À marquer comme telle**, jamais
  à laisser passer pour une citation du corpus.
- **`[INTERPRÉTATION]`** — un jugement de l'auteur, non une affirmation de la
  littérature. Exemple : « la structure de code correcteur quantique est le lien
  le plus profond entre les deux domaines » est une opinion défendable, pas un
  théorème. À signaler comme telle.

Cette distinction a déjà rattrapé une erreur dans ce dépôt : la première version
de `literature_review.md` affirmait en tête que « tous les articles cités sont
dans le corpus ingéré », alors que Callan–Harvey, Altland–Zirnbauer et
Jackiw–Teitelboim étaient cités de mémoire, et que le code torique de Kitaev —
sur lequel repose tout le §5.4 — n'était pas dans le corpus. La phrase a été
corrigée et le code torique ajouté au corpus.

---

## 5. Ce que la TDA et Lean peuvent et ne peuvent pas certifier

Deux confusions à éviter, parce qu'elles donnent une apparence de rigueur là où
il n'y en a pas.

**L'homologie persistante ne prouve pas une affirmation physique.** Elle produit
un **descripteur stable** d'un jeu de données, avec des théorèmes de stabilité
qui garantissent qu'une petite perturbation des données ne change pas beaucoup
le diagramme. C'est précieux. Mais « Gudhi a trouvé une classe $H_1$ persistante »
n'est pas « il existe un état de bord topologiquement protégé » : c'est une
statistique de forme, qui doit être confrontée à une hypothèse nulle — typiquement
le même calcul sur des données de contrôle (réseau trivial, lame plate).
**Toute figure de persistance doit être accompagnée de sa version sur contrôle.**

**Lean 4 ne certifie pas la physique.** Il certifie qu'un théorème découle de ses
hypothèses. Si le modèle SSH ne décrit pas fidèlement le réseau de piliers
imprimé, une preuve Lean impeccable du théorème bulk–boundary ne dit **rien**
sur l'aquarium. La preuve formelle ferme l'écart entre *modèle* et *conclusion* ;
elle laisse entièrement ouvert l'écart entre *réalité* et *modèle*. Ce
second écart se ferme par la mesure, et par rien d'autre.

La valeur de la chaîne complète est justement là : Lean verrouille la déduction,
l'expérience teste la modélisation. Aucun des deux ne remplace l'autre, et les
présenter comme un bloc unique de « preuve » serait précisément le genre
d'affirmation que ce protocole existe pour attraper.

---

## 6. Portes héritées de LeanMaster

Pour la partie formelle, le dépôt frère
`SocrateAI-Scientific-Agora-LeanMaster` fournit déjà des portes exécutables ;
il faut s'y brancher plutôt que les réécrire :

1. **build** — le projet Lake compile ;
2. **sorry** — aucun `sorry` dans les fichiers concernés ;
3. **audit d'axiomes** — aucun axiome ajouté au-delà des trois standard de Lean ;
4. **verrou d'énoncé** — l'énoncé du théorème n'a pas été affaibli pour le
   faire passer (le piège le plus courant) ;
5. **producteur ≠ vérificateur** — la vérification est faite par un agent
   distinct de celui qui a écrit la preuve.

La porte 4 est la plus importante et la moins évidente : un théorème qu'on
affaiblit jusqu'à le rendre trivial compile parfaitement et ne prouve rien.
