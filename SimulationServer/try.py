import pygame
import random
from car2 import Car  # Import the logic-only Car class

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Single-Lane Car Simulation")

# Colors for background and road
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

# Road properties
ROAD_HEIGHT = 100
ROAD_Y = HEIGHT // 2 - ROAD_HEIGHT // 2  # Center the road vertically
CAR_SPAWN_DELAY = 1000  # Time in milliseconds between car spawns

# List to store cars and spawn timer
cars = []
last_car_spawn_time = pygame.time.get_ticks()  # Track time of last car spawn

# Main loop
running = True
clock = pygame.time.Clock()  # Control frame rate

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background with white color
    screen.fill(WHITE)

    # Draw the road as a gray rectangle
    pygame.draw.rect(screen, GRAY, (0, ROAD_Y, WIDTH, ROAD_HEIGHT))

    # Spawn a new car if enough time has passed
    current_time = pygame.time.get_ticks()
    if current_time - last_car_spawn_time > CAR_SPAWN_DELAY:
        speed = random.randint(2, 5)  # Random speed for each car
        new_car = Car(speed)  # Create a new Car object (logic only)
        new_car.y = ROAD_Y + ROAD_HEIGHT // 2 - new_car.height // 2  # Set vertical position
        cars.append(new_car)
        last_car_spawn_time = current_time  # Update the last car spawn time

    # Move, check collision, and draw each car
    for i in range(len(cars) - 1, -1, -1):  # Loop backwards to safely remove cars
        car = cars[i]
        
        # Check for collision with the car in front
        car_in_front = cars[i - 1] if i > 0 else None  # Car in front, if it exists
        
        car.check_collision_and_slow_down(car_in_front)  # Slow down if too close
        

        # Draw the car as a rectangle on the screen
        pygame.draw.rect(screen, (255, 0, 0), (car.x, car.y, car.width, car.height))

        # Print car's position on a 0–1000 scale for debugging
        #print(f"Car position (0-1000): {car.get_position()}")

        # Remove (despawn) car if it reaches the end of the road
        if car.get_position() >= 1000:
            cars.pop(i)  # Remove car from the list

    # Update the screen
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

# Quit Pygame
pygame.quit()
