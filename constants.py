"""Constantes du Snake : grille, couleurs, vitesses, tailles, directions, chemins des images.
Je regroupe tout ici pour régler le jeu sans fouiller le code.
snake.py et menu.py importent ce fichier avec : from constants import *
Par convention, j'écris les constantes en MAJUSCULES : ce sont des valeurs que le jeu ne modifie jamais.
"""

######## Imports
import os										# Module de Python pour manipuler les chemins de fichiers

######## Chemins
# __file__ = le chemin de ce fichier ; os.path.dirname garde seulement son dossier
# os.path.join colle les morceaux d'un chemin avec le bon séparateur (\ sous Windows, / ailleurs)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))	# Dossier du jeu (marche peu importe d'où je lance le script)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")			# Dossier des images
FOOD_IMAGE_PATH = os.path.join(ASSETS_DIR, "bone.png")	# Image de la nourriture
SNAKE_HEAD_IMAGE_PATH = os.path.join(ASSETS_DIR, "snake_head.png")		# Tête : reliée à gauche, regarde vers la droite
SNAKE_BODY_IMAGE_PATH = os.path.join(ASSETS_DIR, "snake_body.png")		# Corps droit : relié à gauche et à droite
SNAKE_CORNER_IMAGE_PATH = os.path.join(ASSETS_DIR, "snake_corner.png")	# Virage : relié à gauche et en bas
SNAKE_TAIL_IMAGE_PATH = os.path.join(ASSETS_DIR, "snake_tail.png")		# Queue : reliée à droite, pointe vers la gauche

######## Grille
CELL_SIZE = 32									# Taille d'une case en pixels
GRID_WIDTH, GRID_HEIGHT = 20, 20				# Nombre de cases en largeur et en hauteur
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE				# Taille de la fenêtre en pixels

######## Directions (en cases)
# Une direction dit de combien de cases je bouge en x et en y
# Rappel : y augmente vers le BAS, donc "haut" = y négatif
RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)

######## Fenêtre
TITLE = "Snakooby"									# Texte de la barre de titre

######## Couleurs (R, V, B)
BG_COLOR = (20, 20, 20)							# Fond gris très foncé (jeu et menu)
GRID_COLOR = (35, 35, 35)						# Lignes de la grille, à peine plus claires que le fond
SNAKE_COLOR = (70, 200, 90)						# Vert du serpent (titre et boutons du menu ; le serpent lui-même est en images)
TEXT_COLOR = (255, 255, 255)					# Blanc pour les textes
TITLE_COLOR = SNAKE_COLOR						# Titre du menu, du même vert que le serpent
BUTTON_COLOR = (60, 60, 60)						# Fond des boutons
BUTTON_HOVER_COLOR = (90, 90, 90)				# Plus clair quand la souris est dessus
BUTTON_BORDER_COLOR = SNAKE_COLOR				# Bordure verte des boutons

######## Vitesses
# L'affichage et le déplacement du serpent ont chacun leur propre vitesse :
# l'écran se redessine 60 fois par seconde, mais le serpent ne change de case que 8 fois par seconde.
# Entre deux changements de case, je le fais glisser petit à petit : c'est ce qui rend le mouvement fluide
FPS = 60										# Images affichées par seconde pendant la partie
SNAKE_SPEED = 8									# Vitesse du serpent : nombre de cases parcourues par seconde
STEP_TIME = 1000 / SNAKE_SPEED					# Durée d'un pas (passage d'une case à la suivante) en millisecondes : 1000 / 8 = 125 ms
MENU_FPS = 30									# Le menu n'a pas besoin de tourner plus vite

######## Clavier
MAX_QUEUED_KEYS = 2								# Nombre maximum de flèches gardées en attente (voir add_direction dans snake.py)
TURN_GRACE = 0.35								# Coup de pouce : une flèche appuyée pendant les premiers 35 % d'un pas fait tourner dans la case
												# que la tête vient de quitter (voir "virage en retard" dans snake.py). 0 = désactivé

######## Serpent
START_CELL = (10, 10)							# Case de départ de la tête (colonne, ligne)

######## Nourriture
FOOD_SIZE = CELL_SIZE							# Taille de l'image de la nourriture en pixels (une case entière)

######## Score
SCORE_Y = 140									# Hauteur (centre) du dernier score dans le menu
SCORE_PADDING = (10, 10)						# Ecart de la position pour le score par rapport au 0, 0 de la fenêtre

######## Polices (tailles)
FONT_SIZE = 32									# Score et boutons
TITLE_FONT_SIZE = 80							# Titre du menu

######## Menu
BUTTON_W, BUTTON_H = 200, 50					# Taille des boutons
BUTTON_RADIUS = 10								# Arrondi des coins
BUTTON_BORDER = 2								# Épaisseur de la bordure
TITLE_Y = 90									# Hauteur (centre) du titre
PLAY_BUTTON_Y = 170								# Haut du bouton Jouer
QUIT_BUTTON_Y = 240								# Haut du bouton Quitter
