# Author:          Maxwell Trotter
# Program name:    Dice Probability Calculator Full
# Date:            11/03/2024

# Design Purpose:  Dice Probability Calculator is designed to count the theoretical
                   # probability of rolling certain numbers on certain pairs of dice in Board Game
                   # Island from Wii Party, and then discover the best dice to maximize probability
                   # of landing on a certan square. This will inform player stategy during gameplay.

                   # This version of the program accounts for the extra die the player gains in-game
                   # when rolling doubles.

import math as math
from operator import itemgetter as itemget
from time import sleep as nap

class Die():
    place = "4th Place"
    face_pips = []
    num_faces = 0

class basicDie(Die):
    place = "ERROR"
    face_pips = [1, 2, 3, 4, 5, 6]
    num_faces = 6

class bronzeDie(Die):
    place = "3rd Place"
    face_pips = [1, 1, 1, 2, 2, 2]
    num_faces = 6

class silverDie(Die):
    place = "2nd Place"
    face_pips = [1, 1, 2, 2, 3, 3]
    num_faces = 6

class goldenDie(basicDie):  # Golden dice are identical to single dice (1-6)
    place = "1st Place"
    pass

class OutOfRangeException(Exception):
    pass

def fake_load():
    nap(0.5)
    print(".")
    nap(0.03)
    print(".")
    nap(0.03)
    print(".")
    nap(0.8)

def place_helper(index):
    if index == 0: return "1st place"
    elif index == 1: return "2nd place"
    elif index == 2: return "3rd place"
    elif index == 3: return "4th place"

def is_int_one_to_eighteen(num):
    if ((num < 1) or (num > 18)):
        raise OutOfRangeException
    return

# Create list of all possible rolls
def tabulate(die_1, die_2):
    results_list = []
    if (die_1.num_faces == 0) or (die_2.num_faces == 0):  # if only 1 die
        for x in range(die_1.num_faces):
            results_list += [(die_1.face_pips[x], 0)]
        return results_list
    else:                                                 # else two dice
        
        for x in range(die_1.num_faces):              
            for y in range(die_2.num_faces):
                results_list += [(die_1.face_pips[x], die_2.face_pips[y])]

    return results_list

# Convert rolls to their sums (no reordering)
def count(list):
    count_list = []
    # Single Die Scaling (36x)
    if ((list[0][0]) == 0 or (list[0][1] == 0)):  # a single die must scale up to parts per 216
        for x in list:
            for i in range(1, 37):
                count_list += [(x[0] + x[1])]
    else:
    # Two Dice Scaling
        for x in list:
            for i in range(1, 7):                  # counting each rolls 6x for the bonus die i
            # Non-Doubles Scaling (6x)
                if (x[0] != x[1]):                     # if 1st die isnt equal to 2nd die,
                    count_list += [(x[0] + x[1])]      # then count that sum
                else:                                  # but if both die are equal (ie. doubles),
            # Doubles Scaling (1x for #1-6)
                    count_list += [(x[0] + x[1] + i)]  # count it with the bonus die added from 1-6.
    print("Total number of outcomes: " + str(len(count_list))) # debug counter checking math
    return count_list

# Count frequency of each sum
def tally_frequency(list):  # Returns (spaces, frequency)
    matrix = []
    for x in range(1, 19):  # Outer layer is desired space x (1-18)
        freq = 0            # counting variable must reset
        for y in list:      # Inner layer is going through every result y in its list,
                            # tracking number of results that equal desired space for
                            # that die.
            if (x == y):
                freq += 1
        matrix += [(x, freq)]
    return matrix

def print_average_roll(list, place):
    n = len(list)
    sum = 0
    for x in list:
        sum += x
    return(print("The average roll for " + place + " is " + str(sum/n)))

# Helper for best_place_comparison()
def optimal_list_inator(tup1, tup2, tup3, tup4):  # Return list of tuples (position - 1, freq) with 
                                                  # optimal first, then offset for other values in list ordered
                                                  #  least-greatest. Parameters are (spaces, frequency) of 1st,
                                                  # 2nd, 3rd, 4th.
    l = [tup1[1], tup2[1], tup3[1], tup4[1]]  # l is ordered 1st-4th and contains frequencies only
    sorted_list = []
    for x in range(4):
        max_index = 0
        max_value = 0
        (max_index, max_value) = max(enumerate(l), key = itemget(1))
        sorted_list += [(max_index, max_value)]
        l[max_index] -= 100000 # MAGIC NUMBER to disqualify the initially found maximum
        if (x == 0):  # offset rest of list after the optimal frequency is found
            for i in range(len(l)): 
                l[i] -= max_value
    return sorted_list

# Find and output the best die for each amount of spaces desired.
def best_place_comparison(l1, l2, l3, l4):
    optimal_die_list = []   # ODL is (place, value)
    for x in range(0, 18):  # for each desired space 1-18 (indexes 0-17)
        optimal_die_list += [optimal_list_inator(l1[x], l2[x], l3[x], l4[x])]  # returns tuple (index, val)
        ######################################################### DEBUG #######################################################
        # For the below triple indices, X is spaces, 0 is maximum, 0 is index of max
        # print("  The best position for " + str(x + 1) + " spaces of movement is: " + place_helper(optimal_die_list[x][0][0])
        #         + " (" + str(optimal_die_list[x][0][1]) + " /216)")
        # nap(0.04)
        # if ((optimal_die_list[x][0][1]) != (-1 * optimal_die_list[x][1][1])): # if it's possible to roll it
        #     print("                                                 " + place_helper(optimal_die_list[x][1][0]) +
        #           " (" + str(optimal_die_list[x][1][1]) + ")")
        # nap(0.04)
        # if ((optimal_die_list[x][0][1]) != (-1 * optimal_die_list[x][2][1])): # if it's possible to roll it
        #     print("                                                 " + place_helper(optimal_die_list[x][2][0]) +
        #           " (" + str(optimal_die_list[x][2][1]) + ")")

        # nap(0.04)
        # if ((optimal_die_list[x][0][1]) != (-1 * optimal_die_list[x][3][1])): # if it's possible to roll it
        #     print("                                                 " + place_helper(optimal_die_list[x][3][0]) +
        #           " (" + str(optimal_die_list[x][3][1]) + ")")

        # nap(0.04)
        # print()
        # nap(1.3)
        ######################################################### DEBUG #######################################################
    return optimal_die_list


# Print the frequency of each possible sum from all 4 unique dice combos
def print_final_comparison(l1, l2, l3, l4):  # (gold, silver, bronze, last)
    ######################################################### DEBUG #######################################################
    # for x in range(0, 18):  # for each desired space 1-18 (indexes 0-17)
        # print("  For " + str(x + 1) +  " space(s):")
        # nap(0.05)
        # print("        golden dice: " + str(l1[x][1]))
        # nap(0.05)
        # print("        silver dice: " + str(l2[x][1]))
        # nap(0.05)
        # print("        bronze dice: " + str(l3[x][1]))
        # nap(0.05)
        # print("        single die : " + str(l4[x][1]))
        # nap(0.5)
    ######################################################### DEBUG #######################################################
    print()
    nap(0.5)
    a = print_average_roll(totals4, d2.place)
    nap(0.2)
    a = print_average_roll(totals3, d4.place)
    nap(0.2)
    a = print_average_roll(totals2, d6.place)
    nap(0.2)
    a = print_average_roll(totals1, d8.place)
    nap(0.2)
    return

def over_totaler(list, num):  # sum all rolls of num or higher
    i = num - 1  # for indexing
    sum = 0
    for x in range(i, len(list)):
        sum += list[x][1]
    return sum

def greater_analysis_string(l1, l2, l3, l4, num):
    odl = best_place_comparison(l1, l2, l3, l4)
    i = goal - 1  # for indexing
    str1  = f"This list shows the best die for the number of spaces, "
    str1 += f"displaying the PROBABILITY for all worse die. \n    In order to move "
    str1 += f"{str(goal)} spaces OR HIGHER: \n"

    str1 += f"        Golden dice: {str(over_totaler(l1, num)):>3}"  # {:>3} pads the number up to 3 places on left
                                                                     # {:>02} pads it 2 places and fills with 0s
    str1 += f"     -->    Optimal: {place_helper(0)} ("
    str1 += f"{str(over_totaler(l1, num)):>03}/216 = {str(round((over_totaler(l1, num)/2.16), 2)):>5}%)\n"
    str1 += f"        Silver dice: {str(over_totaler(l2, num)):>3}"
    if (over_totaler(l2, num) != 0):
        str1 += f"     -->             {place_helper(1)} ("
        str1 += f"{str(over_totaler(l2, num)):>03}/216 = {str(round((over_totaler(l2, num)/2.16), 2)):>5}%)"
    str1 += "\n"                                                     # guaranteeing the line break gets added
    str1 += f"        Bronze dice: {str(over_totaler(l3, num)):>3}"
    if (over_totaler(l3, num) != 0):
        str1 += f"     -->             {place_helper(2)} ("
        str1 += f"{str(over_totaler(l3, num)):>03}/216 = {str(round((over_totaler(l3, num)/2.16), 2)):>5}%)"
    str1 += "\n"
    str1 += f"        Single dice: {str(over_totaler(l4, num)):>3}"
    if (over_totaler(l4, num) != 0):
        str1 += f"     -->             {place_helper(3)} ("
        str1 += f"{str(over_totaler(l4, num)):>03}/216 = {str(round((over_totaler(l4, num)/2.16), 2)):>5}%)"
    str1 += "\n"
    return str1

def equal_analysis_string(l1, l2, l3, l4, goal):  # goal is always 1-18
    odl = best_place_comparison(l1, l2, l3, l4)
    i = goal - 1  # for indexing
    str1  = f"This list shows the best die for the number of spaces, "
    str1 += f"displaying the DIFFERENCE in probability for the other dice. \n    In order to move exactly "
    str1 += f"{str(goal)} spaces: \n"

    # Results List string
    str1 += f"        Golden dice: {str(l1[i][1]):>3}"
    str1 += f"     -->    Optimal: {place_helper(odl[i][0][0])} ("
    str1 += f"{str(odl[i][0][1]):>3}/216 = {str(round((odl[i][0][1]/2.16), 2)):>5}%)\n"
    str1 += f"        Silver dice: {str(l2[i][1]):>3}"
    if ((odl[i][0][1]) != (-1 * odl[i][1][1])): # if it's possible to roll it
        str1 += f"     -->             {place_helper(odl[i][1][0])} ("
        str1 += f"{str(odl[i][1][1]):>3}/216 = {str(round((odl[i][1][1]/2.16), 2)):>5}%)" 
    str1 += "\n"
    str1 += f"        Bronze dice: {str(l3[i][1]):>3}"
    if ((odl[i][0][1]) != (-1 * odl[i][2][1])): # if it's possible to roll it
        str1 += f"     -->             {place_helper(odl[i][2][0])} ("
        str1 += f"{str(odl[i][2][1]):>3}/216 = {str(round((odl[i][2][1]/2.16), 2)):>5}%)" 
    str1 += "\n"
    str1 += f"        Single die:  {str(l4[i][1]):>3}"
    if ((odl[i][0][1]) != (-1 * odl[i][3][1])): # if it's possible to roll it
        str1 += f"     -->             {place_helper(odl[i][3][0])} ("
        str1 += f"{str(odl[i][3][1]):>3}/216 = {str(round((odl[i][3][1]/2.16), 2)):>5}%)"
    str1 += "\n"
    return  str1

def less_analysis(num):
    pass

########################################  START  PROGRAM  #########################################
program_start = "Welcome to the Board Game Island dice probability calculator."
program_start += "\nThis version DOES account for the bonus die from rolling doubles."
print(program_start)
fake_load()

# 4th Place Results
print("4th Place (single):")
d1 = basicDie()
d2 = Die()
result4 = tabulate(d1, d2)
# print(result4) DEBUG
totals4 = count(result4)
print()  # spacing

# 3rd Place Results
print("3rd Place (bronze):")
d3 = basicDie()
d4 = bronzeDie()
result3 = tabulate(d3, d4)
# print(result3) # DEBUG
totals3 = count(result3)
print()  # spacing

# 2nd Place Results
print("2nd Place (silver):")
d5 = basicDie()
d6 = silverDie()
result2 = tabulate(d5, d6)
# print(result2) # DEBUG
totals2 = count(result2)
print()  # spacing

# 1st Place Results
print("1st Place (gold):")
d7 = basicDie()
d8 = goldenDie()
result1 = tabulate(d7, d8)
# print(result1) # DEBUG
totals1 = count(result1)
print("Frequency of Landing on a Space: /216")

a = tally_frequency(totals1)
b = tally_frequency(totals2)
c = tally_frequency(totals3)
d = tally_frequency(totals4)
# print(a) # DEBUG
# print(b) # DEBUG
# print(c) # DEBUG
# print(d) # DEBUG
fake_load()

print_final_comparison(a, b, c, d)  # currently printing is disabled for clarity
# fake_load() # DEBUG

# Query Loop
print()
while True:
    query = ""
    print("What is the goal outcome?")
    nap(0.2)
    query = input("(type \">X\" for movement >= X spaces, " + 
                  "\"=X\" for movement of exactly X spaces, " +
                  "or \"<X\" for movement <= X spaces): ")
    query.split()  # query is now a list of the input characters
    fake_load()
    try:  # handle bad numbers
        goal = int(query[1:])
        is_int_one_to_eighteen(goal)
    except ValueError:
        print("Enter an integer number after the \"" + query[0] + "\" sign")
        pass
    except OutOfRangeException:
        print("It is impossible to roll a number lower than a 1 or higher than an 18.")
        pass
    else:  # if no errors
        if (query[0] == '>'): # Greater than 
            print(greater_analysis_string(a, b, c, d, goal))
        if (query[0] == '='):
            print(equal_analysis_string(a, b, c, d, goal))  # returns one big output string
        if (query[0] == '<'):
            pass

print("Goodbye.")
nap(0.4)
exit(0)