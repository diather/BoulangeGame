#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Écran d'accueil du jeu Boulange
Affiche le menu principal avec le choix des recettes
"""

import pygame
from ui_components import BoutonImage, dessiner_texte_centre

class EcranAccueil:
    """Écran d'accueil avec sélection des recettes"""
    
    def __init__(self, jeu):
        self.jeu = jeu
        self.initialiser_boutons()
    
    def initialiser_boutons(self):
        """Initialise les boutons de sélection des recettes"""
        largeur_bouton = 200
        hauteur_bouton = 180
        espacement = 80
        
        # Position de départ pour centrer les 3 boutons
        debut_x = (self.jeu.largeur - (3 * largeur_bouton + 2 * espacement)) // 2
        y = 300
        
        self.boutons_recettes = {
            'pain': BoutonImage(
                debut_x, y, largeur_bouton, hauteur_bouton,
                "Pain", "images/pain.png", self.jeu.police_normale
            ),
            'croissant': BoutonImage(
                debut_x + largeur_bouton + espacement, y, largeur_bouton, hauteur_bouton,
                "Croissant", "images/croissant.png", self.jeu.police_normale
            ),
            'gateau': BoutonImage(
                debut_x + 2 * (largeur_bouton + espacement), y, largeur_bouton, hauteur_bouton,
                "Gâteau", "images/gateau.png", self.jeu.police_normale
            )
        }
    
    def reinitialiser(self):
        """Remet à zéro l'écran d'accueil"""
        pass  # Rien à réinitialiser pour l'écran d'accueil
    
    def gerer_evenement(self, evenement):
        """Gère les événements sur l'écran d'accueil"""
        for nom_recette, bouton in self.boutons_recettes.items():
            if bouton.gerer_evenement(evenement):
                self.jeu.choisir_recette(nom_recette)
                break
    
    def mettre_a_jour(self):
        """Met à jour l'état de l'écran d'accueil"""
        # Mise à jour des effets de survol
        pos_souris = pygame.mouse.get_pos()
        for bouton in self.boutons_recettes.values():
            bouton.survole = bouton.rect.collidepoint(pos_souris)
    
    def dessiner(self, surface):
        """Dessine l'écran d'accueil"""
        # Titre principal
        dessiner_texte_centre(
            surface, "Boulange", 80, 
            self.jeu.police_titre, self.jeu.COULEURS['marron']
        )
        
        # Sous-titre
        dessiner_texte_centre(
            surface, "Jeu de Boulangerie Interactif", 140,
            self.jeu.police_normale, self.jeu.COULEURS['noir']
        )
        
        # Instructions
        dessiner_texte_centre(
            surface, "Choisissez une recette pour commencer :", 220,
            self.jeu.police_normale, self.jeu.COULEURS['noir']
        )
        
        # Boutons des recettes
        for bouton in self.boutons_recettes.values():
            bouton.dessiner(surface)
        
        # Instructions en bas
        dessiner_texte_centre(
            surface, "Cliquez sur une image pour commencer votre aventure culinaire !", 550,
            self.jeu.police_petite, self.jeu.COULEURS['gris']
        )