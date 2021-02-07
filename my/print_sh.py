import math

n = int(input("Input number: "))
for i in range((-n + 1), n):
    x = abs(i) + 1
    for j in range((2 - x % 2), x + 1, 2):
        if x % 2 == 1:
            print(chr(65 + int(j / 2)), end = " ")
        else:
            print(" " + chr(65 + (26 - (int(j / 2)))), end = " ")
    print("")

print(5 or 9)