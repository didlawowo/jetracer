import pygame

pygame.init()
pygame.joystick.init()

# Afficher le nombre de manettes détectées
print(f"Nombre de manettes détectées : {pygame.joystick.get_count()}")

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"Nom de la manette : {joystick.get_name()}")
    print(f"Nombre d'axes : {joystick.get_numaxes()}")
    print(f"Nombre de boutons : {joystick.get_numbuttons()}")
