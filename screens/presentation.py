#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Écran de présentation du jeu Boulange
Affiche une image d’université, le titre du projet et un bouton “Commencer”.
"""

import pygame
from ui_components import Bouton, dessiner_texte_centre


class EcranPresentation:
    """Page d’accueil avant le menu principal"""

    def __init__(self, jeu):
        self.jeu = jeu
        self.image_universite = None
        self.bouton_commencer = None
        self._charger_elements()

    def _charger_elements(self):
        """Charge l'image et initialise le bouton"""
        # Chargement de l’image
        try:
            self.image_universite = pygame.image.load("images/universite.png")
            # Redimensionne pour s’adapter à l’écran
            self.image_universite = pygame.transform.scale(self.image_universite, (400, 250))
        except FileNotFoundError:
            self.image_universite = None

        # Création du bouton “Commencer”
        self.bouton_commencer = Bouton(
            400, 520, 200, 60, "Commencer",
            self.jeu.COULEURS["vert"], self.jeu.COULEURS["blanc"], self.jeu.police_normale
        )

    def reinitialiser(self):
        """Réinitialise la page"""
        pass  # rien de spécial à faire ici

    def gerer_evenement(self, evenement):
        """Gère les clics sur le bouton"""
        if self.bouton_commencer.gerer_evenement(evenement):
            self.jeu.changer_ecran("accueil")

    def mettre_a_jour(self):
        """Aucune animation nécessaire ici"""
        pass

    def dessiner(self, surface):
        """Dessine la page de présentation"""
        surface.fill(self.jeu.COULEURS["beige"])

        # --- Image université ---
        if self.image_universite:
            rect = self.image_universite.get_rect(center=(self.jeu.largeur // 2, 230))
            surface.blit(self.image_universite, rect)
        else:
            dessiner_texte_centre(surface, "[Aucune image chargée]", 220, self.jeu.police_petite, self.jeu.COULEURS["rouge"])

        # --- Titre du projet ---
        dessiner_texte_centre(surface, "Boulange_Game", 420, self.jeu.police_titre, self.jeu.COULEURS["marron"])

        # --- Bouton “Commencer” ---
        self.bouton_commencer.dessiner(surface)
