from model import Model
import networkx as nx
mymodel = Model()
ok, nodi, archi = mymodel.create_graph(2, 5)

(costo, best) = mymodel.cercaPercorsoMax(10)

print(f"BEST COSTO: {costo}\n\nBEST SOL: ")
print()

for el in best:
    print(el.order_id)


