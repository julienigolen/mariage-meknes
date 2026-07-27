# Site mariage Meknès — Proposition produit (fonctionnalités, intégration, architecture, plan)

> Mariage Kenza & Julien · **Meknès, vendredi 23 octobre 2026** · Site invités multilingue FR/EN/AR (§2 point 6) · accès par code commun.
> Statut : **arbitré par le Patron le 2026-06-12**. Hébergement **Render**, domaine **mariage-maroc.igolen.com**, mariage entièrement au **Palais Laraki** (jusqu'au petit matin, déroulé détaillé à venir). S0 livré (socle : porte à code, layout tokens, modèles, Alembic, render.yaml).
> Référence reprise : site France https://julienigolen.github.io/mariage/ (one-page : hero, histoire, programme, adresses/accès, dress code, RSVP Formspree).
>
> **Direction artistique : voir `charte_graphique.md` (même dossier).** Ce document ne traite plus du design — il a été scindé le 2026-07-27 pour séparer la charte (livrable DA, versionné indépendamment) des décisions produit.

---

## 1. Avis : intégrer dans OWP ou non ?

**Recommandation tranchée : NE PAS développer dans le produit OWP — mais le piller méthodiquement.**

Contre l'intégration produit :
- **Deadline dure** (23/10) vs roadmap produit : coupler le mariage aux sprints OWP met les deux en risque.
- **Modèle d'accès incompatible** : OWP est construit sur des comptes utilisateurs ; le besoin ici est un code commun + RSVP identifié par téléphone. Tordre l'auth OWP coûterait plus cher qu'un module dédié.
- ~~FR seul : l'avantage différenciant d'OWP (i18n FR/AR + RTL) ne sert pas ici~~ — **argument caduc depuis le 2026-07-27** (§2 point 6) : le site est devenu multilingue FR/EN/AR et a exactement ce besoin. Ne remet pas en cause le repo séparé (les deux autres raisons ci-dessus restent valables), mais autant ne pas laisser un argument faux dans le document : c'est justement **le pattern technique d'OWP** qui est repris par copie, cf. §2 point 6.
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

1. **Porte d'entrée** : code commun (un champ, cookie 90 j, message d'erreur doux) **+ sélecteur de langue FR/EN/AR** (2026-07-27, cf. §2 point 6 et §5.15 — c'est le seul écran vu par 100 % des invités avant tout contenu, donc le seul endroit cohérent pour fixer la langue avant que quoi que ce soit ne s'affiche). Tout le site derrière, `noindex` partout.
2. **One-page invités** : hero (noms, 23/10/2026, Meknès, CTA RSVP), mot d'accueil, **programme** — **un seul moment** (décision Patron du 2026-07-27 ; le RSVP n'a donc pas à ventiler la présence par événement, une réponse par foyer suffit), adresses + liens Google Maps, dress code, FAQ.
3. **Guide voyage** — section différenciante, en deux volets repliables pour ne pas polluer les invités locaux :
   - *Vous venez de France* : vols (aéroport Fès-Saïss à ~45 min de Meknès, alternatives Rabat/Casablanca + train/voiture), passeport/formalités, hébergements recommandés (sélection riads/hôtels + distances au lieu), se déplacer (taxis, InDrive), monnaie & pourboires, météo fin octobre (~24 °C jour / 12 °C nuit), à voir sur place.
   - *Vous êtes sur place* : accès au lieu, parking, horaires.
4. **RSVP intégré** (remplace Formspree + Google Sheet) :
   - **identifiant : numéro de téléphone** (décision Patron du 2026-07-27, plutôt que recherche de nom ou email). **Source Excel = une ligne par personne**, avec une colonne **`famille`** optionnelle (libellé libre commun) pour regrouper plusieurs lignes en un seul foyer (précision Patron 2026-07-27) — donc **N numéros possibles par foyer**, pas seulement deux : le cas courant est le couple (2 lignes, même `famille`), mais rien n'empêche un foyer élargi (parent + enfant adulte, fratrie) si le Patron leur donne le même libellé. Une ligne sans `famille` renseignée est son **propre foyer à elle seule**. Le foyer est identifié dès que le numéro saisi correspond à **n'importe lequel** des téléphones qui lui sont rattachés. Pas d'autocomplétion en direct (elle exposerait les autres foyers à qui tape) : le numéro est saisi en entier, matché en exact ; nom/prénom sont **préremplis** dès qu'une personne correspondante est trouvée, modifiables sinon (repli invité oublié dans l'Excel). Pas de vérification par SMS (hors budget) — la connaissance d'un des numéros du foyer fait foi ;
   - **champs du formulaire**, réponse par foyer :
     1. Numéro de téléphone (identifiant)
     2. Nom / prénom (préremplis sur base du téléphone)
     3. **Email — optionnel** (2026-07-27 : pas dans l'import, « on ne le sait pas », collecté ici et **non obligatoire**). Nécessaire pour l'email de confirmation + lien de modification ci-dessous : un foyer qui ne le renseigne pas ne reçoit ni l'un ni l'autre, mais reste identifiable et modifiable par re-saisie de son numéro (§5.11) — l'email n'est qu'un confort, jamais une condition d'accès.
     4. Nombre d'adultes
     5. Nombre d'enfants
     6. Allergies alimentaires : Oui / Non + texte libre si Oui
     7. Besoin de réserver un hôtel (Oui / Non)
   - écriture Postgres + email de notification aux mariés (réutilise le pattern `email_service` OWP), email de confirmation au foyer avec lien de modification si un email a été saisi (ne pas dépendre du seul cookie — perdu au changement d'appareil) ;
   - modifiable : re-saisir n'importe lequel des numéros rattachés au foyer ré-affiche sa réponse enregistrée.
   - **Goodies** (2026-07-27) :
     - **Message de validation personnalisé par foyer**, affiché à l'écran de confirmation après l'envoi du formulaire. Optionnel — un foyer sans message défini voit une confirmation générique. Alimenté depuis l'admin (import Excel ou CRUD), texte libre. **Décision 2026-07-28** : pas de traduction automatique de ce texte — le Patron le saisit directement **dans la langue qu'il suppose être celle du foyer** (« on connaît nos invités »), à l'import ou en CRUD. Un foyer qui consulte sa confirmation dans une autre langue que celle du message verra donc ce texte non traduit, quelle que soit sa langue active — limite assumée, pas un bug à corriger.
     - **Message « quelqu'un de votre famille a déjà répondu » si un second numéro du même foyer se présente.** Un foyer peut regrouper plusieurs personnes, chacune avec son propre numéro (§2 identifiant) ; si l'une répond puis qu'une autre se présente avec **le sien** (différent), le système doit reconnaître que les deux numéros pointent vers le **même foyer** (via le libellé `famille` à l'import) et afficher un message dédié avant de ré-ouvrir le formulaire pré-rempli en modification — sans ça, la seconde personne croirait devoir remplir une réponse séparée. Repose entièrement sur le rattachement des numéros au foyer (§3) : sans lui, ce goodie est impossible à déclencher correctement.
   - **Date limite de réponse : fin août 2026** (2026-07-28) — affichée dans la section RSVP (et probablement rappelée dans le guide voyage). `settings.date_limite_rsvp`, valeur exacte à trancher plus tard entre le Patron et Kenza (« fin août » n'est pas encore un jour précis), le gabarit affiche un texte générique tant qu'aucun jour exact n'est fixé.
5. **Admin** (vous deux, login simple) :
   - **import Excel initial** de la liste, puis CRUD invités en ligne ;
   - tableau de bord : confirmés / refus / sans réponse, total couverts ;
   - **pas d'invitations ni de relances envoyées par le site** (2026-07-28, corrige la v1 de ce document — cf. §5.16) : le Patron gère ça **à la main, au cas par cas, via WhatsApp** (lien + code copiés-collés par ses soins). L'admin se contente d'un **suivi** : marquer un foyer « relancé le » (date, pré-remplie à aujourd'hui, modifiable) pour savoir qui a déjà été recontacté ;
   - export CSV/Excel à tout moment.
6. **Site multilingue FR/EN/AR** (2026-07-27 — **remplace la décision « français uniquement, pas de RTL » du 12/06/2026**, cf. §5.4/§5.14) :
   - **Toutes les pages** traduites : porte d'entrée, one-page (hero/programme/lieu/dress code), guide voyage, formulaire RSVP, emails, admin.
   - **La langue se demande à la porte d'entrée, pas à l'identification RSVP** (correction du 2026-07-27 — §5.15, incohérence relevée par le Patron). La déduction depuis le téléphone (`household_member.langue`, §3) **ne peut pas servir de défaut** : le téléphone n'est connu qu'au moment du RSVP, très après que le foyer a déjà vu la porte d'entrée, le hero, le programme et le guide voyage — tous rendus en `fr` entre-temps, quelle que soit la langue réelle du foyer. Défaut incohérent, donc abandonné.
   - **Sélecteur explicite sur la porte d'entrée** : FR / EN / AR, FR pré-sélectionné, à côté ou au-dessus du champ code. Le choix (ou l'absence de choix, qui vaut FR) est posé en cookie **avant** que la première page de contenu ne s'affiche — c'est le seul point du parcours où ça a un sens.
   - `household_member.langue` (déduite du téléphone) **redevient une donnée dormante** : conservée en base, potentiellement utile plus tard (ex. envoyer les relances admin dans la bonne langue), mais **n'influence plus l'affichage du site** — pour éviter l'autre écueil symétrique : changer silencieusement la langue d'un foyer en pleine lecture, après qu'il a déjà choisi ou implicitement accepté le FR à l'entrée, serait aussi déroutant que le défaut qu'on vient d'abandonner.
   - **L'utilisateur peut changer de langue à tout moment** via le même sélecteur, repris dans le header sur les pages suivantes ; le choix est mémorisé en cookie et reste actif jusqu'au prochain changement explicite.
   - **Technique reprise du projet OWP** (`owp/i18n/translations.py`) :
     - un **catalogue centralisé unique** `app/i18n/translations.py` — `TRANSLATIONS: dict[str, dict] = {"fr": {...}, "en": {...}, "ar": {...}}`, clés à préfixe de domaine (`gate_*`, `hero_*`, `programme_*`, `guide_*`, `rsvp_*`, `admin_*`, `email_*`) pour éviter les collisions. **Aucun texte en dur dans les templates.**
     - route `GET /set-lang?lang=<fr|en|ar>&next=<url>` : pose le cookie `lang` (non httpOnly, `samesite=lax`, `path=/`), redirige vers `next` (doit commencer par `/` — protection open-redirect), reprise à l'identique du pattern OWP.
     - `<html lang="{{ lang }}" dir="{{ 'rtl' if lang == 'ar' else 'ltr' }}">` — `dir` calculé directement depuis `lang`, jamais un état séparé.
     - **RTL uniquement pour l'arabe** : CSS `[lang="ar"]` pour la police (probable Cairo, à valider en charte) ; **utilitaires logiques Tailwind exclusivement** (`ms/me`, `ps/pe`, `text-start/end`, `start/end`) — **inverse de la charte actuelle §4.4**, qui autorisait `left/right` en dur faute de RTL prévu.

### V2 (si le temps le permet, après le 23/10 pour certaines)

Covoiturage/navettes entre hôtels et lieu, galerie photos post-mariage derrière le même code, livre d'or numérique.

---

## 3. Architecture & hébergement

- **Stack** : FastAPI + Jinja2 + Tailwind CDN + HTMX, Postgres 16, Alembic. Repo `mariage-meknes` (structure clonée d'`owp`) — **+ module `app/i18n/translations.py`** repris du pattern OWP (§2 point 6).
- **Modèle de données** (révisé 2026-07-27 : un seul moment de programme → plus de relation foyer × événement) :
  - **Import = une ligne par personne** (colonnes attendues : nom/prénom, téléphone **avec indicatif** (§5.9), `famille` libellé libre optionnel, origine FR/MA, `langue` optionnelle — cf. `household_member` ci-dessous). **Pas d'email dans l'import** (2026-07-27, « on ne le sait pas ») — il est collecté au moment du RSVP, pas au moment de l'import. Le regroupement en foyer se fait **à l'import** : toutes les lignes partageant le même libellé `famille` (non vide) forment un foyer ; une ligne sans `famille` est un foyer à elle seule.
  - `household` : foyer — `import_famille_label` (le libellé Excel d'origine, conservé pour traçabilité/rapprochement admin, pas réutilisé après import), `message_personnalise` (texte libre, nullable — goodie confirmation, §2 point 4, saisi dans la langue jugée adaptée par le Patron, pas traduit), **`relance_le`** (**ajouté 2026-07-28**, date nullable — suivi manuel du dernier contact WhatsApp, saisi par le Patron dans l'admin, champ pré-rempli à la date du jour et modifiable ; vit sur `household` et non sur `rsvp` car il doit pouvoir être renseigné même pour un foyer **sans réponse**, qui n'a justement pas encore de ligne `rsvp`). Pas de colonne `email` ici : elle est saisie une fois, sur `rsvp` (ci-dessous), au moment où le foyer répond — avant ça, aucun email n'est connu pour lui, et **aucune invitation système n'en dépend** (§5.16 : les invitations/relances sont manuelles, hors site).
  - `household_member` : **une ligne par personne importée**, rattachée à un foyer — `household_id`, `nom_prenom`, `phone` (**normalisé, indexé unique** — un numéro n'appartient qu'à une seule personne ; gère tout indicatif international, pas seulement FR/MA, cf. §6.3 numéros de diaspora), `origine` FR/MA, `langue` (**ajouté 2026-07-27**, valeur **déduite de l'indicatif du téléphone importé** : `+33` → `FR`, `+212` → `AR`, tout autre indicatif ou **ligne sans téléphone** → `FR` par défaut. **Donnée réellement dormante** — confirmé 2026-07-28 : comme il n'existe **aucune invitation générée par le site** (§5.16), il n'y a plus aucun usage, même futur, qui la consommerait ; conservée en base par simplicité de ne pas avoir à la retirer, mais elle ne pilote rien), `import_source` (ligne Excel d'origine). Recherche à l'identification : `SELECT household_id FROM household_member WHERE phone = :saisi`.
  - `rsvp` : **une ligne par foyer** — `household_id`, `email` (**nullable, champ optionnel** — 2026-07-27), `presence` (oui/non/sans réponse), `nb_adultes`, `nb_enfants`, `allergies_bool`, `allergies_texte`, `besoin_hotel` (bool), `horodatage`, `token_modification` (pour le lien email de retour, généré seulement si `email` est renseigné — sinon le foyer reste identifiable par re-saisie de son numéro, §5.11). L'existence d'une ligne pour un foyer est le déclencheur du message « quelqu'un de votre famille a déjà répondu » à la resoumission par un autre numéro du même foyer — pas de champ dédié, une simple vérification avant écriture.
  - `admin_user`, `settings` (code d'accès, hashé, **+ `date_limite_rsvp`** — date nullable, cible « fin août 2026 » (§2 point 4) mais jour exact pas encore fixé).
  - Table `event` de la v1 abandonnée avec le modèle mono-moment ; `guest` de la v1 renommée/reprise en `household_member` avec un rôle différent (identification, pas décompte de présence — le décompte reste déclaratif via `nb_adultes`/`nb_enfants` sur `rsvp`).
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
| **S2 · RSVP** | ~~mi-juillet~~ **🔴 pas commencé** | Import Excel, identification par téléphone, formulaire foyer, persistence, email de confirmation | 2 |
| **S3 · Admin & suivi** | ~~fin juillet~~ **🔴 pas commencé** | Login, CRUD invités, dashboard RSVP, suivi « relancé le » (§5.16), export | 2 |
| **S4 · Guide voyage & finitions** | août | Contenu voyage complet, photos, recette mobile, accessibilité, perfs | 1–2 |
| **📨 Envoi officiel** | **cette semaine (28/07–01/08)** | Invitations envoyées par WhatsApp, à la main (§5.16) | — |
| **Exploitation** | sept.–oct. | Suivi « relancé le » (§5.16), gel du contenu à J−7 | ponctuel |

Marge intégrée : le développement se termine fin août pour un mariage fin octobre.

> **Écart au plan constaté le 2026-07-27** : deux itérations de direction artistique (A → T1 → S3) ont consommé du temps qui n'était pas budgété. Le chantier de migration visuelle (`charte_graphique.md` §13) est à absorber avant de reprendre S2/S3.
>
> **🔴 Alerte constatée le 2026-07-28 — l'ordre des jalons vient de s'inverser.** L'envoi officiel passe de « après S2/S3 » à **cette semaine**, mais **S2 n'a pas une ligne de code écrite** : il n'existe ni table `household`/`household_member`/`rsvp`, ni route d'import, ni identification par téléphone, ni formulaire — seulement les décisions de ce document. Pire : la section RSVP actuellement en ligne affiche *« Le formulaire de confirmation ouvrira prochainement — vous recevrez un email dès qu'il sera disponible »*, un texte qui promet un email alors qu'on a décidé §5.16 qu'aucun email automatique n'existe. Si les invitations partent cette semaine, les invités qui cliquent atterrissent sur une promesse qui ne se réalisera jamais telle qu'écrite.
>
> Trois façons de résorber ça, à trancher — je n'en ai retenu aucune à ta place :
> 1. **Décaler l'envoi** de quelques jours/semaines, le temps qu'un formulaire RSVP minimal (même sans multilingue, même sans les goodies) soit en ligne.
> 2. **Envoyer quand même cette semaine**, mais remplacer le texte de la section RSVP par quelque chose d'honnête et d'actionnable tout de suite (ex. « Répondez-moi directement sur WhatsApp d'ici là, le formulaire arrive bientôt ») — ça découple l'envoi du calendrier de dev, au prix d'un aller-retour manuel de plus pour toi.
> 3. **Construire un RSVP minimal en urgence** avant l'envoi (juste téléphone + présence + nb personnes, sans les goodies ni le multilingue, ajoutés ensuite) — resserre S2 à l'extrême, à ne tenter que si tu as du temps Cowork disponible d'ici la fin de la semaine.
>
> **Contradiction introduite le 2026-07-28** : « Envoi officiel » était calé sur la semaine du 31/08 (« ~7 semaines avant » le mariage) — mais la **date limite de réponse est maintenant fixée à fin août** (§5.18/§6.1). On ne peut pas diffuser les invitations la semaine où les réponses sont censées être closes. Soit l'envoi officiel avance nettement (probablement dans la fenêtre S2/S3, pas après), soit la date limite de réponse glisse en septembre — l'un des deux doit bouger, pas les deux tels quels aujourd'hui.
>
> **Second écart, même jour** : le site passe de « FR uniquement » à **multilingue FR/EN/AR** (§5.14) — décision prise après que ce plan a été bâti sur un site mono-langue. Le contenu à traduire couvre S1 (vitrine), S3 (guide voyage), S2 (RSVP) et S3 (admin/emails) : c'est transversal, pas une tâche isolée. Aucune des sessions Cowork listées ci-dessus n'a été dimensionnée pour ça. À rechiffrer avant de committer une nouvelle date de fin.

---

## 5. Décisions prises

1. **Direction design** : S3 · Sahara & Menthe (2026-07-27). Historique complet : `charte_graphique.md` §14.
2. **Hébergement** : Render.
3. **Domaine** : `mariage-maroc.igolen.com`.
4. **Langue** : ~~français uniquement, pas de RTL~~ (12/06/2026) — **remplacé le 2026-07-27 par le site multilingue FR/EN/AR**, §5.14.
5. **Programme : un seul moment** (2026-07-27) — pas de ventilation événement par événement dans le RSVP.
6. **Identifiant RSVP : numéro de téléphone, import une ligne par personne** (2026-07-27) — l'Excel a une ligne par invité, avec une colonne `famille` libre et optionnelle pour regrouper plusieurs lignes en un seul foyer (le cas courant est le couple, mais rien ne limite à deux). N'importe quel numéro rattaché au foyer l'identifie. Nom/prénom préremplis dessus. Pas de vérification SMS. Champs du formulaire : téléphone, nom/prénom, nb adultes, nb enfants, allergies (Oui/Non + texte), besoin d'hôtel (Oui/Non). Détail §2 point 4.
7. **Photo réelle du Palais Laraki** livrée (2026-07-27) — la section « Le lieu » n'affiche plus Bab Mansour.
8. **Deux goodies RSVP** (2026-07-27) : message de confirmation personnalisable par foyer ; message « quelqu'un de votre famille a déjà répondu » quand un second numéro du même foyer se présente. Détail §2 point 4, champ §3.
9. **Numéros saisis avec indicatif pays dans l'Excel** (2026-07-27) — la normalisation FR/MA (§3) n'a donc pas à le déduire d'`origine` ; elle valide/nettoie un numéro déjà complet (espaces, tirets, format `00`/`+`) plutôt que de reconstruire l'indicatif.
10. **Pas d'email dans l'import** (2026-07-27, « on ne le sait pas ») — il est saisi par le foyer directement dans le formulaire RSVP, stocké sur `rsvp.email`, pas sur `household`. Détail §2 point 4, champ §3.
11. **Formulaire toujours modifiable** (2026-07-27) — re-saisir un numéro déjà répondu récupère et pré-remplit la réponse existante ; le foyer peut la corriger et renvoyer, ce n'est jamais figé en lecture seule. Le message « quelqu'un de votre famille a déjà répondu » (§2 point 4) précède ce pré-remplissage, il ne le bloque pas.
12. **Champ email non obligatoire** (2026-07-27) — un foyer qui ne le renseigne pas ne reçoit ni confirmation ni lien de modification par email, mais reste pleinement identifiable et modifiable par re-saisie de son numéro (§5.11). L'email est un confort, jamais une condition d'accès au formulaire.
13. **Langue déduite du téléphone** (2026-07-27) — champ `household_member.langue`, **calculé automatiquement à l'import depuis l'indicatif** (`+33`→FR, `+212`→AR, sinon FR par défaut, y compris sans téléphone). Pas de saisie manuelle. **Donnée réellement dormante depuis §5.16** — conservée en base sans être retirée, mais aucun mécanisme du site (ni défaut d'affichage, ni invitation, ni relance) ne la consulte.
    > Hypothèse posée sans validation explicite, devenue anecdotique : `+212` (Maroc) déduit `AR`, pas `FR`, alors que le français y est très répandu. Comme ce champ ne pilote plus rien, l'impact d'une correction serait nul — je ne la referai pas remonter en question ouverte.
14. **Site multilingue FR/EN/AR** (2026-07-27) — remplace « français uniquement, pas de RTL » (12/06/2026). Détail technique et comportement du sélecteur : §2 point 6. **Reste ouvert : la charte graphique (§4.4 et au-delà) n'est pas encore mise à jour pour cette décision** — cf. §6.4.
15. **Langue demandée à la porte d'entrée, pas déduite au RSVP** (2026-07-27, corrige §5.14 le jour même — incohérence relevée par le Patron : la déduction par téléphone ne peut pas servir de défaut puisque le téléphone n'est connu qu'après que tout le début de la visite a déjà été rendu en FR). Sélecteur explicite FR/EN/AR sur la porte d'entrée, FR pré-sélectionné, cookie posé avant tout contenu. `household_member.langue` redevient une donnée dormante (§5.13). Détail §2 point 1 et point 6.
16. **Pas d'invitations ni de relances envoyées par le site — tout passe par WhatsApp, à la main** (2026-07-28, corrige la v1 de ce document, qui prévoyait un envoi par email). Ça résout du même coup le problème qu'aucun email n'existe avant qu'un foyer ait répondu : le canal d'invitation ne dépend plus de `rsvp.email`. Suivi minimal côté admin : `household.relance_le`, une date, pré-remplie à aujourd'hui, modifiable — juste pour savoir qui a déjà été recontacté. Détail §2 point 5, champ §3.
17. **Message personnalisé saisi dans la langue supposée du foyer, pas traduit** (2026-07-28) — le Patron connaît ses invités et choisit lui-même la langue d'écriture ; pas de champ par langue, pas de traduction automatique. Limite acceptée : le message peut ne pas correspondre à la langue active choisie par l'invité sur le site. Détail §2 point 4.
18. **Date limite de RSVP : fin août 2026** (2026-07-28) — `settings.date_limite_rsvp`, jour exact encore à fixer, mais le mois est acté. Contrainte utile pour le rechiffrage du planning (§4, écart constaté §6.5) : le formulaire RSVP doit être en ligne et les invitations diffusées suffisamment tôt pour laisser un délai de réponse réel avant cette échéance. Détail §2 point 4, champ §3.
19. **Charte multilingue/RTL : le Patron s'en charge lui-même, juste après** (2026-07-28) — répond à §6.3 (recommandation de repasser en `/da`). Pas de blocage côté DP en attendant.
20. **Photo du hero : on reste comme ça** (2026-07-28) — le Patron ne priorise pas le remplacement de l'asset pour l'instant, malgré l'échec de 2 des 3 seuils du §7.1 de la charte. Répond à §6.1, referme le point sans y donner suite pour le moment.
21. **Pas de validateur de doublons `famille` — contrôle visuel manuel par le Patron** (2026-07-28) — répond à §6.2 : pas de garde-fou automatisé à construire pour S2/S3, le Patron relira l'Excel lui-même avant import.

Le RSVP est maintenant **entièrement spécifié** : identification, champs, goodies, modèle de données. Reste ouvert uniquement ce qui suit.

## 6. Décisions encore attendues du Patron

Tous les points de l'audit du 2026-07-27 ont une réponse (§5.16-21), sauf celui-ci :

1. **Le calendrier (§4) reste à rechiffrer**, mais avec une bonne nouvelle et une contrainte neuve depuis la dernière version de ce document :
   - **Bonne nouvelle** : « Save-the-date en ligne » a en fait été livré — `origin/main` porte déjà `d67b54e` (charte v2.0 S3, format faire-part, hero sans voile, photo du Palais Laraki), poussé en prod sur Render. Ma lecture précédente (« rien n'a été commité ») datait d'avant ce push. Les invités France peuvent réserver leurs vols sur le site tel qu'il est aujourd'hui.
   - **Contrainte neuve** : la date limite de réponse est fixée à **fin août 2026** (§5.18). S2 (RSVP) doit être en ligne, et les invitations diffusées par WhatsApp (§5.16), suffisamment tôt avant cette échéance pour laisser un vrai délai de réponse — pas la veille.
   - Seul le RSVP + admin (S2/S3) restent à rechiffrer sur cette base ; S1 (vitrine) est fait. Effort multilingue (§6 ex-item 4) à inclure dans le même rechiffrage, puisque S2 (formulaire RSVP) en fait partie.
