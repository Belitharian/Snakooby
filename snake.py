""" 🐍 SNAKE v1.0.0
-----------------------------------------------------------------------
Jeu du Snake avec pygame-ce.
Contrôles : flèches du clavier pour diriger le serpent.
La partie se termine si le serpent se touche lui-même ou un mur.
Date : 25/11/2026
-----------------------------------------------------------------------
Lancer le jeu :
	pip install pygame-ce
	python snake.py

-----------------------------------------------------------------------
Pourquoi j'utilise pygame
-----------------------------------------------------------------------
- Python seul ne sait pas ouvrir une fenêtre de jeu, lire le clavier en continu ou afficher des images.
  pygame est une bibliothèque (du code déjà écrit par d'autres) qui fait tout ça pour moi.
- C'est la bibliothèque de jeu 2D la plus connue en Python : je trouve facilement des tutoriels, de la documentation et des exemples.
- Elle est simple : une fenêtre, des images, une boucle. Je n'ai pas d'éditeur ni de concepts compliqués à apprendre avant de commencer.
- Elle ne cache rien : c'est MOI qui écris la boucle de jeu (lire le clavier -> déplacer -> dessiner -> attendre).
  C'est idéal pour apprendre comment fonctionne un jeu "de l'intérieur".
- Pour un jeu plus gros (3D, mobile...), je passerais plutôt à un moteur comme Godot ou Unity.
  Pour un Snake, ce serait beaucoup trop lourd.

-----------------------------------------------------------------------
pygame-ce (et pas pygame) : la différence
-----------------------------------------------------------------------
- pygame-ce ("Community Edition") est une version de pygame reprise par une grande partie de ses développeurs.
  Elle a été créée à partir du même code que pygame.
- Elle est mise à jour plus souvent : corrections de bugs, nouvelles fonctions, et nouvelles versions de Python prises en charge plus vite.
- Elle est compatible : le code écrit pour pygame marche presque toujours tel quel avec pygame-ce.
- Attention, je l'installe avec "pip install pygame-ce", mais dans le code j'écris quand même "import pygame".

-----------------------------------------------------------------------
Organisation des fichiers (modules)
-----------------------------------------------------------------------
Un module = un fichier .py. Je découpe le jeu en plusieurs fichiers pour que chacun ait un seul rôle :
- snake.py     : CE fichier. Le point d'entrée : il crée la fenêtre, contient la partie (play) et alterne menu / partie (main).
- menu.py      : l'écran d'accueil avec les boutons Jouer / Quitter. Il ne crée pas de fenêtre, il dessine dans celle de snake.py.
- constants.py : tous les réglages (tailles, couleurs, vitesses, directions, chemins des images). Pour changer le jeu, je commence par là.
- assets/      : les images (nourriture, tête, corps, virage et queue du serpent).

"from menu import menu" veut dire : dans le fichier menu.py, va chercher la fonction appelée menu.
"from constants import *" veut dire : prends TOUT ce qui est dans constants.py (CELL_SIZE, BG_COLOR...).
	J'écris alors CELL_SIZE au lieu de constants.CELL_SIZE.
	Par convention, les constantes sont écrites en majuscules.

-----------------------------------------------------------------------
Fonctionnalités marquantes et pourquoi je les ai faites comme ça
-----------------------------------------------------------------------
1. Le serpent est une simple liste de positions, la tête en premier.
	Pour avancer, j'ajoute une nouvelle tête devant (insert) et j'enlève le bout de la queue (pop).
	Je ne déplace donc jamais chaque morceau un par un : seuls les deux bouts changent.
	Pour grandir, il me suffit de ne pas enlever la queue ce tour-là.

2. Tout est calé sur une grille.
	Le serpent avance d'une case entière (CELL_SIZE pixels) à chaque tour, et la nourriture tombe toujours sur une case.
	Comparer deux positions me suffit pour savoir si le serpent mange ou se cogne : pas de calcul de collision compliqué.

3. Un mouvement fluide : l'affichage et le serpent ont chacun leur vitesse.
	La boucle tourne FPS (60) fois par seconde : l'écran est redessiné 60 fois par seconde.
	Le serpent, lui, ne change de case que SNAKE_SPEED (8) fois par seconde, quand STEP_TIME millisecondes se sont écoulées.
	Entre deux pas, je fais glisser la tête et la queue de quelques pixels à chaque image (fonction draw_snake).
	Le corps reste sur ses cases : comme pour la liste du serpent, seuls les deux bouts bougent.
	La grille, les collisions et la nourriture ne changent pas : elles travaillent toujours case par case.
	Pour changer la vitesse du serpent, je change SNAKE_SPEED dans constants.py.

4. Le serpent peut suivre sa propre queue.
	Pour tester s'il se mord, je regarde son corps SANS le bout de la queue, car la queue bouge en même temps que la tête.
	Sauf s'il mange : là la queue reste en place, donc je la garde dans le test.

5. Pas de demi-tour, et une file d'attente pour les touches.
	Si le serpent va à droite, j'ignore la touche gauche : sinon il rentrerait directement dans son corps.
	Les flèches ne changent pas la direction tout de suite : je les range dans une liste (next_directions)
	et j'en utilise une à chaque pas. Si j'appuie très vite sur haut puis gauche, le serpent tourne en haut, PUIS à gauche,
	au lieu de faire demi-tour et de se mordre. La liste garde au maximum MAX_QUEUED_KEYS touches.
	Coup de pouce pour la réactivité : si j'appuie juste après que la tête a quitté sa case (début du glissement),
	je refais le dernier pas dans la nouvelle direction. Le serpent tourne là où je le vois, et pas une case plus loin.
	Pour ça, le calcul d'un pas est dans une fonction à part (move) que j'appelle aussi pour refaire le pas.

6. La nourriture n'apparaît jamais sur le serpent.
	random_food tire une case au hasard et recommence tant qu'elle tombe sur le serpent.

7. Des images (sprites) pour la tête, le corps, les virages et la queue.
	J'ai généré seulement 4 images, chacune dans un seul sens. Le jeu les tourne (0°, 90°, 180°, 270°) selon le besoin.
	Pour savoir quelle image mettre sur une case, je regarde où sont les cases voisines du serpent (devant / derrière).
	Je charge et je tourne toutes les images UNE fois au lancement, pas à chaque frame (plus rapide).

8. Menu et partie séparés.
	menu() renvoie True (Jouer) ou False (Quitter), play() renvoie le score. main() alterne les deux.
	Je donne la fenêtre au menu au lieu de lui en faire créer une nouvelle : une seule fenêtre pour tout le jeu.

9. Tous les réglages au même endroit (constants.py).
	Je construis les chemins des images à partir de l'emplacement de constants.py : le jeu trouve ses images
	même si je le lance depuis un autre dossier (biscuit...).

-----------------------------------------------------------------------
Notes sur pygame et Python
-----------------------------------------------------------------------
- Une Surface est tout ce qui est visuel (fenêtre principale du jeu, image, etc.)
- Un Font est tout ce qui est un texte
- Un texte ne s'affiche pas directement : font.render() le transforme d'abord en Surface, puis blit() la colle sur l'écran à la position voulue
- Le repère part du coin en haut à gauche (0, 0). x augmente vers la droite, y augmente vers le BAS (c'est pour ça que "haut" = y négatif)
- Les positions sont en pixels, pas en cases. Pour passer de l'un à l'autre : pixels = case * CELL_SIZE (et case = pixels // CELL_SIZE)
- Je dessine tout dans une image "cachée", puis display.flip() l'affiche d'un coup. Si j'oublie flip(), je ne vois rien bouger
- À chaque frame je redessine tout depuis le fond (screen.fill) : sinon les anciennes positions du serpent restent à l'écran
- L'ordre de dessin compte : ce qui est dessiné en dernier passe par-dessus (fond -> grille -> nourriture -> serpent -> score)
- clock.tick(FPS) met le jeu en pause juste ce qu'il faut pour afficher FPS images par seconde, et renvoie le temps écoulé (en millisecondes) depuis son dernier appel
- screen.set_clip(rectangle) limite le dessin à ce rectangle (ce qui dépasse n'est pas dessiné) ; screen.set_clip(None) enlève la limite
- Je dois lire pygame.event.get() à chaque tour de boucle, même si je ne m'en sers pas : sinon Windows croit que la fenêtre a planté ("Ne répond pas")
- Les couleurs sont en (Rouge, Vert, Bleu), chaque valeur entre 0 et 255
- [] = une liste : je peux la modifier (insert, pop...). Par exemple, le serpent
- (x, y) = un vecteur (tuple) : je ne peux pas le modifier. Je m'en sers comme d'un vecteur, pour une position (x, y) ou une direction (dx, dy)
- {clé: valeur} = un dictionnaire (key, value) : je retrouve une valeur à partir de sa clé. Ex. head_images[90] donne la tête tournée de 90°
"""

######## Imports
# "import" charge un module pour que je puisse utiliser ses fonctions
import random										# Module de Python : tirages aléatoire pour la nourriture
import sys											# Module de Python : sys.exit() pour arrêter le programme (sys = system)
import pygame										# pygame-ce (installé avec "pip install pygame-ce")

# Mes propres modules (les autres fichiers .py du dossier)
from menu import menu								# Dans menu.py, la fonction menu() : l'écran avec les boutons Jouer / Quitter
from constants import *								# Dans constants.py, tous les réglages : grille, couleurs, vitesses, directions, chemins des images

######## Démarrage de pygame
# A faire avant toute autre fonction pygame
# Initialise tous les modules pygame (affichage, clavier, polices...).
pygame.init()

######## Fenêtre et outils pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))	# Crée la fenêtre ; screen est la Surface sur laquelle je dessine tout
pygame.display.set_caption(TITLE)					# Texte de la barre de titre de la fenêtre
clock = pygame.time.Clock()							# Sert à limiter la vitesse du jeu
font = pygame.font.SysFont(None, FONT_SIZE)			# Police par défaut (None) pour afficher le score

######## Images
# Je charge les images UNE seule fois ici, au lancement.
# convert_alpha() garde la transparence
food_image = pygame.image.load(FOOD_IMAGE_PATH).convert_alpha()
# transform.scale (et pas smoothscale) garde les pixels nets (smooth = lisse l'image)
food_image = pygame.transform.scale(food_image, (FOOD_SIZE, FOOD_SIZE))

def load_cell_image(path):
	"""Charge une image et la met à la taille d'une case."""
	# Les images sont dessinées en 32 x 32 pixels, je les redimensionne à 20 x 20 (selon la constante)
	image = pygame.image.load(path).convert_alpha()
	image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
	return image

def rotations(image):
	"""Renvoie un dictionnaire avec les 4 versions tournées d'une image : {0: ..., 90: ..., 180: ..., 270: ...}.
	transform.rotate tourne dans le sens INVERSE des aiguilles d'une montre."""
	images = {}										# Déclaration du dictionnaire {key: value}
	images[0] = image								# Pas de rotation : l'image telle qu'elle est dessinée
	images[90] = pygame.transform.rotate(image, 90)
	images[180] = pygame.transform.rotate(image, 180)
	images[270] = pygame.transform.rotate(image, 270)
	return images

# Les images du serpent sont dessinées dans un seul sens, je les tourne selon le besoin (rotation INVERSE)
# Ex. : head_images[90] = la tête qui regarde vers le haut
# Ex. : body_images[180] = une partie du corps vers la gauche
# Chaque variable est un dictionnaire qui permet d'accéder à l'image en fonction de la rotation
head_images = rotations(load_cell_image(SNAKE_HEAD_IMAGE_PATH))
body_images = rotations(load_cell_image(SNAKE_BODY_IMAGE_PATH))
corner_images = rotations(load_cell_image(SNAKE_CORNER_IMAGE_PATH))
tail_images = rotations(load_cell_image(SNAKE_TAIL_IMAGE_PATH))

######## Déclarer une fonction
# def nom_fonction():
# """Description de la fonction."""
# corps de la fonction

######## Fonctions utilitaires
def quit_game():
	"""Ferme proprement pygame et le programme."""
	pygame.quit()									# Ferme la fenêtre et libère pygame
	sys.exit()										# Arrête le programme Python

def random_food(snake):
	"""Renvoie une position aléatoire (en pixels) qui n'est pas sur le serpent."""
	while True:
		# Je tire une case au hasard puis je la convertis en pixels
		# random.randrange(30) donne un nombre entier entre 0 et 29
		pos = (
			random.randrange(GRID_WIDTH) * CELL_SIZE,
			random.randrange(GRID_HEIGHT) * CELL_SIZE,
		)
		# Je recommence tant que la case est occupée par le serpent
		if pos not in snake:
			return pos

######## Choix des images du serpent
def step(a, b):
	"""Direction d'une case A vers une case voisine B, en cases : RIGHT, LEFT, UP ou DOWN."""
	# Les différentes directions sont des tuples (x, y)
	# Ex. : A = (40, 20), B = (60, 20) -> (20 // 20, 0 // 20) = (1, 0) = RIGHT : b est à droite de a
	dx = (b[0] - a[0]) // CELL_SIZE
	dy = (b[1] - a[1]) // CELL_SIZE
	return (dx, dy)

def angle_of(d):
	"""Angle pour tourner une image dessinée "vers la droite" afin qu'elle pointe dans la direction d."""
	if d == RIGHT:
		return 0
	if d == UP:
		return 90
	if d == LEFT:
		return 180
	# Il ne reste que DOWN
	return 270

def corner_angle(a, b):
	"""Angle du virage qui relie les côtés a et b. L'ordre de a et b ne compte pas."""
	# Le virage est dessiné relié à GAUCHE et en BAS ; chaque quart de tour le fait tourner
	# Je teste toutes les combinaisons possibles
	if (a == LEFT and b == DOWN) or (a == DOWN and b == LEFT):
		return 0
	if (a == DOWN and b == RIGHT) or (a == RIGHT and b == DOWN):
		return 90
	if (a == RIGHT and b == UP) or (a == UP and b == RIGHT):
		return 180
	# Il ne reste que haut + gauche
	return 270

def segment_image(snake, i, direction):
	"""Choisit l'image (tête, corps, virage ou queue) du segment i, déjà tournée dans le bon sens."""
	# Tête = premier élément de la liste
	if i == 0:
		# len(snake) retourne le nombre d'éléments dans le serpent
		if len(snake) == 1:
			# Serpent d'une seule CASE : la tête regarde dans le sens du déplacement
			# La direction étant en pixels, il faut la passer en CASES
			facing = (direction[0] // CELL_SIZE, direction[1] // CELL_SIZE)
		else:
			# Sinon la tête regarde dans le sens opposé au segment qui la suit
			facing = step(snake[1], snake[0])
		return head_images[angle_of(facing)]

	# Queue = dernier élément de la liste
	# Il faut faire - 1 sur la taille du serpent car sinon i sera plus grand que le serpent (donc plantage)
	if i == len(snake) - 1:
		# La queue est reliée vers le segment juste devant elle (donc on enlève 1 pour avoir le segment précédent du serpent)
		to_front = step(snake[i], snake[i - 1])
		return tail_images[angle_of(to_front)]

	# Corps : je regarde de quels côtés sont les deux voisins pour savoir si on doit afficher un coin
	to_front = step(snake[i], snake[i - 1])			# Côté du voisin vers la tête
	to_back = step(snake[i], snake[i + 1])			# Côté du voisin vers la queue

	# Les deux voisins sont sur la même ligne (pas de déplacement en y) : corps droit horizontal
	if to_front[1] == 0 and to_back[1] == 0:
		return body_images[0]
	# Les deux voisins sont sur la même colonne (pas de déplacement en x) : corps droit vertical
	if to_front[0] == 0 and to_back[0] == 0:
		return body_images[90]
	# Sinon les voisins sont sur deux côtés qui se touchent (ex. gauche + bas) : c'est un virage
	return corner_images[corner_angle(to_front, to_back)]

def is_straight(snake, i):
	"""Renvoie True si le segment i du corps est droit, False si c'est un virage."""
	to_front = step(snake[i], snake[i - 1])
	to_back = step(snake[i], snake[i + 1])
	# Droit = les deux voisins sont sur la même ligne, ou sur la même colonne
	if to_front[1] == 0 and to_back[1] == 0:
		return True
	if to_front[0] == 0 and to_back[0] == 0:
		return True
	return False

######## Mouvement fluide
# Le serpent change de case seulement SNAKE_SPEED fois par seconde, mais l'écran se redessine FPS fois par seconde.
# Entre deux pas, je fais glisser la tête et la queue de quelques pixels à chaque image : le mouvement paraît continu.
# Le corps, lui, reste dessiné sur ses cases : seuls les deux bouts bougent, comme pour la liste du serpent.
#
#   Exemple : le serpent va vers la droite, shift = nombre de pixels déjà parcourus depuis le dernier pas
#
#        case de la queue   case suivante          avant-dernière case    case de la tête
#       +----------------+----------------+  ...  +----------------+----------------+
#       |  queue -->     |                |       |                |   tête -->     |
#       +----------------+----------------+       +----------------+----------------+
#        <-- shift -->                               <-- shift -->
#        la queue avance de shift pixels             la tête avance de shift pixels
#        vers la case suivante                       depuis l'avant-dernière case

def slide(a, b, shift):
	"""Position (en pixels) entre la case a et sa voisine b, après avoir avancé de shift pixels depuis a."""
	d = step(a, b)
	# Si a et b sont la même case, d = (0, 0) et la position reste a
	return (a[0] + d[0] * shift, a[1] + d[1] * shift)

def back_part(cell, d, length):
	"""Partie ARRIÈRE de la case cell (le côté d'où vient le mouvement d), sur length pixels."""
	# pygame.Rect(x, y, largeur, hauteur)
	if d == RIGHT:
		return pygame.Rect(cell[0], cell[1], length, CELL_SIZE)
	if d == LEFT:
		return pygame.Rect(cell[0] + CELL_SIZE - length, cell[1], length, CELL_SIZE)
	if d == DOWN:
		return pygame.Rect(cell[0], cell[1], CELL_SIZE, length)
	# Il ne reste que UP
	return pygame.Rect(cell[0], cell[1] + CELL_SIZE - length, CELL_SIZE, length)

def front_part(cell, d, length):
	"""Partie AVANT de la case cell (le côté vers lequel va le mouvement d), sur length pixels."""
	if d == RIGHT:
		return pygame.Rect(cell[0] + CELL_SIZE - length, cell[1], length, CELL_SIZE)
	if d == LEFT:
		return pygame.Rect(cell[0], cell[1], length, CELL_SIZE)
	if d == DOWN:
		return pygame.Rect(cell[0], cell[1] + CELL_SIZE - length, CELL_SIZE, length)
	# Il ne reste que UP
	return pygame.Rect(cell[0], cell[1], CELL_SIZE, length)

def draw_snake(snake, previous_snake, direction, shift):
	"""Dessine le serpent en faisant glisser la tête et la queue de shift pixels."""
	# La queue a bougé pendant le dernier pas (sauf si le serpent vient de manger : elle est restée en place)
	tail_moved = previous_snake[-1] != snake[-1]

	# Serpent d'une seule case : il n'y a que la tête, je la fais glisser et c'est fini
	if len(snake) == 1:
		head_pos = slide(previous_snake[0], snake[0], shift)
		screen.blit(segment_image(snake, 0, direction), head_pos)
		return

	# Pour le dessin, je remets l'ancienne case de la queue au bout de la liste : la queue est encore en train de la quitter
	# drawn = la liste des cases à dessiner
	drawn = snake.copy()
	if tail_moved:
		drawn.append(previous_snake[-1])

	######## Corps
	# Tous les segments sauf le premier (tête) et le dernier (queue)
	last = len(drawn) - 1
	for i in range(1, last):
		cell = drawn[i]
		image = segment_image(drawn, i, direction)
		# Par défaut je dessine toute la case
		visible = pygame.Rect(cell[0], cell[1], CELL_SIZE, CELL_SIZE)

		# Case que la tête est en train de quitter : je ne dessine que la partie DERRIÈRE la tête
		# (sinon le corps dépasserait autour du museau)
		if i == 1 and is_straight(drawn, i):
			head_dir = step(drawn[1], drawn[0])
			visible = visible.clip(back_part(cell, head_dir, shift))

		# Case dans laquelle la queue est en train d'entrer : je ne dessine que la partie DEVANT la queue
		# (sinon le corps dépasserait autour de la pointe de la queue)
		if tail_moved and i == last - 1 and is_straight(drawn, i):
			tail_dir = step(drawn[last], drawn[i])
			visible = visible.clip(front_part(cell, tail_dir, CELL_SIZE - shift))

		# set_clip limite le dessin à un rectangle : tout ce qui dépasse est ignoré
		screen.set_clip(visible)
		screen.blit(image, cell)
		screen.set_clip(None)						# None = je peux de nouveau dessiner partout

	######## Queue
	if tail_moved:
		# La queue glisse de son ancienne case vers la nouvelle
		tail_dir = step(previous_snake[-1], snake[-1])
		tail_pos = slide(previous_snake[-1], snake[-1], shift)
		# Si la case suivante est un virage, la queue droite ne peut pas le suivre :
		# je la dessine seulement dans son ancienne case, elle a l'air de "rentrer" dans le virage
		if not is_straight(drawn, last - 1):
			old_cell = previous_snake[-1]
			screen.set_clip(pygame.Rect(old_cell[0], old_cell[1], CELL_SIZE, CELL_SIZE))
		screen.blit(tail_images[angle_of(tail_dir)], tail_pos)
		screen.set_clip(None)
	else:
		# Le serpent vient de manger : la queue ne bouge pas pendant ce pas
		screen.blit(segment_image(snake, len(snake) - 1, direction), snake[-1])

	######## Tête (dessinée en dernier pour passer par-dessus le corps)
	head_pos = slide(previous_snake[0], snake[0], shift)
	screen.blit(segment_image(snake, 0, direction), head_pos)

######## Clavier
def add_direction(queue, direction, wanted):
	"""Ajoute la direction wanted à la file d'attente queue, si c'est un vrai changement de direction."""
	# Je compare avec la dernière direction prévue : la dernière de la file, ou la direction actuelle si la file est vide
	if len(queue) > 0:
		last = queue[-1]
	else:
		last = direction
	# Même direction que la dernière prévue : inutile de l'ajouter
	if wanted == last:
		return
	# Demi-tour (direction opposée, ex. (20, 0) et (-20, 0)) : interdit, le serpent rentrerait dans son corps
	if wanted[0] == -last[0] and wanted[1] == -last[1]:
		return
	# File pleine : j'ignore la touche, sinon le serpent jouerait des touches appuyées il y a longtemps
	if len(queue) >= MAX_QUEUED_KEYS:
		return
	queue.append(wanted)

######## Déplacement
def move(snake, direction, food):
	"""Calcule le serpent après un pas dans la direction donnée.
	Renvoie la nouvelle liste du serpent, ou None si le serpent meurt (mur ou corps).
	La liste snake reçue n'est pas modifiée : je travaille sur une copie."""
	######## Calcul de la nouvelle position de la tête
	# Position de la tête
	head_x, head_y = snake[0]
	# Nouvelle position après la détection de la touche du clavier (ancienne position + direction)
	new_head = (head_x + direction[0], head_y + direction[1])

	# Est ce que le serpent va manger à cette nouvelle position ?
	will_grow = new_head == food
	# Copie du corps du serpent pour savoir s'il se mord lui-même
	# .copy() est important : sans lui, body et snake seraient la MÊME liste et body.pop() raccourcirait le serpent original
	body = snake.copy()
	# Si le serpent NE MANGE PAS, je ne prends pas la dernière position de la queue
	# (la queue libère sa case pendant ce tour, la tête a donc le droit d'y aller)
	if not will_grow:
		body.pop()

	######## Collisions
	# Collisions avec les murs ou le corps : fin de partie, retour au menu
	# new_head[0] = x ; new_head[1] = y
	#
	# 1) Les murs : la tête sort de la fenêtre
	#
	#                     new_head[1] < 0 : sortie par le haut
	#                    X  X  X  X  X  X  X  X
	#                 0 +----------------------+
	#    new_head[0]  X |                      | X   new_head[0] >= WIDTH
	#    < 0          X |       fenêtre        | X   sortie par la droite
	#    sortie par   X |                      | X
	#    la gauche     HEIGHT +----------------+
	#                    X  X  X  X  X  X  X  X
	#                     new_head[1] >= HEIGHT : sortie par le bas
	#
	#    Pourquoi ">=" WIDTH et pas ">" : la dernière case commence à x = WIDTH - CELL_SIZE.
	#    Une case qui commence à x = WIDTH est déjà entièrement en dehors de la fenêtre.
	#
	# 2) Le corps : la tête arrive sur une case du serpent
	#
	#    T = tête   o = corps   q = bout de la queue   * = nouvelle case de la tête (new_head)
	#
	#    Cas A : la tête mord son corps => perdu
	#
	#      . o o o . . .        Le serpent descend (la tête vient de la case au-dessus d'elle)
	#      . o . T . . .        La case en dessous de T est un morceau du corps
	#      . o o * o q .   <-   new_head in body => True => return score
	#
	#    Cas B : la tête va sur la case du bout de la queue => autorisé
	#
	#      . T o .              Le serpent allait à gauche, je tourne vers le bas
	#      . * o .         <-   * est la case de q : pendant ce tour, la queue avance et libère sa case
	#                           body.pop() a déjà retiré q de body => new_head in body => False => la partie continue
	if (
		new_head[0] < 0
		or new_head[0] >= WIDTH
		or new_head[1] < 0
		or new_head[1] >= HEIGHT
		# body est calculé ci-dessus
		or new_head in body
	):
		# Le serpent meurt : None veut dire "pas de serpent"
		return None

	######## Nouveau serpent
	new_snake = snake.copy()
	# J'ajoute la nouvelle tête à la première position donc devant...
	new_snake.insert(0, new_head)
	# S'il ne mange pas, je retire la dernière position de la queue => le serpent garde la même longueur
	# S'il mange, je garde la queue => le serpent grandit d'une case
	if not will_grow:
		new_snake.pop()
	return new_snake

######## Partie
def play():
	"""Joue une partie et renvoie le score quand le serpent meurt."""
	# Le serpent est une liste de positions (x, y) en pixels où snake[0] est la tête
	snake = [(START_CELL[0] * CELL_SIZE, START_CELL[1] * CELL_SIZE)]
	# Copie du serpent AVANT son dernier pas : sert à le faire glisser de son ancienne position vers la nouvelle
	previous_snake = snake.copy()
	# Déplacement appliqué à chaque pas : au départ vers la droite
	direction = (CELL_SIZE, 0)
	# File d'attente des flèches appuyées : une direction est utilisée à chaque pas
	# Ex. : en allant à droite, j'appuie très vite sur haut puis gauche => [haut, gauche] : le serpent tourne en haut, PUIS à gauche
	next_directions = []
	food = random_food(snake) # Position de la première nourriture
	score = 0
	# Temps écoulé (en millisecondes) depuis le dernier pas du serpent
	time_since_step = 0
	# True si le coup de pouce (virage en retard) a déjà servi pendant ce pas : un seul par pas
	late_turn_used = False

	# Boucle principale : un passage dans la boucle = une image affichée (FPS fois par seconde)
	# Le serpent, lui, ne change de case que lorsque STEP_TIME millisecondes se sont écoulées
	# Infinie : j'en sors seulement avec "return" (le serpent meurt) ou quit_game() (fenêtre fermée)
	while True:
		######## Gestion des événements (fermeture de la fenêtre et clavier)
		# Pour chaque événement déclenché dans la fenêtre du jeu
		for event in pygame.event.get():
			# Si c'est le bouton fermer la fenêtre (croix rouge)
			if event.type == pygame.QUIT:
				quit_game()
			# Si c'est une touche enfoncée du clavier
			if event.type == pygame.KEYDOWN:
				# Je ne change pas la direction tout de suite : je la range dans la file d'attente
				# None = aucune flèche appuyée
				wanted = None
				# Axe Y inversé
				if event.key == pygame.K_UP:
					wanted = (0, -CELL_SIZE)
				# Axe Y inversé
				if event.key == pygame.K_DOWN:
					wanted = (0, CELL_SIZE)
				if event.key == pygame.K_LEFT:
					wanted = (-CELL_SIZE, 0)
				if event.key == pygame.K_RIGHT:
					wanted = (CELL_SIZE, 0)
				if wanted is not None:
					# Coup de pouce pour la réactivité ("virage en retard") :
					# si la tête vient JUSTE de quitter sa case (début du glissement), le joueur voulait sûrement tourner
					# dans cette case-là. Je refais alors le dernier pas dans la nouvelle direction, au lieu d'attendre le pas suivant.
					#
					#   Sans coup de pouce :          Avec coup de pouce :
					#     . . . *                       . . * .
					#     o o T >                       o o T .     T = case quittée par la tête, > = tête qui glisse
					#   la tête tourne une case         la tête tourne dans la case T
					#   plus loin (*)                   (petit saut de quelques pixels, invisible à l'œil)
					late_turn_done = False
					# Conditions : début du glissement, aucune touche en attente, au moins un pas déjà fait,
					# le dernier pas n'a pas mangé (sinon la nourriture a déjà été déplacée), et pas déjà utilisé pendant ce pas
					just_stepped = time_since_step < STEP_TIME * TURN_GRACE
					has_stepped = previous_snake != snake
					same_length = len(previous_snake) == len(snake)
					if just_stepped and len(next_directions) == 0 and has_stepped and same_length and not late_turn_used:
						# La touche doit être un vrai virage : ni la même direction, ni un demi-tour
						is_same = wanted == direction
						is_reverse = wanted[0] == -direction[0] and wanted[1] == -direction[1]
						if not is_same and not is_reverse:
							# Je refais le dernier pas depuis l'ancien serpent, dans la nouvelle direction
							retry = move(previous_snake, wanted, food)
							# Si ce nouveau pas tue le serpent, j'oublie le coup de pouce (la touche ira dans la file d'attente)
							if retry is not None:
								snake = retry
								direction = wanted
								late_turn_done = True
								late_turn_used = True
								# Ce nouveau pas peut tomber sur la nourriture
								if len(snake) > len(previous_snake):
									score += 1
									food = random_food(snake)
					# Sinon, comme avant : la touche attend le prochain pas
					if not late_turn_done:
						add_direction(next_directions, direction, wanted)

		######## Pas du serpent (seulement quand assez de temps s'est écoulé)
		if time_since_step >= STEP_TIME:
			# Je retire la durée d'un pas (et pas tout le temps écoulé) pour garder un rythme régulier
			time_since_step = time_since_step - STEP_TIME
			# Nouveau pas : le coup de pouce est de nouveau disponible
			late_turn_used = False

			# Je prends la prochaine direction de la file d'attente, s'il y en a une
			# pop(0) enlève et renvoie le PREMIER élément de la liste (le plus ancien)
			if len(next_directions) > 0:
				direction = next_directions.pop(0)

			# Je calcule le serpent après ce pas (None = il est mort)
			new_snake = move(snake, direction, food)
			if new_snake is None:
				return score

			######## Déplacement du serpent
			# Je garde le serpent d'avant le pas, pour le faire glisser pendant l'affichage
			previous_snake = snake
			snake = new_snake

			# Le serpent est plus long qu'avant : il a mangé
			if len(snake) > len(previous_snake):
				score += 1
				food = random_food(snake)

		######## Affichage
		# Fond gris très foncé (efface aussi tout ce qui a été dessiné à la frame précédente)
		screen.fill(BG_COLOR)

		# Grille légèrement visible
		#
		#  x = 0    20   40   60  ...  WIDTH
		#      |    |    |    |
		#  y=0 +----+----+----+---  <- ligne de (0, y) à (WIDTH, y)
		#      |    |    |    |
		#  20  +----+----+----+---
		#      |    |    |    |
		#  40  +----+----+----+---
		#      ^
		#      ligne de (x, 0) à (x, HEIGHT)
		#
		# range(0, WIDTH, CELL_SIZE) donne 0, 20, 40, etc. => une ligne tous les CELL_SIZE pixels
		for x in range(0, WIDTH, CELL_SIZE):
			pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, CELL_SIZE):
			pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

		# Nourriture : l'image du biscuit, centrée dans sa case (// 2 veut dire une division entière)
		offset = (CELL_SIZE - FOOD_SIZE) // 2
		screen.blit(food_image, (food[0] + offset, food[1] + offset))

		# Avancement entre deux pas : 0 = le serpent vient de changer de case, 1 = le prochain pas arrive
		progress = time_since_step / STEP_TIME
		# Si l'ordinateur a pris du retard, progress peut dépasser 1 : je le bloque à 1 pour ne pas dépasser la case
		if progress > 1:
			progress = 1
		# Nombre de pixels déjà parcourus vers la case suivante (int() garde seulement la partie entière)
		shift = int(CELL_SIZE * progress)

		# Serpent : le corps sur ses cases, la tête et la queue décalées de shift pixels
		draw_snake(snake, previous_snake, direction, shift)

		# Score en haut à gauche
		# le f devant la chaine de caractères permet d'insérer le score avec {score}
		score_surf = font.render(f"Score : {score}", True, TEXT_COLOR)
		screen.blit(score_surf, SCORE_PADDING)

		# Affiche l'image dessinée à l'écran
		pygame.display.flip()
		# Limite à FPS images par seconde
		# clock.tick renvoie le temps (en millisecondes) écoulé depuis son dernier appel : je l'ajoute au compteur du pas
		time_since_step = time_since_step + clock.tick(FPS)

######## Programme principal
def main():
	"""Alterne entre le menu et les parties, jusqu'à ce que le joueur quitte."""
	last_score = None  # Pas de score à afficher au tout premier menu
	# menu() renvoie Vrai pour Jouer, Faux pour Quitter
	# Je donne au menu la fenêtre, l'horloge et la police déjà créées ici : il n'a pas à les refaire
	while menu(screen, clock, font, last_score):
		last_score = play()
	quit_game()

######## Lancement
# Je lance le jeu seulement si ce fichier est exécuté directement
# __name__ vaut "__main__" quand je lance "python snake.py", mais vaut "snake" si un autre fichier fait "import snake"
# Ça évite que le jeu démarre tout seul quand un autre fichier importe celui-ci (pour le tester par exemple)
if __name__ == "__main__":
	main()
