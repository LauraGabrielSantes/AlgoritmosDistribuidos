# construye una instancia de la clase Simulation recibiendo como parametros el nombre del 
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion
import sys
import time
from event import Event
from simulation import Simulation
from algoritmoLCR import AlgoritmoLCR

class main():
 if len(sys.argv) != 2:
  print ("Por favor proporcione el nombre de la grafica de comunicaciones")
  raise SystemExit(1)
    
 inicio = time.time()
 experiment = Simulation(sys.argv[1], 100)  
 m = AlgoritmoLCR()
 # asocia un pareja proceso/modelo con cada nodo de la grafica
 for i in range(1,len(experiment.graph)+1):
  experiment.setModel(m, i)
  m = AlgoritmoLCR()

 # inserta un evento semilla en la agenda y arranca
 inicia=("INICIA",None)
 seed = Event(inicia, 0.0, 6, 1)
 experiment.init(seed)
 experiment.run()
 fin = time.time()
 print("Se han generado ", AlgoritmoLCR.contadorMensajes," mensajes en total \n")
 print("Tiempo de ejecución:", fin-inicio, "segundos \n")