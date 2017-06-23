import numpy as np
from ase.build import bulk
from ase.visualize import view
from ase import Atoms, Atom
from ase.io import write

#==============================================================================
#Leer número de Carbonos SP3,SP2 y H y prioridades iniciales
#==============================================================================

with open ('hac.input') as f:
    inputF = f.readlines()
#    for k, line in enumerate(f.readlines()):
#        if k<=1 :    
#            comp.append(int(line))
#        elif k>1 and k<len(f.readlines()):
#            priority.append(int(line))
#        dens = float( f.readlines()[-1])

comp = [ int(i) for i in inputF[0:1+1] ]
priority = [ int(i) for i in inputF[2:3+1] ]
dens = float(inputF[4])

#==============================================================================
#Hacer celda cúbica y poner carbono
#==============================================================================

rH = 1.2
rC =0.77
a, p =  [] ,  []
a.append ('C') , p.append ([0.,0.,0.])
hac = Atoms(a,p)

simulation = hac

def arist(simulation):
    mass= (np.sum(simulation.get_masses()))/6.023e23
    l = np.cbrt((dens*mass)*1e24)
    return l

simulation.set_cell(arist(simulation)*np.identity(3))
simulation.set_pbc((True,True,True))
simulation.center()

view(simulation)

#==============================================================================
# Añadir 2º carbono y primera optimización y espectro infrarrojo
#==============================================================================

lastpos = simulation.positions[-1]
simulation.append(Atom('C',(lastpos[0] +0. ,lastpos[1]+ 0 , lastpos[2]+1.3)))

simulation.center()
view (simulation)
#==============================================================================
# Empezamos a iterar para construir el grano.
#==============================================================================
import random

def newR(atomType):
    if atomType=='C': r=1.4
    else:  r=1.1 
    theta = random.uniform( (-109.0-90)*np.pi/180,(120.0-90)*np.pi/180 )
    phi = random.uniform( -109.0*np.pi/180, 120*np.pi/180 )
    return (r*np.cos(phi)*np.sin(theta),r*np.sin(phi)*np.sin(theta),r*np.cos(theta))

def cons1(sim,sel):
    near=[]
    for k in range(len(sim)):
        if k==sel:
            pass
        else:
            dist=sim.get_distance(sel,k)
            if dist<1.4: near.append(k)
    return near

#Bucle de prueba para ver que los átomos se van colocando aleatoriamente en el espacio. ()    
i=0
indexes = [0, 1]


while True:
    selected = random.choice(indexes)
    lastpos = simulation.positions[selected]
    if simulation.get_atomic_numbers()[selected] == 6: #Obligamos al sistema a escoger carbono
          near=cons1(simulation,selected)
          if len(near)<3:
              if random.randint(1,2) ==1.:
                  nX, nY, nZ = newR('C')
                  (X,Y,Z)=(lastpos[0]+nX , lastpos[1]+nY, lastpos[2]+nZ)
                  flag=[]
                  for otherPos in simulation.positions:
                      if otherPos == np.asarray(lastpos): pass
                      elif np.linalg.norm(np.asarray([X,Y,Z])-np.asarray(otherPos))<1.4:
                          flag.append(1)
                      else: flag.append(0)
                  if 1 not in flag:
                      simulation.append(Atom('C',(lastpos[0]+nX , lastpos[1]+nY, lastpos[2]+nZ)))
                  else: pass
              else:
                  nX, nY, nZ = newR('H')
                  simulation.append(Atom('H',(lastpos[0]+nX , lastpos[1]+nY, lastpos[2]+nZ)))
              simulation.set_cell(arist(simulation)*np.identity(3))
              simulation.center()
              view (simulation)
              i+=1
              print(i)
              indexes.append(i)
              if i==6: break
          else: indexes.remove(selected)
    else: pass

view (simulation)

    

