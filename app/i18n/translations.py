"""Catalogue de traductions — source unique de vérité pour les libellés du site.

Pattern repris d'OWP (owp/i18n/translations.py) : un dict TRANSLATIONS[lang][cle],
accès en template via `texts = TRANSLATIONS[lang]` puis `texts.ma_cle` (Jinja résout
un attribut de dict comme une clé). Clés préfixées par écran/domaine pour éviter les
collisions (gate_*, header_*, hero_*, programme_*, lieu_*, dresscode_*, guide_*, rsvp_*,
footer_*).

Arabe activé le 2026-07-30 (charte_graphique.md §4.4 : FR+EN d'abord — 2026-07-28 —
puis AR dans un second temps, comme prévu). dir="rtl" se déclenche automatiquement
dès que "ar" est dans SUPPORTED_LANGS (app/i18n/context.py) : rien d'autre à changer
côté routes/templates, ils lisent déjà lang dynamiquement.
"""
from typing import Any

SUPPORTED_LANGS = ["fr", "en", "ar"]
DEFAULT_LANG = "fr"

TRANSLATIONS: dict[str, dict[str, Any]] = {
    "fr": {
        "meta_title": "Kenza & Julien — Meknès, 23 octobre 2026",

        # ---- Porte d'entrée ----
        "gate_page_title": "Bienvenue — Kenza & Julien",
        "gate_overline": "Meknès · 23 octobre 2026",
        "gate_intro": "Ce site est réservé à nos invités.",
        "gate_code_label": "Code d'invitation ou numéro de téléphone",
        "gate_code_placeholder": "Le code sur votre invitation, ou votre numéro",
        "gate_error": "Ce code ou ce numéro ne correspond à rien — vérifiez la saisie ou écrivez-nous.",
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
        "hero_countdown_unit": "jours",
        "hero_cta": "Confirmer ma présence",
        "hero_rsvp_confirmed": "Votre présence est confirmée",
        "hero_rsvp_declined": "Vous avez indiqué ne pas pouvoir venir",
        "hero_rsvp_edit": "Modifier ma réponse",

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
        "guide_intro": "Pour nos invités qui viennent de l'étranger — le guide complet (hébergements "
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
        "gate_code_label": "Invitation code or phone number",
        "gate_code_placeholder": "The code on your invitation, or your phone number",
        "gate_error": "This code or number doesn't match anything — please check it or get in touch.",
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
        "hero_countdown_unit": "days",
        "hero_cta": "Confirm my attendance",
        "hero_rsvp_confirmed": "Your attendance is confirmed",
        "hero_rsvp_declined": "You've let us know you can't make it",
        "hero_rsvp_edit": "Update my response",

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
        "guide_intro": "For our guests travelling from abroad — the full guide (recommended places to "
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
    # Arabe standard (fusha), pas darija — un faire-part formel s'écrit en fusha même
    # au Maroc (2026-07-30, décision Patron via "go" sur la recommandation DA).
    # Chiffres restent en latin (convention OWP reconduite). "Kenza & Julien" reste en
    # LATIN partout, y compris ici : le lockup (charte §1.1) est câblé en dur en latin
    # dans les templates (identité typographique, pas du contenu traduisible) — un
    # premier jet avait translittéré les prénoms dans ces deux clés de titre, repéré
    # incohérent à la vérification visuelle (le lockup affiché restait en latin pendant
    # que l'onglet du navigateur passait en arabe). Corrigé : les prénoms ne sont
    # transcrits nulle part, `كنزة`/`جوليان` n'auraient été qu'une graphie parmi
    # d'autres possibles, sans autorité pour la choisir. "Palais Laraki" -> قصر العراقي :
    # nom arabe réel relevé sur l'enseigne du lieu (photo intégrée §7.4 de la charte),
    # pas une translittération de "Laraki" — à confirmer que c'est bien la graphie
    # qu'utilisent les mariés eux-mêmes, l'enseigne d'un lieu recevant des événements
    # peut différer du nom d'état civil.
    # ⚠️ Premier jet — relecture native indispensable avant mise en ligne (registre,
    # tournures figées, nuances) : c'est un faire-part, pas une notice technique.
    "ar": {
        "meta_title": "Kenza & Julien — مكناس، 23 أكتوبر 2026",

        # ---- Porte d'entrée ----
        "gate_page_title": "أهلاً بكم — Kenza & Julien",
        "gate_overline": "مكناس · 23 أكتوبر 2026",
        "gate_intro": "هذا الموقع مخصص لضيوفنا فقط.",
        "gate_code_label": "رمز الدعوة أو رقم الهاتف",
        "gate_code_placeholder": "الرمز الموجود في دعوتكم، أو رقم هاتفكم",
        "gate_error": "هذا الرمز أو الرقم غير صحيح — يرجى التحقق من الإدخال أو التواصل معنا.",
        "gate_submit": "دخول",

        # ---- Header / footer ----
        "header_subtitle": "مكناس · 23 أكتوبر 2026",
        "nav_programme": "البرنامج",
        "nav_venir": "القدوم إلى مكناس",
        "nav_rsvp": "تأكيد الحضور",
        "footer_date": "الجمعة 23 أكتوبر 2026",
        "footer_lieu": "قصر العراقي، مكناس",

        # ---- Hero ----
        # Basmala à la place d'une traduction de "Save the date" (feedback Patron
        # 2026-07-30) : ouverture traditionnelle des faire-part de mariage en contexte
        # musulman/arabe. Rendue en Cairo (chargée, §3.1/§12) — PAS une image de
        # calligraphie ornementale à ce stade : si tu veux ce traitement (plus proche
        # d'un logo qu'un texte), c'est un chantier DA à part (police calligraphique
        # dédiée ou asset image), pas juste une clé de traduction. Dis-le si tu veux
        # que j'enchaîne dessus.
        "hero_overline": "بسم الله الرحمن الرحيم",
        "hero_intro": "يسعدنا أن ندعوكم إلى المغرب للاحتفال بزفافنا، محاطين بعائلتينا وثقافتينا.",
        "hero_date_label": "التاريخ",
        "hero_date_value": "الجمعة 23 أكتوبر 2026",
        "hero_lieu_label": "المكان",
        "hero_lieu_value": "قصر العراقي، مكناس",
        "hero_countdown_label": "العد التنازلي",
        # "يوماً" (accusatif singulier après un cardinal 11-99, grammaire arabe standard)
        # — plus le préfixe latin bricolé d'avant : ce mot est maintenant HORS du <bdi>
        # isolé (home.html), donc il s'affiche normalement, à droite du chiffre isolé.
        "hero_countdown_unit": "يوماً",
        "hero_cta": "تأكيد حضوري",
        "hero_rsvp_confirmed": "تم تأكيد حضوركم",
        "hero_rsvp_declined": "لقد أخبرتمونا أنه لن يتسنى لكم الحضور",
        "hero_rsvp_edit": "تعديل إجابتي",

        # ---- Programme ----
        "programme_overline": "البرنامج",
        "programme_title": "أمسية في قصر العراقي",
        "programme_item1_time": "19:00",
        "programme_item1_title": "استقبال الضيوف",
        "programme_item1_desc": "شاي وحلويات ولقاءات في صالات القصر.",
        "programme_item2_time": "20:30",
        "programme_item2_title": "دخول العروسين",
        "programme_item2_desc": "اللحظة التي تبدأ فيها الحفلة فعلاً.",
        "programme_item3_time": "22:00",
        "programme_item3_title": "العشاء",
        "programme_item3_desc": "عشاء بنكهات مغربية، يُقدَّم على المائدة.",
        "programme_item4_time": "حتى الصباح",
        "programme_item4_title": "الحفلة",
        "programme_item4_desc": "نرقص حتى آخر الليل.",

        # ---- Le lieu ----
        "lieu_overline": "المكان",
        "lieu_title": "قصر العراقي، مكناس",
        "lieu_img_alt": "مدخل قصر العراقي مضاءً ليلاً، بوابة منحوتة وشمعدانات",
        "lieu_intro": "تقام السهرة بأكملها في المكان نفسه — لا حاجة للتنقل بمجرد وصولكم.",
        "lieu_maps_cta": "عرض على خرائط جوجل",

        # ---- Dress code ----
        "dresscode_overline": "قواعد اللباس",
        "dresscode_title": "أناقة على طريقتكم الخاصة",
        "dresscode_text": "لباس سهرة أنيق. القفطان وفساتين السهرة والبدلات كلها مُرحَّب بها — "
                           "البسوا ما يشرّفكم ويسعدكم.",

        # ---- Guide voyage ----
        "guide_overline": "القدوم إلى مكناس",
        "guide_title": "تحضير رحلتكم",
        "guide_intro": "لضيوفنا القادمين من الخارج — الدليل الكامل (أماكن إقامة موصى بها، "
                        "عناوين مفيدة) سيُنشر قريباً.",
        "guide_avion_title": "بالطائرة",
        "guide_avion_text": "أقرب مطار هو <strong class=\"text-encre\">مطار فاس - سايس (FEZ)</strong>، "
                             "على بعد حوالي 45 دقيقة بالسيارة من مكناس — رحلات مباشرة من باريس وعدة "
                             "مدن فرنسية. بدائل أخرى: الرباط (حوالي ساعة ونصف) أو الدار البيضاء (حوالي "
                             "ساعتين ونصف)، مع إمكانية الربط بالقطار. <strong class=\"text-encre\">احجزوا "
                             "مبكراً لعطلة نهاية أسبوع 23 أكتوبر.</strong>",
        "guide_loger_title": "الإقامة",
        "guide_loger_text": "ستُنشر هنا قريباً جداً قائمة بالفنادق الموصى بها.",
        "guide_savoir_title": "معلومات مفيدة",
        "guide_savoir_text": "في أواخر أكتوبر بمكناس: أيام معتدلة (حوالي 24&nbsp;°C) وأمسيات باردة "
                              "نسبياً (حوالي 12&nbsp;°C) — يُنصح بإحضار سترة أو شال. العملة: الدرهم "
                              "المغربي (MAD)، السحب سهل محلياً، والدفع نقداً شائع. اللغة الفرنسية "
                              "مُتحدَّث بها على نطاق واسع.",

        # ---- RSVP ----
        "rsvp_overline": "تأكيد الحضور",
        "rsvp_title": "تأكيد حضوركم",
        "rsvp_intro": "يرجى الرد قبل نهاية أغسطس 2026.",
        "rsvp_phone_label": "رقم الهاتف",
        "rsvp_phone_placeholder": "الرقم المستخدم في دعوتكم",
        "rsvp_phone_submit": "متابعة",
        "rsvp_phone_notfound": "هذا الرقم غير مرتبط بأي دعوة — يرجى التحقق منه أو التواصل معنا "
                                "مباشرة.",
        "rsvp_greeting_prefix": "مرحباً",
        "rsvp_presence_label": "هل ستكونون حاضرين؟",
        "rsvp_presence_yes": "نعم، بكل سرور",
        "rsvp_presence_no": "لا، لن أتمكن من الحضور",
        "rsvp_nb_adultes_label": "عدد البالغين",
        "rsvp_nb_enfants_label": "عدد الأطفال",
        "rsvp_allergies_label": "هل لديكم حساسية أو نظام غذائي خاص؟",
        "rsvp_allergies_yes": "نعم",
        "rsvp_allergies_no": "لا",
        "rsvp_allergies_detail_placeholder": "يرجى التوضيح هنا",
        "rsvp_hotel_label": "هل ترغبون في حجز فندق؟",
        "rsvp_hotel_yes": "نعم",
        "rsvp_hotel_no": "لا",
        "rsvp_submit": "تأكيد إجابتي",
        "rsvp_success": "شكراً لكم! تم تسجيل إجابتكم بنجاح.",
        "rsvp_edit_note": "يمكنكم تعديل إجابتكم في أي وقت بإعادة إدخال رقم هاتفكم.",
    },
}


def get_texts(lang: str) -> dict[str, Any]:
    """Retourne le dict de textes pour `lang`, replié sur DEFAULT_LANG si inconnue/absente."""
    return TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANG])
