import numpy as np

#So I just saw a wiki article about how to us the "Newton Method" and it seems stupid so I wanna try it

def Newton_Method(Number):
    Guess = Number/1.5
    for i in range(10):
        Guess = (Guess + Number/Guess)/2
    return Guess

L_Square_Root = []

for i in range(1, 100):
    L_Square_Root.append([i, Newton_Method(i)])

print (L_Square_Root)

#This is cool and I like how it works. Also, I would recommend pull requests instead of adding files:
#There might be a latency