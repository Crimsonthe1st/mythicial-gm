import pandas as pd
import random as rand

#SRCs
base_fate_df = pd.read_csv("storage\\base_fate_chart.csv",index_col="certainty",header=0)
ex_yes_fate_df = pd.read_csv("storage\\ex_yes_fate_chart.csv",index_col="certainty",header=0)
ex_no_fate_df = pd.read_csv("storage\\ex_no_fate_chart.csv",index_col="certainty",header=0)

"""
BASE RULES:
    given a chaos_factor, roll a D100. Depending on the roll and chaos factor find the certainty cat.
    Certainty cat is determined by the bounds given-

    If the roll is a double AND is less than the chaos factor, return a random event.

    Scenerio:
    Question: Does the tavern keeper recognize me?
    Set Likelihood: 50/50
    Chaos factor: 5
    Send function: [false, 5, either]

    function:
    rolls a 65
    base rules say 50 for threshold meaning: <=50 = yes, >50 = no
    65 yields "no"
"""
def return_likelihood(use_ex, chaos_factor, certainty, roll, show_thresh=False):

    #VALIDATION STEP:
    valid_factors = ['0','1','2','3','4','5','6','7','8','9']
    chaos_factor = str(chaos_factor)

    valid_certainties = base_fate_df.index.tolist()
    certainty = certainty.lower().strip()

    if(chaos_factor not in valid_factors):
        return "Not a valid chaos factor"

    if(certainty not in valid_certainties):
        return f"""{certainty} is not a valid certainty level please use one of these: \n 
        {", ".join(valid_certainties)}
        """
    
    #CALCULATION STEP:
    rand_check = roll % 11
    if(rand_check == 0 and ( roll%11 <= int(chaos_factor))): 
        print(f"RANDOM EVENT TRIGGERED: ROLL {roll}")


    if(use_ex):
        print("Using exceptional yes/no rules\n")
        base_threshold = base_fate_df.loc[certainty,chaos_factor]
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

        if(roll > base_threshold):
            return "ANSWER: no"

        if(roll >= ex_no_thresh):
            return "ANSWER: exceptional no"
    
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

# print(base_fate_df)
roll = rand.randint(1,100)
chaos_factor = 5
certainty = "either"
print(f"1D100 ROLL: {roll}")
print(return_likelihood(False, chaos_factor, certainty, roll))
print(return_likelihood(True, chaos_factor, certainty, roll, True))
