import pygame
import random
from car3 import Car  # Import the logic-only Car class

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1800, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Single-Lane Car Simulation")

# Colors for background and road
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

# Road properties
ROAD_HEIGHT = 100
ROAD_Y = HEIGHT // 2 - ROAD_HEIGHT // 2  # Center the road vertically
CAR_SPAWN_DELAY = 300  # Time in milliseconds between car spawns
SAFE_SPAWN_DISTANCE = 60  # Minimum distance required to spawn a new car

# List to store cars and spawn timer
cars = []
last_car_spawn_time = pygame.time.get_ticks()  # Track time of last car spawn

# Variable to track selected car
selected_car = None

# Main loop
running = True
clock = pygame.time.Clock()  # Control frame rate

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if any car was clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for car in cars:
                car_rect = pygame.Rect(car._position, car.y, car.width, car.height)
                if car_rect.collidepoint(mouse_x, mouse_y):
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_w]:
                        car.original_speed = car.original_speed + 0.5
                    if pressed[pygame.K_s]:
                        if car.braking == False:
                            car.brake(True,0.005)
                        else:
                            car.brake(False,0.005)
                    selected_car = car
                    break  # Stop checking after finding the clicked car
    # Fill background with white color
    screen.fill(WHITE)

    # Draw the road as a gray rectangle
    pygame.draw.rect(screen, GRAY, (0, ROAD_Y, WIDTH, ROAD_HEIGHT))

    # Spawn a new car if enough time has passed and the spawn area is clear
    current_time = pygame.time.get_ticks()
    if current_time - last_car_spawn_time > CAR_SPAWN_DELAY:
        # Check if there's enough space at the spawn point
        # No car should be within SAFE_SPAWN_DISTANCE
        can_spawn = all(car._position > SAFE_SPAWN_DISTANCE for car in cars)
        if can_spawn:
            new_car = Car()  # Create a new Car object (logic only)
            new_car.y = ROAD_Y + ROAD_HEIGHT // 2 - new_car.height // 2  # Set vertical position
            cars.append(new_car)
            last_car_spawn_time = current_time  # Update the last car spawn time

    # Move, check collision, and draw each car
    for i in range(len(cars) - 1, -1, -1):  # Loop backwards to safely remove cars
        car = cars[i]

        # Check for collision with the car in front
        car_in_front = cars[i - 1] if i > 0 else None  # Car in front, if it exists
        car.check_collision_and_adjust_speed(car_in_front)  # Slow down if too close

        # Draw the car as a rectangle on the screen
        pygame.draw.rect(screen, (car.color_r, car.color_g, car.color_b),
                         (car._position, car.y, car.width, car.height))

        # Remove (despawn) car if it reaches the end of the road
        if car._position >= WIDTH:
            cars.pop(i)  # Remove car from the list

    # Display the speed of the selected car
    if selected_car:
        font = pygame.font.Font(None, 36)
        speed_text = font.render(f"Speed {selected_car.reference_speed}", True, (0, 0, 0))
        screen.blit(speed_text, (10, 10))

    # Update the screen
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

# Quit Pygame
pygame.quit()
