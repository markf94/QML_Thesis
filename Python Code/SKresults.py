# Python plot for SK results
import matplotlib.pyplot as plt
import numpy as np
import math

fig, ax = plt.subplots()

x = [0.06941,0.04389,0.04951,0.02823,0.01008,0.00165,0.00156]

y = [28,146,728,3622,17838,89130,444646]
y = [float(b)/10000. for b in y]
#y = [math.log(28, 8),math.log(146, 8),math.log(728, 8),math.log(3622, 8),math.log(17838, 8),math.log(89130, 8),math.log(444646, 8)]
print np.transpose(np.array(x))
print np.transpose(np.array(y))
plt.plot(y,x)
plt.xlim(-1,45)
ax.set(title=r'Performance of the SK algorithm',
       xlabel='Gate count x $\mathregular{10^4}$',
       ylabel=r'Fowler distance [$\mathregular{d(U,U_{approx})}$]')

plt.show()
