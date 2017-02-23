class A:
    a=0
    b=0
    def __init__(self):
        a=self.a
        b=self.b

    def zmiana(self,a,b):
        self.a=self.a+2
        self.b=self.b+2
    def wypisz(self):
        self.zmiana(self.a,self.b)
        print self.a, self.b
obiekt=A()
obiekt.wypisz()