from . import prepare,tools
from .states import boggling, time_up, high_score_screen, title_screen

def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {"TITLE": title_screen.TitleScreen(),
                   "BOGGLING": boggling.Boggling(),
                   "TIMEUP": time_up.TimeUp(),
                   "HIGH_SCORES": high_score_screen.HighScoreScreen()}
    controller.setup_states(states, "TITLE")
    controller.main()
