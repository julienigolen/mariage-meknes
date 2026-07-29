"""Crée ou met à jour un compte admin (app/admin_auth.py) — pas d'auto-inscription,
les deux seuls comptes (Kenza & Julien) sont créés à la main via ce script.

Usage :
    python scripts/create_admin.py email@exemple.com
    (mot de passe demandé de façon masquée ; si l'email existe déjà, son mot de passe
    est remplacé — sert aussi de "mot de passe oublié" pour un compte bloqué)
"""
import argparse
import getpass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.admin_auth import hash_password  # noqa: E402
from app.database import Base, SessionLocal, engine  # noqa: E402
from app.models import AdminUser  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Crée ou met à jour un compte admin.")
    parser.add_argument("email")
    args = parser.parse_args()
    email = args.email.lower().strip()

    password = getpass.getpass("Mot de passe : ")
    confirm = getpass.getpass("Confirmer : ")
    if password != confirm:
        print("[ERREUR] Les deux saisies ne correspondent pas.")
        return
    if len(password) < 8:
        print("[ERREUR] Mot de passe trop court (8 caractères minimum).")
        return

    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        user = db.query(AdminUser).filter(AdminUser.email == email).one_or_none()
        if user is None:
            user = AdminUser(email=email, password_hash=hash_password(password))
            db.add(user)
            print(f"[OK] Compte créé : {email}")
        else:
            user.password_hash = hash_password(password)
            print(f"[OK] Mot de passe mis à jour : {email}")
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
