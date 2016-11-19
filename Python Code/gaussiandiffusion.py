import matplotlib.pyplot as plt
import numpy as np

## This script plots the absolute value of the Hamming distance versus
# probability when using the diffusion operator by Schuld et al. (inspired by
# quantum random walks)

####################### 1ST PLOT ###########################
# Show that it distributes in a Gaussian fashion
# 3 qubit case with delta = 0.9

x = [-3,-2,-1,0,1,2,3]
#order:
# |101>,|001>,|011>,|010>,|000>,|100>,|101>
y = [0.001100,0.008790,0.078770,0.730840,0.081570,0.009110,0.001100]
plt.plot(x,y)
plt.ylim(0,1)
plt.ylabel('Probability')
plt.xlabel('abs(x) = Hamming distance')
plt.title('3 qubit case with delta=0.9')
plt.show()

####################### 2ND PLOT ###########################
# Show that it distributes in a Gaussian fashion
# 4 qubit case with delta = 0.9

fig, ax = plt.subplots()
x = [-4,-3,-2,-1,0,1,2,3,4]
#order:
# 4:HD |1011>,3HD: |0011>, 2HD: |0111>,1HD: |0110>, 0HD: |0100>, 1HD: |0000>, 2HD: |1110>, 3HD: |1111>, 4HD: |1011>
y = [0.000100, 0.000880, 0.008090, 0.073020,  0.653810 , 0.072500 , 0.007950, 0.000870 , 0.000100]
plt.plot(x,y,label='delta=0.9')
plt.ylim(0,1)
plt.ylabel('Probability')
plt.xlabel('abs(x) = Hamming distance')
#plt.title('4 qubit case with delta=0.9')
#plt.show()

####################### 3RD PLOT ###########################
# Show that it distributes in a Gaussian fashion
# 4 qubit case with delta=0.8

x = [-4,-3,-2,-1,0,1,2,3,4]
#order:
# 4:HD |1011>,3HD: |0011>, 2HD: |0111>,1HD: |0110>, 0HD: |0100>, 1HD: |0000>, 2HD: |1110>, 3HD: |1111>, 4HD: |1011>
y = [0.001600, 0.006500, 0.025810, 0.103850,  0.407530 , 0.101520 , 0.025120, 0.006420 , 0.001600]
plt.plot(x,y,label='delta=0.8')
plt.ylim(0,1)
plt.ylabel('Probability')
plt.xlabel('abs(x) = Hamming distance')
#plt.title('4 qubit case with delta=0.8')
#plt.show()

####################### 4TH PLOT ###########################
# Show that it distributes in a Gaussian fashion
# 4 qubit case with delta=0.7

x = [-4,-3,-2,-1,0,1,2,3,4]
#order:
# 4:HD |1011>,3HD: |0011>, 2HD: |0111>,1HD: |0110>, 0HD: |0100>, 1HD: |0000>, 2HD: |1110>, 3HD: |1111>, 4HD: |1011>
y = [0.007920, 0.018960, 0.043210, 0.101660,  0.239850 , 0.104090 , 0.044750, 0.018530 , 0.007920]
plt.plot(x,y,label='delta=0.7')
plt.ylim(0,1)
plt.ylabel('Probability')
plt.xlabel('abs(x) = Hamming distance')
#plt.title('4 qubit case with delta=0.7')
#plt.show()


####################### 5TH PLOT ###########################
# Show that it distributes in a Gaussian fashion
# 4 qubit case with delta=0.6

x = [-4,-3,-2,-1,0,1,2,3,4]
#order:
# 4:HD |1011>,3HD: |0011>, 2HD: |0111>,1HD: |0110>, 0HD: |0100>, 1HD: |0000>, 2HD: |1110>, 3HD: |1111>, 4HD: |1011>
y = [0.025390, 0.038630, 0.058350, 0.085750,  0.129960 , 0.087560 , 0.056280, 0.038770 , 0.025390]
plt.plot(x,y,label='delta=0.6')
plt.ylim(0,1)
plt.ylabel('Probability')
plt.xlabel('abs(x) = Hamming distance')
#plt.title('4 qubit case with delta=0.6')
#plt.show()


####################### 6TH PLOT ###########################
# Show that it distributes in a Gaussian fashion
# 4 qubit case with delta=0.5

x = [-4,-3,-2,-1,0,1,2,3,4]
#order:
# 4:HD |1011>,3HD: |0011>, 2HD: |0111>,1HD: |0110>, 0HD: |0100>, 1HD: |0000>, 2HD: |1110>, 3HD: |1111>, 4HD: |1011>
y = [0.063610, 0.063770, 0.062440, 0.061800,  0.063010 , 0.062780 , 0.062690, 0.061890 , 0.063610]
plt.plot(x,y,label='delta=0.5')
plt.ylim(0,1)
plt.ylabel('Probability')
plt.xlabel('abs(x) = Hamming distance')
#plt.title('4 qubit case with delta=0.5')
legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.90')

plt.title('4 qubit case with varying delta')
plt.show()
