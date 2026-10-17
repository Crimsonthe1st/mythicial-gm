import cmd
import re
from pathlib import Path

CERTAINTY = 5
CHAOS_FACTOR = 5
VERBOSE = True
USE_EX = True

from mechanics import dice_roll as dr
from mechanics import certainty as cert
from mechanics import magic_eight_ball as fate

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

    def help_set_chaos(self):
        print("""
                CMD (set_chaos [digit]): 1-9
                """)

    def help_fate_roll(self):
        print("""
                CMD (fate_roll [certainty type] [digit_x]): Returns answer.\n
                RESTRICTIONS
                -X must be greater than 0 and less than 10
                -certainty type must be a valid option
                
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

    def do_set_chaos(self, arg):
        valid_fmt = re.compile(r'^[1-9]$')
        check_fmt = re.match(valid_fmt, arg)
        if not check_fmt:
                    self.do_help('set_certainty')
        else:
            print(f"Set chaos factor to: {arg}")
            try:
                globals()["CHAOS_FACTOR"] = int(arg)
            except Exception as e:
                print(e)
            
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
                        globals()["CERTAINTY"] = int(lookup.value)
                    else:
                        self.do_help('set_certainty')
                    
                elif match.group('num'):
                    lookup = cert.Certainty(int(match.group('num')))
                    if lookup.name: 
                        print(f"Set certainty to: {lookup.name}")
                        globals()["CERTAINTY"] = int(lookup.value)
                    else:
                        self.do_help('set_certainty')
            else:
                self.do_help('set_certainty')

    def do_fate_roll(self, arg):

        if arg:
            valid_fmt = re.compile(r'(?i)^(?:(?P<word>[A-Z_]+)|(?P<num>[1-9]))$')

            valid_fmt = re.compile(r'(?i)^(?:(?P<cert>\w*) (?P<fact>\d*))$')
            check_fmt = re.match(valid_fmt,arg)
            if(not check_fmt):
                self.do_help('fate_roll')

            match = valid_fmt.search(arg)
            if match:
                if match.group('cert') and match.group('fact'):
                    certainty = self.do_set_certainty(match.group('cert'))
                    chaos_factor = self.do_set_chaos(match.group('fact'))

        else:
            certainty = cert.Certainty(CERTAINTY).name
            chaos_factor = CHAOS_FACTOR
            print(f'Using preset certainty and chaos_factor ({certainty},{chaos_factor})')

        dice = dr.Dice(int(10))
        base_roll = dice.roll() + dice.roll()
        res = fate.ask_fate_die(chaos_factor, certainty, base_roll, VERBOSE)
        print(res)

    def do_fate_chart(self, arg):

        if arg:
            valid_fmt = re.compile(r'(?i)^(?:(?P<word>[A-Z_]+)|(?P<num>[1-9]))$')

            valid_fmt = re.compile(r'(?i)^(?:(?P<cert>\w*) (?P<fact>\d*))$')
            check_fmt = re.match(valid_fmt,arg)
            if(not check_fmt):
                self.do_help('fate_check')

            match = valid_fmt.search(arg)
            if match:
                if match.group('cert') and match.group('fact'):
                    certainty = self.do_set_certainty(match.group('cert'))
                    chaos_factor = self.do_set_chaos(match.group('fact'))

        else:
            certainty = cert.Certainty(CERTAINTY).name
            chaos_factor = CHAOS_FACTOR
            print(f'Using preset certainty and chaos_factor ({certainty},{chaos_factor})')

        dice = dr.Dice(int(100))
        base_roll = dice.roll()
        res = fate.ask_fate_chart(chaos_factor, certainty, base_roll, VERBOSE, USE_EX)
        print(f"ROLL: {base_roll} and {res}")

    def do_echo_vars(self, arg):
        lookup = cert.Certainty(CERTAINTY).name
        print(f"""
                CURRENT SETTINGS:\n
                CERTAINTY: {lookup}
                CHAOS FACTOR: {CHAOS_FACTOR}
                """)

    def do_get_actions(self, arg):
            dice = dr.Dice(int(100))
            res = dice.rolls(2)
            print("ACTIONS: ",fate.get_actions(res[0], res[1]))

    def do_get_descs(self, arg):
            dice = dr.Dice(int(100))
            res = dice.rolls(2)
            print("DESCRIPTIONS: ",fate.get_descs(res[0], res[1]))

    def do_get_event(self, arg):
            dice = dr.Dice(int(100))
            res = dice.roll()
            print("EVENT: ",fate.get_rand_event(res))
            
if __name__ == "__main__":
    Shell().cmdloop()