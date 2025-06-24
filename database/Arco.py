from dataclasses import dataclass
from datetime import date

@dataclass()
class  Arco:
    u : int
    v : int
    weight : int

    def __str__(self):
        return f"Arco da {self.u} a {self.v}, con peso {self.weight}"

    def __hash__(self):
        return hash(self.u,self.v)
