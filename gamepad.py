import time
from adafruit_servokit import ServoKit
from icecream import ic

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def check():

    pygame.init()
    pygame.joystick.init()

    ic(f"number : {pygame.joystick.get_count()}")

    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        # ic(f"Nom de la manette : {joystick.get_name()}")
        # ic(f"Nombre d'axes : {joystick.get_numaxes()}")
        # ic(f"Nombre de boutons : {joystick.get_numbuttons()}")
    pygame.quit()
    
class ShanWanController:
    def __init__(self):
  

        # Configuration du kit servo
        self.kit = ServoKit(channels=16)
        print("Test du moteur...")
        self.kit.continuous_servo[1].throttle = 0.2
        time.sleep(1)
        self.kit.continuous_servo[1].throttle = 0
        print("Test terminé")
        print("Test des canaux...")
        for i in [0, 1]:
            try:
                self.kit.continuous_servo[i].throttle = 0
                print(f"Canal {i} OK")
            except Exception as e:
                print(f"Erreur sur canal {i}: {e}")
                
        self.max_throttle = 0.4  # Augmenté pour plus de réponse
        self.max_steering = -0.65  # Valeur négative pour corriger le sens
        
        # Initialisation des moteurs à 0
        self.kit.continuous_servo[0].throttle = 0
        self.kit.continuous_servo[1].throttle = 0
        # Initialisation de pygame et du joystick
        pygame.init()
        pygame.joystick.init()

        # Configuration de la manette
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        print("Contrôleur initialisé")
        print("Utilisez le stick gauche pour diriger")
        print("Utilisez les gâchettes pour accélérer/freiner")
        print("Appuyez sur X pour quitter")


    def get_controls(self):
        """Lecture des contrôles de la manette"""
        pygame.event.pump()

        # Direction (stick gauche)
        steering = self.joystick.get_axis(0)  

        # Accélération (gâchettes)
        # Mapping différent pour les gâchettes
        throttle_forward = (1 - self.joystick.get_axis(5)) / 2  # Gâchette droite
        throttle_reverse = -(1 - self.joystick.get_axis(2)) / 2  # Gâchette gauche
        throttle = throttle_forward + throttle_reverse

        quit_button = self.joystick.get_button(3)
        return steering, throttle, quit_button
    
    
    # def get_controls(self):
    #     """Lecture des contrôles de la manette"""
    #     pygame.event.pump()

    #     # Lecture de la direction (stick gauche, axe 0)
    #     steering = self.joystick.get_axis(0)

    #     # Lecture de l'accélération (gâchettes, axes 2 et 5)
    #     throttle_forward = -max(0, -self.joystick.get_axis(5))  # Gâchette droite
    #     throttle_reverse = max(0, -self.joystick.get_axis(2))  # Gâchette gauche
    #     throttle = throttle_forward + throttle_reverse

    #     # Bouton X (3) pour quitter
    #     quit_button = self.joystick.get_button(3)

        # return steering, throttle, quit_button
    def apply_controls(self, steering, throttle):
        """Application des contrôles au robot"""
        # Les servos du JetRacer sont des continuous_servo, pas des servo normaux
        # pour la direction
        steering_value = steering * self.max_steering
        self.kit.continuous_servo[0].throttle = steering_value
        
        # pour l'accélération 
        throttle_value = throttle * self.max_throttle
        self.kit.continuous_servo[1].throttle = throttle_value
        
        # print(f"Debug - Steering: {steering_value:.2f}, Throttle: {throttle_value:.2f}")

    # def apply_controls(self, steering, throttle):
    #     """Application des contrôles au robot"""
    #     # Conversion des valeurs de la manette en commandes pour les servos
    #     steering_value = int(90 + (steering * 45 * self.max_steering))  # 45-135 degrés
    #     throttle_value = throttle * self.max_throttle

    #     # Application des commandes
    #     self.kit.servo[0].angle = steering_value  # Direction
    #     self.kit.continuous_servo[1].throttle = throttle_value  # Vitesse

    def run(self):
        """Boucle principale"""
        running = True
        try:
            while running:
                # Lecture des contrôles
                steering, throttle, quit_button = self.get_controls()

                # Vérification du bouton de sortie
                if quit_button:
                    running = False

                # Application des contrôles
                self.apply_controls(steering, throttle)

                # Affichage des valeurs pour le debugging
                print(f"Direction: {steering:.2f} | Vitesse: {throttle:.2f}", end="\r")

                time.sleep(0.02)  # 50Hz refresh rate

        except KeyboardInterrupt:
            pass
        finally:
            # Arrêt sécurisé
            self.kit.continuous_servo[1].throttle = 0
            self.kit.servo[0].angle = 90
            print("\nArrêt du contrôleur")


