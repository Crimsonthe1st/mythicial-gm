import sys
import shell as sh
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from mechanics import dice_roll as dr
from mechanics import certainty as cert
from mechanics import fate_chart as fate

d100 = dr.Dice(100)
print(f"5 rolls of d100: {d100.rolls(5)}")


# d100 = dr.Dice(100)
# roll = d100.roll()
# chaos_factor = 5
# certainty = str(cert.Certainty(5))
# print(f"1D100 ROLL: {roll}")
# print(ask_fate_chart(False, chaos_factor, certainty, roll))
# print(ask_fate_chart(True, chaos_factor, certainty, 91, True))
