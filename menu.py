"""Menu d'accueil du Snake : boutons Jouer et Quitter.
Ce fichier ne crée pas sa propre fenêtre : il reçoit celle du jeu
(screen, clock, font) en paramètres, depuis snake.py.
Je le garde dans un fichier à part pour que snake.py ne s'occupe que de la partie.
"""

######## Imports
import pygame										# pygame-ce (installé avec "pip install pygame-ce", mais importé sous le nom pygame)

from constants import *								# Couleurs, tailles des boutons, positions du titre et du score

######## Bouton
def draw_button(screen, font, rect, text, hovered):
	"""Dessine un bouton arrondi avec son texte centré ; plus clair si survolé."""
	# hovered vaut True quand la souris est sur le bouton
	if hovered:
		color = BUTTON_HOVER_COLOR
	else:
		color = BUTTON_COLOR
	# Fond du bouton : rectangle plein aux coins arrondis
	pygame.draw.rect(screen, color, rect, border_radius=BUTTON_RADIUS)
	# Bordure verte : même rectangle, mais width=BUTTON_BORDER dessine seulement le contour
	pygame.draw.rect(screen, BUTTON_BORDER_COLOR, rect, width=BUTTON_BORDER, border_radius=BUTTON_RADIUS)
	# Texte : je le transforme en Surface, puis je le colle au centre du bouton
	# get_rect(center=...) me donne le rectangle du texte, placé avec son centre au point voulu
	text_surf = font.render(text, True, TEXT_COLOR)
	screen.blit(text_surf, text_surf.get_rect(center=rect.center))

######## Menu
def menu(screen, clock, font, last_score=None):
	"""Affiche le menu jusqu'à ce que le joueur choisisse.

	Renvoie True s'il clique sur Jouer, False s'il veut quitter.
	"""
	width = screen.get_width()  # Largeur de la fenêtre, pour centrer
	title_font = pygame.font.SysFont(None, TITLE_FONT_SIZE)  # Grande police pour le titre

	# Rectangles des boutons, centrés horizontalement
	# pygame.Rect(x, y, largeur, hauteur) ; x = (largeur fenêtre - largeur bouton) // 2 pour centrer
	play_button = pygame.Rect((width - BUTTON_W) // 2, PLAY_BUTTON_Y, BUTTON_W, BUTTON_H)
	quit_button = pygame.Rect((width - BUTTON_W) // 2, QUIT_BUTTON_Y, BUTTON_W, BUTTON_H)

	# Boucle du menu : je redessine le menu jusqu'à ce que le joueur choisisse (return)
	while True:
		mouse_pos = pygame.mouse.get_pos()			# Position (x, y) de la souris dans la fenêtre

		######## Gestion des événements (souris, clavier, fermeture)
		for event in pygame.event.get():
			# Fermeture de la fenêtre = quitter
			if event.type == pygame.QUIT:
				return False
			# Clic gauche (bouton 1 de la souris) : je regarde sur quel bouton il tombe
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				# collidepoint vérifie si un point (ici le clic) est dans le rectangle
				if play_button.collidepoint(event.pos):
					return True
				if quit_button.collidepoint(event.pos):
					return False
			# Raccourcis clavier : Entrée pour jouer, Échap pour quitter
			if event.type == pygame.KEYDOWN:
				# K_RETURN = Entrée du clavier principal, K_KP_ENTER = Entrée du pavé numérique
				if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
					return True
				if event.key == pygame.K_ESCAPE:
					return False

		######## Affichage
		screen.fill(BG_COLOR)

		# Titre centré en haut
		title_surf = title_font.render(TITLE, True, TITLE_COLOR)
		screen.blit(title_surf, title_surf.get_rect(center=(width // 2, TITLE_Y)))

		# Après une partie, je rappelle le score obtenu (None = aucune partie jouée)
		if last_score is not None:
			score_surf = font.render(f"Score : {last_score}", True, TEXT_COLOR)
			screen.blit(score_surf, score_surf.get_rect(center=(width // 2, SCORE_Y)))

		# Le dernier paramètre vaut True si la souris est sur le bouton : il s'éclaircit
		draw_button(screen, font, play_button, "Jouer", play_button.collidepoint(mouse_pos))
		draw_button(screen, font, quit_button, "Quitter", quit_button.collidepoint(mouse_pos))

		pygame.display.flip()
		clock.tick(MENU_FPS)  # Le menu n'a pas besoin de tourner plus vite
