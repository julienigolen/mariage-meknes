"""Catalogue de traductions — source unique de vérité pour les libellés du site.

Pattern repris d'OWP (owp/i18n/translations.py) : un dict TRANSLATIONS[lang][cle],
accès en template via `texts = TRANSLATIONS[lang]` puis `texts.ma_cle` (Jinja résout
un attribut de dict comme une clé). Clés préfixées par écran/domaine pour éviter les
collisions (gate_*, header_*, hero_*, programme_*, lieu_*, dresscode_*, guide_*, rsvp_*,
footer_*).

L'arabe n'est pas encore dans ce catalogue (charte_graphique.md §4.4 : FR+EN d'abord,
AR suit dans un second temps — décision Patron 2026-07-28). SUPPORTED_LANGS ne liste
donc que fr/en pour l'instant ; ajouter "ar" ici quand son tour vient, sans toucher au
reste du code (routes/templates lisent déjà lang dynamiquement).
"""
from typing import Any

SUPPORTED_LANGS = ["fr", "en"]
DEFAULT_LANG = "fr"

TRANSLATIONS: dict[str, dict[str, Any]] = {
    "fr": {
        "meta_title": "Kenza & Julien — Meknès, 23 octobre 2026",

        # ---- Porte d'entrée ----
        "gate_page_title": "Bienvenue — Kenza & Julien",
        "gate_overline": "Meknès · 23 octobre 2026",
        "gate_intro": "Ce site est réservé à nos invités.",
        "gate_code_label": "Code d'invitation",
        "gate_code_placeholder": "Le code figure sur votre invitation",
        "gate_error": "Ce code ne semble pas le bon — vérifiez votre invitation ou écrivez-nous.",
        "gate_submit": "Entrer",

        # ---- Header / footer ----
        "header_subtitle": "Meknès · 23 octobre 2026",
        "nav_programme": "Programme",
        "nav_venir": "Venir à Meknès",
        "nav_rsvp": "RSVP",
        "footer_date": "vendredi 23 octobre 2026",
        "footer_lieu": "Palais Laraki, Meknès",

        # ---- Hero ----
        "hero_overline": "Save the date",
        "hero_intro": "Nous avons la joie de vous convier au Maroc pour célébrer notre mariage, "
                       "entourés de nos deux familles et de nos deux cultures.",
        "hero_date_label": "Date",
        "hero_date_value": "Vendredi 23 octobre 2026",
        "hero_lieu_label": "Lieu",
        "hero_lieu_value": "Palais Laraki, Meknès",
        "hero_countdown_label": "Compte à rebours",
        "hero_countdown_prefix": "J−",
        "hero_cta": "Confirmer ma présence",

        # ---- Programme ----
        "programme_overline": "Programme",
        "programme_title": "Une soirée au Palais Laraki",
        "programme_item1_time": "19h00",
        "programme_item1_title": "Accueil des invités",
        "programme_item1_desc": "Thé, pâtisseries et retrouvailles dans les salons du palais.",
        "programme_item2_time": "20h30",
        "programme_item2_title": "Entrée des mariés",
        "programme_item2_desc": "Le moment où la fête commence vraiment.",
        "programme_item3_time": "22h00",
        "programme_item3_title": "Dîner",
        "programme_item3_desc": "Un dîner aux saveurs marocaines, servi à table.",
        "programme_item4_time": "Jusqu’au petit matin",
        "programme_item4_title": "La fête",
        "programme_item4_desc": "On danse jusqu'au bout de la nuit.",

        # ---- Le lieu ----
        "lieu_overline": "Le lieu",
        "lieu_title": "Palais Laraki, Meknès",
        "lieu_img_alt": "L'entrée du Palais Laraki illuminée le soir, portail sculpté et candélabres",
        "lieu_intro": "Toute la soirée se déroule au même endroit — aucun déplacement à prévoir une fois sur place.",
        "lieu_maps_cta": "Voir sur Google Maps",

        # ---- Dress code ----
        "dresscode_overline": "Dress code",
        "dresscode_title": "Élégant, à votre façon",
        "dresscode_text": "Tenue de soirée élégante. Caftans, robes de soirées, costumes, sont les bienvenus, "
                           "portez ce qui vous fait honneur et plaisir.",

        # ---- Guide voyage ----
        "guide_overline": "Venir à Meknès",
        "guide_title": "Préparer votre voyage",
        "guide_intro": "Pour nos invités qui viennent de France — le guide complet (hébergements "
                        "recommandés, bonnes adresses) arrive bientôt.",
        "guide_avion_title": "En avion",
        "guide_avion_text": "L'aéroport le plus proche est <strong class=\"text-encre\">Fès-Saïss (FEZ)</strong>, "
                             "à environ 45 minutes de route de Meknès — vols directs depuis Paris et plusieurs "
                             "villes françaises. Alternatives : Rabat (~1h30) ou Casablanca (~2h30), avec liaison "
                             "possible en train. <strong class=\"text-encre\">Réservez tôt pour le week-end du "
                             "23 octobre.</strong>",
        "guide_loger_title": "Se loger",
        "guide_loger_text": "Une sélection d'hôtels recommandés sera publiée ici très prochainement.",
        "guide_savoir_title": "Bon à savoir",
        "guide_savoir_text": "Fin octobre à Meknès : journées douces (~24&nbsp;°C), soirées fraîches "
                              "(~12&nbsp;°C) — prévoyez une veste ou un châle. Monnaie : le dirham (MAD), "
                              "retraits faciles sur place, paiement en espèces fréquent. Le français est très "
                              "largement parlé.",

        # ---- RSVP ----
        "rsvp_overline": "RSVP",
        "rsvp_title": "Confirmer votre présence",
        "rsvp_intro": "Répondez avant fin août 2026.",
        "rsvp_phone_label": "Numéro de téléphone",
        "rsvp_phone_placeholder": "Le numéro utilisé pour votre invitation",
        "rsvp_phone_submit": "Continuer",
        "rsvp_phone_notfound": "Ce numéro ne correspond à aucune invitation — vérifiez la saisie ou "
                                "contactez-nous directement.",
        "rsvp_greeting_prefix": "Bonjour",
        "rsvp_presence_label": "Serez-vous présent(e) ?",
        "rsvp_presence_yes": "Oui, avec plaisir",
        "rsvp_presence_no": "Non, je ne pourrai pas venir",
        "rsvp_nb_adultes_label": "Nombre d'adultes",
        "rsvp_nb_enfants_label": "Nombre d'enfants",
        "rsvp_allergies_label": "Avez-vous des allergies ou régimes alimentaires ?",
        "rsvp_allergies_yes": "Oui",
        "rsvp_allergies_no": "Non",
        "rsvp_allergies_detail_placeholder": "Précisez ici",
        "rsvp_hotel_label": "Souhaitez-vous réserver un hôtel ?",
        "rsvp_hotel_yes": "Oui",
        "rsvp_hotel_no": "Non",
        "rsvp_submit": "Confirmer ma réponse",
        "rsvp_success": "Merci ! Votre réponse a bien été enregistrée.",
        "rsvp_edit_note": "Vous pouvez modifier votre réponse à tout moment en resaisissant votre numéro.",
    },
    "en": {
        "meta_title": "Kenza & Julien — Meknès, October 23, 2026",

        # ---- Gate ----
        "gate_page_title": "Welcome — Kenza & Julien",
        "gate_overline": "Meknès · October 23, 2026",
        "gate_intro": "This site is reserved for our guests.",
        "gate_code_label": "Invitation code",
        "gate_code_placeholder": "The code is on your invitation",
        "gate_error": "This code doesn't seem right — please check your invitation or get in touch.",
        "gate_submit": "Enter",

        # ---- Header / footer ----
        "header_subtitle": "Meknès · October 23, 2026",
        "nav_programme": "Programme",
        "nav_venir": "Getting to Meknès",
        "nav_rsvp": "RSVP",
        "footer_date": "Friday, October 23, 2026",
        "footer_lieu": "Palais Laraki, Meknès",

        # ---- Hero ----
        "hero_overline": "Save the date",
        "hero_intro": "We're delighted to invite you to Morocco to celebrate our wedding, "
                       "surrounded by our two families and our two cultures.",
        "hero_date_label": "Date",
        "hero_date_value": "Friday, October 23, 2026",
        "hero_lieu_label": "Venue",
        "hero_lieu_value": "Palais Laraki, Meknès",
        "hero_countdown_label": "Countdown",
        "hero_countdown_prefix": "D−",
        "hero_cta": "Confirm my attendance",

        # ---- Programme ----
        "programme_overline": "Programme",
        "programme_title": "An evening at Palais Laraki",
        "programme_item1_time": "7:00 PM",
        "programme_item1_title": "Guest arrival",
        "programme_item1_desc": "Tea, pastries, and reunions in the palace's salons.",
        "programme_item2_time": "8:30 PM",
        "programme_item2_title": "Entrance of the newlyweds",
        "programme_item2_desc": "The moment the celebration truly begins.",
        "programme_item3_time": "10:00 PM",
        "programme_item3_title": "Dinner",
        "programme_item3_desc": "A Moroccan-inspired dinner, served at the table.",
        "programme_item4_time": "Until dawn",
        "programme_item4_title": "The celebration",
        "programme_item4_desc": "We dance the night away.",

        # ---- The venue ----
        "lieu_overline": "The venue",
        "lieu_title": "Palais Laraki, Meknès",
        "lieu_img_alt": "The illuminated entrance of Palais Laraki at night, carved portal and candelabra",
        "lieu_intro": "The whole evening takes place in one location — no need to travel once you've arrived.",
        "lieu_maps_cta": "View on Google Maps",

        # ---- Dress code ----
        "dresscode_overline": "Dress code",
        "dresscode_title": "Elegant, your way",
        "dresscode_text": "Elegant evening attire. Caftans, evening gowns, and suits are all welcome — "
                           "wear what makes you feel proud and joyful.",

        # ---- Travel guide ----
        "guide_overline": "Getting to Meknès",
        "guide_title": "Planning your trip",
        "guide_intro": "For our guests travelling from France — the full guide (recommended places to "
                        "stay, good addresses) is coming soon.",
        "guide_avion_title": "By plane",
        "guide_avion_text": "The closest airport is <strong class=\"text-encre\">Fès-Saïss (FEZ)</strong>, "
                             "about 45 minutes from Meknès by road — direct flights from Paris and several "
                             "French cities. Alternatives: Rabat (~1h30) or Casablanca (~2h30), with train "
                             "connections available. <strong class=\"text-encre\">Book early for the "
                             "October 23 weekend.</strong>",
        "guide_loger_title": "Where to stay",
        "guide_loger_text": "A selection of recommended hotels will be published here very soon.",
        "guide_savoir_title": "Good to know",
        "guide_savoir_text": "Late October in Meknès: mild days (~24&nbsp;°C), cool evenings (~12&nbsp;°C) — "
                              "bring a jacket or shawl. Currency: the dirham (MAD), easy to withdraw locally, "
                              "cash is widely used. French is very widely spoken.",

        # ---- RSVP ----
        "rsvp_overline": "RSVP",
        "rsvp_title": "Confirm your attendance",
        "rsvp_intro": "Please respond by the end of August 2026.",
        "rsvp_phone_label": "Phone number",
        "rsvp_phone_placeholder": "The number used for your invitation",
        "rsvp_phone_submit": "Continue",
        "rsvp_phone_notfound": "This number doesn't match any invitation — please check it or contact us "
                                "directly.",
        "rsvp_greeting_prefix": "Hello",
        "rsvp_presence_label": "Will you be attending?",
        "rsvp_presence_yes": "Yes, with pleasure",
        "rsvp_presence_no": "No, I won't be able to make it",
        "rsvp_nb_adultes_label": "Number of adults",
        "rsvp_nb_enfants_label": "Number of children",
        "rsvp_allergies_label": "Do you have any allergies or dietary requirements?",
        "rsvp_allergies_yes": "Yes",
        "rsvp_allergies_no": "No",
        "rsvp_allergies_detail_placeholder": "Please specify",
        "rsvp_hotel_label": "Would you like to book a hotel?",
        "rsvp_hotel_yes": "Yes",
        "rsvp_hotel_no": "No",
        "rsvp_submit": "Confirm my response",
        "rsvp_success": "Thank you! Your response has been recorded.",
        "rsvp_edit_note": "You can update your response at any time by re-entering your phone number.",
    },
}


def get_texts(lang: str) -> dict[str, Any]:
    """Retourne le dict de textes pour `lang`, replié sur DEFAULT_LANG si inconnue/absente."""
    return TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANG])
