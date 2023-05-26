import Menu, Multiplayer, GameBubble, GamePong, GamePongMP, PongCalibrate, PongCalibrateMP
import BubbleCalibrate, FoodCalibrate, FoodRule, GameFood, PongRule, PongRuleMP, BubbleRule, Credits
from time import sleep

def OpenScene(sceneName):
    sleep(0.25)
    if sceneName == 'Menu':
        Menu.Menu()
    elif sceneName == "GameBubble":
        GameBubble.Game()
    elif sceneName == "Multiplayer":
        Multiplayer.Game()
    elif sceneName == "GamePong":
        GamePong.Game()
    elif sceneName == "GamePongMP":
        GamePongMP.Game()
    elif sceneName == "PongCalibrate":
        PongCalibrate.Game()
    elif sceneName == "PongCalibrateMP":
        PongCalibrateMP.Game()
    elif sceneName == "BubbleCalibrate":
        BubbleCalibrate.Game()
    elif sceneName == "GameFood":
        GameFood.Game()
    elif sceneName == "FoodCalibrate":
        FoodCalibrate.Game()
    elif sceneName == "FoodRule":
        FoodRule.Game()
    elif sceneName == "PongRule":
        PongRule.Game()
    elif sceneName == "PongRuleMP":
        PongRuleMP.Game()
    elif sceneName == "BubbleRule":
        BubbleRule.Game()
    elif sceneName == "Credits":
        Credits.Game()