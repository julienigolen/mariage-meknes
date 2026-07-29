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


_PLAUSIBLE_PATTERNS = [
    r"\+33\d{9}",    # FR avec indicatif
    r"\+212\d{9}",   # MA avec indicatif
    r"\+1\d{10}",    # US avec indicatif
    r"0\d{9}",       # FR/MA format national (ambigu — couvert par phone_candidates)
    r"[2-9]\d{9}",   # US format national (10 chiffres, ne commence ni par 0 ni par 1)
]


def is_plausible_phone(raw: str) -> bool:
    """Filtre de format pour l'auto-ajout RSVP (§ « invité non répertorié », Patron
    2026-07-28) : un numéro absent de la liste importée n'est proposé à la création
    d'un nouveau foyer que s'il ressemble à un vrai numéro FR/MA/US — pas une
    validation exhaustive (pas de vérification d'opérateur/plage), juste un garde-fou
    contre une saisie au hasard avant de demander un nom.
    """
    cleaned = normalize_phone(raw)
    return any(re.fullmatch(p, cleaned) for p in _PLAUSIBLE_PATTERNS)
