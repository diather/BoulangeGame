#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Écran de pétrissage pour le jeu Boulange
Affiche une animation de pétrissage avec la pâte qui bouge
"""

import pygame
import math
import time
from ui_components import dessiner_texte_centre

class EcranPetrissage:
    """Écran d'animation de pétrissage"""
    
    def __init__(self, jeu):
        self.jeu = jeu
        self.temps_debut = 0
        self.duree_petrissage = 4.0  # 4 secondes
        self.phase = "petrissage"  # "petrissage" ou "termine"
        self.temps_animation = 0
    
    def reinitialiser(self):
        """Remet à zéro l'animation de pétrissage"""
        self.temps_debut = time.time()
        self.phase = "petrissage"
        self.temps_animation = 0
    
    def gerer_evenement(self, evenement):
        """Gère les événements (aucun pendant le pétrissage)"""
        pass  # Pas d'interaction pendant le pétrissage
    
    def mettre_a_jour(self):
        """Met à jour l'animation de pétrissage"""
        if self.temps_debut == 0:
            self.temps_debut = time.time()
        
        temps_ecoule = time.time() - self.temps_debut
        self.temps_animation = temps_ecoule
        
        if temps_ecoule < self.duree_petrissage:
            self.phase = "petrissage"
        elif temps_ecoule < self.duree_petrissage + 1.5:  # 1.5s pour "terminé"
            self.phase = "termine"
        else:
            # Passage automatique à la cuisson
            self.jeu.changer_ecran('cuisson')
    
    def dessiner(self, surface):
        """Dessine l'écran de pétrissage avec animation"""
        # Titre
        if self.jeu.recette_choisie:
            recette = self.jeu.obtenir_recette_actuelle()
            titre = f"Préparation de votre {recette['nom'].lower()}"
            dessiner_texte_centre(surface, titre, 50, self.jeu.police_titre, self.jeu.COULEURS['marron'])
        
        # Message selon la phase
        if self.phase == "petrissage":
            message = "Pétrissage en cours..."
            couleur = self.jeu.COULEURS['noir']
        else:
            message = "Pétrissage terminé !"
            couleur = self.jeu.COULEURS['vert']
        
        dessiner_texte_centre(surface, message, 150, self.jeu.police_normale, couleur)
        
        # Animation de la pâte au centre
        self.dessiner_animation_pate(surface)
        
        # Barre de progression
        if self.phase == "petrissage":
            self.dessiner_barre_progression(surface)
    
    def dessiner_animation_pate(self, surface):
        """Dessine la pâte animée au centre de l'écran"""
        centre_x = self.jeu.largeur // 2
        centre_y = self.jeu.hauteur // 2
        
        # Paramètres d'animation
        rayon_base = 80
        amplitude = 15
        frequence = 2.0
        
        # Calcul des variations avec math.cos et math.sin
        variation_x = math.cos(self.temps_animation * frequence) * amplitude
        variation_y = math.sin(self.temps_animation * frequence * 1.5) * amplitude * 0.7
        
        # Pulsation du rayon
        pulsation = math.sin(self.temps_animation * frequence * 2) * 10
        rayon = rayon_base + pulsation
        
        # Couleur de la pâte selon la recette
        couleur_pate = (245, 222, 179)  # Beige par défaut
        if self.jeu.recette_choisie:
            recette = self.jeu.obtenir_recette_actuelle()
            if "chocolat" in recette.get("ingredients", []):
                couleur_pate = (139, 69, 19)  # Marron chocolat
            elif self.jeu.recette_choisie == "gateau":
                couleur_pate = (255, 248, 220)  # Jaune clair
        
        # Dessin de la pâte principale
        pos_x = int(centre_x + variation_x)
        pos_y = int(centre_y + variation_y)
        
        pygame.draw.circle(surface, couleur_pate, (pos_x, pos_y), int(rayon))
        pygame.draw.circle(surface, self.jeu.COULEURS['marron'], (pos_x, pos_y), int(rayon), 3)
        
        # Petites bulles d'air animées
        for i in range(5):
            angle = (self.temps_animation * 0.5 + i * 1.2) % (2 * math.pi)
            bulle_x = pos_x + math.cos(angle) * (rayon * 0.6)
            bulle_y = pos_y + math.sin(angle) * (rayon * 0.6)
            rayon_bulle = 3 + math.sin(self.temps_animation + i) * 2
            
            pygame.draw.circle(surface, (255, 255, 255), 
                             (int(bulle_x), int(bulle_y)), int(rayon_bulle))
        
        # Effet de "pétrissage" - mains stylisées
        if self.phase == "petrissage":
            # Mains qui bougent autour de la pâte
            for i in range(2):
                angle_main = self.temps_animation * 2 + i * math.pi
                main_x = pos_x + math.cos(angle_main) * (rayon + 30)
                main_y = pos_y + math.sin(angle_main) * (rayon + 20)
                
                # Dessin stylisé d'une main
                pygame.draw.circle(surface, (255, 220, 177), 
                                 (int(main_x), int(main_y)), 12)
                pygame.draw.circle(surface, (0, 0, 0), 
                                 (int(main_x), int(main_y)), 12, 2)
    
    def dessiner_barre_progression(self, surface):
        """Dessine une barre de progression pour le pétrissage"""
        temps_ecoule = min(self.temps_animation, self.duree_petrissage)
        progression = temps_ecoule / self.duree_petrissage
        
        # Dimensions de la barre
        largeur_barre = 300
        hauteur_barre = 20
        x = (self.jeu.largeur - largeur_barre) // 2
        y = self.jeu.hauteur - 100
        
        # Fond de la barre
        fond_rect = pygame.Rect(x, y, largeur_barre, hauteur_barre)
        pygame.draw.rect(surface, self.jeu.COULEURS['gris_clair'], fond_rect)
        pygame.draw.rect(surface, self.jeu.COULEURS['noir'], fond_rect, 2)
        
        # Barre de progression
        if progression > 0:
            prog_rect = pygame.Rect(x, y, int(largeur_barre * progression), hauteur_barre)
            pygame.draw.rect(surface, self.jeu.COULEURS['vert'], prog_rect)
        
        # Pourcentage
        pourcentage = int(progression * 100)
        texte_prog = f"{pourcentage}%"
        dessiner_texte_centre(surface, texte_prog, y + 30, 
                            self.jeu.police_petite, self.jeu.COULEURS['noir'])