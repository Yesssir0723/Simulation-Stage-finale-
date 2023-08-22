# -*- coding: utf-8 -*-
"""code organisée

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W_EPZmrU45ZxzES4ZutkAn8jf6N2z60S
"""

from qutip import *
import numpy as np
import matplotlib.pyplot as plt
from math import *
import time
import random

"""# Interactio dipole dipole étude .

Constante du problème.
"""

wl=3*1e6*2*np.pi
#gamma=2*np.pi*6*1e6
w2=2*np.pi*50*10**3
#Delta=0
Delta=1.5*1e9*2*np.pi/20
hbar=1.05457182e-34
E=np.sqrt(1/(2*np.pi**2*8.85*1e-9))
#E=0
r=4e-7
d=3.584e-29
G=1/(4*np.pi*8.85*1e-12*r**3)
#G=0
#print(G)
print(d**2*G/hbar)
times1=np.linspace(0, 3.3333333333333335e-06,2000)
alpha1=(d*E)/(2*np.sqrt(2)*hbar)
print(wl/(2*np.pi))
print(alpha1/(2*np.pi))
print(alpha1**2/(4*Delta)/(2*np.pi))

I4=qeye(4)
id16=qeye(16)
H1m=Qobj(np.array([[0,wl/2,0,0],[wl/2,0,0,0],[0,0,0,wl/2],[0,0,wl/2,0]]))

Hdipole=Qobj(np.array([[0,0,0,-alpha1],[0,0,alpha1,0],[0,alpha1,Delta,0],[-alpha1,0,0,Delta]]))
print(H1m+Hdipole)
H2am=tensor(H1m,I4)+tensor(I4,H1m)
H2adipole=tensor(Hdipole,I4)+tensor(I4,Hdipole)
H2at=H2am+H2adipole
Dp=Qobj(np.array([[0,0,0,-1/(2*np.sqrt(2))],[0,0,0,0],[0,1/(2*np.sqrt(2)),0,0],[0,0,0,0]]))
Dm=Qobj(np.array([[0,0,0,0],[0,0,1/(2*np.sqrt(2)),0],[0,0,0,0],[-1/(2*np.sqrt(2)),0,0,0]]))
Dz=Qobj(np.array([[0,0,1/(np.sqrt(2)),0],[0,0,0,1/(np.sqrt(2))],[1/(np.sqrt(2)),0,0,0],[0,1/(np.sqrt(2)),0,0]]))
Hdd=(G*d**2)/hbar*(tensor(Dp,I4)*tensor(I4,Dm)+tensor(Dm,I4)*tensor(I4,Dp))
Htot=H2at+Hdd

I=qeye(2)
Sx=Qobj(np.array([[0,1/2,0,0],[1/2,0,0,0],[0,0,0,1/2],[0,0,1/2,0]]))
Sy=Qobj(np.array([[0,-1j/2,0,0],[1j/2,0,0,0],[0,0,0,-1j/2],[0,0,1j/2,0]]))
Sz=Qobj(np.array([[1/2,0,0,0],[0,-1/2,0,0],[0,0,1/2,0],[0,0,0,-1/2]]))
Sxt1=tensor(Sx,I4)
Sxt2=tensor(I4,Sx)
Spt1=np.sqrt(w2/2)*tensor((Sy+1j*Sz),I4)
Spt2=np.sqrt(w2/2)*tensor(I4,(Sy+1j*Sz))
Smt1=np.sqrt(w2/2)*tensor((Sy-1j*Sz),I4)
Smt2=np.sqrt(w2/2)*tensor(I4,(Sy-1j*Sz))
Szt2=np.sqrt(w2)*tensor(I4,Sz)
Szt1=np.sqrt(w2/2)*tensor(Sz,I4)

etat10=Qobj(np.array([[1/2,0,0,0],[0,1/2,0,0],[0,0,0,0],[0,0,0,0]]))

etatinitial=tensor(etat10,I4)+tensor(I4,etat10)

T=3.3333333333333335e-05
print(1/T)
#T=3.3333333333333335e-6
N=100000
dt=T/(N+1)
print(dt)
print(1/dt)
psi01=Qobj(1/np.sqrt(2)*(np.array([1,0,0,0])))
psi02=Qobj(1/np.sqrt(2)*(np.array([1,0,0,0])))
psi0=tensor(psi01,psi02)
print(psi0)
H=H2at
times=np.linspace(0, T,N+1)

#a1=sesolve(H2am, psi0, times)
b=sesolve(H2at, psi0, times)
c=sesolve(H2at+Hdd, psi0, times)

w=b.states
d=c.states
#a=a1.states
x=[]
z=[]
y=[]
for i in range(N+1):
    y.append(abs(w[i][0][0]))
    #x.append(abs(a[i][0][0]))
    z.append(abs(d[i][0][0]))

#plt.plot(times,x,label='H2am')
plt.plot(times,z,label='H2at+Hdd')
#plt.plot(times,y,label='H2at')
plt.legend()


z1 = [number for array in z for number in np.ravel(array)]
#x1=[number for array in x for number in np.ravel(array)]
y1=[number for array in y for number in np.ravel(array)]


fft_result = np.abs(np.fft.fft(z1))
#fft_result1= np.abs(np.fft.fft(x1))
fft_result2=np.abs(np.fft.fft(y1))


frequence = np.fft.fftfreq(100001, d=(dt) )


plt.figure(2)
#plt.plot(f,g)
plt.plot((1/1e6)*frequence ,fft_result,label='H2at+Hdd')
#plt.plot((1/1e6)*frequence ,fft_result1,label='H2am')
plt.plot((1/1e6)*frequence,fft_result2,'r',linestyle='dashed',label='H2at')
plt.legend()
plt.grid()
plt.xlim(0,8)

import numpy as np
from scipy.signal import find_peaks
def pics(liste):
  # Generate a sample graph
  peaks, _ = find_peaks(liste)
  # Print peaks
  return [peaks[0],peaks[1],peaks[2],peaks[3]]

"""Code pour tracer le ratio des deux premiers pics en fonction de Delta

"""

Deltalist=[1.5*1e9*2*np.pi,1.5*1e9*2*np.pi/10,1.5*1e9*2*np.pi/20,1.5*1e9*2*np.pi/30,1.5*1e9*2*np.pi/40,1.5*1e9*2*np.pi/50,1.5*1e9*2*np.pi/60,1.5*1e9*2*np.pi/70,1.5*1e9*2*np.pi/80,1.5*1e9*2*np.pi/90,1.5*1e9*2*np.pi/100]
h=[]
for i in range(11):
  d=3.584e-29
  Hdipole=Qobj(np.array([[0,0,0,-alpha1],[0,0,alpha1,0],[0,alpha1,Deltalist[i],0],[-alpha1,0,0,Deltalist[i]]]))
  H2am=tensor(H1m,I4)+tensor(I4,H1m)
  H2adipole=tensor(Hdipole,I4)+tensor(I4,Hdipole)
  H2at=H2am+H2adipole
  Dp=Qobj(np.array([[0,0,0,-1/(2*np.sqrt(2))],[0,0,0,0],[0,1/(2*np.sqrt(2)),0,0],[0,0,0,0]]))
  Dm=Qobj(np.array([[0,0,0,0],[0,0,1/(2*np.sqrt(2)),0],[0,0,0,0],[-1/(2*np.sqrt(2)),0,0,0]]))
  Dz=Qobj(np.array([[0,0,1/(np.sqrt(2)),0],[0,0,0,1/(np.sqrt(2))],[1/(np.sqrt(2)),0,0,0],[0,1/(np.sqrt(2)),0,0]]))
  Hdd=(G*d**2)/hbar*(tensor(Dp,I4)*tensor(I4,Dm)+tensor(Dm,I4)*tensor(I4,Dp))
  Htot=H2at+Hdd
  c=sesolve(H2at+Hdd, psi0, times)
  alpha=c.states
  x=[]
  for j in range(N+1):
    x.append(abs(alpha[j][0][0]))
  x1 = [number for array in x for number in np.ravel(array)]
  fft_result1= np.abs(np.fft.fft(x1))
  frequence = np.fft.fftfreq(100001, d=(dt) )
  plt.plot(frequence,fft_result1)
  a=fft_result1[pics(fft_result1)[1]]/fft_result1[pics(fft_result1)[0]]
  h.append(a)
  print(i)
deltalist1=[1;1/10,1/20,1/30,1/40,1/50,1/60,1/70,1/80,1/90,1/100]
plt.plot(deltalist1,h[1:11])
plt.xlim(0.01,0.1)

"""## Atome IN out"""

H=Qobj([[0,wl/(np.sqrt(2)),0 ],[wl/(np.sqrt(2)),0,wl/(np.sqrt(2)) ],[0,wl/(np.sqrt(2)),0 ]])
psi0=Qobj(1/np.sqrt(1)*np.array([1,0,0]))
times1=np.linspace(0, 3.3333333333333335e-06,2000)
Sz= jmat(1,'z')
print(Sz)
T=3.3333333333333335e-5
N=10000
M1=jmat(1,'z')
M2=jmat(1,'x')
M3=jmat(1,'y')
M4=Qobj(np.array([[0,0,1],[0,0,0],[1,0,0]]))
M5=Qobj(np.array([[0,0,1j],[0,0,0],[-1j,0,0]]))
M6=Qobj(1/np.sqrt(2)*np.array([[0,0,1j],[0,0,0],[-1j,0,0]]))
M7=Qobj(1/np.sqrt(2)*np.array([[0,-1j,0],[1j,0,1j],[0,-1j,0]]))
M8=Qobj(1/np.sqrt(3)*np.array([[1,0,0],[0,-2,0],[0,0,1]]))

dt=T/N

def bernoulli(p):
    if random.random() < p:
        return 1
    else:
        return 0
def lorentz(x, x0, gamma):
    return   920*((gamma/2)**2 / ((x - x0) ** 2 + (gamma/2) ** 2))
c=np.linspace(5e6,6.9e6,2000000)
y1=lorentz(c,5999400.059994,2*30e3)
plt.plot(c,y1)

from scipy.signal import welch
T=3.3333333333333335e-5 #intervale sur lequelle on trace
N=10000                 #nombre de pas
M=100#nomre de simulation pas prenddre un M plus grand que 50 ça prendra beaucoup de temps
dt=T/N
p=dt*30e3*2*np.pi  #paramètres de bernoulli
psi0=Qobj(1/np.sqrt(3)*np.array([1,1,1]))
psi01= Qobj(np.array([1,0,0]))#vecteur qui donne une moyenne de spin 1
psi00=Qobj(np.array([0,1,0])) #vecteur qui donne une moyenne de spin nulle
psi0_1=Qobj(np.array([0,0,1])) #vecteur qui donne une moyenne de spin -1
y=np.zeros((N+1,M))
z=np.zeros((N+1,M))
PSD=np.zeros((5001,M))
x=[]
r=[]
expe=[]
PSDM=[]
for k in range(M):
    print(k)
    psi=psi0
    moySz=[expect(M7,psi0*psi0.dag())]
    #pho=[abs(np.array(psi0*psi0.dag()))]
    for i in range(N):
        a=bernoulli(p)   #generation de 0,1 avec une distrubution de bernoulli
        x.append(a)
        if bernoulli(p)==0:
            psi=psi-1j*H*psi*dt-(dt**2)*H*H*psi/2
            psi=psi/psi.norm()
            #pho.append(abs(np.array(psi*psi.dag())[0][0]))
            moySz.append(expect(M7,psi*psi.dag()))
        else:
             a=[random.uniform(-100, 100),random.uniform(-100, 100),random.uniform(-100, 100),random.uniform(-100, 100),random.uniform(-100, 100),random.uniform(-100, 100)]
             l=(a[0]+1j*a[1])*psi01+(a[2]+1j*a[3])*psi00+(a[3]+1j*a[4])*psi0_1
             psi=l/l.norm()
            #pho.append(abs(np.array(psi*psi.dag())[0][0]))
             moySz.append(expect(M7,psi*psi.dag()))
    #print(np.array(moySz).shape)


    #y[:,j]=np.array(pho)
    z[:,k]=np.array(moySz)
    a,b=welch(moySz,1/dt,nperseg=10000)
    print(len(a))
    PSD[:,k]=np.array(b)
#print(np.array(pho).shape)
r=(np.mean(z, axis=1))
x= (np.mean(y, axis=1))
PSDM=(np.mean(PSD, axis=1))
times=np.linspace(0, T,N+1)
plt.figure(1)
plt.plot(times,r)

plt.plot

def lorentz(x, x0, gamma,w):
    return   w*((gamma/2)**2 / ((x - x0) ** 2 + (gamma/2) ** 2))
max_index = np.argmax(PSDM)
print(max(PSDM))
print(abs(a[max_index]))
c=np.linspace(2e6,8e6,2000000)
y1=lorentz(c,2*0.3e7,2*30e3,1.3444997458368919e-06)

plt.plot(a,PSDM,label="PSD")
plt.plot(c,y1,'r',linestyle='dashed',label="fit avec une lorentzienne de largeur gamma ")
plt.xlabel("fréquence en Hz")
plt.ylabel(r'$Tr(M_{7}.\rho)$')
plt.legend()

plt.xlim(0,0.8e7)
plt.ylim(0,1.8e-6)
plt.grid()
plt.show()

"""## Simluation relaxation aléatoire"""

"""définition des variables et des opérateures"""
psi0=Qobj(1/np.sqrt(3)*((np.array([1,1,1]))))
id3=qeye(3)
wl=3*10**(6)*2*np.pi
print(2*np.pi/wl)
w2=2*np.pi*50*10**3
Sx= np.sqrt(w2)*jmat(1,'x')
Sx2= np.sqrt(1.75*w2)*jmat(1,'x')
Sx3= np.sqrt(w2/(2*3))*jmat(1,'x')
Sz= jmat(1,'z')
Sp= np.sqrt(w2/2)*jmat(1,'+')
Sp2= np.sqrt(1.75*w2/2)*jmat(1,'+')
Sp3= np.sqrt(w2/(2*3))*jmat(1,'+')
Sm= np.sqrt(w2/2)*jmat(1,'-')
Sm2= np.sqrt(1.75*w2/2)*jmat(1,'-')
Sm3= np.sqrt(w2/(2*3))*jmat(1,'-')
M1=jmat(1,'z')
M2=jmat(1,'x')
M3=jmat(1,'y')
M4=Qobj(np.array([[0,0,1],[0,0,0],[1,0,0]]))
M5=Qobj(np.array([[0,0,1j],[0,0,0],[-1j,0,0]]))
M6=Qobj(1/np.sqrt(2)*np.array([[0,0,1j],[0,0,0],[-1j,0,0]]))
M7=Qobj(1/np.sqrt(2)*np.array([[0,-1j,0],[1j,0,1j],[0,-1j,0]]))
M8=Qobj(1/np.sqrt(3)*np.array([[1,0,0],[0,-2,0],[0,0,1]]))
H=Qobj([[0,wl/(np.sqrt(2)),0 ],[wl/(np.sqrt(2)),0,wl/(np.sqrt(2)) ],[0,wl/(np.sqrt(2)),0 ]])

dt=3.3333333333333335e-5/10000
times1=np.linspace(0, 3.3333333333333335e-5,10000)
stoc_solution1= smesolve(H, 1/3*id3, times1,c_ops=[Sx,Sp,Sm],sc_ops=[Sx,Sp,Sm],e_ops=[],ntraj=200,dW_factors=[1/np.sqrt(2)*(np.sqrt(dt)-1j*np.sqrt(dt)),1/np.sqrt(2)*(np.sqrt(dt)-1j*np.sqrt(dt)),1/np.sqrt(2)*(np.sqrt(dt)-1j*np.sqrt(dt))])
#stoc_solution2= smesolve(H, 1/3*id3, times1,c_ops=[Sx2,Sp2,Sm2],sc_ops=[Sx2,Sp2,Sm2],e_ops=[],ntraj=50,dW_factors=[np.sqrt(dt)+1j*np.sqrt(dt),np.sqrt(dt)+1j*np.sqrt(dt),np.sqrt(dt)+1j*np.sqrt(dt)])
#stoc_solution3= smesolve(H, 1/3*id3+1/3*M8, times1,c_ops=[Sx3,Sp3,Sm3],sc_ops=[Sx3,Sp3,Sm3],e_ops=[],ntraj=1,dW_factors=[np.sqrt(dt)+1j*np.sqrt(dt),np.sqrt(dt)+1j*np.sqrt(dt),np.sqrt(dt)+1j*np.sqrt(dt)])

def lorentz(x, x0, gamma,a):
    return   a*((gamma/2)**2 / ((x - x0) ** 2 + (gamma/2) ** 2))
M=np.array(stoc_solution1.states)

#print(M.shape)
#c=[]

x=[]
y=np.zeros((10000,200))
for j in range(200):
   c=[]
   d=[]
   for i in range(len(times1)):
    #b=M[0][i][0][0]
       c.append(np.trace(((M6)*M[j][i])))
       d.append(np.trace((M6*M[j][i])))
   a,b=welch(c,1/dt,nperseg=10000)
   print(len(a))
   print(len(b))
   y[:,j]=b
    #a.append(b)
    #d.append(M[0][i][2][2])
    #x.append(b+M[0][i][1][1]+M[0][i][2][2])
x= (np.mean(y, axis=1))
c1=np.linspace(0.5e5,2e7,20000)
y1=lorentz(c1,15*2*3e3,3*30e3,0.4e-9)
#print(np.array(a).shape)
plt.figure(1)
plt.plot(times1,d)
plt.figure(2)
plt.plot(a, x)
plt.plot(c1,y1)
plt.ylim(0,1e-9)
plt.xlim(0,2e7)

plt.figure(2)
plt.plot(a, x,label='PSD du signal')
z=np.array(x)
c1=np.linspace(0.5e5,2e7,20000)
print(max(x))
max_index = np.argmax(x)
print(a[max_index])
y1=lorentz(c1,2*3000000.0,14*2*30e3,2.2e-10)
plt.plot(c1,y1,'r')
plt.ylim(0,0.5e-9)
plt.xlim(0,2e7)
plt.plot(c1,y1,'r',label="fit avec une loretzienne")
plt.xlabel("fréquence en Hz")
plt.ylabel(r'$Tr(M_{7}.\rho)$')
plt.grid()
plt.legend()
plt.show()

"""Tentative à de la résolution à la main"""

"""définition des variables et des opérateures"""
psi0=Qobj(1/np.sqrt(1)*((np.array([1,0,0]))))
id3=qeye(3)
wl=3*10**(6)*2*np.pi
print(2*np.pi/wl)
w2=2*np.pi*50*10**3
Sx= np.sqrt(w2)*jmat(1,'x')
Sz= jmat(1,'z')
Sp= np.sqrt(w2/2)*jmat(1,'+')
Sm= np.sqrt(w2/2)*jmat(1,'-')

H=Qobj([[0,wl/(np.sqrt(2)),0 ],[wl/(np.sqrt(2)),0,wl/(np.sqrt(2)) ],[0,wl/(np.sqrt(2)),0 ]])
times = np.arange(0, 1, 0.0001)
"""fonction utile:"""
"psi=b(psi)dt+sigma(psi,t)dW"
p=time.time()
##le terme brownien.
def B(psi):
        a1=(expect(Sx.dag(),psi)/psi.norm()*Sx-1/2*expect(Sx,psi)*expect(Sx.dag(),psi)/(psi.norm())**2*id3-(1/2)*Sx.dag()*Sx)*psi
        b1=(expect(Sp.dag(),psi)/psi.norm()*Sp-1/2*expect(Sp,psi)*expect(Sp.dag(),psi)/(psi.norm())**2*id3-(1/2)*Sp.dag()*Sp)*psi
        c1=(expect(Sm.dag(),psi)/psi.norm()*Sm-1/2*expect(Sm,psi)*expect(Sm.dag(),psi)/(psi.norm())**2*id3-(1/2)*Sm.dag()*Sm)*psi
        return -1j*H*psi+a1+b1+c1
def a(psi):
        a=(Sx-expect(Sx,psi)/psi.norm())*psi
        return a
def b(psi):
        b=(Sp-expect(Sp,psi)/psi.norm())*psi
        return b
def c(psi):
        c=(Sm-expect(Sm,psi)/psi.norm())*psi
        return c


#Construction du mouvement brownien
def sampleswienner(n,T,M):  ## T c'est la durée sur laquelle on veut faire notre simulation ,celà dépendra des constantes de temps du système "à discuter"
  dt=T/n
  Z=np.random.normal(0,1,(6,M,n))
  Z=np.sqrt(dt)*np.random.normal(0,1,(6,M,n))
  ##W0=[np.zeros((2, M, 1)), np.zeros((2, M, 1))]
  W=np.cumsum(Z,axis=1)
  ##W=np.concatenate((W0,W),axis=0)
  return Z
def eulerstoc( N, T, psi0, M):
    Psit = [psi0]
    psittotale = []
    S = Sz
    dt = T / (N+1)
    valeurfinale =[0]*(N+1)
    moyennes = [0]*(N+1)
    moyennestotale = np.zeros((N+1, M))

    u = sampleswienner(N, T, M)
    for j in range(M):

        psi = psi0
        deltau1=(u[0, j, 0] ) + 1j * (u[1, j, 0] )
        deltau2=(u[2, j, 0] ) + 1j * (u[3, j, 0] )
        deltau3=(u[4, j, 0] ) + 1j * (u[5, j, 0] )
        #psi = psi + B(psi) * dt + a(psi) * deltau1 + b(psi)*deltau2+ c(psi)*deltau3
        #psi=psi/psi.norm()
        moyennes[0] = np.real(expect(S, psi0))
        #moyennes[1] =np.real(np.trace(S*psi*psi.dag()))

        for i in range(0, N):
            deltau1=(u[0, j, i] ) + 1j * (u[1, j, i] )
            deltau2=(u[2, j, i] ) + 1j * (u[3, j, i] )
            deltau3=(u[4, j, i] ) + 1j * (u[5, j, i] )
            ordre21=(a((a(psi)*dt**(0.5))+psi)-a(psi))*dt**(-0.5)*(deltau1**2-dt)/2
            ordre22=(b((b(psi)*dt**(0.5))+psi)-b(psi))*dt**(-0.5)*(deltau2**2-dt)/2
            ordre23=(c((c(psi)*dt**(0.5))+psi)-c(psi))*dt**(-0.5)*(deltau3**2-dt)/2
            psi = psi +  dt*(B(psi))  +  a(psi)*deltau1+b(psi)*deltau2+c(psi)*deltau3+ordre21+ordre22+ordre23
            psi=psi/psi.norm()
            ##Psit.append(psi)
            #moyennes[i] =expect(S,psi*psi.dag())
            moyennes[i+1] =np.real(expect(S,psi))
            ##print(moyennes[i])
            moyennestotale[:,j] = moyennes
            #print(moyennes)
    #print(moyennestotale)
    valeurfinale = list(((np.mean(moyennestotale, axis=1))))
    #print(valeurfinale)


    return (valeurfinale)
dt= 0.000009/1001
a= eulerstoc( 1000, 0.000009, psi0,1)
times=np.linspace(0, 0.000009,1001)
times1=np.linspace(0, 0.000009,1001)

stoc_solution = smesolve(H, psi0*psi0.dag(), times1,c_ops=[Sx,Sp,Sm],sc_ops=[Sx,Sp,Sm],e_ops=[Sz],ntraj=1,dW_factors=[np.sqrt(dt)+1j*np.sqrt(dt),np.sqrt(dt)+1j*np.sqrt(dt),np.sqrt(dt)+1j*np.sqrt(dt)])

result = mesolve(H, psi0*psi0.dag(), times, [Sx,Sp,Sm], [Sz])
plt.figure(1)
plt.plot(times,a,label='mon algo')
plt.plot(times, result.expect[0],label='équation maitresse')
plt.plot(times1, stoc_solution.expect[0],label='qutip résoltution')
plt.show()