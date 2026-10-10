import cmd
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mechanics import dice_roll as dr
from mechanics import certainty as cert
from mechanics import fate_chart as fate

class Shell(cmd.Cmd):
    prompt = "mythic-gm > "
    intro = """
            WELCOME TO MYTHIC-GM!\n
            Type "help" for a list of commands
            Type "exit" to quit
            """

    def default(self, line):
        print(f"Unknown command: {line!r}. Type 'help' for a list of commands.")

    """ACTIONS:"""

    def do_exit(self, arg):
        print("Exiting mythical GM...")
        return True

    def do_roll(self, argline):
        if(argline and argline.isdigit()):
            dice = dr.Dice(int(argline))
            print(f"ROLL: {dice.roll()}")
        else:
            print("Please use format: roll [digit]")


    """DOCS"""
    def help_exit(self):
        print("CMD (exit): Exits Mythic GM prompt.")

    def help_roll(self):
        print("CMD (roll [digit]): Starts a dice roll.")

    """Repeats the last command given"""
    def emptyline(self):
        print(f"REPEAT: {self.lastcmd}")
        super().emptyline()

if __name__ == "__main__":
    Shell().cmdloop()