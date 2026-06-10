# construye una instancia de la clase Simulation recibiendo como parametros el nombre del 
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion
import sys
from event import Event
from simulation import Simulation
from dfs import AlgoritmoDFS

class main():
 if len(sys.argv) != 2:
  print ("Por favor proporcione el nombre de la grafica de comunicaciones")
  raise SystemExit(1)
    
 experiment = Simulation(sys.argv[1], 100)  
 m = AlgoritmoDFS()
 # asocia un pareja proceso/modelo con cada nodo de la grafica
 for i in range(1,len(experiment.graph)+1):
  experiment.setModel(m, i)
  m = AlgoritmoDFS()

 # inserta un evento semilla en la agenda y arranca
 seed = Event("INICIA", 0.0, 1, 1)
 experiment.init(seed)
 experiment.run()
 print("Se han generado ", AlgoritmoDFS.contadorMensajes," mensajes en total \n")
