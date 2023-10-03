import pandas as pd
class A:
    def __init__(self, a, b): # 1
        self.a = a
        self.b = b


    def add(self):
        self.a = 5
        return self
    


abc = A(1,2)
xyz = abc.add()
print(type(abc))
print(type(xyz))

df = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6]})
df_filter = df.filter