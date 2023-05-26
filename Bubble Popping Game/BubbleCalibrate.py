# Import all required libraries
import pygame
import SceneManager
import numpy as np
import cv2
import mediapipe as mp
import random
from Button import ButtonImg
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

# Define the game scene
def Game():
    # Initialize the Pygame
    pygame.init()
    pygame.event.clear()

    # Define mediapipe functions
    mp_draw = mp.solutions.drawing_utils
    mp_draw_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Create window/display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Thesis Project Game")

    # Load all required images
    imgBackground = pygame.image.load("Resources/Bubble/BubblePopBackground.png").convert()
    paw = pygame.image.load("Resources/Bubble/Paw.png").convert_alpha()
    # Scale and resize as required
    paw = pygame.transform.scale(paw, (150, 150))

    # Load all required buttons
    buttonStart = ButtonImg((520, 580), "Resources/Buttons/Start.png",
                           pathSoundClick="Resources/GameClick.wav",
                           pathSoundHover="Resources/Hover.wav")

    # Define a class for the bubble sprites
    class Bubbles(pygame.sprite.Sprite):
        # Variables for the sprites
        def __init__(self, bubble, x, y, speed):
            pygame.sprite.Sprite.__init__(self, self.containers)
            self.image = pygame.image.load(bubble).convert_alpha()
            self.size = random.randint(100,200)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = speed
            self.radius = 25

        # Update the sprite position and set scoring condition
        def update(self, score, position):
            window.blit(self.image, (self.rect))
            if self.rect.y <= height and self.speed != 0:
                self.rect.y -= self.speed
                if self.rect.collidepoint(*position):
                    pop = pygame.mixer.Sound(f"Resources/Bubble/POP.mp3").play()
                    score += 10
                    self.kill()
            return score

        def collide(self, all_bubble_list):
            collections = pygame.sprite.spritecollide(self, all_bubble_list,
                                                      False, pygame.sprite.collide_circle)
            for each in collections:
                if each.speed == 0:
                    self.speed = 0

    # Define a get_frame function to read and convert the camera feedback
    def get_frame(cap):
        success, frame = cap.read()
        frame = cv2.resize(frame, (width, height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame)
        x1, y1 = width//2, height//2
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0].landmark
            single_finger = hand_landmarks[9]
            x1, y1 = width - int(single_finger.x * width), int(single_finger.y * height)

            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_draw_styles.get_default_hand_landmarks_style(),
                    mp_draw_styles.get_default_hand_connections_style())
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        return frame, (x1, y1)

    detector = HandDetector(detectionCon=0.8, maxHands=2)

    # Initialize for FPS
    fps = 60
    clock = pygame.time.Clock()

    # Set the required font
    font = pygame.font.Font(f"Resources/FredokaOne-Regular.ttf", 55)

    # Set boolean variables for the main loop
    running = True
    game_over = False

    # Set the camera to capture the local webcam
    cap = cv2.VideoCapture(0)

    # Main loop
    while not game_over:
        for event in pygame.event.get():
            if event.dict.get('key') == 27:
                game_over = True

        # Use the get_frame function to obtain the webcam feedback and the position of the hand
        frame, position = get_frame(cap)

        # Display the window and all elements on the window
        window.blit(window, (0, 0))
        window.blit(imgBackground, (0, 0))
        window.blit(paw, (position[0]-75, position[1]-75))
        buttonStart.draw(window)

        # Set button properties
        if buttonStart.state == "clicked":
            SceneManager.OpenScene("GameBubble")

        pygame.display.flip()

        # Set FPS
        clock.tick(fps)

if __name__ == "__main__":
    Game()