import os
import random
import cv2
import numpy as np
import pygame
import tensorflow as tf

# 1. Chargi l-model li darrabti
MODEL_PATH = "autopilot_model.keras"
DATA_DIR = "../gtsrb"
model = tf.keras.models.load_model(MODEL_PATH)

# 2. L-ma3ani dyal chi blakat men GTSRB (0 tal 42)
SIGN_RULES = {
    1:  {"name": "Speed Limit 30", "speed": 2.0, "action": "Slowing down to 30"},
    5:  {"name": "Speed Limit 80", "speed": 6.0, "action": "Accelerating to 80"},
    14: {"name": "STOP",           "speed": 0.0, "action": "Stopping for 2s!"},
    17: {"name": "No Entry",       "speed": 0.0, "action": "HALT! Road Closed"},
}

def get_random_sign():
    """Kat-jib tswira haqiqiya men dataset gtsrb"""
    class_id = random.choice(list(SIGN_RULES.keys()))
    folder = os.path.join(DATA_DIR, str(class_id))
    img_name = random.choice(os.listdir(folder))
    img_path = os.path.join(folder, img_name)

    # Qra tswira b OpenCV (BGR) bach t-douz l-AI
    cv_img = cv2.imread(img_path)
    cv_img_resized = cv2.resize(cv_img, (30, 30))

    # Qadd tswira bach t-ban f Pygame (RGB)
    rgb_img = cv2.cvtColor(cv2.resize(cv_img, (80, 80)), cv2.COLOR_BGR2RGB)
    py_surface = pygame.surfarray.make_surface(np.transpose(rgb_img, (1, 0, 2)))

    return cv_img_resized, py_surface

# 3. I3dadat dyal Pygame
pygame.init()
WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CS50 AI - Autopilot Simulation")
font = pygame.font.SysFont("Arial", 22, bold=True)
clock = pygame.time.Clock()

# L-halat dyal tomobil
car_x = 100
car_speed = 4.0
target_speed = 4.0
sign_x = 650
stop_timer = 0
detected = False
ai_status = "Cruising..."
confidence_text = ""

cv_sign, py_sign = get_random_sign()

running = True

def draw_tesla(surface, x, y, is_braking):
    # L-jism dyal Tesla (Body - Red Multi-Coat)
    pygame.draw.rect(surface, (210, 20, 40), (x, y + 18, 125, 26), border_radius=8)
    # S-sqaf dyal Tesla (Aerodynamic glass roof)
    roof_points = [(x + 22, y + 18), (x + 42, y + 3), (x + 88, y + 3), (x + 108, y + 18)]
    pygame.draw.polygon(surface, (20, 25, 35), roof_points)
    pygame.draw.polygon(surface, (210, 20, 40), roof_points, 2)

    # R-rwayd (Wheels + Jantes)
    for wx in (x + 26, x + 98):
        pygame.draw.circle(surface, (15, 15, 15), (wx, y + 44), 13)
        pygame.draw.circle(surface, (180, 180, 190), (wx, y + 44), 6)

    # L-farat l-amamiya (LED Headlights)
    pygame.draw.ellipse(surface, (220, 245, 255), (x + 116, y + 22, 10, 6))

    # L-farat l-khalfiya (Brake lights - kay-cha3lo b l-hmer mli kat-frani!)
    brake_color = (255, 0, 0) if is_braking else (120, 0, 0)
    pygame.draw.rect(surface, brake_color, (x - 2, y + 21, 5, 10), border_radius=2)

road_offset = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 4. L-Autopilot kay-chof l-blaka mli kat-qerreb (masafa < 250px)
    distance = sign_x - car_x
    if 0 < distance < 250 and not detected:
        input_tensor = np.expand_dims(cv_sign, axis=0)
        prediction = model.predict(input_tensor, verbose=0)
        predicted_class = int(np.argmax(prediction))
        confidence = np.max(prediction) * 100

        if predicted_class in SIGN_RULES:
            rule = SIGN_RULES[predicted_class]
            target_speed = rule["speed"]
            ai_status = f"AI Saw: {rule['name']} -> {rule['action']}"
            confidence_text = f"Confidence: {confidence:.1f}%"
            if predicted_class in (14, 17):  # STOP awla No Entry
                stop_timer = 120
        else:
            ai_status = f"AI Saw Class {predicted_class} (Ignored)"

        detected = True

    # 5. T-tahakkom f s-sor3a dyal tomobil
    if stop_timer > 0:
        car_speed = 0
        stop_timer -= 1
        if stop_timer == 0:
            target_speed = 4.0
            ai_status = "Stop complete. Resuming..."
    else:
        if car_speed < target_speed:
            car_speed = min(car_speed + 0.1, target_speed)
        elif car_speed > target_speed:
            car_speed = max(car_speed - 0.2, target_speed)

    # Harrek l-blaka w l-khtout dyal triq
    sign_x -= car_speed
    road_offset = (road_offset - car_speed) % 80
    if sign_x < -100:
        sign_x = 850
        detected = False
        cv_sign, py_sign = get_random_sign()

    # 6. Rsem l-ecran (Triq, Tesla, Blaka, Dashboard)
    screen.fill((34, 139, 34))  # L-khadoura
    pygame.draw.rect(screen, (50, 50, 50), (0, 250, WIDTH, 140))  # T-triq

    # L-khtout l-bida l-m-qatt3a dyal triq (kay-tharrko!)
    for lx in range(-80, WIDTH + 80, 80):
        pygame.draw.rect(screen, (255, 255, 255), (lx + road_offset, 316, 45, 6))

    # L-blaka f jnab t-triq (kamla te7t dashboard)
    pygame.draw.rect(screen, (150, 150, 150), (sign_x + 35, 180, 10, 70))
    screen.blit(py_sign, (sign_x, 105))

    # Tesla Autopilot
    is_braking = (car_speed > target_speed) or (stop_timer > 0)
    draw_tesla(screen, car_x, 272, is_braking)

    # Radar dyal Autopilot
    if not detected:
        pygame.draw.polygon(screen, (0, 255, 255), [(car_x + 125, 294), (car_x + 260, 130), (car_x + 260, 325)], 2)

    # Dashboard l-fouq
    pygame.draw.rect(screen, (20, 20, 30), (0, 0, WIDTH, 90))
    status_surf = font.render(ai_status, True, (0, 255, 127))
    speed_surf = font.render(f"Speed: {car_speed * 15:.0f} km/h   |   {confidence_text}", True, (255, 255, 255))
    screen.blit(status_surf, (20, 15))
    screen.blit(speed_surf, (20, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
