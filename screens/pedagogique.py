#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Écran pédagogique pour le jeu Boulange.
Affiche en une seule colonne :
- la recette choisie
- les paramètres de cuisson (choisis vs conseillés)
- le temps total
- une explication du résultat
- le rôle des ingrédients

Affichage vertical avec scroll + barre de défilement.
"""

import time
import pygame
from ui_components import Bouton, dessiner_texte_centre
from recipes import RECETTES

# Petit dictionnaire pédagogique : rôle des ingrédients
ROLES_INGREDIENTS = {
    "farine": "Donne la structure au pain ou au gâteau : elle forme la mie et la croûte.",
    "eau": "Hydrate la farine et permet la formation du gluten.",
    "sel": "Relève le goût et contrôle l’activité de la levure.",
    "levure": "Fait lever la pâte en produisant du gaz (fermentation).",
    "sucre": "Nourrit la levure, apporte du moelleux et de la coloration.",
    "beurre": "Apporte du fondant, du goût et du moelleux.",
    "lait": "Assouplit la pâte et donne une croûte plus colorée.",
    "œuf": "Lie la pâte et donne de la couleur et du fondant.",
    "chocolat": "Apporte un goût sucré et gourmand.",
    "miel": "Ajoute du sucre, du goût et garde l’intérieur plus moelleux.",
}


class EcranPedagogique:
    """Écran qui explique pédagogiquement la recette réalisée."""

    def __init__(self, jeu):
        self.jeu = jeu
        self.contenu_lignes = []     # toutes les lignes de texte, dans l’ordre
        self.scroll_offset = 0       # défilement vertical
        self._content_height = 0     # hauteur totale estimée du contenu (pour la scrollbar)

        # Boutons en bas (fixes)
        self.bouton_refaire = Bouton(
            220, jeu.hauteur - 80, 250, 50,
            "Refaire la recette",
            jeu.COULEURS["orange"],
            jeu.COULEURS["blanc"],
            jeu.police_normale,
        )
        self.bouton_menu = Bouton(
            560, jeu.hauteur - 80, 220, 50,
            "Menu principal",
            jeu.COULEURS["bleu"],
            jeu.COULEURS["blanc"],
            jeu.police_normale,
        )

    # ---------------------------------------------------------
    # PRÉPARATION DU CONTENU
    # ---------------------------------------------------------
    def reinitialiser(self):
        """Construit tout le texte pédagogique à afficher en une seule colonne."""
        self.scroll_offset = 0
        self._construire_contenu()

        # Estimation simple de la hauteur de contenu (pour la barre de scroll)
        ligne_h = self.jeu.police_petite.get_height() + 4
        self._content_height = max(len(self.contenu_lignes) * ligne_h, 0)

    def _construire_contenu(self):
        self.contenu_lignes = []

        recette_nom = self.jeu.recette_choisie
        recette = RECETTES.get(recette_nom, {})
        res = self.jeu.resultat_cuisson or {}

        nom_affiche = recette.get("nom", "Recette inconnue")
        temp_choisie = self.jeu.temperature_choisie
        temps_choisi = self.jeu.temps_choisi

        temp_ideale = recette.get("temperature_ideale")
        temps_ideal = recette.get("temps_ideal")

        # Temps total utilisé
        temps_total = self.jeu.temps_final
        if temps_total is None and self.jeu.start_time:
            temps_total = int(time.monotonic() - self.jeu.start_time)

        if temps_total is not None:
            minutes = temps_total // 60
            secondes = temps_total % 60
            temps_str = f"{minutes} min {secondes:02d} s"
        else:
            temps_str = "non disponible"

        # ---------- 1) Récap de la recette ----------
        self.contenu_lignes.append(f"Recette réalisée : {nom_affiche}")
        self.contenu_lignes.append("")

        if res.get("succes"):
            self.contenu_lignes.append("Tu as RÉUSSI la recette.")
            self.contenu_lignes.append(
                "La cuisson est adaptée : l’intérieur est cuit et l’extérieur n’est pas brûlé."
            )
        else:
            self.contenu_lignes.append("La recette n’a pas encore été complètement réussie.")
        self.contenu_lignes.append("")

        # Paramètres choisis
        self.contenu_lignes.append("Paramètres que tu as choisis :")
        self.contenu_lignes.append(f"- Température du four : {temp_choisie} °C")
        self.contenu_lignes.append(f"- Durée de cuisson : {temps_choisi} minutes")
        self.contenu_lignes.append("")

        # Paramètres conseillés
        if temp_ideale is not None and temps_ideal is not None:
            self.contenu_lignes.append("Paramètres conseillés pour cette recette :")
            self.contenu_lignes.append(f"- Température idéale : {temp_ideale} °C")
            self.contenu_lignes.append(f"- Durée idéale : {temps_ideal} minutes")
            self.contenu_lignes.append("")

        # Temps total
        self.contenu_lignes.append(f"Temps total utilisé pour cette préparation : {temps_str}")
        self.contenu_lignes.append("")

        # Explication du résultat
        self.contenu_lignes.append("Pourquoi tu as obtenu ce résultat :")
        details = res.get("details", "")
        if res.get("succes"):
            self.contenu_lignes.append(
                "- Tes paramètres sont proches des valeurs idéales de température et de durée."
            )
            self.contenu_lignes.append(
                "- La pâte a eu le temps de cuire à cœur, sans brûler la surface."
            )
        elif details:
            self.contenu_lignes.append(f"- {details}")
        else:
            self.contenu_lignes.append(
                "- Les paramètres de cuisson n’étaient pas adaptés à cette recette."
            )
        self.contenu_lignes.append("")
        self.contenu_lignes.append("Tu peux ajuster la température et/ou la durée en te rapprochant")
        self.contenu_lignes.append("des paramètres conseillés ci-dessus.")
        self.contenu_lignes.append("")

        # ---------- 2) Rôle des ingrédients ----------
        self.contenu_lignes.append("Rôle des ingrédients utilisés :")
        self.contenu_lignes.append("")

        requis = recette.get("ingredients_requis", [])
        selectionnes = self.jeu.ingredients_selectionnes or []

        if not requis:
            self.contenu_lignes.append(
                "Aucun détail disponible sur les ingrédients pour cette recette."
            )
        else:
            for ing in requis:
                role = ROLES_INGREDIENTS.get(
                    ing,
                    "Ingrédient utilisé dans la recette.",
                )
                nom_affiche_ing = ing.capitalize()

                if ing in selectionnes:
                    info_sel = "(bien sélectionné)"
                else:
                    info_sel = "(non sélectionné)"

                self.contenu_lignes.append(f"- {nom_affiche_ing} {info_sel} :")
                self.contenu_lignes.append(f"  {role}")
                self.contenu_lignes.append("")

        # ---------- 3) Conclusion pédagogique ----------
        self.contenu_lignes.append("En résumé :")
        if res.get("succes"):
            self.contenu_lignes.append(
                "- Tu as choisi les bons ingrédients et des paramètres de cuisson adaptés."
            )
            self.contenu_lignes.append(
                "- Tu peux maintenant essayer de refaire la recette en autonomie,"
            )
            self.contenu_lignes.append(
                "  ou tester une autre recette pour transférer ce que tu as appris."
            )
        else:
            self.contenu_lignes.append(
                "- Cette page t’explique ce qui manque encore pour réussir."
            )
            self.contenu_lignes.append(
                "- Tu peux refaire la recette en ajustant progressivement les paramètres."
            )
        self.contenu_lignes.append("")

    # ---------------------------------------------------------
    # ÉVÉNEMENTS / SCROLL
    # ---------------------------------------------------------
    def gerer_evenement(self, evenement):
        # Boutons
        if self.bouton_refaire.gerer_evenement(evenement):
            if self.jeu.recette_choisie:
                self.jeu.choisir_recette(self.jeu.recette_choisie)

        if self.bouton_menu.gerer_evenement(evenement):
            self.jeu.reinitialiser_jeu()

        # Scroll à la molette (pygame 2)
        if evenement.type == pygame.MOUSEWHEEL:
            # event.y > 0 : vers le haut, < 0 : vers le bas
            self.scroll_offset += evenement.y * 30

        # Scroll clavier
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_UP:
                self.scroll_offset += 20
            elif evenement.key == pygame.K_DOWN:
                self.scroll_offset -= 20

    def mettre_a_jour(self):
        pass

    # ---------------------------------------------------------
    # DESSIN
    # ---------------------------------------------------------
    def dessiner(self, surface):
        surface.fill(self.jeu.COULEURS["beige"])

        # Titre principal
        dessiner_texte_centre(
            surface,
            "Page pédagogique",
            40,
            self.jeu.police_titre,
            self.jeu.COULEURS["marron"],
        )

        # Sous-titre
        # dessiner_texte_centre(
           #  surface,
           #  "Comprendre ce que tu as fait et comment t’améliorer",
         #    80,
          #   self.jeu.police_petite,
           #  self.jeu.COULEURS["noir"],
       #  )

        # Zone de contenu (viewport) : entre le titre et les boutons
        viewport_top = 120
        viewport_bottom = self.jeu.hauteur - 120
        viewport_height = viewport_bottom - viewport_top

        # Clamp du scroll pour ne pas sortir du contenu
        if self._content_height <= viewport_height:
            self.scroll_offset = 0
        else:
            max_offset = 0
            min_offset = viewport_height - self._content_height  # valeur négative
            if self.scroll_offset > max_offset:
                self.scroll_offset = max_offset
            if self.scroll_offset < min_offset:
                self.scroll_offset = min_offset

        # Carte blanche pour le contenu
        content_rect = pygame.Rect(
            60,
            viewport_top - 10,
            self.jeu.largeur - 120,
            viewport_height + 20,
        )
        pygame.draw.rect(surface, self.jeu.COULEURS["blanc"], content_rect, border_radius=12)
        pygame.draw.rect(surface, self.jeu.COULEURS["gris_clair"], content_rect, 2, border_radius=12)

        # Dessin du texte à l’intérieur de la carte, en une colonne
        x_contenu = 80
        y_depart = viewport_top + self.scroll_offset
        largeur_max = self.jeu.largeur - 2 * x_contenu

        self._dessiner_contenu_colonne(
            surface,
            x=x_contenu,
            y_depart=y_depart,
            largeur_max=largeur_max,
            lignes=self.contenu_lignes,
            police=self.jeu.police_petite,
            couleur=self.jeu.COULEURS["noir"],
        )

        # Affichage de la barre de scroll à droite
        self._dessiner_scrollbar(surface, viewport_top, viewport_height)

        # Boutons fixes en bas
        self.bouton_refaire.dessiner(surface)
        self.bouton_menu.dessiner(surface)

    # ---------------------------------------------------------
    # OUTIL : DESSIN MULTI-LIGNES AVEC RETOUR À LA LIGNE
    # ---------------------------------------------------------
    def _dessiner_contenu_colonne(
        self, surface, x, y_depart, largeur_max, lignes, police, couleur, interligne=4
    ):
        """
        Dessine une liste de lignes, avec retour à la ligne automatique
        si une ligne est trop longue (wrap par mots).
        """
        y = y_depart
        for ligne in lignes:
            if not ligne:
                # ligne vide -> saut de ligne
                y += police.get_height() + interligne
                continue

            mots = ligne.split(" ")
            courant = ""
            for mot in mots:
                test = (courant + " " + mot).strip()
                rendu_test = police.render(test, True, couleur)
                if rendu_test.get_width() > largeur_max and courant:
                    rendu_courant = police.render(courant, True, couleur)
                    surface.blit(rendu_courant, (x, y))
                    y += police.get_height() + interligne
                    courant = mot
                else:
                    courant = test

            if courant:
                rendu_courant = police.render(courant, True, couleur)
                surface.blit(rendu_courant, (x, y))
                y += police.get_height() + interligne

    # ---------------------------------------------------------
    # BARRE DE SCROLL
    # ---------------------------------------------------------
    def _dessiner_scrollbar(self, surface, viewport_top, viewport_height):
        """Dessine une barre de défilement simple à droite, si nécessaire."""
        if self._content_height <= viewport_height + 5:
            return  # pas besoin de scrollbar

        track_x = self.jeu.largeur - 25
        track_y = viewport_top
        track_w = 8
        track_h = viewport_height

        # Rail
        pygame.draw.rect(
            surface,
            self.jeu.COULEURS["gris_clair"],
            pygame.Rect(track_x, track_y, track_w, track_h),
            border_radius=4,
        )

        # Taille du curseur
        thumb_h = max(40, int(track_h * (viewport_height / self._content_height)))
        scroll_range = self._content_height - viewport_height

        if scroll_range <= 0:
            ratio = 0
        else:
            ratio = -self.scroll_offset / scroll_range
            ratio = max(0, min(1, ratio))

        thumb_y = track_y + int((track_h - thumb_h) * ratio)

        pygame.draw.rect(
            surface,
            self.jeu.COULEURS["marron"],
            pygame.Rect(track_x, thumb_y, track_w, thumb_h),
            border_radius=4,
        )
