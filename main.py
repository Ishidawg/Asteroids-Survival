import pygame
from pygame import mixer
from random import randint, uniform
import sys

def laser_shoot(laser_list, speed = 500):
	for rect in laser_list:
		rect.y -= round(speed * dt)
		if rect.bottom < 0:
			laser_list.remove(rect)

def asteroid_update(asteroids_list, speed = 300):
	for asteroid_tuple in asteroids_list:
		direction = asteroid_tuple[1]
		asteroid_rect = asteroid_tuple[0]
		asteroid_rect.center += direction * speed * dt
		if asteroid_rect.top > screen_height:
			asteroids_list.remove(asteroid_tuple)

def score_props():
	message = None

	if points == 25:
		message = '25 Points!'

	if points == 50:
		message = '50 Points!'

	if points == 100:
		message = 'Insane!!!'

	if points == 200:
		message = 'Are you alright?'

	if points == 210:
		message	= 'Exit on 10secs'

	if points == 215:
		sys.exit()

	score_props_txt = f'{message}'
	txt_surface = font_middle.render(message, False, 'White')
	display_surface.blit(txt_surface, (screen_widht / 2.5, screen_height / 2)) 


def display_time():
	time = f'Time: {round(pygame.time.get_ticks() / 1000)}s'
	txt_surface = font.render(time , False, 'White')
	display_surface.blit(txt_surface, (50, 50))

def laser_timer(shoot, duration = 500):
	if not shoot:
		current_time = pygame.time.get_ticks()
		if current_time - shoot_time > duration:
			shoot = True
	return shoot

# all game init and display settings
pygame.init()
game_running = True
screen_widht, screen_height = 1280, 720
display_surface = pygame.display.set_mode((screen_widht, screen_height))
pygame.display.set_caption("Asteroids Survive")
pygame.display.set_icon(pygame.image.load('assets/spaceship.png'))
clock = pygame.time.Clock()

# assets and collision
background = pygame.image.load('assets/backgroundfilter.png').convert()

	# spaceship
spaceship_surface = pygame.image.load('assets/spaceship.png').convert_alpha()
spaceship_rect = spaceship_surface.get_rect(center = (screen_widht / 2, screen_height / 1.2))

	# asteroids
asteroids_surface = pygame.image.load('assets/asteroidbrown.png').convert_alpha()
asteroids_list = []

	# laser
laser_surface = pygame.image.load('assets/laserbeam.png').convert_alpha()
laser_list = []

# laser time
shoot = True
shoot_time = None

# font
font = pygame.font.Font('font/Minecraft.ttf', 34)
font_middle = pygame.font.Font('font/Minecraft.ttf', 50)

# asteroid time
asteroid_timer = pygame.event.custom_type()
pygame.time.set_timer(asteroid_timer, 140)

# song settings
mixer.init()
mixer.music.load('songs/coolsong.wav')
mixer.music.set_volume(0.04)
mixer.music.play()

# score
points = 0

while game_running:

	for event in pygame.event.get():

	# exit
		if event.type == pygame.QUIT:
			game_running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				game_running = False

		# shoot
		if event.type == pygame.MOUSEBUTTONDOWN and shoot:
			
			# laser
			laser_rect = laser_surface.get_rect(midbottom = spaceship_rect.midtop)
			laser_list.append(laser_rect)

			# *peww* song
			laser_fx = mixer.Sound('songs/laser.wav')
			laser_fx.set_volume(0.12)
			laser_fx.play()

			# shoot time
			shoot = False
			shoot_time = pygame.time.get_ticks()


		if event.type == asteroid_timer:
			random_x = randint(-100, screen_widht + 100)
			random_y = randint(-100, -50) 

			asteroid_rect = asteroids_surface.get_rect(center = (random_x, random_y))

			direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)

			asteroids_list.append((asteroid_rect, direction))

	# frames per second | Framerate
	dt = clock.tick(120) / 1000

	# movement
	spaceship_rect.center = pygame.mouse.get_pos()
	laser_shoot(laser_list)
	asteroid_update(asteroids_list)
	shoot = laser_timer(shoot, 220)

	# asteroid and ship collision
	for asteroid_tuple in asteroids_list:
		asteroid_rect = asteroid_tuple[0]

		if spaceship_rect.colliderect(asteroid_rect):
			# *boom* song
			damage_fx = mixer.Sound('songs/explosion2.mp3')
			damage_fx.set_volume(0.02)
			damage_fx.play()

	# laser and asteroids collision
	for laser_rect in laser_list:
		for asteroid_tuple in asteroids_list:
			if laser_rect.colliderect(asteroid_tuple[0]):
				asteroids_list.remove(asteroid_tuple)
				laser_list.remove(laser_rect)

				collide_fx = mixer.Sound('songs/explosion.wav')
				collide_fx.set_volume(0.02)
				collide_fx.play()

				points = points + 1

	# updates text/assets
	display_surface.fill((0, 0, 0))
	display_surface.blit(background, (0, 0))

	display_surface.blit(spaceship_surface, spaceship_rect)
	
	for rect in laser_list:
		display_surface.blit(laser_surface, rect)

	for asteroid_tuple in asteroids_list:
		display_surface.blit(asteroids_surface, asteroid_tuple[0])

	# text
	display_time()
	score_txt = font.render(f'Score: {points}' , False, 'White')
	display_surface.blit(score_txt, (240, 50))
	score_props()

	pygame.display.update()