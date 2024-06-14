import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(1, 2 * np.pi, 100)
y = []

# i = 0
# while i < len(x_data):
#     y_data.append(np.sin(x_data[i]))
#     i = i + 1


for i in x:
    y.append(np.sin(i))


plt.plot(x, y)

plt.show()
