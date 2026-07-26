# Site mariage Meknès — Proposition (design, fonctionnalités, intégration, plan)

> Mariage Kenza & Julien · **Meknès, vendredi 23 octobre 2026** · Site invités FR · accès par code commun.
> Statut : **arbitré par le Patron le 2026-06-12**, **palette révisée le 2026-07-27** — direction **T1 · Terre de Meknès** (remplace A · Bleu zellige, cf. §2.1 bis), hébergement **Render**, domaine **mariage-maroc.igolen.com**, mariage entièrement au **Palais Laraki** (jusqu'au petit matin, déroulé détaillé à venir). S0 livré (socle : porte à code, layout tokens, modèles, Alembic, render.yaml).
> Référence reprise : site France https://julienigolen.github.io/mariage/ (one-page : hero, histoire, programme, adresses/accès, dress code, RSVP Formspree).

---

## 1. Avis : intégrer dans OWP ou non ?

**Recommandation tranchée : NE PAS développer dans le produit OWP — mais le piller méthodiquement.**

Contre l'intégration produit :
- **Deadline dure** (23/10) vs roadmap produit : coupler le mariage aux sprints OWP met les deux en risque.
- **Modèle d'accès incompatible** : OWP est construit sur des comptes utilisateurs ; le besoin ici est un code commun + RSVP par recherche de nom. Tordre l'auth OWP coûterait plus cher qu'un module dédié.
- **FR seul** : l'avantage différenciant d'OWP (i18n FR/AR + RTL + hijri) ne sert pas ici.
- OWP n'a pas encore de module site-invités/RSVP : il faudrait le créer *dans* le produit sous pression — mauvaises décisions garanties.

Pour la réutilisation (gain de temps réel) :
- **Même stack** : FastAPI + Jinja2 + Tailwind CDN (no build) + HTMX + Postgres/Alembic. Copier la structure du repo OWP (`templates_engine`, `email_service`, setup Alembic, config) = socle en 1 session au lieu de 3.
- **Mécanique de la charte** réutilisée telle quelle : échelle typo, espacements, rayons, ombres, patterns de composants (hero voilé, cartes, badges, modale). Seule la **palette change** (identité propre, voir §2).
- **Retour sur investissement OWP** : ce site devient le prototype réel du futur module « site invités + RSVP » d'OWP (dogfooding inversé, specs déjà éprouvées).

→ **Repo séparé `mariage-zellige`**, projet jetable assumé, qui réutilise les patterns OWP par copie (pas par dépendance).

---

## 2. Design cible

### 2.1 Trois directions nommées

| Direction | Idée | Implication |
|---|---|---|
| **A · Bleu zellige** ~~⭐ recommandée~~ | Ivoire chaud + encre bleu nuit + accent bleu zellige, cuivre en seconde voix. | **Abandonnée le 2026-07-27** — voir §2.1 bis. Contrastes AA corrects sur le papier, mais palette froide incompatible avec l'imagerie réelle du site. |
| **B · Médina d'or** | Continuité du site France : champagne, safran, chic lumineux. | Cohérence entre les deux sites, mais risque « copie » ; ⚠ blanc/safran `#B07014` = 4.06:1 (échec AA) → CTA à assombrir si retenue. |
| **C · Jardin d'Andalou** | Vert zellige profond + ivoire + laiton. Référence aux jardins/riads. | Très élégant (contrastes excellents : 8.9–9.6:1) mais plus sombre, moins festif. |

### 2.1 bis Pourquoi A a été abandonnée (2026-07-27)

L'intégration de la photo de **Bab Mansour** en hero a révélé un conflit que la charte n'avait pas anticipé : elle avait été arbitrée **sans image de référence**, sur une intuition (« le bleu des zelliges des villes impériales »).

Mesure de la colorimétrie réelle du visuel (k-means sur les pixels du monument) :

| Famille de teintes | Part de la surface | Saturation moyenne |
|---|---|---|
| Ocre / or (20–50°) | **73,7 %** | 32 % |
| Rouge / brun (0–20°) | 9,2 % | 33 % |
| Olive (50–90°) | 10,6 % | 10 % |
| Vert (90–160°) | 3,3 % | 10 % |
| Turquoise + bleu (160–260°) | 2,0 % | 6–8 % |

**Verts et bleus à saturation > 30 % : 0,04 % de l'image.** Le zellige de la façade paraît vert-de-gris à l'œil, mais il est colorimétriquement quasi neutre. Poser un voile bleu-nuit `#232E47` sur une façade ocre produit un rendu gris terne, et aucun réglage de dosage ne le corrige — le problème est la teinte, pas l'opacité. Les accents pastels de A (`cuivre.light`, `zellige.light`) tombaient par ailleurs à 1,6–3,4:1 sur cette image, sous le seuil AA.

**Décision Patron : bascule sur T1 · Terre de Meknès**, palette dérivée de la colorimétrie mesurée.

### 2.2 Palette T1 · Terre de Meknès (contrastes WCAG calculés sur ivoire `#FBF7F0`)

| Token | Hex | Usage | Contraste |
|---|---|---|---|
| `ivoire` | `#FBF7F0` | Fond de page | base |
| `surface` | `#FFFDF8` | Cartes, formulaires | base |
| `sable` | `#E9DDC9` | Bordures, séparateurs · accent clair sur photo | base · **11.63:1** sur encre — AAA |
| `encre` | `#2E2117` | Texte principal · sections sombres · voile hero | **14.61:1** — AAA |
| `ardoise` | `#6A5844` | Texte secondaire | **6.36:1** — AA |
| `terre` (accent) | `#9B4A2A` | CTA primaire (texte blanc dessus : **6.16:1** AA), focus | **5.77:1** — AA |
| `terre.text` | `#823E22` | Liens, accents texte | **7.39:1** — AAA |
| `terre.light` | `#E3A98C` | Accent sur fond sombre encre | **7.67:1** sur encre — AAA |
| `laiton` | `#8A6A18` | Seconde voix festive (badges, icônes) | **4.73:1** — AA |
| `laiton.text` | `#75590F` | Variante texte du laiton | **6.16:1** — AA |
| `laiton.light` | `#E8C87E` | Laiton sur fond sombre | **9.65:1** sur encre — AAA |
| `onDark` | `#FAF4EA` | Texte sur sections sombres | **14.26:1** sur encre — AAA |
| `onDark.muted` | `#D5C6B2` | Texte secondaire sur sombre | **9.32:1** sur encre — AAA |
| `danger` | `#9E2B1E` | Erreur (bordure de champ, message) | **6.98:1** — AA |
| `danger.text` | `#8E2318` | Message d'erreur | **8.18:1** — AA |
| `danger.light` | `#F0A99E` | Erreur sur fond sombre | **8.08:1** sur encre — AAA |

**Note sur `danger`** : sous la charte A, la couleur d'erreur était `cuivre` détourné. Impossible ici — `terre` porte le CTA primaire, une erreur de la même teinte que le bouton d'action est un contresens. D'où un token dédié, rouge profond (teinte 5°) qui reste dans la famille chaude.

Règles reprises de la charte OWP : un seul accent par zone visuelle, sections sombres (`encre`) pour rythmer, jamais d'accent foncé sur fond sombre (basculer sur `.light`), voile sombre obligatoire sous tout texte posé sur photo.

**Règle ajoutée (2026-07-27)** : le voile posé sur une photo doit être teinté avec l'`encre` de la charte, et l'`encre` doit appartenir à la famille chromatique de l'imagerie du site. Toute nouvelle direction de palette se valide **contre une image réelle**, pas dans l'abstrait.

### 2.3 Typographie & imagerie

- **Titres Fraunces, corps Plus Jakarta Sans** — réutilisés d'OWP (rendu déjà validé, zéro décision à reprendre). L'identité est portée par la couleur et l'image, pas par une nouvelle typo.
- Échelle typo, espacements, rayons, ombres, motion : **reprendre les tokens §3/§4/§8/§11 de la charte OWP tels quels** (ombres re-teintées encre `rgba(46,33,23,…)`).
- **Imagerie** : photos chaudes de Meknès (médina, zellige, lumière dorée) + vos photos de couple. Le hero porte **Bab Mansour** (façade détourée sur fond transparent, `hero.webp`/`hero.avif` 1920×980) : la porte occupe le haut de la section, le dégradé `encre` se resserre vers le bas pour porter le texte. Motif zellige autorisé uniquement en **filigrane géométrique fin** (séparateurs, fond de section à ~7 % d'opacité) — jamais en tapisserie orientaliste.
- Interdits identiques à la charte : émojis-icônes (Lucide partout), clichés mariage, pages nues.

---

## 3. Fonctionnalités

### MVP (reprise site France + intégrations demandées)

1. **Porte d'entrée** : code commun (un champ, cookie 90 j, message d'erreur doux). Tout le site derrière, `noindex` partout.
2. **One-page invités** : hero photo voilé (noms, 23/10/2026, Meknès, CTA RSVP), mot d'accueil, **programme** multi-temps (le mariage marocain peut compter plusieurs moments — structure N événements dès le départ), adresses + liens Google Maps, dress code, FAQ.
3. **Guide voyage** — section différenciante, en deux volets repliables pour ne pas polluer les invités locaux :
   - *Vous venez de France* : vols (aéroport Fès-Saïss à ~45 min de Meknès, alternatives Rabat/Casablanca + train/voiture), passeport/formalités, hébergements recommandés (sélection riads/hôtels + distances au lieu), se déplacer (taxis, InDrive), monnaie & pourboires, météo fin octobre (~24 °C jour / 12 °C nuit), à voir sur place.
   - *Vous êtes sur place* : accès au lieu, parking, horaires.
4. **RSVP intégré** (remplace Formspree + Google Sheet) :
   - recherche du nom avec autocomplétion sur la liste importée (HTMX), réponse **par foyer** ;
   - présence par événement, nb de personnes, allergies/régimes, message libre ;
   - écriture Postgres + email de notification aux mariés (réutilise le pattern `email_service` OWP) ;
   - modifiable : re-saisir son nom ré-affiche sa réponse.
5. **Admin** (vous deux, login simple) :
   - **import Excel initial** de la liste, puis CRUD invités en ligne ;
   - tableau de bord : confirmés / refus / sans réponse, total couverts, par événement ;
   - **envoi d'invitations et relances par email** (template aux couleurs du site, contient le lien + le code) ;
   - export CSV/Excel à tout moment.

### V2 (si le temps le permet, après le 23/10 pour certaines)

Covoiturage/navettes entre hôtels et lieu, galerie photos post-mariage derrière le même code, livre d'or numérique.

---

## 4. Architecture & hébergement

- **Stack** : FastAPI + Jinja2 + Tailwind CDN + HTMX, Postgres 16, Alembic. Repo `mariage-zellige` (structure clonée d'`owp`).
- **Modèle de données** : `household` (foyer, nom, email, tel, langue, origine FR/MA), `guest` (rattaché au foyer), `event` (N moments du programme), `rsvp` (foyer × événement, statut, nb, régimes, message, horodaté), `admin_user`, `settings` (code d'accès, hashé).
- **Hébergement recommandé** : VPS léger (Hetzner CX22 ou OVH Starter, ~5 €/mois) + **Docker Compose** (app + Postgres + Caddy pour le TLS auto) + nom de domaine. Avantages : maîtrise totale, réutilisable ensuite pour les environnements OWP. Alternative zéro-ops si tu préfères : Railway/Render (~10 €/mois, déploiement git-push, Postgres managé).
- **Emails** : un compte SMTP transactionnel gratuit au volume d'un mariage (Brevo : 300/jour gratuits).
- **Sauvegardes** : `pg_dump` quotidien poussé hors VPS — la liste d'invités et les RSVP sont les seules données irremplaçables.

---

## 5. Plan de réalisation (100 % Cowork, du 12/06 au 23/10/2026)

| Jalon | Quand | Contenu | Sessions Cowork |
|---|---|---|---|
| **S0 · Décisions & socle** | sem. du 16/06 | Arbitrages Patron (direction design, hébergeur, domaine) ; repo, VPS, Compose, DB, Alembic, porte à code, layout tokens | 1–2 |
| **S1 · Vitrine** | fin juin | Hero, programme, adresses, dress code, FAQ — contenu provisoire accepté | 2 |
| **🚀 Save-the-date en ligne** | **début juillet** | Mise en ligne de la vitrine seule : **les invités France doivent réserver leurs vols tôt, c'est la vraie urgence** | — |
| **S2 · RSVP** | mi-juillet | Import Excel, recherche nom, formulaire foyer, persistence, email notification | 2 |
| **S3 · Admin & invitations** | fin juillet | Login, CRUD invités, dashboard RSVP, envoi emails invitation/relance, export | 2 |
| **S4 · Guide voyage & finitions** | août | Contenu voyage complet, photos, recette mobile, accessibilité, perfs | 1–2 |
| **📨 Envoi officiel** | sem. du 31/08 | Invitations envoyées depuis l'admin (~7 semaines avant) | — |
| **Exploitation** | sept.–oct. | Relances ciblées via dashboard, gel du contenu à J−7 | ponctuel |

Marge intégrée : le développement se termine fin août pour un mariage fin octobre.

---

## 6. Décisions attendues du Patron

1. Direction design : **A · Bleu zellige** (reco), B ou C.
2. Hébergement : VPS Hetzner/OVH (reco) ou PaaS Railway/Render.
3. Nom de domaine souhaité (ex. `kenza-julien.ma` / `.fr` / sous-domaine existant).
4. Le programme : combien de moments/événements distincts ? (structure le RSVP)
5. Go S0.
