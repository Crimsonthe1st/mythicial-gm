import sys
import pandas as pd
from pathlib import Path
from mechanics import certainty as cert

MECHANICS_DIR = Path(__file__).resolve().parent

base_fate_csv = MECHANICS_DIR / "storage" / "base_fate_chart.csv"
ex_yes_csv = MECHANICS_DIR / "storage" / "ex_yes_fate_chart.csv"
ex_no_csv = MECHANICS_DIR / "storage" / "ex_no_fate_chart.csv"

actions_csv = MECHANICS_DIR / "storage" / "meaning_actions.csv" 
desc_csv = MECHANICS_DIR / "storage" / "meaning_desc.csv" 
rand_csv = MECHANICS_DIR / "storage" / "rand_events.csv"

fate_roll_ans_csv = MECHANICS_DIR / "storage" / "fate_chk_answers.csv" 
fate_roll_factor_csv = MECHANICS_DIR / "storage" / "fate_chk_factor.csv" 
fate_roll_certainty_csv = MECHANICS_DIR / "storage" / "fate_chk_certainty.csv" 

base_fate_df = pd.read_csv(base_fate_csv, index_col="certainty", header=0)
ex_yes_fate_df = pd.read_csv(ex_yes_csv, index_col="certainty", header=0)
ex_no_fate_df = pd.read_csv(ex_no_csv, index_col="certainty", header=0)

actions_df = pd.read_csv(actions_csv)
desc_df = pd.read_csv(desc_csv)
rand_df = pd.read_csv(rand_csv)

fate_roll_ans_df = pd.read_csv(fate_roll_ans_csv,index_col="answer")
fate_roll_factor_df = pd.read_csv(fate_roll_factor_csv,index_col="chaos_factor")
fate_roll_certainty_df = pd.read_csv(fate_roll_certainty_csv,index_col="certainty")

"""
PARAMS:
    use_ex: True/False; use exceptional yes/no rules
    chaos_factor: 1-9; 
    certainty: player chosen label of level of certainty from impossible to certain
    roll: 1D100 roll
    show_thresh: True/False; show thresholds for fate chart (default False)
"""
def ask_fate_chart(chaos_factor, certainty, roll, show_thresh=False, use_ex=True):

    #VALIDATION STEP:

    valid_factors = ['0','1','2','3','4','5','6','7','8','9']
    chaos_factor = str(chaos_factor)

    valid_certainties = [str(member.name).lower() for member in cert.Certainty]
    certainty = certainty.lower().strip()

    if(roll > 100 or roll < 1):
        return "\nDie roll must fall between 1 and 100"

    if(chaos_factor not in valid_factors):
        return "\nNot a valid chaos factor"

    if(certainty not in valid_certainties):
        return f"""\n{certainty} is not a valid certainty level please use one of these: \n 
        {", ".join(valid_certainties)}
        """
    
    #CALCULATION STEP:
    rand_check = roll % 11
    if(rand_check == 0 and ( roll%11 <= int(chaos_factor))): 
        print(f"RANDOM EVENT TRIGGERED: ROLL {roll}")
        get_rand_event(roll)

    base_threshold = base_fate_df.loc[certainty,chaos_factor]

    if(use_ex):
        print("Using exceptional yes/no rules")
        ex_yes_thresh = ex_yes_fate_df.loc[certainty,chaos_factor]
        ex_no_thresh = ex_no_fate_df.loc[certainty,chaos_factor]

        if(show_thresh):
            print(f"""\n
                      EX YES: roll lower than {ex_yes_thresh}\n
                      YES: roll {base_threshold} or lower\n
                      NO: roll higher than {base_threshold}\n
                      EX NO: roll {ex_no_thresh} or higher\n""")
#6
        if(roll >= ex_no_thresh):
            return "ANSWER: exceptional no"
        
        elif(roll < ex_yes_thresh):
            return "ANSWER: exceptional yes"

        elif(roll <= base_threshold):
            return "ANSWER: yes"
        
        else:#(roll > base_threshold):
            return "ANSWER: no"

    
    else:
        print("Using base rules \n")
        threshold = base_fate_df.loc[certainty,chaos_factor]
        if(show_thresh):
            print(f"""
                    YES: roll {base_threshold} or lower\n
                    NO: roll higher than {base_threshold}\n
                   """)

        if roll <= threshold:
            return "ANSWER: yes"
        else:
            return "ANSWER: no"

def ask_fate_die(chaos_factor, certainty, roll, show_thresh=False): 
    valid_factors = ['0','1','2','3','4','5','6','7','8','9']
    chaos_factor = str(chaos_factor)

    valid_certainties = [str(member.name).lower() for member in cert.Certainty]    
    certainty = certainty.lower().strip()

    if(chaos_factor not in valid_factors):
            return "\nNot a valid chaos factor"

    if(certainty not in valid_certainties):
        return f"""\n{certainty} is not a valid certainty level please use one of these: \n 
        {", ".join(valid_certainties)}
        """
    chaos_factor = int(chaos_factor)

    cert_mod = fate_roll_certainty_df.loc[certainty,"modifier"]
    fact_mod = fate_roll_factor_df.loc[chaos_factor,"modifier"]

    if show_thresh:
        print(f"Certainty MOD: {cert_mod}, Factor MOD: {fact_mod}, RES: {roll + cert_mod + fact_mod}")
    
    res = roll + cert_mod + fact_mod
    
    if(res >= 18):
         return "ANSWER: Exceptional yes"
    
    elif(res >= 11):
         return "ANSWER: Yes" 
    
    elif(res <= 4):
         return "ANSWER: Exceptional No" 

    else:
        return "ANSWER: No"  

def get_actions(roll1, roll2):
    if (roll1 < 1 or roll1 > 100) or ( (roll2 < 1 or roll2 > 100)):
        return "Roll must be between 1 and 100"

    res1 = actions_df.iloc[roll1,0]
    res2 = actions_df.iloc[roll2,1]
    return res1, res2

def get_descs(roll1, roll2):
    if (roll1 < 1 or roll1 > 100) or ( (roll2 < 1 or roll2 > 100)):
        return "Roll must be between 1 and 100"

    res1 = desc_df.iloc[roll1,0]
    res2 = desc_df.iloc[roll2,1]
    return res1, res2

def get_rand_event(roll):
    if (roll < 1 or roll > 100):
        return "Roll must be between 1 and 100"
    matched_row = rand_df[
        (rand_df["range_start"] <= roll) & (roll <= rand_df["range_end"])
    ]
    res = matched_row["result"].values[0]

    return res