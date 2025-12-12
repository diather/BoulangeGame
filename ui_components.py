#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Composants d'interface utilisateur réutilisables pour le jeu Boulange
Contient les boutons, zones de texte et autres éléments graphiques
"""

import pygame
import os

class Bouton:
    """Classe pour créer des boutons interactifs"""
    
    def __init__(self, x, y, largeur, hauteur, texte, couleur_fond, couleur_texte, police):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur_fond = couleur_fond
        self.couleur_fond_survol = tuple(min(255, c + 30) for c in couleur_fond)
        self.couleur_texte = couleur_texte
        self.police = police
        self.survole = False
        self.clique = False
    
    def gerer_evenement(self, evenement):
        """Gère les événements de souris pour le bouton"""
        if evenement.type == pygame.MOUSEMOTION:
            self.survole = self.rect.collidepoint(evenement.pos)
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if evenement.button == 1 and self.rect.collidepoint(evenement.pos):
                self.clique = True
                return True
        elif evenement.type == pygame.MOUSEBUTTONUP:
            self.clique = False
        return False
    
    def dessiner(self, surface):
        """Dessine le bouton sur la surface"""
        couleur = self.couleur_fond_survol if self.survole else self.couleur_fond
        pygame.draw.rect(surface, couleur, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        # Rendu du texte centré
        texte_surface = self.police.render(self.texte, True, self.couleur_texte)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        surface.blit(texte_surface, texte_rect)

class BoutonImage:
    """Bouton avec image et texte"""
    
    def __init__(self, x, y, largeur, hauteur, texte, chemin_image, police):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.police = police
        self.survole = False
        self.selectionne = False
        
        # Chargement de l'image (avec fallback)
        self.image = self._charger_image(chemin_image, (largeur - 20, hauteur - 50))
    
    def _charger_image(self, chemin, taille):
        """Charge une image avec fallback vers un placeholder"""
        try:
            if os.path.exists(chemin):
                image = pygame.image.load(chemin)
                return pygame.transform.scale(image, taille)
        except:
            pass
        
        # Création d'un placeholder coloré
        placeholder = pygame.Surface(taille)
        couleur = (200, 200, 200)  # Gris clair
        if "pain" in chemin.lower():
            couleur = (139, 69, 19)  # Marron
        elif "croissant" in chemin.lower():
            couleur = (255, 215, 0)  # Doré
        elif "gateau" in chemin.lower() or "gâteau" in chemin.lower():
            couleur = (255, 182, 193)  # Rose
        elif "farine" in chemin.lower():
            couleur = (255, 255, 255)  # Blanc
        elif "beurre" in chemin.lower():
            couleur = (255, 255, 0)  # Jaune
        elif "oeuf" in chemin.lower() or "œuf" in chemin.lower():
            couleur = (255, 239, 213)  # Beige
        elif "lait" in chemin.lower():
            couleur = (248, 248, 255)  # Blanc cassé
        
        placeholder.fill(couleur)
        pygame.draw.rect(placeholder, (0, 0, 0), placeholder.get_rect(), 2)
        return placeholder
    
    def gerer_evenement(self, evenement):
        """Gère les événements pour le bouton image"""
        if evenement.type == pygame.MOUSEMOTION:
            self.survole = self.rect.collidepoint(evenement.pos)
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if evenement.button == 1 and self.rect.collidepoint(evenement.pos):
                return True
        return False
    
    def dessiner(self, surface):
        """Dessine le bouton image"""
        # Fond du bouton
        couleur_fond = (255, 255, 255) if not self.survole else (240, 240, 240)
        if self.selectionne:
            couleur_fond = (200, 255, 200)  # Vert clair si sélectionné
        
        pygame.draw.rect(surface, couleur_fond, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        # Image
        image_rect = self.image.get_rect()
        image_rect.centerx = self.rect.centerx
        image_rect.y = self.rect.y + 10
        surface.blit(self.image, image_rect)
        
        # Texte en bas
        texte_surface = self.police.render(self.texte, True, (0, 0, 0))
        texte_rect = texte_surface.get_rect()
        texte_rect.centerx = self.rect.centerx
        texte_rect.bottom = self.rect.bottom - 10
        surface.blit(texte_surface, texte_rect)
        
        # Checkmark si sélectionné
        if self.selectionne:
            checkmark = "✓"
            check_surface = pygame.font.Font(None, 36).render(checkmark, True, (0, 150, 0))
            check_rect = check_surface.get_rect()
            check_rect.topright = (self.rect.right - 5, self.rect.top + 5)
            surface.blit(check_surface, check_rect)

class Compteur:
    """Composant pour afficher et modifier des valeurs numériques"""
    
    def __init__(self, x, y, valeur_initiale, valeur_min, valeur_max, pas, unite, police):
        self.x = x
        self.y = y
        self.valeur = valeur_initiale
        self.valeur_min = valeur_min
        self.valeur_max = valeur_max
        self.pas = pas
        self.unite = unite
        self.police = police
        
        # Boutons + et -
        self.bouton_moins = Bouton(x - 30, y, 25, 30, "-", (255, 200, 200), (0, 0, 0), police)
        self.bouton_plus = Bouton(x + 120, y, 25, 30, "+", (200, 255, 200), (0, 0, 0), police)
    
    def gerer_evenement(self, evenement):
        """Gère les événements pour le compteur"""
        if self.bouton_moins.gerer_evenement(evenement):
            if self.valeur > self.valeur_min:
                self.valeur -= self.pas
                return True
        elif self.bouton_plus.gerer_evenement(evenement):
            if self.valeur < self.valeur_max:
                self.valeur += self.pas
                return True
        return False
    
    def dessiner(self, surface):
        """Dessine le compteur"""
        self.bouton_moins.dessiner(surface)
        self.bouton_plus.dessiner(surface)
        
        # Valeur au centre
        texte = f"{self.valeur} {self.unite}"
        texte_surface = self.police.render(texte, True, (0, 0, 0))
        texte_rect = texte_surface.get_rect()
        texte_rect.center = (self.x + 45, self.y + 15)
        
        # Fond pour le texte
        fond_rect = pygame.Rect(self.x - 5, self.y, 115, 30)
        pygame.draw.rect(surface, (255, 255, 255), fond_rect)
        pygame.draw.rect(surface, (0, 0, 0), fond_rect, 1)
        
        surface.blit(texte_surface, texte_rect)

def dessiner_texte_centre(surface, texte, y, police, couleur):
    """Fonction utilitaire pour dessiner du texte centré"""
    texte_surface = police.render(texte, True, couleur)
    texte_rect = texte_surface.get_rect()
    texte_rect.centerx = surface.get_width() // 2
    texte_rect.y = y
    surface.blit(texte_surface, texte_rect)
    return texte_rect

def dessiner_fenetre_modale(surface, largeur, hauteur, titre, contenu, police_titre, police_contenu):
    """Dessine une fenêtre modale au centre de l'écran"""
    # Fond semi-transparent
    overlay = pygame.Surface((surface.get_width(), surface.get_height()))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))
    
    # Fenêtre modale
    modal_rect = pygame.Rect(
        (surface.get_width() - largeur) // 2,
        (surface.get_height() - hauteur) // 2,
        largeur, hauteur
    )
    
    pygame.draw.rect(surface, (255, 255, 255), modal_rect)
    pygame.draw.rect(surface, (0, 0, 0), modal_rect, 3)
    
    # Titre
    titre_surface = police_titre.render(titre, True, (0, 0, 0))
    titre_rect = titre_surface.get_rect()
    titre_rect.centerx = modal_rect.centerx
    titre_rect.y = modal_rect.y + 20
    surface.blit(titre_surface, titre_rect)
    
    # Contenu (ligne par ligne)
    y_offset = titre_rect.bottom + 30
    for ligne in contenu:
        ligne_surface = police_contenu.render(ligne, True, (0, 0, 0))
        ligne_rect = ligne_surface.get_rect()
        ligne_rect.centerx = modal_rect.centerx
        ligne_rect.y = y_offset
        surface.blit(ligne_surface, ligne_rect)
        y_offset += 35
    
    return modal_rect