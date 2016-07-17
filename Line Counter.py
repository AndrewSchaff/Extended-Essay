"""
import os
files = os.listdir(".")

python_scripts = filter(lambda f: f[-3:] == ".py", files)

lines = 0

for script in python_scripts:
    f = open("./" + script, 'r')
    lines += sum([1 for x in f]) #Count the number of lines
    f.close()

print "This project totals to " + str(lines) + " lines"
"""

#Compressed Version
import os; print "This project totals to " + str(sum([sum([1 for x in open("./" + script, 'r')]) for script in filter(lambda f: f[-3:] == ".py", os.listdir("."))])) + " lines"

