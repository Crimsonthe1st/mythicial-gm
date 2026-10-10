import pandas as pd
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent

STORAGE_DIR = ROOT_DIR / "mechanics" / "storage"

#SRCs
base_fate_df = pd.read_csv(STORAGE_DIR/"base_fate_chart.csv",index_col="certainty",header=0)
ex_yes_fate_df = pd.read_csv(STORAGE_DIR/"ex_yes_fate_chart.csv",index_col="certainty",header=0)
ex_no_fate_df = pd.read_csv(STORAGE_DIR/"ex_no_fate_chart.csv",index_col="certainty",header=0)

"""
PARAMS:
    use_ex: True/False; use exceptional yes/no rules
    chaos_factor: 1-9; 
    certainty: player chosen label of level of certainty from impossible to certain
    roll: 1D100 roll
    show_thresh: True/False; show thresholds for fate chart (default False)
"""
def ask_fate_chart(use_ex, chaos_factor, certainty, roll, show_thresh=False):

    #VALIDATION STEP:

    valid_factors = ['0','1','2','3','4','5','6','7','8','9']
    chaos_factor = str(chaos_factor)

    valid_certainties = base_fate_df.index.tolist()
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

        if(roll < ex_yes_thresh):
            return "ANSWER: exceptional yes"

        if(roll <= base_threshold):
            return "ANSWER: yes"

        if(roll >= ex_no_thresh):
                    return "ANSWER: exceptional no"
        
        if(roll > base_threshold):
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
     return