from icecream import ic
from gamepad import ShanWanController, check 
from adafruit_platformdetect.constants import chips
from jetracer.nvidia_racecar import NvidiaRacecar


# main

if __name__ == "__main__":
    # check()
    # ic(dir(chips))  #
    # controller = ShanWanController()
    # controller.run()
    car = NvidiaRacecar()
    ic(car)
    car.steering_motor.throttle = 0.5
    car.throttle_motor.throttle = 0.5
    car.steering_motor.throttle = 0.0
    car.throttle_motor.throttle = 0.0