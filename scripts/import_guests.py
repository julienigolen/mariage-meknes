"""Import de la liste d'invités depuis un Excel — cf. docs/projet_mariage-meknes/proposition_produit.md §3.

Logique de parsing/écriture dans app/services/import_guests.py (2026-07-28, extraite pour
être partagée avec l'upload web /admin/import ; réalignée le 2026-07-29 sur le format
« une ligne par foyer » de la table admin — invité principal/secondaire). Ce script reste
la façade CLI.

Usage :
    python scripts/import_guests.py chemin/vers/invites.xlsx [--dry-run]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.services.import_guests import existing_phones, parse_workbook, write_import  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Import invités depuis un Excel (une ligne par foyer).")
    parser.add_argument("fichier", help="Chemin du fichier .xlsx")
    parser.add_argument("--dry-run", action="store_true", help="N'écrit rien en base, affiche seulement le résumé.")
    args = parser.parse_args()

    Base.metadata.create_all(engine)  # no-op si les tables existent déjà (dev SQLite ; en prod, alembic upgrade head avant)
    db = SessionLocal()

    with open(args.fichier, "rb") as f:
        result = parse_workbook(f, existing_phones(db))

    if result.header_error:
        print(f"[ERREUR] {result.header_error}")
        db.close()
        return

    print(f"Lignes lues : {result.n_lignes}")
    print(f"Foyers valides : {result.n_foyers}")
    print(f"Personnes valides : {result.n_personnes}")
    if result.erreurs:
        print(f"\n[ATTENTION]  {len(result.erreurs)} avertissement(s) :")
        for e in result.erreurs:
            print(f"   - {e}")
    if result.doublons:
        print(f"\n[DOUBLONS]  {len(result.doublons)} numéro(s) déjà connu(s), ignoré(s) :")
        for d in result.doublons:
            print(f"   - {d}")

    if args.dry_run:
        print("\n--dry-run : rien n'a été écrit en base.")
        db.close()
        return

    try:
        write_import(db, result)
        print(f"\n[OK] Import terminé : {result.n_foyers} foyers, {result.n_personnes} personnes.")
    except Exception as exc:
        db.rollback()
        print(f"\n[ERREUR] Import annulé (transaction annulée, rien n'a été écrit) : {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
