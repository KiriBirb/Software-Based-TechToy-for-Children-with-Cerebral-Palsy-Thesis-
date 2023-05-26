# Import all required libraries
import pygame
import SceneManager
import numpy as np
import cv2
import mediapipe as mp
import random
from Button import ButtonImg

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

    # Create a window/display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Thesis Project Game")

    # Load all required images
    imgBackground = pygame.image.load("Resources/Bubble/BubblePopBackground.png").convert_alpha()
    imgGO = pygame.image.load("Resources/Bubble/BPGameOver.png").convert_alpha()
    paw = pygame.image.load("Resources/Bubble/Paw.png").convert_alpha()

    # Resize image as required
    paw = pygame.transform.scale(paw, (150, 150))

    # Load all required buttons
    buttonPlayAgain = ButtonImg((520, 500), "Resources/Buttons/PlayAgain.png",
                               pathSoundClick="Resources/GameClick.wav",
                               pathSoundHover="Resources/Hover.wav")
    buttonMenu = ButtonImg((520, 600), "Resources/Buttons/ButtonMenu.png",
                               pathSoundClick="Resources/MenuClick.wav",
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

    # Initialize for FPS
    fps = 60
    clock = pygame.time.Clock()
    countdown = 4
    lastCount = pygame.time.get_ticks()
    GOsound = True

    # Images
    font = pygame.font.Font(f"Resources/FredokaOne-Regular.ttf", 55)
    running = True
    gameOver = False

    # Variables for bubble sprites
    bubble_drop = 10
    pygame.time.set_timer(bubble_drop, 2000)
    score = 0
    all_bubble_list = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    Bubbles.containers = all_sprites, all_bubble_list

    startTime = pygame.time.get_ticks()
    maxTime = 60

    # Initialize video capture for local webcam
    cap = cv2.VideoCapture(0)

    # Main loop
    while running:
        for event in pygame.event.get():
            if event.dict.get('key') == 27:
                gameOver = True
            if event.type == bubble_drop:
                # Drop the bubbles in from the bottom up and randomize floating speed and x position
                for i in range(random.randint(2,5)):
                    Bubbles('Resources/Bubble/Bubble.png', random.randint(100, width-100),
                            height-100, random.randint(2,3))

        # Use the previous function to get the webcam feedback and hand postition
        frame, position = get_frame(cap)

        # Display all required images and text
        window.blit(window, (0, 0))
        window.blit(imgBackground, (0, 0))
        score_text = font.render(f'score: {score}', True, (214, 72, 111), None)
        window.blit(score_text, (width//2, 0))
        window.blit(paw, (position[0]-75, position[1]-75))

        # Countdown before the game starts
        if countdown > 0:
            countdownText = font.render(f'Get Ready!', True, (59, 108, 234), None)
            window.blit(countdownText, (510, 260))
            counting = font.render(f'{countdown}', True, (59, 108, 234), None)
            window.blit(counting, (625, 320))
            count_timer = pygame.time.get_ticks()
            if count_timer - lastCount > 1000:
                countdown -= 1
                lastCount = count_timer

        # Start the bubble drop once the countdown ends
        if running and countdown == 0:
            currentTime = pygame.time.get_ticks()

            for bubble in all_bubble_list:
                score = bubble.update(score, position)
            for bubble in all_bubble_list:
                all_bubble_list.remove(bubble)
                bubble.collide(all_bubble_list)
                all_bubble_list.add(bubble)

            # Render and display the remaining time
            time_text = font.render(f'Time: {int(maxTime)}', True, (214, 72, 111), None)
            window.blit(time_text, (200, 0))

            if currentTime - startTime > 1000:
                maxTime -= 1
                startTime = currentTime

        if maxTime <= 0:
            all_bubble_list.remove(bubble)
            window.blit(imgGO, (0, 0))
            score_text = font.render(f'{score}', True, (214, 72, 111), None)
            window.blit(score_text, (580, 300))
            buttonPlayAgain.draw(window)
            buttonMenu.draw(window)

            if gameOver:
                # Play the game over sound once
                if GOsound:
                    GOsound = False
                    pygame.mixer.Sound(f"Resources/gameOverSound.wav").play().set_volume(0.5)

                # Define button properties
                if buttonMenu.state == "clicked":
                    SceneManager.OpenScene("Menu")
                if buttonPlayAgain.state == "clicked":
                    SceneManager.OpenScene("GameBubble")

        pygame.display.flip()
        pygame.display.update()

        # Set FPS
        clock.tick(fps)

if __name__ == "__main__":
    Game()