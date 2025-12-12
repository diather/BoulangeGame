#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Point d'entrée principal du jeu Boulange
Jeu de boulangerie interactif en français
"""

import pygame
import sys
from game import Game


def main():
    """Point d'entrée principal du jeu"""
    # Initialisation de Pygame
    pygame.init()

    try:
        # Création et lancement du jeu
        jeu = Game()
        jeu.executer()
    except Exception as e:
        print(f"Erreur lors du lancement du jeu: {e}")
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
