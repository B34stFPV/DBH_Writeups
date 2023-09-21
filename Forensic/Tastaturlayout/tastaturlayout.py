# Programm, that reads in the file type.log and extracts all values like this: 69.04*/100.32*
# and displays them in a coordinate system

import matplotlib.pyplot as plt
import numpy as np

file = open("type.log", "r")
lines = file.readlines()
file.close()

values = []
for line in lines:
    if "down" in line:
        values.append((str(line.split("/")[0][-7:]).replace('*', ''), str(line.split("/")[1][:6]).replace('*', '')))

# values is now a list of tuples, where the first element is the x-value and the second element is the y-value
# Convert the values to float
values = [(float(x.replace("\t", '')), float(y.replace("\t", ''))) for x, y in values]

# map the values to a keyboard layout if x and y in certain positions
# create a dictionary with max and min values for x and y for every key
out_string = ""

for touple in values:
    if touple[0] < 46 and touple[0] > 30 and touple[1] < 78 and touple[1] > 40:
        out_string += "2"
    elif touple[0] < 62 and touple[0] > 50 and touple[1] < 78 and touple[1] > 40:
        out_string += "3"
    elif touple[0] < 78 and touple[0] > 64 and touple[1] < 78 and touple[1] > 40:
        out_string += "4"
    elif touple[0] < 94 and touple[0] > 80 and touple[1] < 78 and touple[1] > 40:
        out_string += "5"
    elif touple[0] < 108 and touple[0] > 96 and touple[1] < 78 and touple[1] > 40:
        out_string += "6"
    elif touple[0] < 122 and touple[0] > 110 and touple[1] < 78 and touple[1] > 40:
        out_string += "7"
    elif touple[0] < 136 and touple[0] > 124 and touple[1] < 78 and touple[1] > 40:
        out_string += "8"
    elif touple[0] < 148 and touple[0] > 140 and touple[1] < 78 and touple[1] > 40:
        out_string += "9"
    elif touple[0] < 164 and touple[0] > 149 and touple[1] < 78 and touple[1] > 40:
        out_string += "0"
    elif touple[0] < 183 and touple[0] > 166 and touple[1] < 78 and touple[1] > 40:
        out_string += "-"
    elif touple[0] < 230 and touple[0] > 184 and touple[1] < 78 and touple[1] > 40:
        out_string += "="
    
    # second keyboard row
    elif touple[0] < 42 and touple[0] > 30 and touple[1] < 94 and touple[1] > 78:
        out_string += "q"
    elif touple[0] < 58 and touple[0] > 44 and touple[1] < 94 and touple[1] > 78:
        out_string += "w"
    elif touple[0] < 74 and touple[0] > 58.1 and touple[1] < 94 and touple[1] > 78:
        out_string += "e"
    elif touple[0] < 88 and touple[0] > 75 and touple[1] < 94 and touple[1] > 78:
        out_string += "r"
    elif touple[0] < 102 and touple[0] > 88 and touple[1] < 94 and touple[1] > 78:
        out_string += "t"
    elif touple[0] < 118 and touple[0] > 104 and touple[1] < 94 and touple[1] > 78:
        out_string += "y"
    elif touple[0] < 132 and touple[0] > 118 and touple[1] < 94 and touple[1] > 78:
        out_string += "u"
    elif touple[0] < 147 and touple[0] > 132 and touple[1] < 94 and touple[1] > 78:
        out_string += "i"
    elif touple[0] < 162 and touple[0] > 147 and touple[1] < 94 and touple[1] > 78:
        out_string += "o"
    elif touple[0] < 178 and touple[0] > 163 and touple[1] < 94 and touple[1] > 78:
        out_string += "p"
    
    # third keyboard row
    elif touple[0] < 46 and touple[0] > 30 and touple[1] < 110 and touple[1] > 94:
        out_string += "a"
    elif touple[0] < 60 and touple[0] > 46 and touple[1] < 110 and touple[1] > 94:
        out_string += "s"
    elif touple[0] < 76 and touple[0] > 60 and touple[1] < 110 and touple[1] > 94:
        out_string += "d"
    elif touple[0] < 91 and touple[0] > 76 and touple[1] < 110 and touple[1] > 94:
        out_string += "f"
    elif touple[0] < 106 and touple[0] > 91 and touple[1] < 110 and touple[1] > 94:
        out_string += "g"
    elif touple[0] < 120 and touple[0] > 106 and touple[1] < 110 and touple[1] > 94:
        out_string += "h"
    elif touple[0] < 134 and touple[0] > 120 and touple[1] < 110 and touple[1] > 94:
        out_string += "j"
    elif touple[0] < 149 and touple[0] > 134 and touple[1] < 110 and touple[1] > 94:
        out_string += "k"
    elif touple[0] < 168 and touple[0] > 149 and touple[1] < 110 and touple[1] > 94:
        out_string += "l"
    elif touple[0] < 180 and touple[0] > 168 and touple[1] < 110 and touple[1] > 94:
        out_string += "ö"

    # fourth keyboard row
    elif touple[0] < 50 and touple[0] > 40 and touple[1] < 126 and touple[1] > 110:
        out_string += "z"
    elif touple[0] < 70 and touple[0] > 50 and touple[1] < 126 and touple[1] > 110:
        out_string += "x"
    elif touple[0] < 86 and touple[0] > 70 and touple[1] < 126 and touple[1] > 110:
        out_string += "c"
    elif touple[0] < 99 and touple[0] > 86 and touple[1] < 126 and touple[1] > 110:
        out_string += "v"
    elif touple[0] < 116 and touple[0] > 99 and touple[1] < 126 and touple[1] > 110:
        out_string += "b"
    elif touple[0] < 130 and touple[0] > 116 and touple[1] < 126 and touple[1] > 110:
        out_string += "n"
    elif touple[0] < 144 and touple[0] > 130 and touple[1] < 126 and touple[1] > 110:
        out_string += "m"
    elif touple[0] < 157 and touple[0] > 144 and touple[1] < 126 and touple[1] > 110:
        out_string += ","
    elif touple[0] < 173 and touple[0] > 164 and touple[1] < 126 and touple[1] > 110:
        out_string += "."
    elif touple[0] < 176 and touple[0] > 162 and touple[1] < 126 and touple[1] > 110:
        out_string += "?"
    elif touple[0] < 190 and touple[0] > 176 and touple[1] < 126 and touple[1] > 110:
        out_string += "SHIFT"
    
    # fifth keyboard row
    # this is also the Space row
    elif touple[0] < 140 and touple[0] > 74 and touple[1] < 142 and touple[1] > 125:
        out_string += " "

# print string but if theres = in string remove it with the letter before it
out_string2 = ""
append = True
for letter in out_string:
    if letter == "=":
        append = False
    else:
        if append is True:
            out_string2 += letter
        else:
            append = True

# print the string
print(out_string)
print(out_string2)

# Create the plot
plt.plot(*zip(*values), 'ro')
plt.axis([0, 255, 0, 255])
plt.show()

# Flag is:
# DBH{1_4m_4_1337_h4ck3r}
# DBH{bildschirmtastaturen_sind_lustig_2mdnl3pqx6w7dsnrz3hdn2ndsh2sk9}