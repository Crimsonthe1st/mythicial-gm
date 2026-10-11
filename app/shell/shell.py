import cmd
import re
import shlex
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

    """DOCS"""
    def help_exit(self):
        print("CMD (exit): Exits Mythic GM prompt.")

    def help_roll(self):
        print("""CMD (roll [digit]): Starts a dice roll.\n
                 RESTRICTIONS:\n
                 -digit must be 2 or greater
              """)

    def help_rolls(self):
        print("""CMD (roll [digit_x]d[digit_y]): Rolls x amount of y type dice.\n
                RESTRICTIONS:\n
                -Y must be 2 or greater""")

    def help_set_certainty(self):
            print("""
                    CMD (set_certainty [certainty type]): Sets the certainty type.\n
                    VALID OPTIONS: 
                        CERTAIN = 1
                        NEARLY_CERTAIN = 2
                        VERY_LIKELY = 3
                        LIKELY = 4
                        EITHER = 5
                        UNLIKELY = 6
                        VERY_UNLIKELY = 7
                        NEARLY_IMPOSSIBLE = 8
                        IMPOSSIBLE = 9
                """)

    """Repeats the last command given"""
    def emptyline(self):
        print(f"REPEAT: {self.lastcmd}")
        super().emptyline()

    def default(self, line):
        print(f"Unknown command: {line!r}. Type 'help' for a list of commands.")


    """ACTIONS:"""
    def do_exit(self, arg):
        print("Exiting mythical GM...")
        return True

    def do_roll(self, argline):
        if(argline and argline.isdigit() and int(argline) >= 2):
            dice = dr.Dice(int(argline))
            print(f"1D{dice.sides} ROLL: {dice.roll()}")
        else:
            self.do_help('roll')

    def do_rolls(self, arg):
        #validation
        valid_fmt = re.compile(r'(?i)^(\d*)d(\d*)$')
        check_fmt = re.match(valid_fmt,arg)
        if(not check_fmt):
                self.do_help('rolls')

        #calculation
        else:
            match = valid_fmt.search(arg)
            if match:
                num_dice = match.group(1)
                dice_type = match.group(2)
                if int(dice_type) < 2:
                    self.do_help('rolls')
                else:
                    dice = dr.Dice(int(dice_type))
                    print(f"{num_dice}D{dice.sides} ROLL: {dice.rolls(int(num_dice))}")

    def do_set_certainty(self, arg):
        valid_fmt = re.compile(r'(?i)^(?:(?P<word>[A-Z_]+)|(?P<num>[1-9]))$')
        check_fmt = re.match(valid_fmt, arg)
        if not check_fmt:
            self.do_help('set_certainty')
        else:
            match = valid_fmt.search(arg)
            if match:
                if match.group('word'):
                    lookup = cert.Certainty[match.group('word').upper()]
                    if lookup.value:
                        print(f"Set certainty to: {match.group('word').upper()}")
                    else:
                        self.do_help('set_certainty')
                    
                elif match.group('num'):
                    lookup = cert.Certainty(int(match.group('num')))
                    if lookup.name: 
                        print(f"Set certainty to: {lookup.name}")
                    else:
                        self.do_help('set_certainty')
            else:
                self.do_help('set_certainty')

        
if __name__ == "__main__":
    Shell().cmdloop()