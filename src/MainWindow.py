# this is a file to store all the global variables needed
# it's initiated only once when the mainwindow is created
# please don't temper with it

import os
import sys
import ctypes.wintypes
from datetime import datetime
import Scripts.Configs as cfg
from Scripts.BasicLogger import Log
#//////////////////////////////////////////#
#//#    Global Variables Declarations   #//#
#//////////////////////////////////////////#

# appStartDate is the dateTime when the launcher was started, this is used to name the logs
appStartDate = ""
configData = {}
modPath = ""
configPath = ""
iow = False
iol = False
nf = os.sep # this way the logging won't break if someone runs the app on mac
hadtoresetconfig = False
executable = os.path.abspath(sys.executable)
def DefAfterFunction():
    print("after function is null")
AfterFunction = DefAfterFunction
translations = {}

def init():
    global appStartDate, modPath, iow, iol, nf, configPath

    appStartDate = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

    if (sys.platform == "win32"):
        iow = True

        # again thanks stackOverflow for this
        # this code allows us to get the document's folder on any windows pc with any language
        CSIDL_PERSONAL = 5       # My Documents
        SHGFP_TYPE_CURRENT = 0   # Get current, not default value

        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

        # set the modpath to the users documents folder
        modPath = buf.value + nf + "p2mm"
        configPath = buf.value + nf + "p2mm"

    elif (sys.platform.startswith("linux")):
        iol = True
        # set the modpath the the users home directory
        modPath = os.path.expanduser("~") + nf + ".cache/p2mm"
        configPath = os.path.expanduser("~") + nf + ".config/p2mm"

    else:
        # feel sad for the poor people who are running templeOS :(
        Log("This operating system is not supported!")
        Log("We only support Windows and Linux as of current.")
        quit()

    # check if the modpath exists, if not create it
    if not os.path.exists(modPath):
        os.makedirs(modPath)
    if not os.path.exists(configPath):
        os.makedirs(configPath)

def LoadConfig():
    global configData
    configData = cfg.ImportConfig()
    Log("Config data loaded.")

def LoadTranslations():
    global translations
    translations = json.load(open(LanguagesIndex.get(configData["activeLanguage"]["value"]).get('file'), "r", encoding="utf8"))
selectedpopupbutton = 0

CurrentSelectedPlayer = 0

###############################################################################

Floaters = []


# surf = pygame.surface.Surface([int(W / 25) + int(H / 50), int(W / 25) + int(H / 50)])
#     surf.set_colorkey((0, 0, 0))
#     surf.fill((255, 255, 255))
#     surf = pygame.transform.rotate(surf, 19)

def PlaySound(sound):
    LauncherSFX = GVars.configData["LauncherSFX"]["value"] == "true"
    if LauncherSFX:
        pygame.mixer.Sound.play(sound)


def Floater(width, height, rot, x, y, negrot):
    surf = pygame.image.load("GUI/assets/images/button.png")
    surf = pygame.transform.scale(surf, (width, height))
    # surf.set_colorkey((0, 0, 0))
    # surf.fill((130, 130, 140))
    surf = pygame.transform.rotate(surf, 0)
    nrot = rot
    nsurf = surf

    class Floater:
        rot = nrot
        surf = nsurf

    Floater.x = x
    Floater.y = y
    Floater.negrot = negrot
    return Floater


def AddFloater(width, height, rot, x, y):
    # random bool
    negrot = random.randint(0, 1) == 1
    Floaters.append(Floater(width, height, rot, x, y, negrot))


AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)
AddFloater(50, 50, 20, 75, 75)


def gradientRect(window, left_colour, right_colour, target_rect):
    colour_rect = pygame.Surface((2, 2))  # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, left_colour, (0, 0), (0, 1))  # left colour line
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))  # right colour line
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
    window.blit(colour_rect, target_rect)




def SelectAnimation(btn, anim):
    if anim == "pop":
        btn.curanim = "pop1"


def RunAnimation(button, anim):
    if anim == "pop1":
        if button.sizemult < 1.3:
            button.sizemult += 0.1
        else:
            button.curanim = "pop2"
    if anim == "pop2":
        if button.sizemult > 1:
            button.sizemult -= 0.1
        else:
            button.sizemult = 1
            button.curanim = ""


directorymenu = []

CurrentMenu = None
SelectedButton = None
CurrentButtonsIndex = 0


def ChangeMenu(menu, append=True):
    global CurrentMenu
    global SelectedButton
    global directorymenu
    global CurrentButtonsIndex
    if append:
        directorymenu.append(CurrentMenu)
    CurrentMenu = menu
    CurrentButtonsIndex = 0
    SelectedButton = CurrentMenu[0]


def BackMenu():
    if len(directorymenu) > 0:
        ChangeMenu(directorymenu.pop(), False)
        # global CurrentButtonsIndex
        # CurrentButtonsIndex = 0


def BlitDescription(txt, x=screen.get_width() / 16, y=screen.get_height() / 16, clr=(255, 255, 255)):
    try:
        if (len(txt) > 0):
            text1 = pygame.font.Font("GUI/assets/fonts/pixel.ttf", int(int(
                int((int(screen.get_width() / 25) + int(screen.get_height() / 50)) / 1)) / (len(txt) / 10))).render(txt, True, clr)
            if not (LookingForInput):
                screen.blit(text1, (x, y))
    except Exception as e:
        Log(str(e))


def RefreshSettingsMenu(menu):
    SettingsButtons.clear()
    for key in GVars.configData:
        if GVars.configData[key]["menu"] == menu:
            Log(str(key) + ": " + str(GVars.configData[key]["value"]))

            class curkeyButton:
                txt = GVars.configData[key]["value"]
                mlen = 10
                if len(txt) > mlen:
                    txt = txt[:mlen] + "..."
                text = key + ": " + txt
                cfgkey = key
                cfgvalue = GVars.configData[key]["value"]
                keyobj = GVars.configData[key]
                activecolor = (255, 255, 0)
                inactivecolor = (155, 155, 155)
                sizemult = 1

                def whileselectedfunction(keyobj=keyobj):
                    BlitDescription(keyobj["description"], SelectedButton.x,
                                    SelectedButton.y + (SelectedButton.height * 1), (130, 130, 255))
                    BlitDescription(keyobj["warning"], SelectedButton.x,
                                    SelectedButton.y + (SelectedButton.height * 1.25), (255, 50, 50))

                selectanim = "pop"
                selectsnd = pwrsnd
                hoversnd = blipsnd
                curanim = ""

                def function(keyobj=keyobj, cfgkey=cfgkey, cfgvalue=cfgvalue, text=text):
                    if cfgvalue == "true" or cfgvalue == "false":
                        if cfgvalue == "false":
                            cfg.EditConfig(cfgkey, "true")
                        # default to false to avoid errors
                        else:
                            cfg.EditConfig(cfgkey, "false")
                        RefreshSettingsMenu(menu)
                    else:
                        def AfterInputGenericSetConfig(inp, cfgkey=cfgkey, cfgvalue=cfgvalue):
                            cfg.EditConfig(cfgkey, inp.strip())
                            Log("Saved '" + inp.strip() + "' to config " + cfgkey)
                            Error(translations["error_saved"], 5, (75, 200, 75))
                            RefreshSettingsMenu(menu)

                        GetUserInputPYG(AfterInputGenericSetConfig, keyobj["prompt"], cfgvalue)

                isasync = False

            SettingsButtons.append(curkeyButton)
    SettingsButtons.append(BackButton)


def RefreshPlayersMenu():
    cfg.ValidatePlayerKeys()
    global CurrentSelectedPlayer
    PlayersMenu.clear()
    # for player in GVars.configData["Players"]["value"][CurrentSelectedPlayer]:
    #     Log(player)
    #     Log(GVars.configData["Players"]["value"][CurrentSelectedPlayer][player])
    # PlayerKey = GVars.configData["Players"]["value"]["0"]
    # indx = 0
    # for player in GVars.configData["Players"]["value"]:
    #     Log(player)
    #     print(GVars.configData["Players"]["value"][player])
    #     if indx == CurrentSelectedPlayer:
    #         PlayerKey = GVars.configData["Players"]["value"][player]
    #     indx += 1
    # if indx < CurrentSelectedPlayer:
    #     CurrentSelectedPlayer = 0
    #     PlayerKey = GVars.configData["Players"]["value"]["0"]
    PlayerKey = GVars.configData["Players"]["value"][CurrentSelectedPlayer]
    print(PlayerKey)

    class CurPlayername:
        text = translations["players_name"] + PlayerKey["name"]
        activecolor = (255, 255, 120)
        inactivecolor = (155, 155, 155)
        sizemult = 1
        selectanim = "pop"
        selectsnd = pwrsnd
        hoversnd = blipsnd
        curanim = ""

        def function():
            def AfterInputPlayerName(inp, PlayerKey=PlayerKey):
                Log("Saving player name...")
                Log(inp)
                curkey = GVars.configData["Players"]
                curkey["value"][CurrentSelectedPlayer]["name"] = inp.strip()
                cfg.WriteConfigFile(GVars.configData)
                # Log("Saved '" + inp.strip() + "' to config " + "Players")
                Error(translations["error_saved"], 5, (75, 200, 75))
                RefreshPlayersMenu()

            GetUserInputPYG(AfterInputPlayerName, translations["players_enter_username"], PlayerKey["name"])

            Log("Name: " + PlayerKey["name"])

        isasync = False

    class CurSteamID:
        text = "SteamID64: " + PlayerKey["steamid"]
        activecolor = (255, 255, 120)
        inactivecolor = (155, 155, 155)
        sizemult = 1
        selectanim = "pop"
        selectsnd = pwrsnd
        hoversnd = blipsnd
        curanim = ""

        def function():
            def AfterInputSteamID(inp, PlayerKey=PlayerKey):
                Log("Saving SteamID...")
                Log(inp)

                if not (inp.isdigit()):
                    try:
                        inp = Converter.to_steamID3(inp.strip())
                        # replace all [] with ""
                        inp = inp.replace("[", "")
                        inp = inp.replace("]", "")
                        # only get everything after the last ":"
                        inp = inp.split(":")[-1]
                        Error(translations["players_converted_steamid"], 5, (75, 120, 255))
                    except Exception as e:
                        Error(translations["players_invalid_steamid"], 5, (255, 50, 50))
                        Log(str(e))
                        return

                curkey = GVars.configData["Players"]
                curkey["value"][CurrentSelectedPlayer]["steamid"] = inp.strip()
                cfg.WriteConfigFile(GVars.configData)
                Error(translations["error_saved"], 5, (75, 200, 75))
                RefreshPlayersMenu()

            GetUserInputPYG(AfterInputSteamID, "Enter A SteamID", PlayerKey["steamid"])

        isasync = False

    class NextPlayer:
        text = translations["players_next_button"]
        activecolor = (255, 255, 120)
        inactivecolor = (155, 155, 155)
        sizemult = 1
        selectanim = "pop"
        selectsnd = pwrsnd
        hoversnd = blipsnd
        curanim = ""

        def function():
            global CurrentSelectedPlayer
            if CurrentSelectedPlayer < len(GVars.configData["Players"]["value"]) - 1:
                Log("Next player")
                CurrentSelectedPlayer += 1
                RefreshPlayersMenu()
                ChangeMenu(PlayersMenu, False)
            else:
                Log("No more players")
                CurrentSelectedPlayer = 0
                RefreshPlayersMenu()
                ChangeMenu(PlayersMenu, False)

        isasync = False

    class AdminLevel:
        text = translations["players_admin_level"] + PlayerKey["adminlevel"]
        activecolor = (255, 255, 120)
        inactivecolor = (155, 155, 155)
        sizemult = 1
        selectanim = "pop"
        selectsnd = pwrsnd
        hoversnd = blipsnd
        curanim = ""
        isasync = False

        def function():
            def AfterInputAdminLevel(inp, PlayerKey=PlayerKey):
                if not inp.isdigit():
                    Error(translations["players_admin_error_not-a-number"], 5, (255, 50, 50))
                    inp = "0"
                elif int(inp) > 6:
                    Error(translations["players_admin_error_too-high"], 5, (255, 255, 50))
                    Error(translations["error_saved"], 5, (75, 200, 75))
                    inp = "6"
                elif int(inp) < 0:
                    Error(translations["players_admin_error_too-low"], 5, (255, 50, 50))
                    inp = "0"
                else:
                    Error(translations["error_saved"], 5, (75, 200, 75))
                Log("Saving admin level...")
                Log(inp)
                curkey = GVars.configData["Players"]
                curkey["value"][CurrentSelectedPlayer]["adminlevel"] = inp.strip()
                cfg.WriteConfigFile(GVars.configData)
                RefreshPlayersMenu()

            GetUserInputPYG(AfterInputAdminLevel, translations["players_admin-enter-admin-level"],
                            PlayerKey["adminlevel"])

    class AddPlayer:
        text = translations["players_add_player"]
        activecolor = (120, 255, 120)
        inactivecolor = (155, 155, 155)
        sizemult = 1
        selectanim = "pop"
        selectsnd = pwrsnd
        hoversnd = blipsnd
        curanim = ""

        def function():
            global CurrentSelectedPlayer
            Log("Adding blank player...")
            print(f"appended: {cfg.defaultplayerarray}")
            GVars.configData["Players"]["value"].append(cfg.defaultplayerarray)
            cfg.WriteConfigFile(GVars.configData)
            Log(str(len(GVars.configData["Players"]["value"]) - 1))
            CurrentSelectedPlayer = len(GVars.configData["Players"]["value"]) - 1
            RefreshPlayersMenu()

        isasync = False

    class DeletePlayer:
        text = translations["players_remove_player"]
        activecolor = (255, 50, 50)
        inactivecolor = (155, 155, 155)
        sizemult = 1
        selectanim = "pop"
        selectsnd = pwrsnd
        hoversnd = blipsnd
        curanim = ""
        isasync = False

        def function():
            if len(GVars.configData["Players"]["value"]) > 1:
                global CurrentSelectedPlayer
                Log("Deleting player...")
                curkey = GVars.configData["Players"]
                del curkey["value"][CurrentSelectedPlayer]
                cfg.WriteConfigFile(GVars.configData)
                if CurrentSelectedPlayer > 0:
                    CurrentSelectedPlayer -= 1
                RefreshPlayersMenu()
            else:
                Error(translations["players_error_must_be_at_least_one_player"], 5, (255, 50, 50))

    PlayersMenu.append(CurPlayername)
    PlayersMenu.append(CurSteamID)
    PlayersMenu.append(AdminLevel)
    PlayersMenu.append(NextPlayer)
    PlayersMenu.append(AddPlayer)
    PlayersMenu.append(DeletePlayer)
    PlayersMenu.append(BackButton)


def GetUserInputPYG(afterfunc=None, prompt="", preinput=""):
    global LookingForInput
    global CurInput
    global AfterInputFunction
    global InputPrompt
    Log("Getting user input...")
    LookingForInput = True
    CurInput = preinput
    InputPrompt = prompt
    AfterInputFunction = afterfunc
    Log("AfterInputFunction: " + str(AfterInputFunction))


def Error(text, time=3, clr=(255, 75, 75)):
    Log(text)
    # if the text has newlines, split it up
    if "\n" in text:
        text = text.split("\n")
    else:
        ERRORLIST.append([text, time, clr])
        return
    for i in range(0, len(text)):
        ERRORLIST.append([text[i], time, clr])
    return


def PopupBox(title, text, buttons):
    global selectedpopupbutton

    # MANUAL #
    # title = "A String Title For The Box"
    # text = "A String Of Text To Display In The Box (use \n for newlines)"
    # buttons = [["Button Text", "Button Function"], ["Button Text", "Button Function"], etc, etc.....]
    ##########

    selectedpopupbutton = buttons[0]

    PopupBox = [title, text, buttons]  # TITLE, TEXT, BUTTONS
    Log("Creating popup box... Tile: " + str(title) + " Text: " + text + " Buttons: " + str(buttons))
    PopupBoxList.append(PopupBox)


############ BUTTON CLASSES

class LaunchGameButton:
    text = translations["play_button"]
    activecolor = (50, 255, 120)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        global coolDown
        if coolDown <= 0:
            coolDown = int(3 * 60)
            RunGameScript()

    isasync = True


class LauncherSettingsButton:
    text = translations["launcher_settings_button"]
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        RefreshSettingsMenu("launcher")
        ChangeMenu(SettingsButtons)

    isasync = False


class HiddenSettingsButton:
    text = translations["hidden_config_button"]
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        RefreshSettingsMenu("hidden")
        ChangeMenu(SettingsButtons)

    isasync = False


class Portal2SettingsButton:
    text = translations["portal2_config_button"]
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        RefreshSettingsMenu("portal2")
        ChangeMenu(SettingsButtons)

    isasync = False


class SettingsButton:
    text = translations["settings_button"]
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        ChangeMenu(SettingsMenus)

    isasync = False


class PlayersButton:
    text = translations["player_button"]
    activecolor = (0, 255, 255)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        RefreshPlayersMenu()
        ChangeMenu(PlayersMenu)

    isasync = False


class UpdateButton:
    text = translations["update_button"]
    activecolor = (255, 0, 255)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        global coolDown
        if coolDown <= 0:
            coolDown = int(3 * 60)
            if not CheckForUpdates():
                Error(translations["update_already_up_to_date"], 5, (200, 75, 220))

    isasync = True


class ManualButton:
    text = translations["manual_mounting_button"]
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        ChangeMenu(ManualButtons)

    isasync = False


class WorkshopButton:
    text = translations["workshop_button"]
    activecolor = (50, 50, 255)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        ChangeMenu(WorkshopButtons)

    isasync = False


class GuideButton:
    text = translations["guide_button"]
    activecolor = (35, 35, 50)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        # open the steam guide in the default browser
        webbrowser.open("https://steamcommunity.com/sharedfiles/filedetails/?id=2458260280")

    isasync = True


class ExitButton:
    text = translations["exit_button"]
    activecolor = (255, 50, 50)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "none"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        global running
        running = False

    isasync = True


class DiscordButton:
    text = translations["discord_server_button"]
    activecolor = (75, 75, 150)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        # open the discord invite in the default browser
        webbrowser.open("https://discord.com/invite/kW3nG6GKpF")

    isasync = True


class GitHubButton:
    text = translations["github_button"]
    activecolor = (255, 255, 255)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        # open the discord invite in the default browser
        webbrowser.open("https://github.com/kyleraykbs/Portal2-32PlayerMod#readme")

    isasync = True


class LanguagesButton:
    text = translations["languages_button"]
    activecolor = (255, 255, 255)
    inactivecolor = (215, 215, 255)
    sizemult = 0.725
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        # for choosing a languages
        ChangeMenu(LanguagesMenu)

    isasync = True


class TestingButton:
    text = translations["testing_button"]
    activecolor = (175, 75, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        ChangeMenu(TestingMenu)

    isasync = False


class InputButton:
    text = "User Input Test"
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        def AfterInput(input):
            Error("Input: " + input, 3, (255, 255, 0))

        GetUserInputPYG(AfterInput)

    isasync = False


class PopupBoxButton:
    text = "Popup Box"
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        def YesInput():
            Error(translations["error_yes"], 3, (75, 255, 75))

        def NoInput():
            Error(translations["error_no"], 3, (255, 75, 75))

        class YesButton:
            text = translations["error_yes"]
            function = YesInput
            activecolor = (75, 200, 75)
            inactivecolor = (155, 155, 155)

        class NoButton:
            text = translations["error_no"]
            function = NoInput
            activecolor = (255, 75, 75)
            inactivecolor = (155, 155, 155)

        PopupBox("Are You A Mogus?", "have you done 1 sussy thing \n and or have done a VENT, SUS?",
                 [YesButton, NoButton])

    isasync = False


class RunButton:
    text = translations["mount_button"]
    activecolor = (50, 255, 120)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        global coolDown
        if coolDown <= 0:
            coolDown = int(3 * 60)
            MountModOnly()

    isasync = True


class StopButton:
    text = translations["unmount_button"]
    activecolor = (255, 50, 50)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        global coolDown
        if coolDown <= 0:
            coolDown = int(3 * 60)
            UnmountScript()

    isasync = True


class BackButton:
    text = translations["back_button"]
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        BackMenu()

    isasync = False


class GetChangelevelButton:
    text = translations["get_level_button"]
    activecolor = (255, 255, 0)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        def AfterInput(input):
            map = workshop.MapFromSteamID(input)
            if map != False:
                Error(translations["workshop_changelevel_command"], 3, (255, 0, 255))
                Error(translations["workshop_copied_to_clipboard"], 3, (0, 255, 0))
            else:
                Error(translations["workshop_map_not_found"])
                Error(translations["workshop_sentence0_sure-you-are-sub"], 6, (255, 255, 0))
                Error(translations["workshop_sentence0_to-map-and-play-it"], 6, (255, 255, 0))
                Error(translations["workshop_sentence0_least-once"], 6, (255, 255, 0))

        GetUserInputPYG(AfterInput, translations["workshop_link"])

    isasync = False


class ResourcesButton:
    text = translations["resources_button"]
    activecolor = (75, 0, 255)
    inactivecolor = (155, 155, 155)
    sizemult = 1
    selectanim = "pop"
    selectsnd = pwrsnd
    hoversnd = blipsnd
    curanim = ""

    def function():
        ChangeMenu(RecourcesButtons)

    isasync = False


class LanguagesButtonDef:
    def __init__(self, Lang, IETF):
        self.text = Lang
        self.activecolor = (150, 150, 255)
        self.inactivecolor = (155, 155, 155)
        self.sizemult = 1
        self.selectanim = "pop"
        self.selectsnd = pwrsnd
        self.hoversnd = blipsnd
        self.curanim = ""
        self.isasync = False
        self.code = IETF

    def function(self):
        print("Language set: " + self.code)
        GVars.configData["activeLanguage"]["value"] = self.code
        cfg.WriteConfigFile(GVars.configData)
        restart_game_text0 = json.load(open(LanguagesIndex.get(GVars.configData["activeLanguage"]["value"]).get('file'),
                                           "r", encoding="utf8"))["language_error0_language_update"]
        restart_game_text1 = json.load(open(LanguagesIndex.get(GVars.configData["activeLanguage"]["value"]).get('file'),
                                           "r", encoding="utf8"))["language_error0_relaunch_game"]
        Error(restart_game_text0)
        Error(restart_game_text1)
        LanguageButton()


def LanguageButton():
    LanguagesMenu.clear()
    for x in LanguagesIndex:
        if GVars.configData["activeLanguage"]["value"] == x:
            LanguagesMenu.append(LanguagesButtonDef("→ " + LanguagesIndex[x].get('name'), x))
        else:
            LanguagesMenu.append(LanguagesButtonDef(LanguagesIndex[x].get('name'), x))
    LanguagesMenu.append(BackButton)


##############################

### BUTTONS
WorkshopButtons = [GetChangelevelButton, BackButton]

SettingsMenus = [LauncherSettingsButton, Portal2SettingsButton, PlayersButton, BackButton]

SettingsButtons = []

PlayersMenu = []

ManualButtons = [RunButton, StopButton, BackButton]

MainButtons = [LaunchGameButton, SettingsButton, UpdateButton, ManualButton, WorkshopButton, ResourcesButton,
               ExitButton, LanguagesButton]

RecourcesButtons = [GitHubButton, GuideButton, DiscordButton, BackButton]

TestingMenu = [InputButton, PopupBoxButton, BackButton]

LanguagesMenu = []
###########

CurrentMenu = MainButtons

SelectedButton = CurrentMenu[CurrentButtonsIndex]

LookingForInput = False
CurInput = ""
AfterInputFunction = None
InputPrompt = ""

###############################################################################

SecAgo = time.time()


def Update():
    global CurrentMenu
    global SelectedButton
    global CurInput
    global LookingForInput
    global AfterInputFunction
    global SecAgo

    W = screen.get_width()
    H = screen.get_height()

    fntdiv = 32
    fntsize = int(W / fntdiv)
    mindiv = int(fntdiv / 1.25)

    ########### DEBUG

    # tempsurf = pygame.font.Font("GUI/assets/fonts/pixel.ttf", int(int((int(W / 25) + int(H / 50)) / 1.5))).render("CuM", True, (255, 100, 255))
    # screen.blit(tempsurf, (mousex - tempsurf.get_width()/2, mousey - tempsurf.get_height()/2))

    ########### BACKGROUND

    for floater in Floaters:
        surf = floater.surf
        if (SelectedButton.text == translations["unmount_button"] or SelectedButton.text == translations["exit_button"]):
            surf = angrycube
        elif (SelectedButton.text == translations["back_button"]):
            surf = goldencube
        surf = pygame.transform.scale(surf, (W / 15, W / 15))
        surf = pygame.transform.rotate(surf, floater.rot)
        center = surf.get_rect().center
        LauncherCubes = GVars.configData["LauncherCubes"]["value"] == "true"
        if (LauncherCubes):
            screen.blit(surf, (floater.x - center[0], floater.y - center[1]))
        if floater.negrot:
            floater.rot -= (1 + random.randint(0, 2))
        else:
            floater.rot += (1 + random.randint(0, 2))
        if (SelectedButton.text == translations["back_button"]):
            floater.x -= W / 60
            if floater.x < (floater.surf.get_width() * -2):
                floater.y = random.randint(0, H)
                floater.x = (floater.surf.get_width() * 2) + (random.randint(W, W * 2)) * 1
                floater.negrot = random.randint(0, 1) == 1
        elif (SelectedButton.text == translations["unmount_button"] or SelectedButton.text == translations["exit_button"]):
            floater.y -= H / 60
            if floater.y < (floater.surf.get_height() * -2):
                floater.y = (floater.surf.get_height() * 2) + (random.randint(H, H * 2))
                floater.x = random.randint(0, W)
                floater.negrot = random.randint(0, 1) == 1
        else:
            floater.y += H / 60
            if floater.y > (H + floater.surf.get_height() * 2):
                floater.y = (floater.surf.get_height() * -2) + (random.randint(0, H)) * -1
                floater.x = random.randint(0, W)
                floater.negrot = random.randint(0, 1) == 1

    # Put assets/images/keys.png on the top right corner of the screen
    keys = pygame.image.load("GUI/assets/images/keys.png")
    keys = pygame.transform.scale(keys, (W / 10, W / 10))
    screen.blit(keys, ((W / 1.05) - keys.get_width(), H / 15))

    ########### MENU

    # loop through all buttons
    indx = 0
    for button in CurrentMenu:
        indx += 1
        clr = (0, 0, 0)
        if button == SelectedButton:
            clr = button.activecolor
        else:
            clr = button.inactivecolor
        RunAnimation(button, button.curanim)
        text1 = pygame.font.Font("GUI/assets/fonts/pixel.ttf",
                                 int(int((int(W / 25) + int(H / 50)) / 1.5) * button.sizemult)).render(button.text,
                                                                                                       True, clr)
        if not (LookingForInput):
            screen.blit(text1, (W / 16, (H / 2 - (text1.get_height() / 2)) * (indx / 5)))
        button.x = W / 16
        button.y = (H / 2 - (text1.get_height() / 2)) * (indx / 5)
        button.width = text1.get_width()
        button.height = text1.get_height()
    SelectedButton = CurrentMenu[CurrentButtonsIndex]

    ############# OVERLAY

    indx = 0
    for error in ERRORLIST[::-1]:
        indx += 1
        errortext = pygame.font.Font("GUI/assets/fonts/pixel.ttf", int(int(W / 60) + int(H / 85))).render(error[0],
                                                                                                          True,
                                                                                                          error[2])
        screen.blit(errortext, (W / 30, ((errortext.get_height() * indx) * -1) + (H / 1.05)))

    # every 1 second go through each error and remove it if it's been there for more than 1 second
    if (time.time() - SecAgo) > 1:
        for error in ERRORLIST:
            if (error[1] < 0):
                ERRORLIST.remove(error)
            error[1] -= 1
        SecAgo = time.time()

    try:
        SelectedButton.whileselectedfunction()
    except:
        pass

    ####################### DRAW POPUP BOX
    if len(PopupBoxList) > 0:
        sz = 1.25

        # draw a white box that is half the width and height of the screen
        boxbackground = pygame.Surface((W / sz, W / (sz * 2)))
        boxbackground.fill((255, 255, 255))
        boxbackground.set_alpha(175)
        screen.blit(boxbackground, (W / 2 - (boxbackground.get_width() / 2), H / 2 - (boxbackground.get_height() / 2)))

        bw = boxbackground.get_width()
        bh = boxbackground.get_height()
        bx = W / 2 - (bw / 2)
        by = H / 2 - (bh / 2)

        # put the title in the box
        boxtitle = pygame.font.Font("GUI/assets/fonts/pixel.ttf", fntsize).render(PopupBoxList[0][0], True,
                                                                                  (255, 255, 0))
        titlew = boxtitle.get_width()
        titleh = boxtitle.get_height()
        titlex = bx + (bw / 2) - (titlew / 2)
        titley = by + (titleh / 2)
        screen.blit(boxtitle, (titlex, titley))

        # put the text in the box
        ctext = PopupBoxList[0][1].split("\n")
        indx = 0
        for line in ctext:
            text = pygame.font.Font("GUI/assets/fonts/pixel.ttf", int(fntsize / 1.5)).render(line, True, (0, 0, 0))
            textw = text.get_width()
            texth = text.get_height()
            textx = bx + (bw / 2) - (textw / 2)
            texty = by + (titleh * 2) + (texth * indx)
            screen.blit(text, (textx, texty))
            indx += 1

        # put the buttons in the box
        amtob = len(PopupBoxList[0][2])
        indx = 0
        for button in PopupBoxList[0][2]:
            buttonsurf = pygame.surface.Surface(((bw / amtob) / 1.2, (bh / 5)))
            if (button == selectedpopupbutton):
                buttonsurf.fill(button.activecolor)
            else:
                buttonsurf.fill(button.inactivecolor)
            surfw = buttonsurf.get_width()
            surfh = buttonsurf.get_height()
            surfx = bx + (bw / amtob) * indx + (bw / amtob) / 2 - (surfw / 2)
            surfy = by + bh - (bh / 4)
            button.x = surfx
            button.y = surfy
            button.width = surfw
            button.height = surfh
            screen.blit(buttonsurf, (surfx, surfy))

            text = pygame.font.Font("GUI/assets/fonts/pixel.ttf", int(fntsize / 1.5)).render(button.text, True,
                                                                                             (255, 255, 255))
            textw = text.get_width()
            texth = text.get_height()
            textx = bx + (bw / amtob) * (indx) + ((bw / amtob) / 2) - (textw / 2)
            texty = by + bh - (bh / 5) + (texth / 2)
            screen.blit(text, (textx, texty))
            indx += 1

    ####################### DRAW INPUT BOX
    if LookingForInput:

        # divide the CurrentInput into lines
        lines = []
        # every  23 characters, add a new line
        lines.append(CurInput[0:mindiv])
        for i in range(mindiv, len(CurInput), mindiv):
            lines.append(CurInput[i:i + mindiv])

        InputText = ""
        for i in range(len(lines)):
            InputText = pygame.font.Font("GUI/assets/fonts/pixel.ttf", fntsize).render(lines[i], True, (255, 255, 175))
            screen.blit(InputText, (W / 2 - (InputText.get_width() / 2), (
            (((H / 2) - (InputText.get_height() * 1.25)) + ((text1.get_height() * 1.25) * i))) - (
                                    (((text1.get_height() * 1.25) * (len(lines) / 2))))))

        surf1 = pygame.Surface((W / 1.5, W / 100))
        surf1.fill((255, 255, 255))
        surf2 = pygame.Surface((W / 1.5, W / 100))
        blitpos = (
        (W / 2) - (surf2.get_width() / 2), (H / 2) + ((InputText.get_height() * 1.725) * ((len(lines) / 2) - 1)))
        screen.blit(surf1, blitpos)

        surfInputPrompt = pygame.font.Font("GUI/assets/fonts/pixel.ttf", fntsize).render(InputPrompt, True,
                                                                                         (255, 255, 255))
        # blit it right below the surf1
        screen.blit(surfInputPrompt, (blitpos[0] + (surf1.get_width() / 2) - (surfInputPrompt.get_width() / 2),
                                      blitpos[1] + surfInputPrompt.get_height()))


###############################################################################

def Main():
    global running
    global screen
    global fps
    global SelectedButton
    global CurrentButtonsIndex
    global LookingForInput
    global CurInput
    global AfterInputFunction
    global coolDown
    global selectedpopupbutton
    global IsUpdating

    IsUpdating = False
    coolDown = 0
    LastBackspace = 0

    LanguageButton()
    SetLanguage()

    while running:

        # so you can hold backspace to delete
        if (LookingForInput):
            BACKSPACEHELD = pygame.key.get_pressed()[pygame.K_BACKSPACE]
            if (BACKSPACEHELD):
                LastBackspace += 0.3
            # if its been a second since the last backspace, delete the last character
            if (LastBackspace > 1):
                if (len(CurInput) > 0):
                    CurInput = CurInput[:-1]
                LastBackspace = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            ############################ INPUT BOX INPUT
            if (LookingForInput):
                CTRLHELD = pygame.key.get_mods() & pygame.KMOD_CTRL
                SHIFTHELD = pygame.key.get_mods() & pygame.KMOD_SHIFT

                if event.type == pygame.KEYDOWN:
                    # get the key and add it to CurInput
                    name = pygame.key.name(event.key)
                    if name == "space":
                        CurInput += " "
                    elif name in ["return", "enter"]:
                        LookingForInput = False
                        AfterInputFunction(CurInput)
                    elif name == "escape":
                        LookingForInput = False
                    elif name == "tab":
                        CurInput += "    "
                    elif CTRLHELD and name == "v":
                        try:
                            str1 = str(tk.selection_get(selection="CLIPBOARD")).replace("\n", "")
                            Log(f"Pasted: {str1}")
                            CurInput += str1
                        except Exception as e:
                            Log(str(e))  # always log the error
                            pass
                    elif len(name) == 1:
                        if SHIFTHELD:
                            # if the name doesnt contain a letter
                            if not name.isalpha():
                                name = name.replace("1", "!").replace("2", "@").replace("3", "#").replace("4",
                                                                                                          "$").replace(
                                    "5", "%").replace("6", "^").replace("7", "&").replace("8", "*").replace("9",
                                                                                                            "(").replace(
                                    "0", ")").replace("`", "~").replace("-", "_").replace("=", "+").replace("[",
                                                                                                            "{").replace(
                                    "]", "}").replace("\\", "|").replace(";", ":").replace("'", "\"").replace(",",
                                                                                                              "<").replace(
                                    ".", ">").replace("/", "?")
                            # convert lowercase to uppercase
                            else:
                                name = name.upper()
                            CurInput += name
                        else:
                            CurInput += name
                    # support for numpad
                    elif len(name) == 3:
                        CurInput += name[1]


            ######################## POPUP BOX INPUT
            elif len(PopupBoxList) > 0:
                boxlen = len(PopupBoxList[0][2])
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        PopupBoxList.pop()
                    elif event.key == K_RIGHT:
                        for btn in PopupBoxList[0][2]:
                            if btn == selectedpopupbutton:
                                if PopupBoxList[0][2].index(btn) < boxlen - 1:
                                    selectedpopupbutton = PopupBoxList[0][2][PopupBoxList[0][2].index(btn) + 1]

                    elif event.key == K_LEFT:
                        for btn in PopupBoxList[0][2]:
                            if btn == selectedpopupbutton:
                                if PopupBoxList[0][2].index(btn) > 0:
                                    selectedpopupbutton = PopupBoxList[0][2][PopupBoxList[0][2].index(btn) - 1]

                    elif event.key == K_SPACE or event.key == K_RETURN:
                        selectedpopupbutton.function()
                        PopupBoxList.pop()

                elif event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    mousex = mouse[0]
                    mousey = mouse[1]
                    # if the mouse is over a button
                    for btn in PopupBoxList[0][2]:
                        if btn.x < mousex < btn.x + btn.width and btn.y < mousey < btn.y + btn.height:
                            selectedpopupbutton = btn
                            selectedpopupbutton.function()
                            PopupBoxList.pop()
                            break

            ######################## NORMAL INPUT
            elif event.type == KEYDOWN:
                if event.key in [K_ESCAPE, K_BACKSPACE]:
                    BackMenu()
                elif event.key in [K_DOWN, K_s]:
                    if CurrentButtonsIndex < len(CurrentMenu) - 1:
                        CurrentButtonsIndex += 1
                        SelectedButton = CurrentMenu[CurrentButtonsIndex]
                        PlaySound(SelectedButton.hoversnd)
                    else:
                        CurrentButtonsIndex = 0
                        SelectedButton = CurrentMenu[CurrentButtonsIndex]
                        PlaySound(SelectedButton.hoversnd)
                elif event.key in [K_UP, K_w]:
                    if CurrentButtonsIndex > 0:
                        CurrentButtonsIndex -= 1
                        SelectedButton = CurrentMenu[CurrentButtonsIndex]
                        PlaySound(SelectedButton.hoversnd)
                    else:
                        CurrentButtonsIndex = len(CurrentMenu) - 1
                        SelectedButton = CurrentMenu[CurrentButtonsIndex]
                        PlaySound(SelectedButton.hoversnd)
                elif event.key in [K_SPACE, K_RETURN, K_KP_ENTER]:
                    SelectAnimation(SelectedButton, SelectedButton.selectanim)
                    if SelectedButton.function:
                        if SelectedButton.isasync:
                            threading.Thread(target=SelectedButton.function).start()
                        else:
                            SelectedButton.function()

                    PlaySound(SelectedButton.selectsnd)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                ############################ LMB
                if event.button == 1:
                    # loop through every button in the current menu
                    for button in CurrentMenu:
                        try:
                            # if the mouse is over the button
                            if (mousex > button.x and mousex < button.x + button.width) and (
                                    mousey > button.y and mousey < button.y + button.height):
                                if SelectedButton.function:
                                    if SelectedButton.isasync:
                                        threading.Thread(target=SelectedButton.function).start()
                                    else:
                                        SelectedButton.function()

                                SelectAnimation(SelectedButton, SelectedButton.selectanim)

                                PlaySound(SelectedButton.selectsnd)
                        except Exception as e:
                            Log(str(e))

            ###############################
            elif event.type == pygame.MOUSEMOTION:

                mouse = pygame.mouse.get_pos()
                mousex = mouse[0]
                mousey = mouse[1]
                # loop through every button in the current menu
                for button in CurrentMenu:
                    try:
                        # if the mouse is over the button
                        if mousex > button.x and mousex < button.x + button.width and mousey > button.y and mousey < button.y + button.height:
                            # if the button isnt already selected
                            if button != SelectedButton:
                                # select the button
                                SelectedButton = button
                                # set current buttons index to the button
                                CurrentButtonsIndex = CurrentMenu.index(button)
                                # play the hover sound
                                PlaySound(hvrclksnd)
                    except Exception as e:
                        Log(str(e))

        if len(PopupBoxList) > 0:
            # loop through every button in the current popupbox list
            for button in PopupBoxList[0][2]:
                try:
                    # if the mouse is over the button
                    if mousex > button.x and mousex < button.x + button.width and mousey > button.y and mousey < button.y + button.height:
                        if button != selectedpopupbutton:
                            selectedpopupbutton = button
                            PlaySound(button.hoversnd)
                except Exception as e:
                    Log(str(e))

        # make the screen a gradient
        screen.fill((0, 0, 0))
        gradientRect(screen, (0, 2, 10), (2, 2, 10), pygame.Rect(0, 0, screen.get_width(), screen.get_height()))
        Update()
        pygame.display.update()
        fpsclock.tick(fps)

        if coolDown > 0:
            coolDown -= 1

    PostExit()

    pygame.quit()
    os._exit(0)


# !######################################################
# !                       Logic
# !######################################################

# Start of - Translation Functions



def SetLanguage():
    GVars.init()
    GVars.LoadConfig()


def PostExit():
    if (GVars.iow):
        # windows
        os.system("taskkill /f /im portal2.exe")
    if (GVars.iol):
        # linux
        os.system("killall -9 portal2_linux")
    # this is to make sure the portal 2 thread is dead
    # 1 second should be enough for it to die
    time.sleep(1)
    if (GVars.configData["AutoUnmount"]["value"] == "true"):
        UnmountScript(False)
        Error(translations["unmounted_error"], 5, (125, 0, 125))


def GetGamePath():
    tmpp = BF.TryFindPortal2Path()
    if not tmpp:
        def AfterInputGP(inp):
            cfg.EditConfig("portal2path", inp.strip())
            Log("Saved '" + inp.strip() + "' as the game path!")
            Error(translations["game_path_error-saved"], 5, (75, 200, 75))
            VerifyGamePath()

        GetUserInputPYG(AfterInputGP, translations["game_path_enter_path"])
    else:
        cfg.EditConfig("portal2path", tmpp.strip())
        Log("Saved '" + tmpp.strip() + "' as the game path!")
        VerifyGamePath()


def VerifyGamePath(shouldgetpath=True):
    Log("Verifying game path...")
    gamepath = GVars.configData["portal2path"]["value"]
    if ((os.path.exists(gamepath)) != True) or (os.path.exists(gamepath + GVars.nf + "portal2_dlc2") != True):
        Error(translations["game_path-is-invalid"])
        Error(translations["game_path-attempt-to-fetch"], 5, (255, 255, 75))

        tmpp = BF.TryFindPortal2Path()
        if tmpp != False:
            tmpp = tmpp.strip()
            # replace \\ with \
            Error(translations["game_path_error-founded"], 5, (255, 255, 75))
            tmpp = tmpp.replace("\\\\", "\\")
            cfg.EditConfig("portal2path", tmpp)
            Log("Saved '" + tmpp + "' as the game path!")
            Error(translations["game_path_error-saved"], 5, (75, 200, 75))
            return True

        if (shouldgetpath):
            GetGamePath()
        return False
    return True


def VerifyModFiles():
    modFilesPath = GVars.modPath + GVars.nf + "ModFiles" + GVars.nf + "Portal 2" + GVars.nf + "install_dlc"
    Log("Searching for mod files in: " + modFilesPath)
    if (os.path.exists(modFilesPath)) and (os.path.exists(modFilesPath + GVars.nf + "32playermod.identifier")):
        Log("Mod files found!")
        return True

    Log("Mod files not found!")
    return False


def UseFallbacks(gamepath):
    # copy the "FALLBACK" folder to the modpath "GVars.modPath + GVars.nf + "ModFiles""
    BF.CopyFolder(cwd + GVars.nf + "FALLBACK" + GVars.nf + "ModFiles", GVars.modPath + GVars.nf + "ModFiles")
    DoEncrypt = GVars.configData["EncryptCvars"]["value"] == "true"
    RG.MountMod(gamepath, DoEncrypt)
    Error(translations["mount_complete"], 5, (75, 255, 75))
    # RG.LaunchGame(gamepath)


def DEVMOUNT():
    try:
        # delete the old modfiles
        BF.DeleteFolder(GVars.modPath + GVars.nf + "ModFiles")
    except Exception as e:
        Log("Error deleting mod files in dev mount")
        Log(str(e))

    # copy the one in the current directory to the modpath
    BF.CopyFolder(cwd + GVars.nf + "ModFiles", GVars.modPath + GVars.nf + "ModFiles")


def MountModOnly():
    cfg.ValidatePlayerKeys()

    if not VerifyGamePath():
        return

    if IsUpdating:
        Error(translations["update_is-updating"], 5, (255, 75, 75))
        return

    Error(translations["mounting_mod"], 5, (75, 255, 75))

    gamepath = GVars.configData["portal2path"]["value"]

    if (GVars.configData["developer"]["value"] == "true"):
        Error(translations["devmod_is_active"], 5, (255, 180, 75))
        DEVMOUNT()
        Error(translations["devmod_copied_from_local_repo"], 5, (75, 255, 75))

    if (VerifyModFiles()):
        DoEncrypt = GVars.configData["EncryptCvars"]["value"] == "true"
        RG.MountMod(gamepath, DoEncrypt)
        Error(translations["mounted"], 5, (75, 255, 75))
        return True

    # if the he's not a developer and the mod files don't exist ask him to download the files from the repo
    else:
        if (os.path.exists(GVars.modPath + GVars.nf + "ModFiles")):
            BF.DeleteFolder(GVars.modPath + GVars.nf + "ModFiles")
        if up.haveInternet():
            def YesInput():
                Log("Yes input has been called! Fetching mod...")
                UpdateModFiles()

            class YesButton:
                text = translations["error_yes"]
                function = YesInput
                activecolor = (75, 200, 75)
                inactivecolor = (155, 155, 155)

            class NoButton:
                text = translations["game_files_use_fallbacks"]

                def function():
                    UseFallbacks(gamepath)

                activecolor = (255, 75, 75)
                inactivecolor = (155, 155, 155)

            PopupBox(translations["game_files_fetch_game"], translations["game_files_no_cached_files"],
                     [YesButton, NoButton])
        else:
            Error(translations["update_error_connection_problem"], 5, (255, 75, 75))
            UseFallbacks(gamepath)
            Error(translations["mounted"], 5, (75, 255, 75))
            return True


def UpdateModFiles():
    PostExit()
    Error(translations["update_fetching"], 5000, (255, 150, 75))

    def UpdateThread():
        Log("Updating...")
        global IsUpdating
        IsUpdating = True
        up.DownloadNewFiles()
        Error(translations["update_complete"], 5, (75, 255, 75))
        IsUpdating = False
        for thing in ERRORLIST:
            if thing[0] == translations["update_fetching"]:
                ERRORLIST.remove(thing)

    thread = threading.Thread(target=UpdateThread)
    thread.start()


def UpdateModClient():
    PostExit()
    Error(translations["updating_client"], 5000, (255, 150, 75))

    def UpdateThread():
        Log("Updating...")
        global IsUpdating
        IsUpdating = True
        up.DownloadClient()
        global running
        running = False
        Log("running set to false")

    thread = threading.Thread(target=UpdateThread)
    thread.start()


def RunGameScript():
    VerifyGamePath()
    gamepath = GVars.configData["portal2path"]["value"]
    if MountModOnly():
        RG.LaunchGame(gamepath)
        Error(translations["game_launched"], 5, (75, 255, 75))


def UnmountScript(shouldgetpath=True):
    Log("___Unmounting Mod___")
    gamepath = GVars.configData["portal2path"]["value"]
    VerifyGamePath(shouldgetpath)
    RG.DeleteUnusedDlcs(gamepath)
    RG.UnpatchBinaries(gamepath)
    Log("____DONE UNMOUNTING____")


def RestartClient(path):
    if (GVars.iol):
        permissioncommand = "chmod +x " + path
        os.system(permissioncommand)

    command = path
    subprocess.Popen(command, shell=True)
    Log("Restarting client")
    global running
    running = False


def IsNew():
    if len(sys.argv) != 3:
        return

    if (sys.argv[1] != "updated") or (not os.path.exists(sys.argv[2])):
        return

    Log("This is first launch after a successful update")

    Log("Deleting old client...")
    os.remove(sys.argv[2])

    # this will rename the new clien to the old client's name
    Log("Renaming new client...")
    os.rename(GVars.executable, sys.argv[2])
    RestartClient("\"" + sys.argv[2] + "\"")


def ClientUpdateBox(update):
    def YesInput():
        Log("Fetching mod...")
        UpdateModClient()

    class YesButton:
        text = translations["error_yes"]
        function = YesInput
        activecolor = (75, 200, 75)
        inactivecolor = (155, 155, 155)

    class NoButton:
        text = translations["error_no"]

        def function():
            pass

        activecolor = (255, 75, 75)
        inactivecolor = (155, 155, 155)

    PopupBox(update["name"], update["message"], [YesButton, NoButton])


def ModFilesUpdateBox():
    class YesButton:
        text = translations["error_yes"]
        function = UpdateModFiles
        activecolor = (75, 200, 75)
        inactivecolor = (155, 155, 155)

    class NoButton:
        text = translations["error_no"]

        def function():
            pass

        activecolor = (255, 75, 75)
        inactivecolor = (155, 155, 155)

    PopupBox(translations["update_available"], translations["update_would_you_like_to"], [YesButton, NoButton])


def CheckForUpdates():
    Log("Checking for updates...")
    clientUpdate = up.CheckForNewClient()
    if clientUpdate["status"]:
        ClientUpdateBox(clientUpdate)
        return True

    if up.CheckForNewFiles():
        ModFilesUpdateBox()
        return True

    return False


def OnStart():
    # Load the global variables
    GVars.init()
    SetLanguage()
    # to do the fancy log thing
    StartLog()
    # load the config file into memmory
    GVars.LoadConfig()
    # make sure the players config is in tact
    cfg.ValidatePlayerKeys()
    # so it only runs in release mode
    if not sys.argv[0].endswith(".py"):
        cfg.EditConfig("developer", "false")
        IsNew()  # Check for first time setup
        time.sleep(1)
        CheckForUpdates()
    else:
        Log("Running through Python! Not checking for updates.")
        cfg.EditConfig("developer", "true")

    VerifyGamePath(False)

    def NewAfterFunction():
        Error(translations["game_exited"], 5, (125, 0, 125))
        if (GVars.configData["AutoUnmount"]["value"] == "true"):
            UnmountScript()
            Error(translations["unmounted_error"], 5, (125, 0, 125))

    GVars.AfterFunction = NewAfterFunction

    if (GVars.configData["developer"]["value"] == "true"):
        SettingsMenus.pop()
        SettingsMenus.append(HiddenSettingsButton)
        SettingsMenus.append(BackButton)

    # remove old temp files
    if (os.path.exists(GVars.modPath + GVars.nf + ".temp")):
        BF.DeleteFolder(GVars.modPath + GVars.nf + ".temp")

    if (GVars.hadtoresetconfig):
        Log("Config has been reset to default settings!")

        class OkButton:
            text = translations["error_ok"]

            def function():
                pass

            activecolor = (75, 255, 75)
            inactivecolor = (155, 155, 155)

        PopupBox(translations["launcher_config_reset"], translations["launcher_had_to_reset"], [OkButton])


if __name__ == '__main__':
    try:
        OnStart()
        Main()
    except Exception as e:
        Log("Exception encountered: " + str(e))
