from . import prepare,tools
from .states import title_screen,mode_select,level_play,custom,help

def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {"TITLE": title_screen.TitleScreen(),
              'MODE':mode_select.ModeSelect(),
              'HELP':help.Help(),
              "PLAY":level_play.LevelPlay(),
              'CUSTOM':custom.Custom()}
    controller.setup_states(states, "TITLE")
    controller.main()