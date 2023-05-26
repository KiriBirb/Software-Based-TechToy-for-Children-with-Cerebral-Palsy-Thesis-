# Import the required libraries
import pygame
import SceneManager
from Button import ButtonImg

# Define the menu
def Menu():
    # Initialize the Pygame
    pygame.init()
    pygame.event.clear()

    # Create a window/display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Thesis Project Game")

    # Initialize for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Load all required images
    imgBackground = pygame.image.load("Resources/MenuBackground.jpg").convert()

    # Load all required buttons
    buttonPop = ButtonImg((510, 400), "Resources/Buttons/ButtonBubble.jpg",
                        pathSoundClick="Resources/MenuClick.wav",
                        pathSoundHover="Resources/Hover.wav")
    buttonPong = ButtonImg((760, 400), "Resources/Buttons/ButtonPong.png",
                        pathSoundClick="Resources/MenuClick.wav",
                        pathSoundHover="Resources/Hover.wav")
    buttonFood = ButtonImg((260, 400), "Resources/Buttons/FoodGame.png",
                        pathSoundClick="Resources/MenuClick.wav",
                        pathSoundHover="Resources/Hover.wav")
    buttonThank = ButtonImg((510, 500), "Resources/Buttons/Thankyou.png",
                           pathSoundClick="Resources/MenuClick.wav",
                           pathSoundHover="Resources/Hover.wav")
    buttonQuit = ButtonImg((510, 600), "Resources/Buttons/ButtonQuit.jpg",
                               pathSoundClick="Resources/MenuClick.wav",
                               pathSoundHover="Resources/Hover.wav")

    # Initialize a true value for the loop
    start = True

    # Start of the main loop for the Pygame event
    while start:
        # Get events
        for event in pygame.event.get():
            # If the game quits then the main loop is stopped
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()

        # Draw Background/Buttons
        window.blit(imgBackground, (0, 0))
        buttonPop.draw(window)
        buttonPong.draw(window)
        buttonFood.draw(window)
        buttonThank.draw(window)
        buttonQuit.draw(window)

        # Define button scene properties
        if buttonPop.state == "clicked":
            SceneManager.OpenScene("BubbleRule")
        if buttonPong.state == "clicked":
            SceneManager.OpenScene("Multiplayer")
        if buttonFood.state == "clicked":
            SceneManager.OpenScene("FoodRule")
        if buttonThank.state == "clicked":
            SceneManager.OpenScene("Credits")
        if buttonQuit.state == "clicked":
            pygame.quit()

        # Update display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)

if __name__ == "__main__":
    Menu()