#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Écran de résultat pour le jeu Boulange
Affiche le résultat de la cuisson avec messages personnalisés.
"""

import os
import pygame
from ui_components import Bouton, dessiner_texte_centre


class EcranResultat:
    """Écran de résultat final avec messages adaptés."""

    def __init__(self, jeu):
        self.jeu = jeu
        self.resultat_cuisson = None
        self.bouton_action = None

    def reinitialiser(self):
        """Prépare le résultat et le bouton d’action."""
        self.resultat_cuisson = self.jeu.resultat_cuisson
        self.creer_bouton()

    def creer_bouton(self):
        """Le bouton apparaît seulement en cas d'échec."""
        if not self.resultat_cuisson:
            self.bouton_action = None
            return

        if self.resultat_cuisson.get("succes"):
            self.bouton_action = None
        else:
            self.bouton_action = Bouton(
                420, 550, 180, 50,
                "Réessayer",
                self.jeu.COULEURS["orange"],
                self.jeu.COULEURS["blanc"],
                self.jeu.police_normale,
            )

    def gerer_evenement(self, evenement):
        """Bouton Réessayer."""
        if self.bouton_action and self.bouton_action.gerer_evenement(evenement):
            self.jeu.changer_ecran("cuisson")

    def mettre_a_jour(self):
        pass

    def dessiner(self, surface):
        """Affiche le résultat final."""
        if not self.resultat_cuisson or not self.jeu.recette_choisie:
            return

        recette = self.jeu.obtenir_recette_actuelle()

        # --- TITRE ---
        dessiner_texte_centre(
            surface,
            "Résultat de la cuisson",
            50,
            self.jeu.police_titre,
            self.jeu.COULEURS["marron"],
        )

        # --- IMAGE ---
        self.dessiner_produit(surface, recette)

        # --- MESSAGE PERSONNALISÉ ---
        self.dessiner_messages(surface)

        # --- BOUTON SI ECHEC ---
        if self.bouton_action:
            self.bouton_action.dessiner(surface)

    # --------------------------------------------------------------
    # AFFICHAGE DU PRODUIT
    # --------------------------------------------------------------
    def dessiner_produit(self, surface, recette):
        largeur = 250
        hauteur = 180
        x = (self.jeu.largeur - largeur) // 2
        y = 150

        rect_img = pygame.Rect(x, y, largeur, hauteur)
        pygame.draw.rect(surface, (240, 240, 240), rect_img)
        pygame.draw.rect(surface, self.jeu.COULEURS["noir"], rect_img, 3)

        # Produit
        chemin = self.resultat_cuisson.get("image_path")
        if chemin:
            try:
                img = pygame.image.load(chemin).convert_alpha()
                img = pygame.transform.scale(img, (largeur, hauteur))
                surface.blit(img, (x, y))
            except:
                pass

    # --------------------------------------------------------------
    # AFFICHAGE DES MESSAGES SELON LE RÉSULTAT
    # --------------------------------------------------------------
    def dessiner_messages(self, surface):

        statut = self.resultat_cuisson.get("image_statut")

        # ---------------------------
        # 🔵 CAS SUCCÈS
        # ---------------------------
        if self.resultat_cuisson.get("succes"):
            dessiner_texte_centre(
                surface,
                "🎉 Félicitations ! Vous avez réussi !",
                360,
                self.jeu.police_normale,
                self.jeu.COULEURS["bleu"]
            )
            return

        # ---------------------------
        # 🔴 CAS CRU
        # ---------------------------
        if statut == "cru":
            dessiner_texte_centre(
                surface,
                "Pas assez cuit ! Pain cru.",
                360,
                self.jeu.police_normale,
                self.jeu.COULEURS["rouge"]
            )
            dessiner_texte_centre(
                surface,
                "Veuillez réessayer.",
                400,
                self.jeu.police_petite,
                self.jeu.COULEURS["noir"]
            )
            return

        # ---------------------------
        # 🔴 CAS BRÛLÉ
        # ---------------------------
        if statut == "brule":
            dessiner_texte_centre(
                surface,
                "Trop cuit ! Pain brûlé.",
                360,
                self.jeu.police_normale,
                self.jeu.COULEURS["rouge"]
            )
            dessiner_texte_centre(
                surface,
                "Veuillez réessayer.",
                400,
                self.jeu.police_petite,
                self.jeu.COULEURS["noir"]
            )
            return
