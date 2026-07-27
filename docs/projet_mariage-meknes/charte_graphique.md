# Charte graphique — Mariage Kenza & Julien, Meknès

> Direction retenue : **S3 · Sahara & Menthe** — sable de plein jour, vert zellige en action, or de la porte en ornement.
> Destinataire : développeur front (FastAPI + Jinja2 + Tailwind CDN + HTMX, no-build).
> Statut : **v2.1 validée par le Patron — 2026-07-28**. v2.0 (2026-07-27) reste la direction visuelle de fond ; v2.1 y ajoute le **multilingue FR/EN/AR** (§4.4 réécrit, RTL pour l'arabe, typographie Cairo, sélecteur de la porte d'entrée §5.10). Historique et motifs d'abandon des directions antérieures : §14.
> Site **multilingue FR/EN/AR**, derrière un code d'accès commun, `noindex`. RTL pour l'arabe uniquement (§4.4).
> Tous les ratios de contraste sont calculés en WCAG 2.1 sur `dune #F4EADA` (fond de page), `surface #FDF8EF` (cartes) ou `encre #38301F` (footer), sauf mention contraire.
> Proposition produit, fonctionnalités, architecture et planning : `proposition_produit.md` (même dossier).

---

## 1. Plateforme de marque visuelle

**Moodboard décrit.** Midi sur un parvis de Meknès. Le sable des remparts prend toute la lumière ; le bois de la porte monumentale renvoie un or chaud ; dans l'ombre des arcs, le zellige donne un vert profond et un bleu de faïence. Un verre de thé à la menthe posé sur une table de cuivre. Beaucoup de clair, peu d'éléments, deux ou trois couleurs justes qui tranchent sur le sable.

**5 adjectifs directeurs.** Lumineux · Chaleureux · Élégant · Ancré · Intime.

**Ce qu'on est.**
- Un faire-part, pas un produit : la page se lit d'une traite, elle donne envie de venir.
- Ancré à Meknès : le lieu est le sujet visuel, pas un décor interchangeable.
- Franco-marocain sans folklore : les codes marocains par la matière et la couleur, jamais par le cliché.
- Sobre : trois voix de couleur, une seule à la fois par zone.

**Ce qu'on n'est pas.**
- Pas de clair-obscur. **Aucune section en fond sombre hors footer** (règle fondatrice de v2.0, §2.5).
- Pas « mariage cliché » : ni script doré, ni cœurs, ni colombes, ni alliances, ni confettis.
- Pas orientaliste : ni lanternes empilées, ni « mille et une nuits », ni tapisserie de motifs.
- Pas corporate : ce n'est pas un dashboard, on n'importe pas les patterns produit d'OWP tels quels.

### 1.1 Identité — lockup typographique

Pas de logo dessiné : l'identité est **purement typographique**.

| Élément | Traitement |
|---|---|
| Nom | **« Kenza & Julien »** en Fraunces 500. Toujours les deux prénoms en toutes lettres. |
| Esperluette | En **`vert.text #24573F`** (7.02:1 sur dune — AAA). Décision Patron du 2026-07-27 : l'esperluette porte la voix de l'union, qui est la voix d'action du site. Une première version l'avait mise en `or.text` ; l'or est revenu à son rôle strict d'ornement (§2.4). |
| Sous-ligne | « MEKNÈS · 23 OCTOBRE 2026 » en token `overline`, `ardoise`, majuscules, `ls 0.08em`. |

Le lockup est **centré** dans le hero, **aligné à gauche** dans le header. Taille minimale d'usage : 16px pour le nom (en dessous, Fraunces devient illisible — §3.3).

**Ornement d'accompagnement.** Un filet de **losanges zellige** (motif §6.1) peut souligner le lockup dans le hero et sur la porte d'entrée, jamais dans le header (qui doit rester sobre).

---

## 2. Palette de couleurs

Le système repose sur **trois nuances de sable** en fonds, une **encre chaude** pour le texte, et **trois voix d'accent aux rôles strictement séparés** :

| Voix | Couleur | Rôle exclusif |
|---|---|---|
| **Vert médina** | `#2F6B4F` | **Agir** — CTA, jalons du programme, état confirmé |
| **Bleu zellige** | `#0F5B78` | **Écrire & naviguer** — liens, sur-titres, anneau de focus |
| **Or de la porte** | `#C8862E` | **Décorer** — filets, motifs, séparateurs. **Jamais de texte dessus.** |

> Règle d'or : **une seule voix dominante par zone visuelle.** Un bloc qui porte un CTA vert ne porte pas de badge bleu à côté.

### 2.1 Neutres (fonds & textes)

| Nom | Hex | Usage | Contraste |
|---|---|---|---|
| `cadre` | `#241C13` | **Fond hors carton** — le brun du faire-part, seul fond sombre du site avec le footer (§4.5) | **14.10:1** vs dune — c'est lui qui détache la carte |
| `dune` | `#F4EADA` | **Fond de page principal** — sable de plein jour | base |
| `surface` | `#FDF8EF` | Cartes, encarts, champs de formulaire | base |
| `sable` | `#EADCC4` | Section alternée (rythme), fond désactivé | base · texte encre dessus **9.64:1** AAA |
| `bord` | `#D9C7A9` | Filets décoratifs, séparateurs de liste | base (décoratif, aucun seuil) |
| `bord.fort` | `#9C8455` | **Bordure de champ de formulaire** | **3.40:1** sur surface — seuil UI 3:1 ✅ |
| `encre` | `#38301F` | Texte principal · fond du footer | **10.94:1** sur dune — AAA |
| `ardoise` | `#6B5C42` | Texte secondaire, légendes, méta | **5.45:1** sur dune — AA |

> **Il n'y a pas de token « taupe »/hint.** Sur un site de 6 sections, tout texte affiché est porteur de sens : pas de niveau de gris décoratif.

### 2.2 Vert médina — l'action

| Nom | Hex | Usage | Contraste |
|---|---|---|---|
| `vert` | `#2F6B4F` | **CTA primaire** (texte blanc dessus **6.29:1** AA), points de la timeline, switch actif | **5.28:1** sur dune — AA |
| `vert.hover` | `#275C43` | Survol du CTA primaire (blanc dessus **7.78:1** AAA) | **6.53:1** — AA |
| `vert.text` | `#24573F` | Texte accent vert sur fond clair | **7.02:1** sur dune — AAA |
| `vert.light` | `#A3CCB2` | Vert sur fond encre (footer) | **7.35:1** sur encre — AAA |
| `vert.veil` | `#E1EEE4` | Fond de badge « confirmé », encart doux (texte `vert.text` dessus **6.99:1** AA) | base |

**Le vert n'a pas de doublon « succès ».** Il porte à la fois l'action et la confirmation — c'est le prix assumé de la direction S3. Pour que ça ne devienne pas ambigu, une seule règle, stricte :

> **Aplat vert plein = une action à faire, et son libellé commence toujours par un verbe** (« Confirmer ma présence », « Modifier ma réponse »).
> **État déjà acquis = jamais un aplat plein** : badge `vert.veil` + texte `vert.text` + icône `check`. Un état ne se déguise jamais en bouton.

### 2.3 Bleu zellige — les écritures & le focus

| Nom | Hex | Usage | Contraste |
|---|---|---|---|
| `zellige` | `#0F5B78` | **Anneau de focus**, bordure de champ actif, icônes de lien | **6.32:1** sur dune — AA |
| `zellige.text` | `#0D4E66` | **Liens**, sur-titres `overline` de section, horaires du programme | **7.67:1** sur dune — AAA |
| `zellige.light` | `#8FC7DC` | Bleu sur fond encre (footer) | **7.06:1** sur encre — AAA |
| `zellige.veil` | `#DCEBF1` | Fond de badge informatif (texte `zellige.text` dessus **7.48:1** AAA) | base |

### 2.4 Or de la porte — l'ornement

| Nom | Hex | Usage | Contraste |
|---|---|---|---|
| `or` | `#C8862E` | **Filets, motifs zellige, séparateurs, puces décoratives.** Aplat décoratif uniquement. | **2.55:1** — ⛔ décoratif seul |
| `or.text` | `#744E0E` | **Seule variante autorisée à porter du texte** : chiffres du compte à rebours. (L'esperluette du lockup est passée au vert le 2026-07-27 — §1.1.) | **6.21:1** sur dune — AA |
| `or.light` | `#EFD09A` | Or sur fond encre (footer) | **8.79:1** sur encre — AAA |
| `or.veil` | `#F6E7C9` | Fond d'encart chaleureux (texte `or.text` dessus **6.06:1** AA) | base |

> ⛔ **Interdits absolus sur l'or.** Pas de texte blanc sur `or` (3.04:1 — échec). Pas d'anneau de focus en or (2.09:1 sur surface — échec). Pas de CTA en aplat or. L'or décore, il n'agit pas et il ne parle pas. C'est la contrepartie de sa luminosité.

### 2.5 Rythme des sections — pas de fond sombre

**Règle fondatrice de v2.0.** Le rythme vertical se fait par **trois nuances de clair**, jamais par une section sombre :

| Ordre | Fond | Usage type |
|---|---|---|
| 1 | `dune #F4EADA` | Section standard (Programme, RSVP) |
| 2 | `surface #FDF8EF` | Section « encart » (Venir à Meknès, accordéons) |
| 3 | `sable #EADCC4` | Section d'accent (Le lieu, Dress code) |

Deux sections consécutives ne portent jamais le même fond. Le seul fond `encre` du site est le **footer** (§5.8).

> **Ce que cette règle ne couvre pas.** Le `cadre` brun (§4.5) est sombre, mais il n'est pas une *section* : c'est ce qui entoure le carton, pas ce qu'on lit. La règle interdit d'assombrir **le contenu**, pas de poser une carte claire sur un fond profond — c'est même exactement ce qui la met en valeur.

### 2.6 Erreur

| Nom | Hex | Usage | Contraste |
|---|---|---|---|
| `danger` | `#A32B1C` | Bordure de champ en erreur, icône (blanc dessus **7.19:1** AAA) | **6.04:1** sur dune — AA |
| `danger.text` | `#8E2318` | Message d'erreur sous le champ | **7.33:1** sur dune — AAA |
| `danger.veil` | `#F7E0DC` | Fond de bandeau d'erreur (texte `danger.text` dessus **6.93:1** AA) | base |
| `danger.light` | `#F0A99E` | Erreur sur fond encre | **6.75:1** sur encre — AA |

Pas de token `warning` ni `info` : un site de faire-part n'a que deux états à signaler — ça marche, ou le champ est mal rempli.

### 2.7 Comportement sur le footer (fond `encre #38301F`)

| Rôle | Hex | Contraste |
|---|---|---|
| Texte principal clair | `onDark #FBF5EA` | **12.01:1** — AAA |
| Texte secondaire clair | `onDark.muted #D7C7AC` | **7.86:1** — AAA |
| Accent (date, lien) | `or.light #EFD09A` | **8.79:1** — AAA |

> Sur fond encre, **on n'utilise jamais** `vert`, `zellige` ni `or` foncés — on bascule sur les variantes `.light`.

### 2.8 Mapping Tailwind (`theme.extend.colors`)

```js
colors: {
  // Neutres — le cadre, puis trois nuances de sable
  cadre:   '#241C13',   // fond hors carton (§4.5)
  dune:    '#F4EADA',   // fond de page
  surface: '#FDF8EF',   // cartes, champs
  sable:   '#EADCC4',   // section d'accent
  bord:    { DEFAULT:'#D9C7A9', fort:'#9C8455' },  // filets · bordure de champ (3:1)
  encre:   '#38301F',   // texte principal / footer
  ardoise: '#6B5C42',   // texte secondaire

  // Trois voix
  vert:    { DEFAULT:'#2F6B4F', hover:'#275C43', text:'#24573F', light:'#A3CCB2', veil:'#E1EEE4' },
  zellige: { DEFAULT:'#0F5B78', text:'#0D4E66', light:'#8FC7DC', veil:'#DCEBF1' },
  or:      { DEFAULT:'#C8862E', text:'#744E0E', light:'#EFD09A', veil:'#F6E7C9' },

  // Erreur
  danger:  { DEFAULT:'#A32B1C', text:'#8E2318', light:'#F0A99E', veil:'#F7E0DC' },

  // Footer
  onDark:  { DEFAULT:'#FBF5EA', muted:'#D7C7AC' },
}
```

---

## 3. Typographie

### 3.1 Familles

| Rôle | Police (FR/EN, latin) | Police (AR) | Source | Graisses |
|---|---|---|---|---|
| Titres | **Fraunces** (serif expressif, optical sizing) | **Cairo** 700 | Google Fonts | 400, 500, 600 (latin) · 700 (arabe) |
| Corps | **Plus Jakarta Sans** | **Cairo** 400/500 | Google Fonts | 400, 500, 600 (latin) · 400, 500 (arabe) |

**FR/EN : deux familles latines, pas trois.** Reprises telles quelles de la charte OWP, rendu déjà validé — l'identité de ce site est portée par la couleur et la photo, pas par le choix typographique. L'anglais ne demande aucune police supplémentaire : Fraunces et Plus Jakarta Sans couvrent le latin nativement.

**AR : Cairo, ajoutée le 2026-07-28.** Fraunces n'a pas de glyphes arabes ; en `lang="ar"`, **les titres basculent sur Cairo 700** (graisse forte qui reprend, en sans-serif, le rôle d'affirmation que joue le serif expressif de Fraunces en latin) et le corps sur Cairo 400/500. Choix repris directement du pattern déjà validé sur OWP — Cairo couvre proprement l'arabe et le latin, rendu net, bon support RTL, aucune raison d'introduire une troisième famille rien que pour l'arabe. Pas de contraste à recalculer : le changement de police ne touche aucun token couleur.

```css
/* pile latine (défaut, FR/EN) */
--font-display: 'Fraunces', Georgia, serif;
--font-body:    'Plus Jakarta Sans', system-ui, sans-serif;

/* pile arabe — appliquée sous [lang="ar"] */
--font-display-ar: 'Cairo', system-ui, sans-serif;
--font-body-ar:    'Cairo', system-ui, sans-serif;
```

> **Précharger Fraunces** (`<link rel="preload" as="font">`) : le lockup du hero et du header en dépend, et sans elle le nom retombe sur un serif système terne. `font-display: swap`. **Précharger aussi Cairo 700** dès que `lang="ar"` est actif (ou en avance si le poids le permet — un seul fichier de plus, la porte d'entrée est la première page vue et peut être en arabe dès le premier chargement).

### 3.2 Échelle typographique

Base 16px (`1rem`). `ls` = letter-spacing, `lh` = line-height.

| Token | Taille | Police | Graisse | lh | ls | Usage |
|---|---|---|---|---|---|---|
| `display` | 3.5rem / 56px (clamp 2.25→3.5) | Fraunces | 500 | 1.05 | -0.02em | Lockup du hero |
| `h1` | 2.5rem / 40px | Fraunces | 500 | 1.1 | -0.015em | (réservé) |
| `h2` | 1.875rem / 30px | Fraunces | 500 | 1.15 | -0.01em | Titre de section |
| `h3` | 1.5rem / 24px | Fraunces | 500 | 1.2 | 0 | Sous-section |
| `h4` | 1.25rem / 20px | Fraunces | 500 | 1.3 | 0 | Titre d'étape du programme, valeur de carte |
| `overline` | 0.875rem / 14px | Plus Jakarta | 600 | 1.4 | 0.08em (MAJ) | Sur-titre de section, label |
| `body-lg` | 1.125rem / 18px | Plus Jakarta | 400 | 1.7 | 0 | Chapô, mot d'accueil |
| `body` | 1rem / 16px | Plus Jakarta | 400 | 1.7 | 0 | Texte courant |
| `small` | 0.875rem / 14px | Plus Jakarta | 400 | 1.6 | 0 | Légendes, méta |
| `caption` | 0.75rem / 12px | Plus Jakarta | 500 | 1.5 | 0.01em | Mentions |
| `button` | 1rem / 16px | Plus Jakarta | 600 | 1 | 0.01em | Libellés de bouton |

### 3.3 Règles d'usage

- **Un seul `display` par page** (le lockup du hero). Les titres de section en `h2` Fraunces, tout le reste (corps, boutons, formulaires, badges) en Plus Jakarta.
- **Jamais Fraunces sous 20px** — seule exception, le nom du header à 17px (titre de marque, §1.1).
- **Jamais Fraunces sur des chiffres de données** (compteurs RSVP, montants du back-office) : Plus Jakarta 600 `tabular-nums`. Exception assumée : le **compte à rebours** et les **horaires du programme**, qui sont éditoriaux, pas des données.
- **Casse** : phrase normale partout. L'`overline` est la seule exception en MAJUSCULES.
- **Couleur du texte** : principal `encre`, secondaire `ardoise`, liens `zellige.text` (soulignés au survol), sur-titres de section `zellige.text`.
- **Longueur de ligne** : corps limité à ~65–75 caractères (`max-w-prose`).
- **Arabe** : tailles identiques au latin mais `line-height` **+0.1** (l'arabe respire davantage verticalement) ; pas de MAJUSCULES sur l'`overline` (n'existe pas en arabe — le token devient un simple label Cairo 600, sans `text-transform`, `letter-spacing` normal).

---

## 4. Espacement, grille & gabarits

### 4.1 Espacement

Échelle Tailwind native (multiples de 4px) : `1`=4 · `2`=8 · `3`=12 · `4`=16 · `6`=24 · `8`=32 · `12`=48 · `16`=64 · `20`=80 · `24`=96.
**Rythme vertical de section : 64–96px desktop, 40–48px mobile.**

### 4.2 Conteneurs

| Token | Largeur max | Usage |
|---|---|---|
| `prose` | 720px | Texte éditorial, programme, accordéons du guide voyage, formulaire RSVP |
| `content` | 1120px | Header, footer, grilles de cartes |
| `wide` | 1320px | Contenu du hero |

**Règle : fond pleine largeur, contenu centré.** Toute section est `w-full` avec son fond ; le contenu passe dans `mx-auto max-w-*` + `px-6 lg:px-8`. Jamais de contenu collé au bord.

> **Ce site est un faire-part, pas une marketplace** : la colonne resserrée (`prose` 720) est le gabarit **par défaut** du contenu — l'inverse d'OWP. Le `content` 1120 est réservé au header, au footer et aux rares grilles de cartes.

### 4.3 Points de rupture

Tailwind par défaut : `sm` 640 · `md` 768 · `lg` 1024 · `xl` 1280. **Mobile-first** — la majorité des invités ouvriront le lien depuis un téléphone.

### 4.4 Multilingue FR/EN/AR — RTL pour l'arabe

**Décision produit du 2026-07-28** (`proposition_produit.md` §2 point 6, §5.14-15/19) — **remplace intégralement** la décision « mono-langue, pas de RTL » du 12/06 puis reconduite le 27/07. Le site est traduit en français, anglais et arabe ; l'arabe se lit de droite à gauche.

**La langue se choisit à la porte d'entrée, nulle part ailleurs par défaut** (décision produit, non négociable côté DA) : sélecteur FR/EN/AR, FR pré-sélectionné, posé avant tout contenu — c'est le seul écran garanti vu par 100 % des invités avant d'avoir lu quoi que ce soit. Design du sélecteur : §5.10. Mécanique cookie/route côté technique (`app/i18n/translations.py`, `/set-lang`) — hors périmètre DA, ne touche pas cette charte.

`<html lang="{{ lang }}" dir="{{ 'rtl' if lang == 'ar' else 'ltr' }}">` — `dir` se déduit de `lang`, jamais un état à part.

**Audit RTL du code déjà construit (2026-07-28) : rien à corriger.** Vérification faite ligne par ligne sur `base.html`, `home.html`, `gate.html`, `app.css` — **zéro utilitaire `left`/`right`/`ml-`/`mr-`/`pl-`/`pr-` en dur**, zéro `space-x-*` (qui aurait exigé `rtl:space-x-reverse`), zéro icône encore posée à mirorer. Tout est construit en `text-center`, `mx-auto`, `flex` (qui mirore tout seul sous `dir="rtl"` — la propriété CSS `flex-direction: row` suit l'axe inline, donc le sens d'écriture), et `gap-x`/`gap-y` (symétriques, non directionnels). L'autorisation `left`/`right` de l'ancien §4.4 existait sur le papier mais n'a jamais été exercée en pratique.

**Conséquence : la règle change pour la suite du chantier, pas le code existant.** À partir de maintenant (formulaire RSVP, back-office, tout ajout) : **utilitaires logiques exclusivement** — `ms-*`/`me-*` (jamais `ml`/`mr`), `ps-*`/`pe-*` (jamais `pl`/`pr`), `text-start`/`text-end` (jamais `text-left`/`text-right`), `start-*`/`end-*` en position absolue (jamais `left-*`/`right-*`). Si `space-x-*` devient nécessaire, toujours accompagné de `rtl:space-x-reverse`.

> **Point de vigilance non négociable : le contenu latin reste `dir="ltr"` même en page arabe.** Numéro de téléphone, compte à rebours (« J−88 » → les chiffres), dates, montants, le **champ code de la porte d'entrée** lui-même — tout ce qui est intrinsèquement numérique/latin doit porter un `dir="ltr"` explicite (ou `unicode-bidi: isolate` + `dir="ltr"`), sinon le moteur bidi de l'arabe réordonne ou désaligne les chiffres au milieu d'un paragraphe RTL. C'est le bug RTL le plus courant et le plus facile à rater : à vérifier composant par composant à l'implémentation, pas seulement au niveau `<html>`.

### 4.5 Format faire-part — le carton et son cadre

**Décision Patron du 2026-07-27.** Le site n'occupe pas l'écran : c'est **un carton posé sur un fond brun**. C'est ce qui lui donne son contraste et sa lecture d'invitation plutôt que de page web.

| Élément | Valeur |
|---|---|
| Fond hors carton | `cadre #241C13` |
| Carton | `bg-dune`, largeur max **1180px**, centré |
| Espacement du cadre | **`padding` du `body`** (`lg:py-10`), jamais une marge du carton |
| Bord du carton | **filet 1px `or #C8862E`** — le fil doré du faire-part |
| Ombre | `lg` (`0 12px 32px rgba(56,48,31,0.12)`) |
| Angles | **droits** — un faire-part est rectangulaire, et des angles arrondis exigeraient un `overflow:hidden` qui casserait tout positionnement collant à l'intérieur |

> ⚠️ **L'espacement autour du carton est un `padding` du `body`, pas une `margin` du carton.** Une marge verticale s'échappe par *margin collapsing* : le carton se retrouve collé au haut de l'écran et le brun disparaît au-dessus de lui (constaté le 2026-07-27).

**Le filet doré est ici structurel, pas ornemental** — c'est la seule chose qui sépare le carton du cadre là où les deux sont sombres. Il est visible des deux côtés : **5.52:1** contre le `cadre`, **4.29:1** contre le `encre` du footer, et 2.55:1 contre `dune` (suffisant, c'est un trait décoratif au sens du §2.4).

**Mobile (< 1024px) : pas de cadre.** Le carton occupe toute la largeur, sans marge ni filet. Sur un téléphone la largeur est trop précieuse pour être dépensée en décor, et le format faire-part n'a de sens qu'à partir du moment où l'écran est plus large que la lecture.

**Conséquence : le header n'est plus collant.** Une barre de navigation qui suit le scroll est un pattern de produit, pas de faire-part — et `position: sticky` ne survit pas proprement au conteneur du carton. Le CTA RSVP reste accessible dans le hero et dans sa propre section.

---

## 5. Composants (specs visuelles)

> Rayons : `sm` 4px · `md` 8px · `lg` 14px · `xl` 20px · `full` 9999px.
> **Toute cible interactive : 44px de haut minimum.**

### 5.1 Boutons

| Variante | Repos | Hover | Focus | Disabled |
|---|---|---|---|---|
| **Primaire** | fond `vert #2F6B4F`, texte blanc (**6.29:1** AA), radius `md`, padding `12px 28px`, h 48px, `button` 600 | fond `vert.hover #275C43` (blanc **7.78:1** AAA) | voir §5.1 bis | fond `sable`, texte `ardoise` (**4.80:1**), pas d'ombre |
| **Secondaire** | fond transparent, bordure 1px `zellige`, texte `zellige.text` | fond `zellige.veil #DCEBF1` | idem | bordure `bord`, texte `ardoise` |
| **Lien fléché** | texte `zellige.text` + chevron 20px, pas de fond | soulignement | idem | — |

Icône optionnelle 20px, `gap-2`. Jamais de coin arrondi sur un seul côté. **Un seul bouton primaire par section.**

### 5.1 bis Anneau de focus — la règle qui n'est pas négociable

L'anneau de focus est **`ring-2 zellige #0F5B78` + `ring-offset-2` dans la couleur du fond de la section**.

> ⚠️ **L'offset est obligatoire, pas décoratif.** Le bleu zellige posé directement sur le vert du CTA donne **1.20:1** — invisible. L'anneau ne doit jamais toucher le bouton : les 2px d'offset le ramènent contre le fond de page, où il vaut **6.32:1** sur `dune`, **7.12:1** sur `surface`, **5.57:1** sur `sable`. Tous ✅ au seuil UI de 3:1.
>
> Alternative admise si l'offset est impossible (élément collé à un bord) : anneau `vert.light #A3CCB2`, qui vaut **3.55:1** sur le vert du bouton. Jamais d'or, jamais de blanc.

### 5.2 Champs de formulaire (RSVP, code d'accès, back-office)

- Hauteur **48px**, fond `surface`, **bordure 1px `bord.fort #9C8455`** (3.40:1 — seuil UI atteint), radius `md`, texte `encre`, padding `12px 16px`.
- **Placeholder** : `ardoise` — et le placeholder ne remplace **jamais** le label.
- **Focus** : bordure `zellige`, anneau `ring-2 zellige/30` + offset. Pas d'ombre portée.
- **Erreur** : bordure `danger`, message sous le champ en `small` `danger.text`, icône `alert-circle` 16px.
- **Label** : au-dessus, `small` graisse 600 `encre`. Requis : astérisque `danger`.
- **Aide** : `caption` `ardoise` sous le champ.
- **Cases / radios** : 20px, coché = fond `vert`, coche blanche. **Switch** : piste `bord` → `vert` activé.
- **Autocomplétion de nom (RSVP, HTMX)** : liste déroulante `surface`, bordure `bord.fort`, ombre `md`, ligne survolée `vert.veil`, ligne active `vert.veil` + bordure gauche 3px `vert`. 44px par ligne. Navigation clavier ↑↓ + Entrée obligatoire.

### 5.3 Hero — sans voile

**Le changement structurel de v2.0.** Le hero n'assombrit plus rien : le texte ne se pose pas *sur* la photo, il se pose *au-dessus d'elle*, sur un fond clair.

```
┌─────────────────────────────────────┐
│  fond : dégradé ciel → dune → sable │
│                                     │
│        SAVE THE DATE  (overline)    │
│        Kenza & Julien  (display)    │
│        ◆ ─────── ◆  (filet or)      │
│     Date  ·  Lieu   (méta)          │
│        [ Confirmer ma présence ]    │
│                                     │
│   ▒▒▒ photo Bab Mansour détourée ▒▒▒│  ← ancrée en bas, pleine largeur
└─────────────────────────────────────┘
```

- **Fond** : dégradé vertical `#FBF3E4` (0 %) → `dune #F4EADA` (60 %) → `sable #EADCC4` (100 %). Un lever de lumière, pas un voile.
- **Photo** : Bab Mansour **détourée sur fond transparent**, ancrée en bas du hero, **à fleur des bords du carton** — pas de largeur max, pas de gouttière latérale. Elle se pose sur le dégradé, d'où l'exigence de détourage (§7). Décision Patron du 2026-07-27 : *« je n'aime pas l'espace à gauche et à droite de l'image »* — la façade borde le carton, elle ne flotte pas dedans. Toute `max-w-*` posée sur cette image rouvre la marge de sable et est donc interdite.
- **Créneaux** : la façade doit être vue **entière, tours et créneaux compris**. Ne jamais rogner le haut (§7).
- **Texte** : `overline` `zellige.text`, lockup `display` `encre` avec esperluette `vert.text`, puis une phrase d'accueil en `body` sur **52 caractères max**.
- **Ligne de coordonnées** : **Date · Lieu · Compte à rebours sur une seule ligne**, séparés par un filet vertical `bord` de 36px. Label en `overline` `ardoise`, valeur en `h4` Fraunces (`encre`, sauf le compte à rebours en `or.text`). Ce sont trois informations de même nature — elles ne s'empilent pas.
- **CTA primaire vert** en dernier, juste avant la photo.
- **Rythme resserré** (décision Patron du 2026-07-27 : *« la partie haute semble flotter »*). Écarts : `pt-8 lg:pt-12` en tête, puis `mt-1` / `mt-3` / `mt-4` / `mt-5` / `mt-6`, et `mt-6 lg:mt-8` avant la photo. **L'aération de ce site vient du brun autour du carton, pas du vide à l'intérieur du bloc de tête.** Repère : le bloc de texte fait ~360px et la façade commence à ~470px du haut du carton.
- **Aucun texte n'est jamais posé sur la photo.** C'est la règle qui remplace celle du voile.
- Mobile : photo jamais recadrée dans sa largeur (la façade doit rester entière) ; `display` en clamp 2.25rem.

### 5.4 Cartes

- Fond `surface`, radius `lg` (14px), bordure 1px `bord`, padding 16–20px, ombre `sm`.
- Carte cliquable : ombre `md` + `translateY(-2px)` au survol, 250ms `premium`. Carte non cliquable : **pas d'effet de survol**.
- Structure : label `overline` `ardoise`, valeur `h4` Fraunces `encre`, méta `small` `ardoise`.
- Grille : `grid-cols-1 sm:grid-cols-2`, `gap-4`.

### 5.5 Programme — timeline verticale

Composant signature du site.

- Colonne de gauche : **point `vert #2F6B4F` de 11px** (5.28:1 sur dune ✅), relié au suivant par un filet 1px `bord`.
- Colonne de droite : horaire en `overline` **`zellige.text`**, titre en `h4` Fraunces `encre`, description en `body` `ardoise`.
- Espacement inter-étapes : 40px. Conteneur `prose` centré.
- L'horaire est en bleu (écriture), le jalon en vert (déroulé) — les deux voix cohabitent ici parce qu'elles portent deux choses différentes. C'est la **seule** zone du site où c'est admis.

### 5.6 Accordéon (guide voyage)

- `<details>` natif, fond `surface`, bordure 1px `bord`, radius `lg`, 8px entre items.
- `<summary>` : 44px mini, padding `16px 24px`, texte `body` 600 `encre`, indicateur `+` `zellige.text` qui pivote à 45° à l'ouverture (150ms).
- Contenu : padding `0 24px 20px`, `body` `ardoise`, termes saillants en `encre` 600.
- `summary` focusable, anneau §5.1 bis. `list-style: none` + `::-webkit-details-marker { display:none }`.

### 5.7 Badges

- Radius `full`, padding `4px 12px`, `caption` 600.
- **Confirmé / acquis** : `vert.veil` + `vert.text` + icône `check` (6.99:1 ✅).
- **Informatif** : `zellige.veil` + `zellige.text` (7.48:1 ✅).
- **Chaleureux / éditorial** : `or.veil` + `or.text` (6.06:1 ✅).
- **Erreur** : `danger.veil` + `danger.text` (6.93:1 ✅).
- ⛔ Jamais d'aplat plein `vert` en badge — l'aplat plein est réservé aux boutons (§2.2).

### 5.8 Header & footer

**Header** — `surface`, **opaque**, bordure-bas 2px `bord`, hauteur 72px, **non collant** (§4.5).
- Lockup `start` : « Kenza & Julien » Fraunces 17px `encre`, esperluette `vert.text`, sous-ligne `caption` MAJ `ardoise`.
- Nav `end` : liens `zellige.text` + CTA primaire « RSVP ». Mobile : les liens tombent, le CTA reste.
- **Jamais translucide** — un header pâle sur un fond sable efface le lockup.

**Footer** — le seul fond `encre` **à l'intérieur** du carton. Il jouxte le `cadre`, dont il n'est séparé que par le filet doré (4.29:1) : ne jamais retirer ce filet, le bord bas du carton disparaîtrait.
- Nom en Fraunces `onDark`, lieu et date en `small` `onDark.muted`, date accentuée en `or.light`.
- Padding 40px vertical. Pas de colonnes, pas de mentions légales inutiles : deux lignes suffisent.

### 5.9 Tableau (back-office : liste d'invités, RSVP)

- Ligne 44px mini, padding horizontal 16px.
- Filet 1px `bord` entre les lignes. **Pas de fond alterné** — l'alternance n'existe nulle part ailleurs dans la charte.
- En-tête de colonne : `overline` `ardoise`, sans fond distinct.
- Survol de ligne : `vert.veil`.
- Statut en badge §5.7. Chiffres en Plus Jakarta 600 `tabular-nums`.
- Vide : message travaillé + micro-CTA, jamais un tableau nu.

### 5.10 Porte d'entrée (code d'accès + sélecteur de langue)

Première page vue par tous les invités — elle donne le ton, **et fixe la langue de toute la visite**.

- Fond `dune`, contenu centré verticalement, `max-w-[380px]`.
- **Ordre du contenu, de haut en bas** : sélecteur de langue → filet zellige `or` (§6.1) → lockup Fraunces `h2` → sous-ligne Meknès/date → phrase d'accueil `body` `ardoise` → champ code §5.2 → bouton primaire pleine largeur.
- **Erreur douce** : « Ce code ne correspond pas — vérifiez votre invitation. » en `danger.text`, jamais « Accès refusé ». Pas de compteur de tentatives affiché.

#### 5.10 bis Sélecteur de langue — 3 pilules, pas un menu déroulant

**Décision DA (2026-07-28).** Trois langues seulement, toutes visibles d'un coup, zéro clic pour ouvrir un menu : un **segmented control** de 3 pilules, pas un dropdown. La logique dropdown d'OWP (§5.6 de sa charte) répond à un header chargé qui doit rester compact ; ici la porte d'entrée n'a **aucun autre élément de navigation** à ce moment-là — le dropdown n'économiserait rien et coûterait un clic de plus à la toute première interaction du site.

**Structure** : piste `bg-surface border border-bord rounded-full p-1`, `inline-flex gap-1`, centrée au-dessus du filet zellige.

| État | Traitement |
|---|---|
| Pilule active | fond `vert` plein, texte blanc (**6.29:1** — AA), `rounded-full` | reprend le pattern « switch activé » déjà établi en §5.2 (piste `bord` → `vert`) : un sélecteur de langue est un réglage persistant, pas un CTA à verbe (§2.2) ni un statut acquis (§5.7) — c'est une troisième catégorie, et §5.2 est le précédent le plus proche dans la charte. |
| Pilule inactive | fond transparent, texte `ardoise` (**5.45:1** sur dune — AA) |
| Focus | anneau §5.1 bis (`zellige` + offset `dune`) |
| Hover (inactive) | fond `sable` |

**Libellés : codes courts, pas les noms complets.** `FR` / `EN` / `AR`, en latin dans les trois cas (pas d'écriture arabe pour le libellé « AR ») — trois raisons : (1) le mot complet dans sa propre langue (« Français » / « English » / « العربية ») déborderait sur 380px de large ; (2) l'arabe rendu par Cairo n'est pas garanti chargé à ce tout premier paint, un code latin reste lisible même avant que la police custom arrive ; (3) c'est exactement le pattern que l'utilisateur reconnaît déjà (sélecteurs FR/EN/AR quasi universels sur le web). Chaque pilule porte un `aria-label` complet (« Français » / « English » / « العربية ») pour le lecteur d'écran, indépendamment du texte visible abrégé.

**Taille tactile** : chaque pilule 44px de haut minimum (règle §5, aucune exception), padding horizontal suffisant pour ne pas paraître écrasée malgré le code court (`px-4` mini).

**Comportement** : clic → pose immédiate du cookie `lang` (route technique `/set-lang`, hors périmètre DA) → réaffichage de la page dans la langue choisie, sélecteur toujours visible, pilule active mise à jour. FR pré-sélectionné par défaut, avant toute interaction.

Motif zellige `or` en filet au-dessus du lockup, sous le sélecteur (§6.1).

---

## 6. Iconographie & ornement

- **Banque : Lucide**, style trait, épaisseur **1.75px**, bouts arrondis, grille 24px. Taille 24px par défaut (20px inline). Couleur héritée (`currentColor`).
- ⛔ **Aucun émoji en guise d'icône**, nulle part.
- Pas d'icônes pleines, pas de mélange de banques.
- Icônes décoratives `aria-hidden="true"` ; icône seule porteuse de sens → `aria-label`.
- **Mirroring RTL (2026-07-28)** : icônes **directionnelles** (flèches, chevrons, « étape suivante », le futur chevron « Voir sur Google Maps » ou tout lien externe fléché) — retournées en arabe via `rtl:-scale-x-100`. Icônes **non directionnelles** (calendrier, cœur décoratif s'il en apparaît un jour hors interdiction §10, check, alert) — inchangées. Aucune icône n'est encore posée dans le code à ce jour (audit §4.4) ; cette règle s'applique dès la première.

### 6.1 Motif zellige — l'ornement maison

Le seul motif du site, en `or #C8862E`, en **filet fin uniquement** :

- **Filet de losanges** : bande de 8–10px de haut, losanges de 14px espacés, opacité 55 %. Usage : séparateur entre deux sections, soulignement du lockup dans le hero et sur la porte d'entrée.
- **Fond de section en filigrane** : même motif à **7 % d'opacité maximum**, uniquement sur `sable`.
- ⛔ **Jamais en tapisserie pleine**, jamais en fond de carte, jamais derrière du texte à plus de 7 %. Le zellige souligne, il n'habille pas.

---

## 7. Direction photographique

- **Style** : lumière franche de plein jour ou de fin d'après-midi. **Pas de clair-obscur, pas de contre-jour, pas de nocturne** — une seule exception, nommée et bornée : la photo du lieu (§7.4). Le site vend le soleil du Maroc.
- **Traitement** : tons chauds, sable dominant, saturation naturelle. ⛔ Éviter les filtres froids, les HDR, et — leçon de v1 — les **photos plates et désaturées** qui paraissent « patrimoniales » plutôt que solaires.
- **Sujets** : Bab Mansour et l'architecture de Meknès, le Palais Laraki, matières (zellige, bois, cuivre, thé), vos photos de couple.
- ⛔ **À éviter** : clichés mariage (alliances, colombes, cœurs, confettis), imagerie orientaliste, foules, banques d'images occidentales génériques.
- **Formats** : hero détouré en **WebP à fond transparent** (obligatoire — il se pose sur le dégradé, §5.3) ; photos de contenu en 3:2 ou 4:3. **WebP uniquement** (§7.3), `loading="lazy"`, dimensions explicites (`width`/`height`).

### 7.2 Détourage du hero — rogner jusqu'au sujet

**Le fichier ne doit contenir aucune marge transparente latérale.** La photo borde le carton (§5.3) : si le PNG détouré garde 50px de vide de chaque côté, ils se traduisent à l'écran par une bande de sable entre la façade et le filet doré — c'est exactement le défaut relevé par le Patron le 2026-07-27 (57px à gauche, 61px à droite, soit ~35px visibles de chaque côté).

Procédure : mesurer le canal alpha **sur la moitié basse** de l'image (là où les colonnes sont pleines), retenir les colonnes opaques à plus de 90 %, rogner à ces bornes. Le haut garde sa silhouette naturelle — c'est le creux entre les deux tours qui laisse voir le ciel de sable, et c'est voulu.

État courant : `hero.webp` **1802×976** (ratio 1,85), bords gauche et droit pleins à 99–100 %, 277 ko (WebP q78).

### 7.3 Un seul format : WebP. Pas d'AVIF.

**Décision du 2026-07-27, sur signalement du Patron** (*« il y a un écart colorimétrique entre le rendu dans ta preview et le rendu dans Chrome »*).

Constat mesuré en décodant les fichiers dans le navigateur (canvas, mêmes coordonnées) : **les AVIF de ce projet ne rendent pas la même couleur que leur jumeau WebP.**

| Fichier | Écart moyen AVIF vs WebP | Écart max | Sens |
|---|---|---|---|
| `hero` (ré-encodé Pillow) | **2,7** / 255 par canal | 7 | plus sombre |
| `lieu` (pipeline d'origine) | **8,7** / 255 par canal | 15 | plus sombre et plus terne |

Les fichiers sont pourtant identiques quand Pillow les relit (écart moyen < 0,6) et **aucun ne porte de profil ICC** : le décalage naît à la décision du navigateur, pas dans les pixels. Ni le sous-échantillonnage 4:4:4, ni le forçage en pleine plage, ni la montée en qualité ne l'annulent — et à fidélité égale l'AVIF ne pèse plus rien de moins (270 ko contre 277 en WebP).

**Conséquence : l'AVIF est retiré du site.** Tant qu'un `<picture>` propose les deux formats, deux invités voient deux images différentes selon le support AVIF de leur navigateur — un site de mariage n'a pas à jouer aux dés sur ses couleurs pour économiser 100 ko sur deux images. Le WebP est supporté par tous les navigateurs concernés.

> Règle : **un seul format par image.** Si l'AVIF revient un jour (beaucoup d'images, poids réellement critique), il faudra d'abord vérifier l'égalité de décodage **dans le navigateur**, pas dans la bibliothèque de traitement — c'est précisément ce qui manquait ici.

### 7.4 L'exception nocturne — la photo du lieu, et elle seule

**Décision Patron du 2026-07-27.** Le §7 interdit le nocturne. La photo du **Palais Laraki** l'enfreint, et c'est assumé : **le mariage lui-même est nocturne** (accueil 19h, fête jusqu'au petit matin). Appliquer la règle ici reviendrait à n'afficher aucune photo du lieu réel — la section « Le lieu » montrait Bab Mansour, qui n'est pas l'endroit où le mariage a lieu. L'entorse coûte moins cher que le mensonge.

**L'exception est unique et bornée.** Elle vaut pour **la photo du lieu, et pour aucune autre**. Le hero, les futures photos de contenu et toute nouvelle imagerie restent en plein soleil : c'est la promesse que porte l'invitation.

Conditions cumulatives, toutes obligatoires :

1. **Réétalonnage chaud** avant intégration — jamais la photo brute.
2. **Zéro violet/magenta.** Un éclairage scénique coloré doit être neutralisé (voir la méthode ci-dessous), résiduel < 1 % du cadre.
3. **Seuils du §7.1 respectés après retouche** : luminance ≥ 65 %, ocre ≥ 50 %.
4. **Hors champ** : signalétique commerciale envahissante, matériel technique, logistique de prestataire. Les invités et le personnel en situation sont admis — ils donnent l'échelle.

**Méthode de neutralisation d'un éclairage coloré** (celle qui a servi ici) :

> **Désaturer la plage parasite, ne pas la faire tourner.** Une rotation de teinte vers l'ocre produit des franges colorées sur les arêtes et des halos dans les dégradés de ciel — premier essai écarté pour cette raison. La bonne séquence : (a) désaturer la plage fautive (ici 235–350°, plume de 30°) à ~100 % ; (b) remonter l'exposition par gamma ; (c) réchauffer **par canal** (R ×1.07, G ×1.01, B ×0.90) ; (d) micro-contraste en S. Le réchauffement global rend leur chaleur aux zones neutralisées sans jamais créer de bande.
>
> ⚠️ **Ne jamais corriger en global** quand l'éclairage est mixte : ici les murs mesuraient `#837AA1` (R−B = −30, violet) pendant que le sol mesurait `#8C7663` (R−B = +41, chaud). Une balance des blancs unique aurait viré le sol au jaune en rattrapant les murs.

**État livré** : `lieu.webp` **1536×768** (ratio 2:1), 176 ko. Mesures après retouche — luminance **69,9 %**, ocre **86,0 %**, violet résiduel **0,1 %**. Cadre : bandeau symétrique, les deux candélabres, ciel et caisse de matériel hors champ. L'enseigne du palais est conservée (choix Patron) : elle nomme le lieu.

**Traitement en page** : rectangle plein, `rounded-lg` + ombre `md`, `max-w-3xl` centré dans la section `sable`. Contrairement aux visuels détourés du hero, l'ombre est ici légitime — elle suit le cadre, qui est le sujet.

### 7.1 Règle de validation d'une photo (héritée, renforcée)

> **Toute nouvelle direction de palette se valide contre une image réelle, jamais dans l'abstrait** — et réciproquement : **toute photo candidate au hero se mesure avant d'être posée.**

Seuils à respecter, mesurés sur les pixels opaques :

| Critère | Seuil | Pourquoi |
|---|---|---|
| Luminance moyenne (V) | **≥ 65 %** | En dessous, la photo tire la page vers le sombre quel que soit le fond |
| Part ocre / or (teinte 20–50°) | **≥ 50 %** | C'est la famille chromatique de la charte |
| Verts + bleus à saturation > 25 % | **≥ 2 % du cadre** | En dessous, le zellige de la charte n'a aucun écho dans l'image |

**L'asset actuel `hero.webp` échoue à deux seuils sur trois** : luminance **50 %** ❌, ocre 73,6 % ✅, verts/bleus saturés **0,09 %** ❌. Son zellige « vert » mesure `#888777` et sa frise « bleue » `#6F655C` — ce sont des gris. **Il doit être remplacé** avant mise en ligne (§14, reste ouvert).

---

## 8. Motion

- **Durées** : micro 150ms · standard 250ms · entrée 400ms. Jamais au-delà de 400ms.
- **Courbe** : `cubic-bezier(0.22, 1, 0.36, 1)` (`premium`) pour les entrées et survols ; `ease-in-out` pour les bascules d'état.
- **Où** : survol de carte cliquable, apparition de l'anneau de focus, rotation du `+` d'accordéon, apparition au scroll des étapes du programme (fondu + montée de 8px, **une seule fois**), `scale(0.98)` à l'appui d'un bouton.
- ⛔ **Où pas** : aucune animation en boucle, pas de parallaxe, pas de carrousel automatique, pas de rebond, pas de compte à rebours qui s'incrémente en direct.
- **`prefers-reduced-motion: reduce`** → plus aucune translation ni apparition, fondus instantanés uniquement.

---

## 9. Accessibilité (WCAG 2.1 AA)

- **Contrastes** : tous les couples texte/fond du §2 sont ≥ 4.5:1 (texte) ou ≥ 3:1 (UI). Les seules valeurs sous le seuil — `or #C8862E`, `or.light` sur clair, les `.veil` — sont **exclusivement décoratives** et la charte l'écrit à chaque occurrence.
- **Aucun texte sur photo.** Règle absolue depuis v2.0 : le texte est toujours sur un aplat de la palette (§5.3). Elle remplace la règle du voile de v1 et supprime la classe de risque associée.
- **Focus** : visible partout, anneau `zellige` + **offset obligatoire** (§5.1 bis). Jamais `outline: none` sans remplacement.
- **Cibles tactiles** : ≥ 44×44px, ≥ 8px entre deux cibles. Prioritaire : la majorité du trafic sera mobile.
- **Sémantique** : landmarks (`header`/`main`/`footer`/`nav`), hiérarchie de titres unique et continue, `<label for>` sur chaque champ, `<details>/<summary>` natifs pour les accordéons.
- **Formulaire RSVP** : erreurs annoncées (`aria-live="polite"`), champ fautif ciblé par `aria-describedby`, autocomplétion accessible au clavier (↑↓, Entrée, Échap).
- **Images** : `alt` descriptif pour le contenu, `alt=""` pour la photo d'ambiance du hero (décorative — le nom est déjà dans le titre).
- **Couleur seule** : jamais porteuse d'information — un état confirmé porte toujours un texte et une icône, pas seulement du vert.
- **`lang`/`dir`** sur `<html>`, mis à jour au changement de langue (§4.4) — `lang="fr"`, `"en"` ou `"ar"`, `dir` déduit automatiquement.
- **Contenu latin isolé en RTL** : `dir="ltr"` explicite sur tout numéro/date/compte à rebours à l'intérieur d'une page arabe (§4.4) — sans ça, le lecteur d'écran et l'affichage visuel désynchronisent l'ordre des chiffres.

---

## 10. Do's & Don'ts

**Do**
- Laisser entrer la lumière : fonds clairs, marges généreuses, une idée par section.
- Rythmer par **dune / surface / sable**, jamais par du sombre.
- Une seule voix de couleur dominante par zone : vert = agir, bleu = écrire, or = décorer.
- Poser le texte sur un aplat de la palette, jamais sur une photo.
- Détourer la photo du hero et la poser sur le dégradé.
- Colonne resserrée (`prose` 720) par défaut — c'est un faire-part.
- Libeller les boutons avec un verbe.
- Le zellige en filet fin, jamais en tapisserie.
- **Utilitaires logiques (`ms/me`, `ps/pe`, `text-start/end`) pour tout ce qui s'écrit à partir de maintenant** (§4.4) — le site est RTL pour l'arabe.
- Isoler en `dir="ltr"` tout chiffre/numéro/date au sein d'une page arabe.

**Don't**
- ⛔ Pas de section en fond `encre` hors footer.
- ⛔ Pas de voile sombre sur une photo, ni de texte posé dessus.
- ⛔ Pas de texte, pas de CTA, pas d'anneau de focus en `or` (2.09–3.04:1).
- ⛔ Pas d'anneau de focus posé à même le bouton vert (1.20:1) — l'offset est obligatoire.
- ⛔ Pas d'aplat vert plein pour un état déjà acquis (il se lit comme un bouton).
- ⛔ Pas d'émoji en guise d'icône, pas de mélange de banques.
- ⛔ Pas de photo terne : les seuils du §7.1 se mesurent, ils ne s'estiment pas.
- ⛔ Pas de Fraunces sous 20px ni sur des chiffres de données.
- ⛔ Pas de `left`/`right`/`ml`/`mr`/`pl`/`pr` en dur à partir de maintenant (§4.4) — c'était autorisé, ça ne l'est plus.
- ⛔ Pas de cliché mariage ni d'orientalisme.

---

## 11. Tokens consolidés (`tailwind.config`)

```js
tailwind.config = {
  theme: {
    extend: {
      colors: {
        cadre:'#241C13', dune:'#F4EADA', surface:'#FDF8EF', sable:'#EADCC4',
        bord:{ DEFAULT:'#D9C7A9', fort:'#9C8455' },
        encre:'#38301F', ardoise:'#6B5C42',
        vert:{ DEFAULT:'#2F6B4F', hover:'#275C43', text:'#24573F', light:'#A3CCB2', veil:'#E1EEE4' },
        zellige:{ DEFAULT:'#0F5B78', text:'#0D4E66', light:'#8FC7DC', veil:'#DCEBF1' },
        or:{ DEFAULT:'#C8862E', text:'#744E0E', light:'#EFD09A', veil:'#F6E7C9' },
        danger:{ DEFAULT:'#A32B1C', text:'#8E2318', light:'#F0A99E', veil:'#F7E0DC' },
        onDark:{ DEFAULT:'#FBF5EA', muted:'#D7C7AC' },
      },
      fontFamily: {
        display:['Fraunces','Georgia','serif'],
        body:['"Plus Jakarta Sans"','system-ui','sans-serif'],
        arabic:['Cairo','system-ui','sans-serif'],  // titres ET corps en lang="ar" — §3.1
      },
      fontSize: {
        display:['3.5rem',{ lineHeight:'1.05', letterSpacing:'-0.02em' }],
        h1:['2.5rem',{ lineHeight:'1.1', letterSpacing:'-0.015em' }],
        h2:['1.875rem',{ lineHeight:'1.15', letterSpacing:'-0.01em' }],
        h3:['1.5rem',{ lineHeight:'1.2' }],
        h4:['1.25rem',{ lineHeight:'1.3' }],
        overline:['0.875rem',{ lineHeight:'1.4', letterSpacing:'0.08em' }],
        'body-lg':['1.125rem',{ lineHeight:'1.7' }],
        body:['1rem',{ lineHeight:'1.7' }],
        small:['0.875rem',{ lineHeight:'1.6' }],
        caption:['0.75rem',{ lineHeight:'1.5', letterSpacing:'0.01em' }],
      },
      borderRadius:{ sm:'4px', md:'8px', lg:'14px', xl:'20px' },
      boxShadow:{
        sm:'0 1px 2px rgba(56,48,31,0.06)',
        md:'0 4px 16px rgba(56,48,31,0.09)',
        lg:'0 12px 32px rgba(56,48,31,0.12)',
      },
      maxWidth:{ prose:'720px', content:'1120px', wide:'1320px' },
      backgroundImage:{
        'hero-sable':'linear-gradient(180deg,#FBF3E4 0%,#F4EADA 60%,#EADCC4 100%)',
      },
      transitionTimingFunction:{ premium:'cubic-bezier(0.22,1,0.36,1)' },
      transitionDuration:{ micro:'150ms', std:'250ms', enter:'400ms' },
    }
  }
}
```

| Catégorie | Token | Valeur |
|---|---|---|
| Rayon | sm / md / lg / xl | 4 / 8 / 14 / 20 px |
| Ombre | sm / md / lg | teintées encre `rgba(56,48,31,…)`, douces |
| Conteneur | prose / content / wide | 720 / 1120 / 1320 px |
| Carton | largeur / marge / filet | 1180 px · `lg:my-10` · 1px `or` (§4.5) |
| Motion | micro / std / enter | 150 / 250 / 400 ms · courbe `premium` |
| Tactile | min | 44 px |

---

## 12. Notes d'implémentation (Tailwind CDN + Jinja2)

**Faisable en utilitaires purs :** couleurs, typo, espacements, rayons, ombres, conteneurs, boutons, champs, cartes, badges, header, footer, timeline, accordéons, focus (`focus-visible:ring-2 focus-visible:ring-zellige focus-visible:ring-offset-2 focus-visible:ring-offset-dune`), `motion-reduce:`. RTL : le `dir` porté par `<html>` mirore déjà tout seul les layouts en `flex`/`text-center` existants (§4.4) ; variantes `rtl:` de Tailwind (le mode JIT CDN les supporte) pour le reste.

**À prévoir en CSS custom dans `app.css` :**

```css
/* Polices — préchargement de Fraunces obligatoire (cf. §3.1), + Cairo 700 dès lang="ar" */

/* Bascule de pile arabe (§3.1/§3.3) */
[lang="ar"] { font-family: var(--font-body-ar); }
[lang="ar"] h1, [lang="ar"] h2, [lang="ar"] h3, [lang="ar"] .font-display {
  font-family: var(--font-display-ar);
  font-weight: 700;
}
[lang="ar"] { line-height: 1.1; } /* +0.1 relatif aux valeurs latines du §3.2, ajuster par token si besoin plus fin */

/* Filet de losanges zellige (§6.1) */
.zellige-rule{
  height:9px;
  background-image:radial-gradient(circle at 7px 9px, #C8862E 2.2px, transparent 2.4px);
  background-size:14px 9px;
  opacity:.55;
}
/* Filigrane de section — 7 % max, uniquement sur sable */
.zellige-veil{
  background-image:radial-gradient(circle at 7px 9px, #C8862E 2.2px, transparent 2.4px);
  background-size:14px 9px;
  opacity:.07;
}
/* Accordéon natif */
summary{ list-style:none }
summary::-webkit-details-marker{ display:none }
```

Reste en JS vanilla / HTMX : autocomplétion RSVP (navigation clavier), `aria-live` des erreurs de formulaire, apparition au scroll de la timeline (IntersectionObserver, une seule fois, désactivée sous `prefers-reduced-motion`).

**Passation.** Chaque token a une valeur exacte, chaque composant a ses états, chaque contrainte d'accessibilité est chiffrée. Le dev peut reprendre `base.html` et `home.html` sans nouvelle décision graphique — sauf le remplacement de la photo du hero (§14).

---

## 13. Chantier de migration depuis v1 (T1 · Terre de Meknès)

Ordre d'application sur le code existant :

1. **`base.html` — bloc `tailwind.config`** : remplacer intégralement par le §11. Les anciens noms (`ivoire`, `terre`, `laiton`) disparaissent — aucun alias, la migration est franche.
2. **`home.html` — hero** : supprimer `bg-encre` sur la `<section>`, supprimer la `<div>` de dégradé/voile, appliquer `bg-hero-sable`, déplacer le bloc de texte **au-dessus** de la `<picture>` (§5.3).
3. **`home.html` — section « Le lieu »** : `bg-encre` → `bg-sable` ; textes `onDark`/`onDark-muted` → `encre`/`ardoise` ; sur-titre `terre-light` → `zellige-text`.
4. **Boutons** : `bg-terre text-white` → `bg-vert text-white hover:bg-vert-hover` ; **tous** les `focus-visible:ring-*` → `ring-zellige` + `ring-offset-2` + `ring-offset-<fond de la section>`.
5. **Sur-titres de section** : `text-laiton-text` → `text-zellige-text`. **Points de la timeline** : `bg-terre` → `bg-vert`. **Horaires** : `text-terre-text` → `text-zellige-text`.
6. **`.terre-divider`** dans `app.css` → `.zellige-rule` (§12).
7. **Footer** : conserver `bg-encre`, passer l'accent de date en `or.light`.
8. **Alternance des fonds** : vérifier qu'aucune section ne reprend le fond de la précédente (§2.5).
9. **Carton faire-part** (§4.5) : `body` en `bg-cadre`, wrapper `.carton` autour du header/main/footer, filet `border border-or`, header dé-collé (`sticky` retiré).
10. **Photo du hero** : remplacer par l'asset validé au §7.1, détouré, fond transparent. **Bloquant pour la mise en ligne.**

---

## 14. Journal des décisions & reste ouvert

### Historique des directions

| Version | Direction | Sort |
|---|---|---|
| v1.0 (2026-06-12) | **A · Bleu zellige** | **Abandonnée le 2026-07-27.** Arbitrée sans image de référence, sur l'intuition « le bleu des zelliges des villes impériales ». La mesure de Bab Mansour a montré 73,7 % d'ocre et **0,04 %** de vert/bleu saturé : un voile bleu-nuit sur une façade ocre donne un gris terne, et aucun réglage d'opacité ne le corrige — le problème était la teinte, pas le dosage. |
| v1.x (2026-07-27, matin) | **T1 · Terre de Meknès** | **Abandonnée le 2026-07-27, après-midi.** Palette juste (dérivée de la colorimétrie réelle) mais **traitement trop sombre** : voile de hero à 93 % d'opacité, deux sections sur fond encre, accent terre brûlée sans luminosité. Diagnostic du Patron : « trop sombre, je veux quelque chose de plus lumineux ». |
| **v2.0 (2026-07-27)** | **S3 · Sahara & Menthe** | **En vigueur.** Retenue parmi trois directions plein soleil (S1 · Plein Soleil, S2 · Ciel de Meknès, S3). |
| **v2.1 (2026-07-28)** | **S3 + multilingue FR/EN/AR** | **En vigueur.** Aucun changement de direction visuelle — ajoute le multilingue (§4.4 réécrit, typographie Cairo §3.1, sélecteur §5.10 bis) suite à la décision produit du 2026-07-28. |

**Ce que v2.0 corrige, au-delà de la palette.** L'erreur de v1 n'était pas chromatique mais **structurelle** : la charte avait hérité d'OWP le pattern « sections sombres pour rythmer » et « voile sombre sous le texte sur photo », qui sont des patterns de **produit** (marketplace, dashboard) et non de **faire-part**. v2.0 les supprime tous les deux : rythme par trois clairs (§2.5), aucun texte sur photo (§5.3).

**Ce que v2.1 découvre en auditant le code pour le RTL.** Le code construit sous v2.0 n'a jamais exercé l'autorisation `left`/`right` en dur que l'ancien §4.4 lui donnait — tout est en `flex`/`text-center`/`gap`, qui mirore tout seul sous `dir="rtl"`. Zéro dette à rattraper ; seule la règle change pour la suite (§4.4).

### Réserve du DA sur S3, et comment elle est traitée

Le vert en couleur d'action se lit spontanément comme « succès / validé » sur le web. Le Patron a tranché en connaissance de cause. Conséquences intégrées à la charte :
- **Aucun token `success` séparé** — le vert porte l'action *et* la confirmation (§2.2).
- **Règle de désambiguïsation stricte** : aplat plein = action + libellé verbal ; état acquis = badge `vert.veil` + icône, jamais d'aplat plein.
- À surveiller au premier test réel : si un invité hésite devant « Confirmer ma présence » en le prenant pour un statut déjà acquis, la règle ne suffit pas et il faudra rebasculer l'action sur `zellige` (variante S2, déjà chiffrée : blanc sur `#0F5B78` = 7.53:1 AAA).

### Reste ouvert

- **Photo du hero — pas prioritaire pour l'instant (décision Patron, 2026-07-28).** L'asset actuel échoue toujours à deux des trois seuils du §7.1 (luminance 50 %, ocre 29 %) ; le Patron a choisi de ne pas la remplacer maintenant (« on reste comme ça »). Reste techniquement non conforme à la charte — à reprendre si/quand le Patron fournit une nouvelle photo en pleine résolution.
- Photo du couple (`couple.jpg`) — optionnelle, non fournie.
- **Contenu traduit EN/AR** : la charte spécifie la typographie, le RTL et le sélecteur (§3.1/§4.4/§5.10) ; la traduction des textes eux-mêmes (copywriting, catalogue `translations.py`) est un chantier technique/produit distinct, hors périmètre DA — cf. `proposition_produit.md` §6.4 (effort non budgété).

**Résolu depuis la dernière version** : photo réelle du Palais Laraki livrée (§7.4, 2026-07-27) ; nombre de moments du programme tranché à « un seul » (2026-07-27, `proposition_produit.md` §5.5).
