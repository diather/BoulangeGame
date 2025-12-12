#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe principale du jeu Boulange
Gère l'état global, les couleurs, le timer et les transitions entre écrans
"""

import pygame
import time
from recipes import RECETTES
from screens.accueil import EcranAccueil
from screens.selection_ingredients import EcranSelectionIngredients
from screens.petrissage import EcranPetrissage
from screens.cuisson import EcranCuisson
from screens.resultat import EcranResultat
from screens.pedagogique import EcranPedagogique


class Game:
    """Classe principale du jeu"""

    COULEURS = {
        'blanc': (255, 255, 255),
        'noir': (0, 0, 0),
        'beige': (245, 235, 210),
        'marron': (139, 69, 19),
        'vert': (34, 139, 34),
        'rouge': (220, 20, 60),
        'rouge_clair': (255, 180, 180),
        'bleu': (70, 130, 180),
        'orange': (255, 140, 0),
        'gris': (128, 128, 128),
        'gris_clair': (211, 211, 211)
    }

    def __init__(self):
        pygame.init()
        self.largeur = 1000
        self.hauteur = 700
        self.ecran = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Boulange - Jeu de Boulangerie Interactif")

        self.horloge = pygame.time.Clock()
        self.fps = 60
        self.en_cours = True

        # --- Gestion du temps ---
        self.timer_total = 300  # 5 minutes
        self.start_time = None
        self.time_up = False
        self.temps_final = None  # Temps pris pour réussir

        # --- État du jeu ---
        self.ecran_actuel = "accueil"
        self.recette_choisie = None
        self.ingredients_selectionnes = []
        self.temperature_choisie = 180
        self.temps_choisi = 20
        self.compteur_erreurs = 0
        self.resultat_cuisson = None
        self.aide_cuisson_pending = False
        self.transition_vers_pedagogique = None

        # --- Page temps écoulé ---
        self.afficher_page_temps_ecoule = False

        # --- Polices ---
        self.police_titre = pygame.font.SysFont("arial", 48)
        self.police_normale = pygame.font.SysFont("arial", 32)
        self.police_petite = pygame.font.SysFont("arial", 24)

        # --- Initialisation des écrans ---
        self._initialiser_ecrans()

    def _initialiser_ecrans(self):
        """Initialise tous les écrans"""
        self.ecrans = {
            'accueil': EcranAccueil(self),
            'selection_ingredients': EcranSelectionIngredients(self),
            'petrissage': EcranPetrissage(self),
            'cuisson': EcranCuisson(self),
            'resultat': EcranResultat(self),
            'pedagogique': EcranPedagogique(self)
        }

    # --------------------------
    # NAVIGATION ET ÉTATS
    # --------------------------

    def changer_ecran(self, nouvel_ecran):
        """Change d’écran"""
        if nouvel_ecran in self.ecrans:
            self.ecran_actuel = nouvel_ecran
            if hasattr(self.ecrans[nouvel_ecran], "reinitialiser"):
                self.ecrans[nouvel_ecran].reinitialiser()

    def choisir_recette(self, nom_recette):
        """Quand une recette est choisie, on démarre le timer"""
        if nom_recette in RECETTES:
            self.recette_choisie = nom_recette
            self.ingredients_selectionnes = []
            self.compteur_erreurs = 0
            self.start_time = time.monotonic()  # 🟢 Le timer démarre ici
            self.time_up = False
            self.temps_final = None
            self.changer_ecran('selection_ingredients')

    def reinitialiser_jeu(self):
        """Redémarre le jeu depuis le début"""
        self.recette_choisie = None
        self.ingredients_selectionnes = []
        self.temperature_choisie = 180
        self.temps_choisi = 20
        self.compteur_erreurs = 0
        self.start_time = None
        self.time_up = False
        self.afficher_page_temps_ecoule = False
        self.transition_vers_pedagogique = None
        self.temps_final = None
        self.changer_ecran('accueil')

    # --------------------------
    # GESTION DU TIMER
    # --------------------------

    def temps_restant(self):
        """Retourne le temps restant en secondes"""
        if not self.start_time:
            return self.timer_total
        elapsed = int(time.monotonic() - self.start_time)
        return max(0, self.timer_total - elapsed)

    def dessiner_timer(self, surface):
        """Affiche juste le temps restant (sans texte)"""
        restant = self.temps_restant()
        minutes = restant // 60
        secondes = restant % 60
        texte = f"{minutes:02d}:{secondes:02d}"
        txt_surface = self.police_normale.render(texte, True, self.COULEURS['noir'])
        bg_rect = txt_surface.get_rect(topright=(self.largeur - 30, 20))
        pygame.draw.rect(surface, self.COULEURS['blanc'], bg_rect.inflate(20, 10))
        surface.blit(txt_surface, bg_rect)

    def arreter_timer(self):
        """Stoppe le timer et enregistre le temps total écoulé"""
        if self.start_time:
            elapsed = int(time.monotonic() - self.start_time)
            self.temps_final = elapsed
            self.start_time = None

    # --------------------------
    # BOUCLE DU JEU
    # --------------------------

    def executer(self):
        """Boucle principale"""
        while self.en_cours:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.en_cours = False
                elif self.afficher_page_temps_ecoule:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.reinitialiser_jeu()
                else:
                    self.ecrans[self.ecran_actuel].gerer_evenement(event)

            if not self.afficher_page_temps_ecoule:
                self.ecrans[self.ecran_actuel].mettre_a_jour()

            # Transition automatique vers la page pédagogique après 10s
            if self.transition_vers_pedagogique and time.time() >= self.transition_vers_pedagogique:
                self.transition_vers_pedagogique = None
                self.changer_ecran("pedagogique")

            # Temps écoulé
            if self.start_time and self.temps_restant() <= 0:
                self.start_time = None
                self.afficher_page_temps_ecoule = True

            # --- Rendu ---
            if self.afficher_page_temps_ecoule:
                self.afficher_temps_ecoule()
            else:
                self.ecran.fill(self.COULEURS['beige'])
                self.ecrans[self.ecran_actuel].dessiner(self.ecran)
                if self.start_time:
                    self.dessiner_timer(self.ecran)

            pygame.display.flip()
            self.horloge.tick(self.fps)

    # --------------------------
    # PAGE “TEMPS ÉCOULÉ”
    # --------------------------

    def afficher_temps_ecoule(self):
        """Affiche la page spéciale temps écoulé"""
        self.ecran.fill(self.COULEURS['rouge_clair'])

        titre = self.police_titre.render("⏰ Ooups ! Temps écoulé !", True, self.COULEURS['blanc'])
        texte = self.police_normale.render("Le temps est écoulé, recommencez une nouvelle partie.", True, self.COULEURS['blanc'])
        bouton = pygame.Rect(self.largeur // 2 - 100, self.hauteur // 2 + 60, 200, 50)

        # Centrage du texte
        self.ecran.blit(titre, (self.largeur // 2 - titre.get_width() // 2, self.hauteur // 2 - 80))
        self.ecran.blit(texte, (self.largeur // 2 - texte.get_width() // 2, self.hauteur // 2 - 20))

        # Bouton “Recommencer”
        pygame.draw.rect(self.ecran, self.COULEURS['blanc'], bouton, border_radius=12)
        label = self.police_normale.render("Recommencer", True, self.COULEURS['rouge'])
        self.ecran.blit(label, (bouton.centerx - label.get_width() // 2, bouton.centery - label.get_height() // 2))

    # --------------------------
    # UTILITAIRE
    # --------------------------

    def obtenir_recette_actuelle(self):
        if self.recette_choisie:
            return RECETTES[self.recette_choisie]
        return None
