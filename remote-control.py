import pygame
import jetracer.nvidia_racecar as rc


class GamepadController:
    def __init__(self):
        # Initialiser pygame et le joystick
        pygame.init()
        pygame.joystick.init()

        # Vérifier si une manette est connectée
        if pygame.joystick.get_count() == 0:
            raise RuntimeError("Aucune manette détectée")

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        # Initialiser la voiture
        self.car = rc.NvidiaRacecar()

        # Paramètres de contrôle
        self.max_speed = 0.3  # Vitesse maximum (0 à 1)
        self.max_steering = 0.7  # Angle de braquage maximum

    def update(self):
        pygame.event.pump()  # Traiter les événements pygame

        # Lire les axes de la manette
        # L'axe 1 est généralement l'accélérateur/frein
        # L'axe 0 est généralement la direction gauche/droite
        throttle = -self.joystick.get_axis(
            1
        )  # Inverser pour que vers le haut soit positif
        steering = self.joystick.get_axis(0)

        # Appliquer les limites de vitesse et de direction
        throttle = throttle * self.max_speed
        steering = steering * self.max_steering

        # Mettre à jour les commandes de la voiture
        self.car.throttle = throttle
        self.car.steering = steering

    def run(self):
        try:
            print("Contrôle par manette activé. Appuyez sur Ctrl+C pour quitter.")
            while True:
                self.update()
                pygame.time.wait(10)  # Petit délai pour ne pas surcharger le CPU

        except KeyboardInterrupt:
            print("\nArrêt du programme")
            # Arrêter la voiture
            self.car.throttle = 0
            self.car.steering = 0

        finally:
            pygame.quit()


if __name__ == "__main__":
    controller = GamepadController()
    controller.run()
