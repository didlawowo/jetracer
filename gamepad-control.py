import pygame
import time
import board
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit


class USBGamepadController:
    def __init__(self):
        # Initialiser pygame et le joystick
        pygame.init()
        pygame.joystick.init()

        # Vérifier si une manette est connectée
        if pygame.joystick.get_count() == 0:
            raise RuntimeError("Aucune manette USB détectée")

        # Initialiser la première manette trouvée
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        print(f"Manette détectée : {self.joystick.get_name()}")
        print(f"Nombre d'axes : {self.joystick.get_numaxes()}")
        print(f"Nombre de boutons : {self.joystick.get_numbuttons()}")

        # Initialiser le contrôleur PCA9685
        i2c = busio.I2C(board.SCL, board.SDA)
        self.kit = ServoKit(channels=16)

        # Configuration des moteurs
        self.steering_channel = 0  # Canal pour la direction
        self.throttle_channel = 1  # Canal pour l'accélération

        # Paramètres de contrôle
        self.max_speed = 0.3  # Vitesse maximum (0 à 1)
        self.max_steering = 0.7  # Angle maximum de direction

    def test_controls(self):
        """Test des contrôles de base"""
        print("Test des contrôles... Appuyez sur les boutons et bougez les joysticks")
        try:
            while True:
                pygame.event.pump()

                # Afficher l'état des axes
                for i in range(self.joystick.get_numaxes()):
                    axis_val = self.joystick.get_axis(i)
                    if abs(axis_val) > 0.1:  # Filtrer le bruit
                        print(f"Axe {i}: {axis_val:.2f}")

                # Afficher les boutons pressés
                for i in range(self.joystick.get_numbuttons()):
                    if self.joystick.get_button(i):
                        print(f"Bouton {i} pressé")

                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nTest terminé")

    def update(self):
        """Mise à jour des commandes de la voiture"""
        pygame.event.pump()

        # Lecture des axes (peut nécessiter ajustement selon votre manette)
        throttle = -self.joystick.get_axis(1)  # Inverser pour que haut soit positif
        steering = self.joystick.get_axis(0)

        # Appliquer les limites
        throttle = throttle * self.max_speed
        steering = steering * self.max_steering

        # Convertir en valeurs pour les servos/moteurs
        throttle_value = int(1500 + (throttle * 500))  # 1000-2000 µs
        steering_value = int(90 + (steering * 45))  # 45-135 degrés

        # Appliquer les commandes
        self.kit.servo[self.steering_channel].angle = steering_value
        self.kit.continuous_servo[self.throttle_channel].throttle = throttle

    def run(self):
        """Boucle principale"""
        print("Contrôle par manette activé. Ctrl+C pour quitter")
        try:
            while True:
                self.update()
                time.sleep(0.02)  # 50Hz refresh rate

        except KeyboardInterrupt:
            print("\nArrêt du programme")
            # Arrêter la voiture
            self.kit.continuous_servo[self.throttle_channel].throttle = 0
            self.kit.servo[self.steering_channel].angle = 90


if __name__ == "__main__":
    controller = USBGamepadController()
    # Décommenter pour tester les contrôles
    # controller.test_controls()
    controller.run()
