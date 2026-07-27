"""Normalisation du numéro de téléphone — identifiant RSVP (charte §5.2, proposition §3).

Numéros déjà saisis avec indicatif à l'import (décision §5.9) : on nettoie un numéro
déjà complet (espaces, tirets, points, parenthèses, préfixe international 00), on ne
reconstruit pas l'indicatif depuis l'origine.
"""
import re


def normalize_phone(raw: str) -> str:
    cleaned = re.sub(r"[\s\-.()]", "", raw.strip())
    if cleaned.startswith("00"):
        cleaned = "+" + cleaned[2:]
    return cleaned
