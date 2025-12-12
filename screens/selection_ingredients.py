#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Écran de sélection des ingrédients pour le jeu Boulange
Permet de choisir les ingrédients nécessaires à la recette
"""

import pygame
import time
import random
from ui_components import BoutonImage, Bouton, dessiner_texte_centre, dessiner_fenetre_modale
from recipes import TOUS_INGREDIENTS, valider_ingredients, obtenir_aide_ingredients


class EcranSelectionIngredients:
    """Écran de sélection des ingrédients"""

    def __init__(self, jeu):
        self.jeu = jeu
        self.boutons_ingredients = {}
        self.afficher_aide = False
        self.temps_debut_aide = 0
        self.duree_aide = 10  # 10 secondes
        self.message_erreur = ""
        self.temps_message = 0
        self.positions_ingredients = []  # mémorise les positions initiales
        self.initialiser_boutons()

    def initialiser_boutons(self):
        """Initialise les boutons d'ingrédients et les boutons d'action"""
        # Boutons des ingrédients (grille 5x3)
        colonnes = 5
        lignes = 3
        largeur_bouton = 160
        hauteur_bouton = 130
        espacement_x = 25
        espacement_y = 20

        # Calcul de la position de départ pour centrer
        largeur_totale = colonnes * largeur_bouton + (colonnes - 1) * espacement_x
        debut_x = (self.jeu.largeur - largeur_totale) // 2
        debut_y = 120

        self.boutons_ingredients = {}
        self.positions_ingredients = []

        for i, ingredient in enumerate(TOUS_INGREDIENTS):
            ligne = i // colonnes
            colonne = i % colonnes

            if ligne < lignes:  # Ne pas dépasser le nombre de lignes
                x = debut_x + colonne * (largeur_bouton + espacement_x)
                y = debut_y + ligne * (hauteur_bouton + espacement_y)

                bouton = BoutonImage(
                    x,
                    y,
                    largeur_bouton,
                    hauteur_bouton,
                    ingredient.capitalize(),
                    f"images/{ingredient}.png",
                    self.jeu.police_petite,
                )
                self.boutons_ingredients[ingredient] = bouton
                self.positions_ingredients.append((x, y))

        # --- Boutons d'action ---

        # Bouton "Valider"
        self.bouton_valider = Bouton(
            200,
            600,
            150,
            50,
            "Valider",
            self.jeu.COULEURS["vert"],
            self.jeu.COULEURS["blanc"],
            self.jeu.police_normale,
        )

        # Bouton "Reset" (anciennement "Réinitialiser")
        self.bouton_reinitialiser = Bouton(
            370,
            600,
            150,
            50,
            "Reset",
            self.jeu.COULEURS["orange"],
            self.jeu.COULEURS["blanc"],
            self.jeu.police_normale,
        )

        # Bouton "Nouvelle recette" (anciennement "Changer de recette")
        self.bouton_changer_recette = Bouton(
            540,
            600,
            260,
            50,
            "Nouvelle recette",
            self.jeu.COULEURS["bleu"],
            self.jeu.COULEURS["blanc"],
            self.jeu.police_normale,
        )

    def reinitialiser(self):
        """Remet à zéro l'écran de sélection"""
        self.afficher_aide = False
        self.message_erreur = ""
        self.temps_message = 0
        # Remet à zéro la sélection des ingrédients
        for bouton in self.boutons_ingredients.values():
            bouton.selectionne = False

    def gerer_evenement(self, evenement):
        """Gère les événements sur l'écran de sélection"""
        if self.afficher_aide:
            # En mode aide, seule l'échap ou le temps peut fermer
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_ESCAPE:
                self.afficher_aide = False
            return

        # Gestion des ingrédients
        for nom_ingredient, bouton in self.boutons_ingredients.items():
            if bouton.gerer_evenement(evenement):
                self.basculer_ingredient(nom_ingredient)
                break

        # Gestion des boutons d'action
        if self.bouton_valider.gerer_evenement(evenement):
            self.valider_selection()
        elif self.bouton_reinitialiser.gerer_evenement(evenement):
            self.reinitialiser_selection()
        elif self.bouton_changer_recette.gerer_evenement(evenement):
            self.jeu.changer_ecran("accueil")

    def basculer_ingredient(self, nom_ingredient):
        """Active/désactive la sélection d'un ingrédient"""
        bouton = self.boutons_ingredients[nom_ingredient]

        if bouton.selectionne:
            bouton.selectionne = False
            if nom_ingredient in self.jeu.ingredients_selectionnes:
                self.jeu.ingredients_selectionnes.remove(nom_ingredient)
        else:
            bouton.selectionne = True
            if nom_ingredient not in self.jeu.ingredients_selectionnes:
                self.jeu.ingredients_selectionnes.append(nom_ingredient)

    def valider_selection(self):
        """Valide la sélection d'ingrédients"""
        if not self.jeu.recette_choisie:
            return

        if valider_ingredients(self.jeu.recette_choisie, self.jeu.ingredients_selectionnes):
            # Sélection correcte, passer au pétrissage
            self.jeu.changer_ecran("petrissage")
        else:
            # Sélection incorrecte
            self.jeu.compteur_erreurs += 1
            self.message_erreur = f"Ingrédients incorrects ! Tentative {self.jeu.compteur_erreurs}/5"
            self.temps_message = time.time()

            # 🔁 Mélange aléatoire des positions des ingrédients
            positions_melangees = self.positions_ingredients[:]
            random.shuffle(positions_melangees)

            for (ingredient, bouton), pos in zip(self.boutons_ingredients.items(), positions_melangees):
                bouton.rect.topleft = pos

            # Réinitialise la sélection
            self.jeu.ingredients_selectionnes = []
            for bouton in self.boutons_ingredients.values():
                bouton.selectionne = False

            # Après 5 erreurs → aide
            if self.jeu.compteur_erreurs >= 5:
                self.afficher_aide = True
                self.temps_debut_aide = time.time()
                self.jeu.compteur_erreurs = 0  # reset

    def reinitialiser_selection(self):
        """Remet à zéro la sélection des ingrédients"""
        self.jeu.ingredients_selectionnes = []
        for bouton in self.boutons_ingredients.values():
            bouton.selectionne = False
        self.message_erreur = ""

    def mettre_a_jour(self):
        """Met à jour l'état de l'écran"""
        # Gestion du temps d'affichage de l'aide
        if self.afficher_aide:
            temps_ecoule = time.time() - self.temps_debut_aide
            if temps_ecoule >= self.duree_aide:
                self.afficher_aide = False

        # Effacement du message d'erreur après 3 secondes
        if self.message_erreur and time.time() - self.temps_message > 3:
            self.message_erreur = ""

    def dessiner(self, surface):
        """Dessine l'écran de sélection des ingrédients"""
        # Titre avec nom de la recette
        if self.jeu.recette_choisie:
            recette = self.jeu.obtenir_recette_actuelle()
            titre = f"Ingrédients pour : {recette['nom']}"
            dessiner_texte_centre(
                surface,
                titre,
                30,
                self.jeu.police_titre,
                self.jeu.COULEURS["marron"],
            )

        # Instructions
        instruction = f"Sélectionnés : {len(self.jeu.ingredients_selectionnes)} ingrédients"
        dessiner_texte_centre(
            surface,
            instruction,
            80,
            self.jeu.police_normale,
            self.jeu.COULEURS["noir"],
        )

        # Boutons des ingrédients
        for bouton in self.boutons_ingredients.values():
            bouton.dessiner(surface)

        # ✅ Message d'erreur juste après les boutons d'ingrédients (en bas de la grille)
        if self.message_erreur:
            dessiner_texte_centre(
                surface,
                self.message_erreur,
                548,  # sous la grille, au-dessus des boutons d'action
                self.jeu.police_normale,
                self.jeu.COULEURS["rouge"],
            )

        # Boutons d'action (sous le message d’erreur)
        self.bouton_valider.dessiner(surface)
        self.bouton_reinitialiser.dessiner(surface)
        self.bouton_changer_recette.dessiner(surface)

        # Fenêtre d'aide
        if self.afficher_aide and self.jeu.recette_choisie:
            temps_restant = max(0, self.duree_aide - int(time.time() - self.temps_debut_aide))

            # Contenu de l'aide
            ingredients_corrects = obtenir_aide_ingredients(self.jeu.recette_choisie)
            contenu = [
                "Voici les bons ingrédients :",
                "",
            ]
            contenu.extend([f"• {ingredient.capitalize()}" for ingredient in ingredients_corrects])
            contenu.extend(
                [
                    "",
                    f"Cette aide se fermera dans {temps_restant}s",
                    "Appuyez sur Échap pour fermer",
                ]
            )

            dessiner_fenetre_modale(
                surface,
                500,
                400,
                "Aide aux ingrédients",
                contenu,
                self.jeu.police_normale,
                self.jeu.police_petite,
            )
