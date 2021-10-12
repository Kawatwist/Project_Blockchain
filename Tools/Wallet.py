from random import *
import math

class Wallet:
    Username = "User"
    Credit = 0

    def __init__(self):
        self.Username = "User"
        # print("Wallet Created")
    
    def connect(self, name, credit) :
        print("Wallet Connected ", name, " : ", credit, "$")
        self.Username = name
        self.Credit = credit
        self.findKey()
    
    def UpdateWallet(self, bc):
        print(bc)
        if self.Username in bc:
            self.Credit = bc[self.Username]
            print("New Credit :", self.Credit)

    def findKey(self) :
        P = 3
        Q = 5
        n = P * Q
        z = (P - 1)*(Q - 1)
        e = randrange(n)
        while not math.gcd(e, z) == 1 :
            # print("Rand fail :", e)
            e = randrange(n)
        d = randrange(e)
        test = 0
        while not (e * d) % z == 1 :
            # print("Mod fail :", d, "(", e, ")")
            # print(e, " * ", d, " % ", z, " = ", (e*d)%z)
            d = randrange(e)
            test += 1
            if test > 100:
                e = randrange(n)
                while not math.gcd(e, z) == 1 :
                    print("Rand fail :", e)
                    e = randrange(n)
                test = 0
        print("My key :", n,"\nPrivate Key :", e, "\nPublic Key :", d)
        self.Common = n
        self.Public = e
        self.Private = d
    