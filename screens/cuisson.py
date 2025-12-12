#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Écran de cuisson pour le jeu Boulange
Permet de régler la température et le temps de cuisson,
et redirige vers l’écran de résultat (succès ou échec).
"""

import pygame
import time
from ui_components import Compteur, Bouton, dessiner_texte_centre, dessiner_fenetre_modale
from recipes import valider_cuisson, obtenir_parametres_cuisson


class EcranCuisson:
    """Écran de réglage des paramètres de cuisson"""

    def __init__(self, jeu):
        self.jeu = jeu
        self.tentatives = 0           # compteur d'échecs successifs
        self.max_tentatives = 5
        self.afficher_aide = False
        self.temps_debut_aide = 0
        self.duree_aide = 10  # secondes
        self.initialiser_controles()

    # ---------------------------------------------------------
    # INITIALISATION DES CONTRÔLES
    # ---------------------------------------------------------
    def initialiser_controles(self):
        """Initialise les éléments interactifs"""

        # Zone paramètres à droite
        self.x_params = self.jeu.largeur // 2 + 40
        self.y_temp_texte = 240
        self.y_temp_compteur = 290
        self.y_duree_texte = 360
        self.y_duree_compteur = 410

        # Compteur de température (à droite, sous le texte)
        self.compteur_temperature = Compteur(
            self.x_params + 20,  # compteur un peu à droite du texte
            self.y_temp_compteur,
            self.jeu.temperature_choisie,
            100,
            300,
            10,
            "°C",
            self.jeu.police_normale,
        )

        # Compteur de temps (à droite, sous le texte)
        self.compteur_temps = Compteur(
            self.x_params + 20,
            self.y_duree_compteur,
            self.jeu.temps_choisi,
            1,
            60,
            1,
            "min",
            self.jeu.police_normale,
        )

        # Bouton LANCER au centre en bas
        self.bouton_lancer = Bouton(
            self.jeu.largeur // 2 - 150,   # centré horizontalement
            self.jeu.hauteur - 100,
            300,
            60,
            "Lancer la cuisson",
            self.jeu.COULEURS["rouge"],
            self.jeu.COULEURS["blanc"],
            self.jeu.police_normale,
        )

    # ---------------------------------------------------------
    # RÉINITIALISATION DE L'ÉCRAN
    # ---------------------------------------------------------
    def reinitialiser(self):
        """
        Réinitialise l'écran de cuisson avec les paramètres actuels.

        ⚠️ On NE remet PAS self.tentatives à 0 ici,
        pour conserver le comptage des 5 essais même si on revient
        depuis l'écran de résultat.
        """
        self.afficher_aide = False
        self.temps_debut_aide = 0

        params = obtenir_parametres_cuisson(self.jeu.recette_choisie)
        if params:
            if self.jeu.temperature_choisie is None:
                self.jeu.temperature_choisie = params["temperature"]
            if self.jeu.temps_choisi is None:
                self.jeu.temps_choisi = params["duree"]

        self.compteur_temperature.valeur = self.jeu.temperature_choisie or 180
        self.compteur_temps.valeur = self.jeu.temps_choisi or 20

    # ---------------------------------------------------------
    # GESTION ÉVÉNEMENTS
    # ---------------------------------------------------------
    def gerer_evenement(self, evenement):
        """Gère les interactions clavier/souris."""
        if self.afficher_aide:
            # En mode aide, Échap permet de fermer avant la fin
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_ESCAPE:
                self.afficher_aide = False
            return

        if self.compteur_temperature.gerer_evenement(evenement):
            self.jeu.temperature_choisie = self.compteur_temperature.valeur

        elif self.compteur_temps.gerer_evenement(evenement):
            self.jeu.temps_choisi = self.compteur_temps.valeur

        if self.bouton_lancer.gerer_evenement(evenement):
            self.lancer_cuisson()

    # ---------------------------------------------------------
    # MISE À JOUR
    # ---------------------------------------------------------
    def mettre_a_jour(self):
        """Met à jour l'état de l'écran (fermeture automatique de l'aide)."""
        if self.afficher_aide and (time.time() - self.temps_debut_aide >= self.duree_aide):
            self.afficher_aide = False

    # ---------------------------------------------------------
    # LANCER CUISSON
    # ---------------------------------------------------------
    def lancer_cuisson(self):
        """Valide la cuisson et redirige vers l'écran résultat."""
        recette_nom = self.jeu.recette_choisie
        recette = self.jeu.obtenir_recette_actuelle()
        if not recette_nom or not recette:
            return

        # On laisse recipes.valider_cuisson construire tout le résultat
        res = valider_cuisson(
            recette_nom,
            self.jeu.temperature_choisie,
            self.jeu.temps_choisi,
        )

        # Gestion des tentatives / aide
        if res.get("succes"):
            # Succès → on remet les tentatives à zéro
            self.jeu.transition_vers_pedagogique = time.time() + 10
            self.tentatives = 0
        else:
            # Échec → on incrémente
            self.tentatives += 1
            if self.tentatives >= self.max_tentatives:
                # Au bout de 5 échecs consécutifs, on déclenche l'aide
                self.jeu.aide_cuisson_pending = True
                self.tentatives = 0  # on repart sur un nouveau cycle après l'aide

        # On enregistre directement la structure retournée
        self.jeu.resultat_cuisson = res
        self.jeu.changer_ecran("resultat")

    # ---------------------------------------------------------
    # DESSIN
    # ---------------------------------------------------------
    def dessiner(self, surface):
        surface.fill(self.jeu.COULEURS["beige"])

        # Titre
        dessiner_texte_centre(
            surface,
            "Réglage de la cuisson",
            60,
            self.jeu.police_titre,
            self.jeu.COULEURS["marron"],
        )

        # Nom de la recette
        recette = self.jeu.obtenir_recette_actuelle()
        if recette:
            dessiner_texte_centre(
                surface,
                f"Recette : {recette['nom']}",
                120,
                self.jeu.police_normale,
                self.jeu.COULEURS["noir"],
            )

        # --- FOUR À GAUCHE ---
        self.dessiner_four(surface)

        # --- PARAMÈTRES À DROITE ---
        # Texte température
        temp_txt = self.jeu.police_normale.render(
            "Température du four :", True, self.jeu.COULEURS["noir"]
        )
        surface.blit(temp_txt, (self.x_params, self.y_temp_texte))

        # Texte durée
        duree_txt = self.jeu.police_normale.render(
            "Durée de cuisson :", True, self.jeu.COULEURS["noir"]
        )
        surface.blit(duree_txt, (self.x_params, self.y_duree_texte))

        # Compteurs
        self.compteur_temperature.dessiner(surface)
        self.compteur_temps.dessiner(surface)

        # Bouton LANCER au centre bas
        self.bouton_lancer.dessiner(surface)

        # Aide si demandée après plusieurs échecs
        if getattr(self.jeu, "aide_cuisson_pending", False) and not self.afficher_aide:
            self.afficher_aide = True
            self.jeu.aide_cuisson_pending = False
            self.temps_debut_aide = time.time()

        if self.afficher_aide:
            self.dessiner_aide(surface)

    # ---------------------------------------------------------
    # AIDE
    # ---------------------------------------------------------
    def dessiner_aide(self, surface):
        params = obtenir_parametres_cuisson(self.jeu.recette_choisie)

        # On prépare une LISTE de lignes, pas une seule grosse chaîne
        contenu = [
            
            "Pour une bonne cuisson :",
           
            f"- Température idéale : {params['temperature']}°C",
           
            f"- Durée idéale : {params['duree']} minutes",
           
            "Appuie sur Échap pour fermer cette aide."
        ]

        dessiner_fenetre_modale(
            surface,
            600,
            300,
            "Aide à la cuisson",
            contenu,                  # ✅ une liste de lignes
            self.jeu.police_titre,
            self.jeu.police_normale,
        )


    # ---------------------------------------------------------
    # DESSIN FOUR
    # ---------------------------------------------------------
    def dessiner_four(self, surface):
        """Dessine le four à GAUCHE."""
        four_largeur = 320
        four_hauteur = 230
        four_x = 80
        four_y = 240

        four_rect = pygame.Rect(four_x, four_y, four_largeur, four_hauteur)
        pygame.draw.rect(surface, self.jeu.COULEURS["gris"], four_rect)
        pygame.draw.rect(surface, self.jeu.COULEURS["noir"], four_rect, 3)

        vitre_rect = pygame.Rect(
            four_x + 20,
            four_y + 30,
            four_largeur - 40,
            four_hauteur - 80,
        )
        pygame.draw.rect(surface, (200, 220, 255), vitre_rect)
        pygame.draw.rect(surface, self.jeu.COULEURS["noir"], vitre_rect, 2)

        texte_four = self.jeu.police_petite.render("FOUR", True, self.jeu.COULEURS["blanc"])
        surface.blit(texte_four, (four_x + 10, four_y + 10))
