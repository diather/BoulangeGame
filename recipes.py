#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TOUS_INGREDIENTS = [
    "farine",
    "sucre",
    "beurre",
    "œuf",
    "lait",
    "levure",
    "eau",
    "sel",
    "chocolat",
    "miel",
]

RECETTES = {
    "pain": {
        "nom": "Pain",
        "ingredients_requis": ["farine", "eau", "sel", "levure"],
        "temperature_ideale": 220,
        "tolerance_temp": 10,
        "temps_ideal": 25,
        "tolerance_temps": 5,
        "images": {
            "base": "pain.png",
            "reussie": "pain_reussi.png",
            "cru": "pain_cru.png",
            "brule": "pain_brule.png",
        },
    },
    "croissant": {
        "nom": "Croissant",
        "ingredients_requis": ["farine", "beurre", "levure", "sucre", "lait", "sel"],
        "temperature_ideale": 200,
        "tolerance_temp": 10,
        "temps_ideal": 20,
        "tolerance_temps": 4,
        "images": {
            "base": "croissant.png",
            "reussie": "croissant_reussi.png",
            "cru": "croissant_cru.png",
            "brule": "croissant_brule.png",
        },
    },
    "gateau": {
        "nom": "Gâteau",
        "ingredients_requis": ["farine", "sucre", "œuf", "lait", "beurre"],
        "temperature_ideale": 180,
        "tolerance_temp": 10,
        "temps_ideal": 35,
        "tolerance_temps": 5,
        "images": {
            "base": "gateau.png",
            "reussie": "gateau_reussi.png",
            "cru": "gateau_cru.png",
            "brule": "gateau_brule.png",
        },
    },
}


def valider_ingredients(recette_nom, ingredients_selectionnes):
    """Vérifie si l’ensemble des ingrédients sélectionnés correspond exactement aux requis."""
    req = set(RECETTES[recette_nom]["ingredients_requis"])
    return set(ingredients_selectionnes) == req


def obtenir_aide_ingredients(recette_nom, ingredients_selectionnes=None):
    """
    Retourne une LISTE des ingrédients corrects pour la recette.
    Le 2e argument est optionnel pour être compatible avec les anciens appels.
    """
    requis = RECETTES[recette_nom]["ingredients_requis"]
    # On renvoie simplement la liste triée des bons ingrédients
    return sorted(requis)




def valider_cuisson(recette_nom, temperature, temps):
    """Valide la cuisson et renvoie succès/échec + message + image_statut + image_path."""
    r = RECETTES[recette_nom]
    t0, tol_t = r["temperature_ideale"], r["tolerance_temp"]
    d0, tol_d = r["temps_ideal"], r["tolerance_temps"]

    ok_temp = (t0 - tol_t) <= temperature <= (t0 + tol_t)
    ok_time = (d0 - tol_d) <= temps <= (d0 + tol_d)

    # ✅ Cas réussite
    if ok_temp and ok_time:
        fichier = r["images"]["reussie"]
        return {
            "succes": True,
            "message": "🎉 Félicitations ! Cuisson parfaite.",
            "details": f"Température {temperature}°C et durée {temps} min.",
            "image_statut": "reussie",
            "image_path": f"images/{fichier}",
        }

    # ❌ Cas échec : on distingue brûlé / cru
    if temperature > (t0 + tol_t):
        detail = "Trop chaud → brûlé."
        statut = "brule"
    elif temperature < (t0 - tol_t):
        detail = "Pas assez chaud → cru."
        statut = "cru"
    elif temps > (d0 + tol_d):
        detail = "Trop longtemps → trop cuit."
        statut = "brule"
    else:
        detail = "Pas assez longtemps → pas assez cuit."
        statut = "cru"

    fichier = r["images"].get(statut)

    return {
        "succes": False,
        "message": "C'est trop cuit ou pas bien cuit",
        "details": f"Détails: {detail}",
        "image_statut": statut,
        "image_path": f"images/{fichier}" if fichier else None,
    }


def obtenir_parametres_cuisson(nom_recette):
    """Renvoie les paramètres de base pour initialiser les compteurs de cuisson."""
    r = RECETTES.get(nom_recette)
    if not r:
        return {"temperature": 180, "duree": 20}
    return {
        "temperature": r["temperature_ideale"],
        "duree": r["temps_ideal"],
    }
