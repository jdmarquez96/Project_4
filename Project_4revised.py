import numpy as np
import matplotlib.pyplot as plt

m0 = 9450 #MeV
s0 = 0.054 #MeV

m1 = 10023
s1 = 0.025


#controllable variables
Nexp = 1000
Nmeas = 1000
detector = 8000
#alpha = 0.05

def h0(sigdetector):
        mu = np.random.normal(m0, s0) #true measurements
        x0 = np.random.normal(mu,sigdetector) #detector measurements
        return x0 

def h1(sigdetector):
        mu1 = np.random.normal(m1, s1) 
        x1 = np.random.normal(mu1,sigdetector) 
        return x1

x0list = [] #generating random x cooridantes for H0
#track0 = []
for i in range(1, Nexp):
        y0 = h0(detector)
        x0list.append(y0)
#        trk0 = np.random.randint(1, 4)
#        track0.append(trk0)

x1list = [] #generating random x cooridnate for H1
#track1 = []
for i in range(1, Nexp): 
        y1 = h1(detector) 
        x1list.append(y1)
#        trk1 = np.random.randint(1, 4)
#        track1.append(trk1)



#z0list = [] #list of masses with a certain track number specified
#z1list = []



#picks out the mass with 1 or 2 tracks
#for i in track0:
#        if track0[i] == 2:
#               z0list.append(x0list[i])
#        if track0[i] == 1:
#               z0list.append(x0list[i])


#for i in track1:
#        if track1[i] == 2:
#               z1list.append(x1list[i])
#        if track1[i] == 1:
#               z1list.append(x1list[i])

plt.figure()
plt.hist(x0list, 50, density = True, label = "Probability distribution of H0", alpha = 0.5)
plt.hist(x1list, 50, density = True, label = "Probability distribution of H1", alpha = 0.5)
plt.title("Probability Distribution of 1S and 2S Upsilon")
plt.xlabel("Mass (GeV)")
plt.ylabel("Probability")
plt.legend()
plt.savefig("distribution.png")
plt.show()
plt.close()

#gets the probability from the bin
def bincontent(bin, value, list):
        for j in range(len(bin)):
                if bin[j-1] <= value < bin[j]:
                        return list[j-1]




n0, bin0, _ = plt.hist(x0list, bins= 50, density = True)
n1, bin1, _ = plt.hist(x1list, bins= 50, density = True)




LLR0 = []
for i in range(1, Nexp):
        LLR = 0 
        for m in range(1, Nmeas):
                y = h0(detector)
                if y > 0:
                        trk = np.random.randint(1, 4)  #produces a tracks seen in event
                        if trk == 2:
                                p1 = bincontent(bin1, y, n1)
                                p0 = bincontent(bin0, y, n0)
                                if p1 is None:   #This is to correct for any values of 0 or none because you can't add an interger to none or arrays
                                        p1 = 0.00000001
                                if p0 is None:
                                        p0 = 0.00000001
                                if p0 == 0:          #avoid any divisions by zero
                                        p0 = 0.00000001
                                if p1 == 0:
                                        p1 = 0.00000001
                                LLR += np.log(p1/p0)
                                LLR0.append(LLR)

LLR1 = []
for i in range(1, Nexp):
        LLR = 0 
        for m in range(1,Nmeas):
                y1 = h1(detector)
                if y1 > 0:
                        trk = np.random.randint(1,4)
                        if trk == 2: 
                                p1 = bincontent(bin1, y1, n1)
                                p0 = bincontent(bin0, y1, n0)
                                if p1 is None:   #This is to correct for any values of 0 or none because you can't add an interger to none or arrays
                                        p1 = 0.000001
                                if p0 is None:
                                        p0 = 0.000001
                                if p0 == 0:          #avoid any divisions by zero
                                        p0 = 0.000001
                                if p1 == 0:
                                        p1 = 0.000001
                                LLR += np.log(p1/p0)
                                LLR1.append(LLR)


print(len(LLR0))
print(len(LLR1))


#sort the arrays
LLR0.sort()
LLR1.sort()

#calculate alpha
alpha = 0.05
a = len(LLR0) - int(len(LLR0)*alpha)

count = float(0)
for x in range(0,len(LLR1)):
    if LLR1[x] < LLR0[a]:
        count += 1

beta = count/len(LLR0)

plt.figure()
plt.grid(True)
plt.hist(x0list, 50, density = True, label = "H0 distribution", alpha = 0.5,color = "blue")
plt.hist(x1list, 50, density = True, label = "H1 distribution", alpha = 0.5, color= "red")
plt.xlabel("mass(MeV)")
plt.ylabel("Probability")
plt.title("LLR Ratio for H0 with the number to tracks = 2")
plt.legend()
#plt.savefig("probdist.png")
plt.show()
plt.close()

plt.figure()
plt.grid(True)
plt.hist(LLR0, 50, density = True, label = "H0|log(p1/p0)", alpha = 0.5,color='blue')
plt.hist(LLR1, 50, density = True, label = "H1|log(p1/p0)", alpha = 0.5, color='red')
plt.xlabel("Log Likilhood ratio|log(L(H1)/L(H0))")
plt.ylabel("log(Probability)")
plt.axvline(LLR0[a], color = 'green',label="$\\alpha$ = %.2f" %(alpha))
plt.axvline(LLR0[a], color = 'green',label="$\\beta$ = %.2f" %(beta))
#plt.text(0.2+left,0.75*top, "$\\alpha$ = %.2f" %(alpha), fontweight="bold")
#plt.text(0.2+left,0.70*top, "$\\beta$ = %.4f" %(beta), fontweight="bold")
plt.yscale('log')
plt.legend()
plt.title("LLR ratios between H0 and H1 when tracks = 2")
plt.savefig("likelihood_ratios.png")
plt.show()


