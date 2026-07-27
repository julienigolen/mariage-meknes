# Site mariage Meknès — Proposition produit (fonctionnalités, intégration, architecture, plan)

> Mariage Kenza & Julien · **Meknès, vendredi 23 octobre 2026** · Site invités FR · accès par code commun.
> Statut : **arbitré par le Patron le 2026-06-12**. Hébergement **Render**, domaine **mariage-maroc.igolen.com**, mariage entièrement au **Palais Laraki** (jusqu'au petit matin, déroulé détaillé à venir). S0 livré (socle : porte à code, layout tokens, modèles, Alembic, render.yaml).
> Référence reprise : site France https://julienigolen.github.io/mariage/ (one-page : hero, histoire, programme, adresses/accès, dress code, RSVP Formspree).
>
> **Direction artistique : voir `charte_graphique.md` (même dossier).** Ce document ne traite plus du design — il a été scindé le 2026-07-27 pour séparer la charte (livrable DA, versionné indépendamment) des décisions produit.

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
- **Mécanique de la charte** réutilisée : échelle typo, espacements, rayons, ombres, patterns de composants. La palette et le parti visuel sont propres au mariage (cf. `charte_graphique.md`).
- **Retour sur investissement OWP** : ce site devient le prototype réel du futur module « site invités + RSVP » d'OWP (dogfooding inversé, specs déjà éprouvées).

→ **Repo séparé `mariage-meknes`**, projet jetable assumé, qui réutilise les patterns OWP par copie (pas par dépendance).

> ⚠️ Leçon apprise (2026-07-27) : la copie des patterns OWP a été poussée trop loin côté design — les patterns « sections sombres » et « voile sur photo » sont des patterns de produit, pas de faire-part. Voir `charte_graphique.md` §14. La réutilisation vaut pour la **mécanique** (tokens, échelles, structure du repo), pas pour le **parti visuel**.

---

## 2. Fonctionnalités

### MVP (reprise site France + intégrations demandées)

1. **Porte d'entrée** : code commun (un champ, cookie 90 j, message d'erreur doux). Tout le site derrière, `noindex` partout.
2. **One-page invités** : hero (noms, 23/10/2026, Meknès, CTA RSVP), mot d'accueil, **programme** multi-temps (le mariage marocain peut compter plusieurs moments — structure N événements dès le départ), adresses + liens Google Maps, dress code, FAQ.
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

## 3. Architecture & hébergement

- **Stack** : FastAPI + Jinja2 + Tailwind CDN + HTMX, Postgres 16, Alembic. Repo `mariage-meknes` (structure clonée d'`owp`).
- **Modèle de données** : `household` (foyer, nom, email, tel, langue, origine FR/MA), `guest` (rattaché au foyer), `event` (N moments du programme), `rsvp` (foyer × événement, statut, nb, régimes, message, horodaté), `admin_user`, `settings` (code d'accès, hashé).
- **Hébergement retenu** : **Render** (`render.yaml` livré en S0) — déploiement git-push, Postgres managé, zéro ops. Le VPS Hetzner/OVH + Docker Compose avait été proposé mais n'a pas été retenu.
- **Domaine** : `mariage-maroc.igolen.com`.
- **Emails** : un compte SMTP transactionnel gratuit au volume d'un mariage (Brevo : 300/jour gratuits).
- **Sauvegardes** : `pg_dump` quotidien poussé hors hébergeur — la liste d'invités et les RSVP sont les seules données irremplaçables.

---

## 4. Plan de réalisation (100 % Cowork, du 12/06 au 23/10/2026)

| Jalon | Quand | Contenu | Sessions Cowork |
|---|---|---|---|
| **S0 · Décisions & socle** | sem. du 16/06 | Arbitrages Patron (direction design, hébergeur, domaine) ; repo, DB, Alembic, porte à code, layout tokens, render.yaml | 1–2 · **livré** |
| **S1 · Vitrine** | fin juin | Hero, programme, adresses, dress code, FAQ — contenu provisoire accepté | 2 |
| **🚀 Save-the-date en ligne** | **début juillet** | Mise en ligne de la vitrine seule : **les invités France doivent réserver leurs vols tôt, c'est la vraie urgence** | — |
| **S2 · RSVP** | mi-juillet | Import Excel, recherche nom, formulaire foyer, persistence, email notification | 2 |
| **S3 · Admin & invitations** | fin juillet | Login, CRUD invités, dashboard RSVP, envoi emails invitation/relance, export | 2 |
| **S4 · Guide voyage & finitions** | août | Contenu voyage complet, photos, recette mobile, accessibilité, perfs | 1–2 |
| **📨 Envoi officiel** | sem. du 31/08 | Invitations envoyées depuis l'admin (~7 semaines avant) | — |
| **Exploitation** | sept.–oct. | Relances ciblées via dashboard, gel du contenu à J−7 | ponctuel |

Marge intégrée : le développement se termine fin août pour un mariage fin octobre.

> **Écart au plan constaté le 2026-07-27** : deux itérations de direction artistique (A → T1 → S3) ont consommé du temps qui n'était pas budgété. Le chantier de migration visuelle (`charte_graphique.md` §13) est à absorber avant de reprendre S2/S3.

---

## 5. Décisions prises

1. **Direction design** : S3 · Sahara & Menthe (2026-07-27). Historique complet : `charte_graphique.md` §14.
2. **Hébergement** : Render.
3. **Domaine** : `mariage-maroc.igolen.com`.
4. **Langue** : français uniquement, pas de RTL.

## 6. Décisions encore attendues du Patron

1. **Le programme : combien de moments/événements distincts ?** (structure le RSVP par événement — bloquant pour S2).
2. Photo réelle du Palais Laraki (la section « Le lieu » affiche aujourd'hui Bab Mansour, qui n'est pas le lieu du mariage).
3. Photo du hero en pleine résolution (bloquant mise en ligne — `charte_graphique.md` §7.1).
