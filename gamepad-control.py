import pygame
import time
from adafruit_servokit import ServoKit


class ShanWanController:
    def __init__(self):
        # Initialisation de pygame et du joystick
        pygame.init()
        pygame.joystick.init()

        # Configuration de la manette
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        # Configuration du kit servo
        self.kit = ServoKit(channels=16)

        # Paramètres de contrôle (à ajuster selon vos besoins)
        self.max_throttle = 0.3  # Vitesse maximum
        self.max_steering = 0.5  # Angle maximum de direction

        print("Contrôleur initialisé")
        print("Utilisez le stick gauche pour diriger")
        print("Utilisez les gâchettes pour accélérer/freiner")
        print("Appuyez sur X pour quitter")

    def map_range(self, x, in_min, in_max, out_min, out_max):
        """Fonction utilitaire pour mapper une valeur d'une plage à une autre"""
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    def get_controls(self):
        """Lecture des contrôles de la manette"""
        pygame.event.pump()

        # Lecture de la direction (stick gauche, axe 0)
        steering = self.joystick.get_axis(0)

        # Lecture de l'accélération (gâchettes, axes 2 et 5)
        throttle_forward = -max(0, -self.joystick.get_axis(5))  # Gâchette droite
        throttle_reverse = max(0, -self.joystick.get_axis(2))  # Gâchette gauche
        throttle = throttle_forward + throttle_reverse

        # Bouton X (3) pour quitter
        quit_button = self.joystick.get_button(3)

        return steering, throttle, quit_button

    def apply_controls(self, steering, throttle):
        """Application des contrôles au robot"""
        # Conversion des valeurs de la manette en commandes pour les servos
        steering_value = int(90 + (steering * 45 * self.max_steering))  # 45-135 degrés
        throttle_value = throttle * self.max_throttle

        # Application des commandes
        self.kit.servo[0].angle = steering_value  # Direction
        self.kit.continuous_servo[1].throttle = throttle_value  # Vitesse

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


if __name__ == "__main__":
    controller = ShanWanController()
    controller.run()
