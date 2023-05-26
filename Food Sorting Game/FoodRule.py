import pygame
import SceneManager
from Button import ButtonImg

def Game():
    # Initialize
    pygame.init()
    pygame.event.clear()

    # Create Window/Display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Thesis Project Game")

    # Initialize for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Images
    imgBackground = pygame.image.load("Resources/Food/Frules.png").convert()

    # Buttons
    buttonCalibrate = ButtonImg((510, 580), "Resources/Buttons/Calibrate.png",
                        pathSoundClick="Resources/GameClick.wav",
                        pathSoundHover="Resources/Hover.wav")
    buttonBack = ButtonImg((0, 50), "Resources/BackButton.png",
                           pathSoundClick="Resources/MenuClick.wav",
                           pathSoundHover="Resources/Hover.wav")

    # Main loop
    start = True
    while start:
        # Get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()

        # Draw Background/Buttons
        window.blit(imgBackground, (0, 0))
        buttonCalibrate.draw(window)
        buttonBack.draw(window)

        if buttonCalibrate.state == "clicked":
            SceneManager.OpenScene("FoodCalibrate")
        if buttonBack.state == "clicked":
            SceneManager.OpenScene("Menu")

        # Update display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)

if __name__ == "__main__":
    Game()