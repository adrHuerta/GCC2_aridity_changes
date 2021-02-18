# in aridity_comparison2

def IA_two(T):
    if np.isnan(T):
        return np.nan
    elif ((T == 1) or (T == 2) or (T == 3) or (T == 4)):
        return 10
    else:
        return 20

def RA_two(T):
    if np.isnan(T):
        return np.nan
    elif (T == 1) or ((T == 2) or (T == 3) or (T == 4) or (T == 5)):
        return 10
    else:
        return 20

def RAIA(Tra, Tia):
    if (np.isnan(Tra)) or (np.isnan(Tia)):
        return np.nan
    elif (Tra == 1) and (Tia == 1):
        return 10
    elif (Tra == 2) and (Tia == 2):
        return 20
    elif (Tra == 1) and (Tia == 2):
        return 30
    elif (Tra == 2) and (Tia == 1):
        return 40

# in aridity_changes

def similar_subtypes(x):
    if np.std(x) == 0:
        value = 0
    else:
        value = np.max(x) - np.min(x)

    if value >= 2:
        value = 2

    return value

def change_of_RA(present, future):
    if np.isnan(present) or np.isnan(future):
        response = np.nan
    else:
        present = int(present)
        future = int(future)
        if present == future:
            value = 9
        elif (present == 1) and (future == 2):
            value = 1
        elif (present == 2) and (future == 3):
            value = 2
        elif (present == 3) and (future == 4):
            value = 3
        elif (present == 4) and (future == 5):
            value = 4
        elif (present == 5) and (future == 6):
            value = 5
        elif (present == 6) and (future == 7):
            value = 6
        elif (present == 7) and (future == 8):
            value = 7
        elif (present == 8) and (future == 9):#
            value = 8
        elif (present == 2) and (future == 1):
            value = 10
        elif (present == 3) and (future == 2):
            value = 11
        elif (present == 4) and (future == 3):
            value = 12
        elif (present == 5) and (future == 4):
            value = 13
        elif (present == 6) and (future == 5):
            value = 14
        elif (present == 7) and (future == 6):
            value = 15
        elif (present == 8) and (future == 7):
            value = 16
        elif (present == 9) and (future == 8):
            value = 17
        elif (present-future) <= -2:
            value = 0
        else:
            value = 18

        response = value

    return response