"""Import de la liste d'invités depuis un Excel — cf. docs/projet_mariage-meknes/proposition_produit.md §3.

Une ligne par personne. Colonnes attendues (en-têtes en première ligne, insensibles à la
casse/aux espaces) :

    Nom Prénom  (ou "Nom" + "Prénom" séparés)
    Téléphone   (avec indicatif, déjà complet — §5.9)
    Famille     (optionnel — libellé libre, regroupe plusieurs lignes en un foyer)
    Origine     (optionnel — "fr" ou "ma", défaut "fr")

Regroupement (§2 point 4 de la proposition) : toutes les lignes qui partagent le même
libellé Famille (non vide) forment un foyer. Une ligne sans Famille est son propre foyer.

Langue déduite de l'indicatif (§5.13, dormante pour l'instant) : +33 -> fr, +212 -> ar,
sinon fr par défaut.

[ATTENTION] Pas de détection automatique des libellés Famille proches ("Dupont" vs "Famille
Dupont") — décision Patron (2026-07-28) : contrôle visuel manuel avant import, pas de
validateur construit pour ce MVP. Ce script AFFICHE la liste des libellés Famille
distincts en fin d'exécution pour faciliter cette relecture.

Usage :
    python scripts/import_guests.py chemin/vers/invites.xlsx [--dry-run]
"""
import argparse
import sys
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.models import Household, HouseholdMember  # noqa: E402
from app.phone import normalize_phone  # noqa: E402

HEADER_ALIASES = {
    "nom_prenom": ["nom prenom", "nom prénom", "nom et prenom", "nom et prénom"],
    "nom": ["nom"],
    "prenom": ["prenom", "prénom"],
    "phone": ["telephone", "téléphone", "tel", "téléphone (avec indicatif)"],
    "famille": ["famille"],
    "origine": ["origine"],
}


def _clean(s) -> str:
    return str(s).strip() if s is not None else ""


def _find_columns(headers: list[str]) -> dict[str, int]:
    normalized = [_clean(h).lower() for h in headers]
    found: dict[str, int] = {}
    for field, aliases in HEADER_ALIASES.items():
        for i, h in enumerate(normalized):
            if h in aliases:
                found[field] = i
                break
    return found


def _deduce_langue(phone: str) -> str:
    if phone.startswith("+33"):
        return "fr"
    if phone.startswith("+212"):
        return "ar"
    return "fr"


def main() -> None:
    parser = argparse.ArgumentParser(description="Import invités depuis un Excel (une ligne par personne).")
    parser.add_argument("fichier", help="Chemin du fichier .xlsx")
    parser.add_argument("--dry-run", action="store_true", help="N'écrit rien en base, affiche seulement le résumé.")
    args = parser.parse_args()

    wb = openpyxl.load_workbook(args.fichier, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        print("Fichier vide.")
        return

    headers = list(rows[0])
    cols = _find_columns(headers)

    if "phone" not in cols:
        print(f"[ERREUR] Colonne téléphone introuvable. En-têtes lus : {headers}")
        return
    if "nom_prenom" not in cols and ("nom" not in cols or "prenom" not in cols):
        print(f"[ERREUR] Colonne nom/prénom introuvable (ni 'Nom Prénom', ni 'Nom'+'Prénom'). En-têtes lus : {headers}")
        return

    Base.metadata.create_all(engine)  # no-op si les tables existent déjà (dev SQLite ; en prod, alembic upgrade head avant)
    db = SessionLocal()

    familles: dict[str, list[dict]] = {}
    sans_famille: list[dict] = []
    famille_labels_vues: set[str] = set()
    n_lignes = 0
    erreurs: list[str] = []

    for row_idx, row in enumerate(rows[1:], start=2):
        if row is None or all(c is None for c in row):
            continue
        n_lignes += 1

        if "nom_prenom" in cols:
            nom_prenom = _clean(row[cols["nom_prenom"]])
        else:
            nom_prenom = f"{_clean(row[cols['prenom']])} {_clean(row[cols['nom']])}".strip()

        phone_raw = _clean(row[cols["phone"]])
        famille = _clean(row[cols["famille"]]) if "famille" in cols else ""
        origine = (_clean(row[cols["origine"]]) or "fr").lower() if "origine" in cols else "fr"

        if not nom_prenom or not phone_raw:
            erreurs.append(f"ligne {row_idx} : nom ou téléphone manquant, ignorée")
            continue

        phone = normalize_phone(phone_raw)
        if not phone.startswith("+"):
            erreurs.append(f"ligne {row_idx} ({nom_prenom}) : numéro « {phone_raw} » sans indicatif reconnu (+..), importé tel quel")

        member = {
            "nom_prenom": nom_prenom,
            "phone": phone,
            "origine": origine if origine in ("fr", "ma") else "fr",
            "langue": _deduce_langue(phone),
            "import_source": f"ligne {row_idx}",
        }

        if famille:
            famille_labels_vues.add(famille)
            familles.setdefault(famille, []).append(member)
        else:
            sans_famille.append(member)

    n_foyers = len(familles) + len(sans_famille)
    n_personnes = sum(len(v) for v in familles.values()) + len(sans_famille)

    print(f"Lignes lues : {n_lignes}")
    print(f"Personnes valides : {n_personnes}")
    print(f"Foyers à créer : {n_foyers} ({len(familles)} regroupés par famille, {len(sans_famille)} seuls)")
    if erreurs:
        print(f"\n[ATTENTION]  {len(erreurs)} avertissement(s) :")
        for e in erreurs:
            print(f"   - {e}")

    print(f"\n[FAMILLES] Libellés « famille » distincts ({len(famille_labels_vues)}) — relire avant de valider :")
    for label in sorted(famille_labels_vues):
        print(f"   - {label!r}  ({len(familles[label])} personne(s))")

    if args.dry_run:
        print("\n--dry-run : rien n'a été écrit en base.")
        return

    try:
        for famille_label, members in familles.items():
            household = Household(import_famille_label=famille_label)
            db.add(household)
            db.flush()
            for m in members:
                db.add(HouseholdMember(household_id=household.id, **m))
        for m in sans_famille:
            household = Household(import_famille_label=None)
            db.add(household)
            db.flush()
            db.add(HouseholdMember(household_id=household.id, **m))
        db.commit()
        print(f"\n[OK] Import terminé : {n_foyers} foyers, {n_personnes} personnes.")
    except Exception as exc:
        db.rollback()
        print(f"\n[ERREUR] Import annulé (transaction annulée, rien n'a été écrit) : {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
