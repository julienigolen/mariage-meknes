"""Normalisation du numéro de téléphone — identifiant RSVP (charte §5.2, proposition §3).

Numéros déjà saisis avec indicatif à l'import (décision §5.9) : on nettoie un numéro
déjà complet (espaces, tirets, points, parenthèses, préfixe international 00), on ne
reconstruit pas l'indicatif depuis l'origine.
"""
import re
import unicodedata


def normalize_phone(raw: str) -> str:
    # Retire d'abord les caractères de contrôle/formatage INVISIBLES (marques
    # bidirectionnelles type U+202C, espaces de largeur nulle, BOM...) -- artefact
    # fréquent d'un copier-coller depuis WhatsApp ou une autre app qui enveloppe un
    # numéro pour son affichage RTL/LTR (Patron 2026-08-01 : "+33616095740" suivi d'un
    # POP DIRECTIONAL FORMATTING invisible à l'oeil mais stocké tel quel -- unicité et
    # comparaisons faussées en aval sans que rien ne le laisse deviner à l'écran).
    raw = "".join(ch for ch in raw if unicodedata.category(ch) not in ("Cf", "Cc"))
    cleaned = re.sub(r"[\s\-.()]", "", raw.strip())
    if cleaned.startswith("00"):
        cleaned = "+" + cleaned[2:]
    return cleaned


def phone_candidates(raw: str) -> list[str]:
    """Formes plausibles d'un numéro saisi SANS indicatif, pour la RECHERCHE
    (gate/RSVP) — pas pour le stockage, où l'indicatif est toujours connu (§5.9).

    Un format national à 10 chiffres commençant par 0 (« 06 55 44 33 22 ») est
    ambigu entre FR et MA : les deux pays partagent ce format. Plutôt que de
    deviner, on propose les deux candidats +33/+212 et on matche sur n'importe
    lequel des deux (feedback Patron 2026-07-29 : « 06 55443322 », « +33
    655443322 » et « 0033655443322 » doivent être reconnus comme le même numéro).
    """
    cleaned = normalize_phone(raw)
    candidates = [cleaned]
    if re.fullmatch(r"0\d{9}", cleaned):
        rest = cleaned[1:]
        candidates.append("+33" + rest)
        candidates.append("+212" + rest)
    return candidates
