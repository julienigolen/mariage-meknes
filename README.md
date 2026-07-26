# Site mariage Kenza & Julien — Meknès, 23 octobre 2026

Site invités (FR) protégé par code commun, avec RSVP intégré et admin de la liste d'invités.
Stack : FastAPI + Jinja2 + Tailwind CDN + HTMX + Postgres (patterns repris d'OWP).
Design : direction **T1 · Terre de Meknès** (palette dérivée de la colorimétrie de Bab Mansour, remplace « A · Bleu zellige » depuis le 27/07/2026) — cf. `docs/PROPOSITION_site_mariage_meknes.md` §2.1 bis et §2.2.

## Lancer en local

```bash
pip install -r requirements.txt
cp .env.example .env        # code d'accès dev : meknes2026
uvicorn app.main:app --reload
# http://localhost:8000 → redirige vers /entree
```

En dev : SQLite (`dev.db`), schéma créé automatiquement. En prod : Postgres + Alembic.

## Déployer sur Render

1. Pousser ce repo sur GitHub (repo privé).
2. Render → **New → Blueprint** → sélectionner le repo : `render.yaml` crée le service web (starter) et la base Postgres (basic-256mb).
   ⚠ Ne pas prendre les plans free : la base free **expire après 90 jours** et le web free se met en veille (~50 s de réveil pour un invité).
3. Dashboard du service → Environment → renseigner **ACCESS_CODE** (le code des invitations).
4. Vérifier `https://mariage-zellige.onrender.com/healthz` puis la porte d'entrée.

## Domaine `mariage-maroc.igolen.com`

1. Service Render → Settings → **Custom Domains** → ajouter `mariage-maroc.igolen.com`.
2. Chez le registrar d'`igolen.com`, créer l'enregistrement DNS indiqué par Render :
   `CNAME  mariage-maroc  →  mariage-zellige.onrender.com`
3. Render provisionne le certificat TLS automatiquement (quelques minutes après propagation DNS).

## Sauvegardes

La liste d'invités et les RSVP sont irremplaçables. Le plan basic-256mb inclut des
sauvegardes quotidiennes Render ; faire en plus un `pg_dump` manuel avant tout envoi
d'invitations (External Connection String dans le dashboard de la base).

## Roadmap

- **S0 ✅** socle : porte à code, layout tokens, save-the-date, modèles, Alembic, Render.
- **S1** vitrine : photos Palais Laraki/Meknès, programme détaillé, dress code, FAQ → mise en ligne save-the-date.
- **S2** RSVP : import Excel des foyers, recherche du nom, formulaire, notification email.
- **S3** admin : login, CRUD invités, dashboard RSVP, envoi invitations/relances, export.
- **S4** guide voyage complet + finitions (mobile, accessibilité, perfs).
