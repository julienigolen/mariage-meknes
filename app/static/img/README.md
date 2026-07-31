# Photos attendues (libres de droits ou personnelles)

Statut : `hero` et `lieu` livrés **en WebP** mais **`hero` est à remplacer** — voir ci-dessous.
Reste optionnel : `couple.jpg`.

> ⚠️ **WebP uniquement, pas d'AVIF** (charte §7.3). Les AVIF de ce projet se décodaient plus
> sombres que leur jumeau WebP dans le navigateur (écart moyen 2,7 sur `hero`, 8,7 sur `lieu`) :
> selon le support AVIF de son navigateur, un invité ne voyait pas les mêmes couleurs.
> Les trois fichiers `.avif` ont été supprimés le 2026-07-27. Ne pas en régénérer sans
> vérifier l'égalité de décodage **dans le navigateur**.

| Fichier | Format | Sujet (direction artistique) |
|---|---|---|
| `hero.webp` | **1802×976** (ratio 1,85), **fond transparent** | Bab Mansour — sujet détouré, ancré en bas du hero, **à fleur des bords du carton**. Il se pose sur le dégradé `bg-hero-sable`, d'où l'exigence de détourage. **Aucun texte n'est posé dessus** (charte §5.3).<br>⚠️ **Ne pas rogner le haut** : une version 1920×863 avait retiré 12 % en haut — donc les créneaux des deux tours — pour compenser le `object-cover` de la v1, qui n'existe plus. La façade se voit **entière, créneaux compris**.<br>⚠️ **Rogner les côtés jusqu'au sujet** : la version 1920×980 gardait 57px de transparent à gauche et 61px à droite, visibles à l'écran comme une bande de sable entre la façade et le filet doré. Procédure de mesure : charte §7.2. |
| `lieu.webp` | **1536×768** (2:1), rectangle plein | **Palais Laraki** — l'entrée illuminée le soir. Livrée le 2026-07-27, elle remplace un Bab Mansour détouré qui n'était pas le lieu du mariage. Nocturne réétalonnée : c'est l'**exception unique** de la charte §7.4 (le mariage est nocturne). Affichée `rounded-lg` + ombre `md` — l'ombre est légitime, elle suit le cadre.<br>Mesures après retouche : luminance **69,9 %**, ocre **86,0 %**, violet résiduel **0,1 %** — les trois seuils du §7.1 passent (la photo brute en ratait deux : 48,4 % et 29,1 %).<br>⚠️ Toute nouvelle photo du lieu suit la **méthode §7.4** : désaturer la plage colorée parasite, **ne pas la faire tourner** (franges et halos garantis). |
| `couple.webp` | 800×600 (4:3) | Vous deux (photo perso). Pas encore référencée dans les templates. |
| `basmala_verset.webp` | **1714×550** (ratio 3,12), **fond transparent** | Calligraphie de tête du hero, **toutes langues** (Patron, 2026-07-31) : Basmala + verset Ar-Roum 30:21 + « صدق الله العظيم ». Détourée du fond crème d'origine (sinon plaque opaque sur le dégradé `hero-sable`) et **filigrane ✦ du générateur effacé** (zone 65×65 px en bas à droite). Trait `#1F492C` : **7,6:1 minimum** sur le dégradé, AAA.<br>⚠️ **Affichage large obligatoire** (`max-w-[560px]` mini) : composition sur une seule ligne, la ligne du verset devient illisible en dessous. Une version qui devrait tenir en étroit doit être **recomposée sur plusieurs lignes**, pas réduite. |

## 🔴 `hero.webp` — à remplacer avant mise en ligne

L'asset actuel échoue à deux des trois seuils photo de la charte (§7.1), mesurés sur ses pixels opaques :

| Critère | Seuil | Mesure de l'asset actuel |
|---|---|---|
| Luminance moyenne (V) | ≥ 65 % | **50 %** ❌ |
| Part ocre / or (teinte 20–50°) | ≥ 50 % | 73,6 % ✅ |
| Verts + bleus à saturation > 25 % | ≥ 2 % du cadre | **0,09 %** ❌ |

Son zellige « vert » mesure `#888777` et sa frise « bleue » `#6F655C` — ce sont des gris. La photo paraît patrimoniale là où le site doit vendre le soleil du Maroc. **Fournir la photo avec ciel, parvis clair et porte dorée, en pleine résolution** ; le DA la mesure et la détoure avant intégration.

## ⚠️ Deux fichiers orphelins (2026-07-31) — validation Patron avant suppression

Depuis que `basmala_verset.webp` ouvre le hero dans toutes les langues, ces deux assets ne
sont **plus référencés par aucun template** (vérifié par `grep` sur `app/`) :

| Asset | Pourquoi | Statut |
|---|---|---|
| `basmala.webp` | Sa Basmala est la première ligne du bandeau de tête. | Retirée du hero arabe le 2026-07-31. Fichier conservé. |
| `verse.webp` | Son verset (Ar-Roum 30:21) est **le même** que celui du bandeau : l'invité francophone le lisait deux fois sur la même page. | Section de clôture retirée le 2026-07-31 (Patron). Fichier conservé. |

Les deux fichiers restent sur disque tant que le Patron n'a pas validé leur suppression
(constitution : pas de suppression de fichier sans accord).

## Critères de choix (charte §7)

Lumière franche de plein jour, tons chauds, sable dominant, matières (zellige, bois, cuivre).
⛔ À éviter : clair-obscur, contre-jour, nocturne, HDR saturé, filtres froids, foules,
clichés mariage (alliances, colombes, cœurs), imagerie orientaliste.

Sources libres de droits (licence permettant l'usage sans attribution) :
- https://unsplash.com/s/photos/meknes
- https://unsplash.com/s/photos/morocco-palace
- https://www.pexels.com/search/meknes/
- https://www.pexels.com/search/moroccan%20architecture/
