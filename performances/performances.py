import matplotlib.pyplot as plt
import time
import os

x = [i for i in range(50)]
y = []
for i in range(len(x)):
    start = time.time()
    os.system("python3 main.py -n 100")
    end = time.time()
    y.append(end-start)

plt.title(
    f"Temps d'execution de la simulation sur {len(x)} essaies pour un pas de 100")
plt.plot(x, y, label="temps d'execution")
plt.plot(x, [sum(y)/len(y) for i in range(len(y))], label="moyenne")
plt.plot(x, [max(y) for i in range(len(y))], label="max")
plt.plot(x, [min(y) for i in range(len(y))], label="min")
plt.xlabel("Nombre d'essaies")
plt.ylabel("Temps d'execution (s)")
plt.legend()
plt.show()
