#Importar Librerias ------------------------------------------------------------------------------------------------------------------------
import requests
import sys
import random
import copy
import math
from itertools import product
import time


#Funcion para extraer informacion sobre las instancias -------------------------------------------------------------------------------------
Instancias = {}
Contador=0
for i in range(7):
    for j in range(100):
        Contador+=1
        nombre_archivo=("wtpack"+str(i+1)+"_"+str(j+1)+".txt")
        with open(nombre_archivo, "r") as archivo:
            lista=[]
# Lee cada línea del archivo y la agrega a la list
            for linea in archivo:
                lista.append(list(map(float,linea.split())))
            Instancias[Contador]=lista

#Explicacion Instancias --------------------------------------------------------------------------------------------------------------------
#Existen 700 instancias
#Las instacias son diccionarios con #id como llave y contienen una lista de listas.
# la primera lista contienen la informacion del largo, ancho, alto de contenedor
#Instacnia[ID][0][0]=Largo , #Instacnia[ID][0][1] = Ancho , #Instacnia[ID][0][2]=Alto
Instancias[1][0][0]

    
Instancias[1][1][0]
#la segunda lista contiene la informacion sobre el numero de tipos de cajas y el volumen en m3 total ocupado
Instancias[1][1][0]

# las siguientes listas contiennes informacion sobre cada tipo de caja
# esta organizada por: longitud, indicador: ubicacion vertical de longitud permitida, ancho, indicador, altura, indicador, numero de cajas,
#peso, capacidad de carga si la longitud esta en vertical, 
#capacidad de carga si el ancho esta en vertical
#capacidad de carga si la altura esta en vertical (11 indices en total) y Instancias[1][1][0] de filas

Instancias[1][3][0]

#TipoCajas ---------------------------------------------------------------------------------------------------------------------------------
#crear la clase cajas que con contiene la informacion del tipo de Caja que contiene la instancia
#InformacIon del Id, longitud indicador de rotacion en longitud, ancho, .. ........ , Cantidad, Peso,
#PesoCapas de soportar en longitud, ................, Y finalmente se genera una lista donde se agregan
# las diferentes rotaciones que puede tomar el tipo de caja

class TipoCaja:
    def __init__(self, id, lx,rx, ly,ry, lz,rz, cantidad, peso, cargax, cargay, cargaz):
        self.id = id #definirlo nosotros (1,2,..n)
        self.lx = lx
        self.rx = rx #rotacion de la caja
        self.ly = ly
        self.ry = ry
        self.lz = lz
        self.rz = rz
        self.cantidad = cantidad
        self.peso = peso
        self.cargax = cargax
        self.cargay = cargay
        self.cargaz = cargaz
        self.q0 = cantidad
        self.listaCajaRot= []
        #lista caja rotada es un tipo elemento caja rot

# CajasEmpacadas --------------------------------------------------------------------------------------------------------------------------
#Esta clase solicita informacion sobre las posiciones de las aristan en el eje X,Y y Z
#en el area del contenedor ademas de el peso soportado
class CajaEmpacada:
    def __init__(self, px1,px2, py1, py2, pz1, pz2, sopAbajo, Tipo):
        self.px1 = px1
        self.px2 = px2
        self.py1 = py1
        self.py2 = py2
        self.pz1 = pz1
        self.pz2 = pz2
        self.sopAbajo=sopAbajo
        self.Tipo=Tipo

# Espacio -----------------------------------------------------------------------------------------------------------------------------------
#Esta clase crea expacios maximales dentro del contenedor solicitando la posicion de las aristas y el peso que puede soportar el espacio
#Ademas de lo anterior creara un esquina de la base inferior alatoria entre 1 a 4
#la cual sera un indidor de donde se empacar una la caja en ese espacio maximal

class Espacio:
    def __init__(self, px1,px2, py1, py2, pz1, pz2,sm= sys.float_info.max):
        self.px1 = px1
        self.px2 = px2
        self.py1 = py1
        self.py2 = py2
        self.pz1 = pz1
        self.pz2 = pz2
        self.sm = sm
        self.esquina = 1  #definir la esquina con distancia manhatahan


#CajaRota ------------------------------------------------------------------------------------------------------------------------------------
#Esta clase contienen
# sm = soporte maximo
# Definiimos una clase de caja rotada que tendra como como entrada el ID, X,Y,Z=su longitud en el
#eje X, Y, Z, y el peso soportado sobre el espacio maximal en el que estamos.

class CajaRot:
    def __init__(self,id, x, y, z, c,pes):
        self.id= id
        self.x =x
        self.y = y
        self.z = z
        self.p = c
        self.pes=pes

#Contenedor--------------------------------------------------------------------------------------------------------------------------------------------------------
# Se crea una clase llamada contenedor, esta clase contiene varias listas y metodos utilizados para
#la heuristica.
class Contenedor:
    def __init__(self, listaTC):
        # Parámetros
        self.listaTC = listaTC #Esta lista guarda los tipos de cajas que la instancia tienen
        self.listaCE = []  # Esta lista contiene todas las Cajas empacadas en el contenedor
        self.listaEM = []  # Lista que contiene los espacios maximales dentro del contenedor - Espacios maximales se inicializa con el espacio del contenedor
        self.utilizacion = 0  # Funcion Objetivo Se inicializa con 0 y no puede ser mayor a 1
        self.FaltanCajasPorEmpacar=0
    # Métodos
    #Este metodo crear el primer espacio maximal del contenedor siendo las dimensiones del contenedor los imputs
    def CrearPrimerEspacio(self):
        if len(self.listaCE) == 0:
            self.listaEM.append(DimensionesContenedor)

    #El metodo  EmpcarCaja tiene como Imputs una caja rotada y un espacio maximal,
    #Verifica si las dimensiones de la caja rotada caben dentro de las dimensiones del expacio maximal
    #Y de ser asi, crear una clase de caja empacada y asigna su posicion de acuerdo a la esquina
    #Ademas la agrega a la lista de cajasempacadas

    def EmpacarCaja(self,CajaRota , EMaximal, Tipo):
        
        if ((EMaximal.px2 - EMaximal.px1) >= CajaRota.x  and
            (EMaximal.py2 - EMaximal.py1) >= CajaRota.y and
            (EMaximal.pz2 - EMaximal.pz1) >= CajaRota.z):


            if EMaximal.esquina == 1:
               CajaPorEmpacar= CajaEmpacada(EMaximal.px1, EMaximal.px1 + CajaRota.x, EMaximal.py1, EMaximal.py1 + CajaRota.y, EMaximal.pz1, EMaximal.pz1+CajaRota.z, min(CajaRota.p,EMaximal.sm), Tipo )
               
            if EMaximal.esquina == 2:
               CajaPorEmpacar= CajaEmpacada(EMaximal.px1, EMaximal.px1 + CajaRota.x, EMaximal.py2-CajaRota.y, EMaximal.py2, EMaximal.pz1, EMaximal.pz1+CajaRota.z, min(CajaRota.p,EMaximal.sm),Tipo)
               
            if EMaximal.esquina == 3:
                CajaPorEmpacar=CajaEmpacada(EMaximal.px2-CajaRota.x, EMaximal.px2, EMaximal.py1, EMaximal.py1 + CajaRota.y, EMaximal.pz1, EMaximal.pz1+CajaRota.z, min(CajaRota.p,EMaximal.sm),Tipo)
                
            if EMaximal.esquina == 4:
                CajaPorEmpacar=CajaEmpacada(EMaximal.px2-CajaRota.x, EMaximal.px2,  EMaximal.py2-CajaRota.y, EMaximal.py2, EMaximal.pz1, EMaximal.pz1+CajaRota.z, min(CajaRota.p,EMaximal.sm),Tipo )
                
            self.listaCE.append(CajaPorEmpacar)

    #Este metodo crea espacios maximales de acuerdo al espacio maximal de acuerdo a una caja empacada.
    #Dado que esta contenida dentro del espacio, se crearan otrds espacios maximales dentro del los
    #limites del espacio original.
    def CrearEMP(self,CEmpacada,Emaximal):

        x1=CEmpacada.px1
        x2=CEmpacada.px2
        y1=CEmpacada.py1
        y2=CEmpacada.py2
        z1=CEmpacada.pz1
        z2=CEmpacada.pz2
        xx1=Emaximal.px1
        xx2=Emaximal.px2
        yy1=Emaximal.py1
        yy2=Emaximal.py2
        zz1=Emaximal.pz1
        zz2=Emaximal.pz2
        
        
        
        if xx2>x2:  
            self.listaEM.append(Espacio(x2,xx2,yy1,yy2,zz1,zz2,Emaximal.sm ))

        if xx1<x1:
            self.listaEM.append(Espacio(xx1,x1,yy1,yy2,zz1,zz2,Emaximal.sm))

        if yy2>y2:
            self.listaEM.append(Espacio(xx1,xx2,y2,yy2,zz1,zz2,Emaximal.sm))

        if y1>yy1:
            self.listaEM.append(Espacio(xx1,xx2,yy1,y1,zz1,zz2,Emaximal.sm))

        if zz2>z2:
            self.listaEM.append(Espacio(xx1,xx2,yy1,yy2,z2,zz2,min(Emaximal.sm-CEmpacada.sopAbajo,CEmpacada.sopAbajo)))


        return

    #para este metodo, se recibe como parametro un i que indica la posicion del espacio maximal dentro
    #de la lista de espacios maximales dentro del contenedor y la elimina
    def EliminarEspaciosMaximales(self, i):
        del self.listaEM[i]

    #El metodo busca dentro de la lista de espacios maximale aquellos que esten siendo
    #Contenidos por otros espacios maximales y los elimina

    def EliminarEspaciosContenidos(self):
        
        listaContenidos=[]
        
        for i in range(len(self.listaEM)):
            for j in range(len(self.listaEM)):
                if i != j:
                    if ((self.listaEM[i].px1 <=  self.listaEM[j].px1 and self.listaEM[j].px2 <=  self.listaEM[i].px2) and
                        (self.listaEM[i].py1 <=  self.listaEM[j].py1 and self.listaEM[j].py2 <=  self.listaEM[i].py2) and
                        (self.listaEM[i].pz1 <=  self.listaEM[j].pz1 and self.listaEM[j].pz2 <=  self.listaEM[i].pz2)):
                        
                        listaContenidos.append(self.listaEM[j])
                        
                        if self.listaEM[i].pz1>0:
                            self.listaEM[i].sm+= self.listaEM[j].sm
                        
        
        conjunto_unicos = set(listaContenidos)
        lista_unicos = list(conjunto_unicos)  
        

        
        
        if len(lista_unicos)>0:

            Lista_Nueva = [element for element in self.listaEM if element not in lista_unicos]
            self.listaEM = Lista_Nueva

    #Este Metodo tiene como objetivo utilizar los metodos de crear y elimiar espacio maximales dada una caja empacada
    # su objetivo es que dada una caja empacada, buscamos entre los espacios maximales aquellos que contienen la caja
    # Dado que si la caja se empaco entonces almenos uno de los espacios la contiene
    # Si hay mas, entonces se crear los espacios maximales contenidos en sus limites y se elimina


    def ActualizarEspaciosMaximales(self, CEmpacada):
        ListaEliminar=[]
        for i in range(len(self.listaEM)):
              x1=CEmpacada.px1
              x2=CEmpacada.px2
              y1=CEmpacada.py1
              y2=CEmpacada.py2
              z1=CEmpacada.pz1
              z2=CEmpacada.pz2
              

              
              xx1=self.listaEM[i].px1
              xx2=self.listaEM[i].px2
              yy1=self.listaEM[i].py1
              yy2=self.listaEM[i].py2
              zz1=self.listaEM[i].pz1
              zz2=self.listaEM[i].pz2
              

              if not (xx1 >= x2 or x1 >= xx2 or yy1 >= y2 or y1 >= yy2 or zz1 >= z2 or z1 >= zz2):
                  ListaEliminar.append(i)

                  
        if len(ListaEliminar)>0:
            for Esp in ListaEliminar[::-1]:

                
                self.CrearEMP(CEmpacada,self.listaEM[Esp])
                
                self.EliminarEspaciosMaximales(Esp)
                


#Heuristica- -----------------------------------------------------------------------

#Definimos la instancia de acuerdo a las encontradas en la base de datos
InstanciaPrueba=201
#******************************************************************************************************************************

#Dada una instancia, definimos el numero de tipos de cajas de la instancia
NumeroDeCajas = int(Instancias[InstanciaPrueba][1][0])

#******************************************************************************************************************************

#Utilizaremos 2 diccionarios para meter a informacion dada la instancia
DiccionarioInstancia = {}
DiccionarioTipoCaja = {}
DiccionarioInstancia[InstanciaPrueba]=DiccionarioTipoCaja

#Tambien Incializaremos la variable del numero de cajas disponibles en la instancia con 0
NumerosDeCajasPorInstancia=0

#******************************************************************************************************************************

inicio = time.time()



 # 1.0005340576171875
# para cada tipo de caja definiremos una clase de tipo de caja y meteremos la informacion en un 
# diccionario dado el tipo de caja i, definimos la clase de caja i. Tambien asiganeros el valor
# de la variable NumerosDeCajasPorInstancia

for i in range(NumeroDeCajas):
    
    Id= i 
    lx=Instancias[InstanciaPrueba][2+i][0]
    rx=Instancias[InstanciaPrueba][2+i][1]
    ly=Instancias[InstanciaPrueba][2+i][2]
    ry=Instancias[InstanciaPrueba][2+i][3]
    lz=Instancias[InstanciaPrueba][2+i][4]
    rz=Instancias[InstanciaPrueba][2+i][5]
    cantidad=Instancias[InstanciaPrueba][2+i][6]
    peso=Instancias[InstanciaPrueba][2+i][7]
    cargax=Instancias[InstanciaPrueba][2+i][8]
    cargay =Instancias[InstanciaPrueba][2+i][9]
    cargaz=Instancias[InstanciaPrueba][2+i][10]
    
    ClaCaja = TipoCaja(Id, lx,rx, ly,ry, lz,rz, cantidad, peso, cargax, cargay, cargaz)
    
    DiccionarioInstancia[InstanciaPrueba][i]=ClaCaja
    
    NumerosDeCajasPorInstancia+= Instancias[InstanciaPrueba][2+i][6]

#******************************************************************************************************************************
DiccionarioInstancia[InstanciaPrueba][0].lx
DiccionarioInstancia[InstanciaPrueba][0].ly
DiccionarioInstancia[InstanciaPrueba][0].lz

#Organizamos las clases de tipo de caja de acuerdo a su volumen de mayor a menor
listaVolumenMayor = sorted(DiccionarioInstancia[InstanciaPrueba].items(), key=lambda x: -x[1].lx * x[1].ly * x[1].lz)

#******************************************************************************************************************************
    
#Crearemos un espacio maximal con las dimensiones de la caja
DimensionesContenedor =Espacio(0,Instancias[InstanciaPrueba][0][0],0,Instancias[InstanciaPrueba][0][1],0,Instancias[InstanciaPrueba][0][2]) 

#******************************************************************************************************************************
 
#Dada la informacion de la instancia, definiremos para cada tipo de caja todas las rotaciones posibles

RotacionPorTipodeCajas={}

for J in range(NumeroDeCajas):
    RotacionPorTipodeCajas[J]=[]
    TpCaja = DiccionarioInstancia[InstanciaPrueba][J]
    
    if TpCaja.rx ==1 :
        RotacionPorTipodeCajas[J].append(CajaRot(TpCaja.id,TpCaja.ly,TpCaja.lz,TpCaja.lx,TpCaja.cargax,(TpCaja.peso/(TpCaja.ly*TpCaja.lz))))
        RotacionPorTipodeCajas[J].append(CajaRot(TpCaja.id,TpCaja.lz,TpCaja.ly,TpCaja.lx,TpCaja.cargax,(TpCaja.peso/(TpCaja.ly*TpCaja.lz))))
    if TpCaja.ry ==1 :
        RotacionPorTipodeCajas[J].append(CajaRot(TpCaja.id,TpCaja.lx,TpCaja.lz,TpCaja.ly,TpCaja.cargay,(TpCaja.peso/(TpCaja.lx*TpCaja.lz))))
        RotacionPorTipodeCajas[J].append(CajaRot(TpCaja.id,TpCaja.lz,TpCaja.lx,TpCaja.ly,TpCaja.cargay,(TpCaja.peso/(TpCaja.lx*TpCaja.lz))))
    if TpCaja.rz ==1 :
        RotacionPorTipodeCajas[J].append(CajaRot(TpCaja.id,TpCaja.ly,TpCaja.lx,TpCaja.lz,TpCaja.cargaz,(TpCaja.peso/(TpCaja.ly*TpCaja.lx))))
        RotacionPorTipodeCajas[J].append(CajaRot(TpCaja.id,TpCaja.lx,TpCaja.ly,TpCaja.lz,TpCaja.cargaz,(TpCaja.peso/(TpCaja.ly*TpCaja.lx))))
   
#******************************************************************************************************************************
 
#HEURISTICA


#Definiremos el contenedor con los tipos de cajas y crearemos el primer espacio ademas de la variable
# que determina si hacen faltas por empacar. Tambien agregaremos un diccionario que contendra los movimientos de la solucion
Movimientos={}
ContenedorActual=Contenedor(listaVolumenMayor)   
ContenedorActual.CrearPrimerEspacio()
ContenedorActual.FaltanCajasPorEmpacar=NumerosDeCajasPorInstancia

# mientas hallan cajas posibles por ingresa, hallan espacios maximales disponibles y falten cajas por ingresas
# iteraremos ingresando cajas en el contenedor

#Generaremos variables para el espacio maximal de prueba, indice de tipo de cajas disponibles en la lista y 
#Una lista de rotaciones
    
EspacioMaximal=None
NTipoCaja=None
Rotaciones = []
    
while (len(ContenedorActual.listaEM)>0 and ContenedorActual.FaltanCajasPorEmpacar> 0):  
    for EM in range(len(ContenedorActual.listaEM)): #Buscaremos entre todos los espacios maximales del contenedor
        EMSeleccionado = ContenedorActual.listaEM[EM]
        for G in range(len(ContenedorActual.listaTC)): #Buscaremos dentro de la lista ordenada por volumen de los tipos de caja
    
                #Seleccionar una caja rotada Iniciando desde la de mayor volumen
    
                Mayor=G # variable que indica la posicion en la lista del tipo de caja seleccionado
    
                Tipo=ContenedorActual.listaTC[Mayor][0] # Asignamos la clase de tipo de caja a la variable

                # Dado Un tipo de caja seleccioando, Extraemos la informacon de la cantidad de cajas disponibles de este tipo
                Cn=ContenedorActual.listaTC[Mayor][1].q0
    
                Rotaciones = []
    
                if Cn>0: #verificamos si hay cajas de ese tipo por empacar
                    # para cada rotacion de ese tipo, verificamos si esta esta contenida y si puede ser soportada
                    for i in range(len(RotacionPorTipodeCajas[Tipo])):
                        
                       
                        if ((EMSeleccionado.px2 - EMSeleccionado.px1) >= RotacionPorTipodeCajas[Tipo][i].x  and
                            (EMSeleccionado.py2 - EMSeleccionado.py1) >= RotacionPorTipodeCajas[Tipo][i].y and
                            (EMSeleccionado.pz2 - EMSeleccionado.pz1) >= RotacionPorTipodeCajas[Tipo][i].z):
    
                            if RotacionPorTipodeCajas[Tipo][i].pes <=EMSeleccionado.sm:
                        
                                Rotaciones.append( RotacionPorTipodeCajas[Tipo][i])
                # Una vez analizadas las rotaciones, verificaremos si alguna rotacion sirve

                if len(Rotaciones)>0:
                    NTipoCaja=Mayor
                    # Si hay almenos una rotacion asiganremos al NtipoCajas el indice que indica la posicion de la clasedisponible
                    break # de haber alguna rotacion valida dejamos de buscar en los tipos de caja
        if len(Rotaciones)>0:
          EspacioMaximal = EM #si hay almenos alguna rotacion que se contenga en ese espacio maximal, selecionamos el EM

          break
        
        #Una vez que encontramos la caja y el espacio Maximal verificamos si las variables correspondientes
        #No estan vacias
        
        #Para ello verificamos si hay almenos una rotacion valida para ser asignada
    if len(Rotaciones)==0:
        ContenedorActual.FaltanCajasPorEmpacar=0 # Si no hay una rotacion significa que no es posible asignar mas cajas de ninguna tipo a ningun espacio, Terminamos la heuristica

    else:

        #Empacamos la caja seleccionada en el espacio seleccionado
      
        CajasAdentroAntes = len(ContenedorActual.listaCE) #Indicaremos cuantas cajas hay en la solucion antes de ingresar la caja
        
        H=ContenedorActual.listaEM[EspacioMaximal]
        
        #Elegimos como criterio la primera rotacion valida dentro de la lista (debe contener almenos 1)
        #La primera rotaciond e la lista representa la que mejor proporciones tiene respecto al espacio maximal
        
        RotaMayor = sorted(Rotaciones, key=lambda x: -x.x/(H.px2 - H.px1) - x.y/(H.py2 - H.py1)- x.z/(H.pz2 - H.pz1))
        
        Rotaciones=RotaMayor
        
        #Crearemos el movimiento con la solucion antes de ingresasr la caja, el tipo de caja que se va a ingresar y la rotacion 
        Movimientos[CajasAdentroAntes]= {"Contenedor": copy.deepcopy(ContenedorActual), "Caja por meter":NTipoCaja , "Rotacion":Rotaciones[0] }
        
        #Se empaca la caja
        ContenedorActual.EmpacarCaja(Rotaciones[0], ContenedorActual.listaEM[EspacioMaximal],ContenedorActual.listaTC[NTipoCaja][0])
        #Se resta a la cantidad de cajas disponibles  
        ContenedorActual.listaTC[NTipoCaja][1].q0 += (-1)
        
        #Se resta una caja al total general
        ContenedorActual.FaltanCajasPorEmpacar += (-1)
        
        #Se actualiza la utilizacion
        ContenedorActual.utilizacion =ContenedorActual.utilizacion+(Rotaciones[0].x*Rotaciones[0].y*Rotaciones[0].z)/(DimensionesContenedor.px2*DimensionesContenedor.py2*DimensionesContenedor.pz2)
          
        # Dada la caja empacada, actualizamos los espacios maximales donde si alguno de estos contiene la cajaempacada
        # se generan nuevos espacios maximales en los limites de ese espacio y se elimina (Si la caja se empaco
        # almenos debe haber 1 espacio maximal que lo contenga)
          
        ContenedorActual.ActualizarEspaciosMaximales(ContenedorActual.listaCE[-1])
          
        # Verificamos que dado los nuevos espacios maximales, eliminamos aquellos que estan contenidos
        # dentro de otro año
        
        ContenedorActual.EliminarEspaciosContenidos()
        
        #Se reorganiza la lista para que los primeros espacios sean los mas cercanos a la superficie inferior de Contenedor
        EMMayor = sorted(ContenedorActual.listaEM, key=lambda x: (x.pz1))
        ContenedorActual.listaEM=EMMayor
################################################################################################################################################################################################################################
#METAHEURISTICA
################################################################################################################################################################################################################################




#Calcularemos el numero de iteraciones de cajas por sacar (Esto representa la cantidad de vecinos que se generaran)
NumeroDecajasSacar=int(0.5*len(ContenedorActual.listaCE))

#Este representa la cantidad de cajas consecutivas que se sacaran (Representa el cambio de vecindario)
IteracionesShak=int(0.075*len(ContenedorActual.listaCE))

#Se considera una solucion global que sera la mejor
SolucionGlobal=ContenedorActual.utilizacion

#Tambien se guardara el contendor global que contiene toda la informacion de la solucion
ContendorGlobal=ContenedorActual

#Estas variables identifican la solucion actual del vecindario en el que se trabaje y cambiaran a media que se itere en los vecindarios
MejorSolucionActualContenedor =ContenedorActual
MejorSolucionActualUtilidad =ContenedorActual.utilizacion
MejorSolucionActualMovimientos =Movimientos

#Tiempo inicial
time1=time.time()

#
ContenedorActual

#Para cada cambio de veindario
for Shake in range(IteracionesShak):
    
    #Los salto representan la cantidad de cajas que se sacaran para generar los vecinos
    Saltos=Shake+1
    #Este guardara a los vecinos
    VecindarioSoluciones={}
    

    
    #Generaremos vecinos
    for PO in range(NumeroDecajasSacar):
        # Elegiremos un movimietno de manera aleatoria
        MovimientoDeprueba=random.choice(list(MejorSolucionActualMovimientos))
        
        #Definieremos la solucion incial como las cajas empacadas hasta ese momento
        SolucionIncial=MejorSolucionActualMovimientos[MovimientoDeprueba]
        
        ContenedorSolu = copy.deepcopy(SolucionIncial["Contenedor"])
        RotacionSolu = SolucionIncial["Rotacion"]
        TipoDeCajaMeterSolu= SolucionIncial["Caja por meter"]
        
        
        #Definimos numero de cajas faltantes por empacar
        ContenedorSolu.FaltanCajasPorEmpacar= NumerosDeCajasPorInstancia- len(ContenedorSolu.listaCE)
        
        NumeroDeSaltos=Saltos
        
        
        EspacioMaximal=None
        NTipoCaja=None
        Rotaciones = []
        Movimientos2={}  
        
        
        while (len(ContenedorSolu.listaEM)>0 and ContenedorSolu.FaltanCajasPorEmpacar> 0 and ContenedorSolu.utilizacion<=1):
            Rotaciones = []
            if NumeroDeSaltos>0:
                #Crearemos una lista para guardas combinaciones
                Combinada=[]

                for G in range(len(ContenedorSolu.listaTC)): #Buscaremos dentro de la lista ordenada por volumen de los tipos de caja
                       
                                     
                        Mayor=G # variable que indica la posicion en la lista del tipo de caja seleccionado                       
                        Tipo=ContenedorSolu.listaTC[Mayor][0] # Asignamos la clase de tipo de caja a la variable
                        #Encontraemos todas la posibles combiancaiones de como meter las cajas
                        if ContenedorSolu.listaTC[Mayor][1].q0 >0:
                            Combinada.extend(product(list(range(len(ContenedorSolu.listaEM))), [Mayor], RotacionPorTipodeCajas[Tipo]))
                # Busaremos en las combinaciones    
                while len(Combinada)>0:   
                    
                    #Elegiremos una combinacion aleatoriamente
                    Elegido=random.choice(Combinada)           
                    Cn=ContenedorSolu.listaTC[Elegido[1]][1].q0
                    EMSeleccionado=ContenedorSolu.listaEM[Elegido[0]]
                    
                    
                    #verificamos si la caja se puede empacar
                    if Cn>0: 
                        # para cada rotacion de ese tipo, verificamos si esta esta contenida y si puede ser soportada
        
                        if ((EMSeleccionado.px2 - EMSeleccionado.px1) >= Elegido[2].x  and
                            (EMSeleccionado.py2 - EMSeleccionado.py1) >= Elegido[2].y and
                            (EMSeleccionado.pz2 - EMSeleccionado.pz1) >= Elegido[2].z):
        
                            if Elegido[2].pes <=EMSeleccionado.sm:
                                 Rotaciones.append(Elegido[2])
                    #Si la combinacion no puede entrar, se elimina de la lista de combiandos             
                    if len(Rotaciones)==0:
                        if Elegido in Combinada:

                            Combinada.remove(Elegido)
                    #Si la combinacion  puede entrar, se seleccionan los datos 
                    else:
                        EspacioMaximal=Elegido[0]
                        NTipoCaja=Elegido[1]
                        break
                # Si entra, restaremos 1 a la cantidad de cajas consecutivas por meter         
                if not len(Rotaciones) ==0:
                    
                    NumeroDeSaltos += (-1)
                else:
                    #si ninguna caja entra, se termina el proceso llevando a que no falten cajas por empacar
                    ContenedorSolu.FaltanCajasPorEmpacar=0
            else:  
                #Si ya se acabaron las cajas que se cambiaron, se realiza el mismo proceso de la heuristica para recontruir el resto de la solucion
                for EM in range(len(ContenedorSolu.listaEM)): #Buscaremos entre todos los espacios maximales del contenedor
                    EMSeleccionado = ContenedorSolu.listaEM[EM]
                    for G in range(len(ContenedorSolu.listaTC)): #Buscaremos dentro de la lista ordenada por volumen de los tipos de caja
                
                            #Seleccionar una caja rotada Iniciando desde la de mayor volumen
                
                            Mayor=G # variable que indica la posicion en la lista del tipo de caja seleccionado
                
                            Tipo=ContenedorSolu.listaTC[Mayor][0] # Asignamos la clase de tipo de caja a la variable
            
                            # Dado Un tipo de caja seleccioando, Extraemos la informacon de la cantidad de cajas disponibles de este tipo
                            Cn=ContenedorSolu.listaTC[Mayor][1].q0
                
                            Rotaciones = []
                
                            if Cn>0: #verificamos si hay cajas de ese tipo por empacar
                                # para cada rotacion de ese tipo, verificamos si esta esta contenida y si puede ser soportada
                                for i in range(len(RotacionPorTipodeCajas[Tipo])):
                                    
                                   
                                    if ((EMSeleccionado.px2 - EMSeleccionado.px1) >= RotacionPorTipodeCajas[Tipo][i].x  and
                                        (EMSeleccionado.py2 - EMSeleccionado.py1) >= RotacionPorTipodeCajas[Tipo][i].y and
                                        (EMSeleccionado.pz2 - EMSeleccionado.pz1) >= RotacionPorTipodeCajas[Tipo][i].z):
                
                                        if RotacionPorTipodeCajas[Tipo][i].pes <=EMSeleccionado.sm:
                                    
                                            Rotaciones.append( RotacionPorTipodeCajas[Tipo][i])
                            # Una vez analizadas las rotaciones, verificaremos si alguna rotacion sirve
            
                            if len(Rotaciones)>0:
                                NTipoCaja=Mayor
                                # Si hay almenos una rotacion asiganremos al NtipoCajas el indice que indica la posicion de la clasedisponible
                                break # de haber alguna rotacion valida dejamos de buscar en los tipos de caja
                    if len(Rotaciones)>0:
                      EspacioMaximal = EM #si hay almenos alguna rotacion que se contenga en ese espacio maximal, selecionamos el EM
            
                      break
                
                #Una vez que encontramos la caja y el espacio Maximal verificamos si las variables correspondientes
                #No estan vacias
                
                #Para ello verificamos si hay almenos una rotacion valida para ser asignada
            if len(Rotaciones)==0:
                ContenedorSolu.FaltanCajasPorEmpacar=0 # Si no hay una rotacion significa que no es posible asignar mas cajas de ninguna tipo a ningun espacio, Terminamos la heuristica
        
            else:
                
              #Empacamos la caja seleccionada en el espacio seleccionado
              #Elegimos como criterio la primera rotacion valida dentro de la lista (debe contener almenos 1)
              
                #Variable que guarda la informacion sobre la soluciona ctual  
                CajasAdentroAntes = len(ContenedorSolu.listaCE)
                
                H=ContenedorSolu.listaEM[EspacioMaximal]
                #Organizamos las rotaciones de acuerdo a la porporcion frente al espacio maximal
                RotaMayor = sorted(Rotaciones, key=lambda x: -x.x/(H.px2 - H.px1) - x.y/(H.py2 - H.py1)- x.z/(H.pz2 - H.pz1))
                
                Rotaciones=RotaMayor
                
                #movimientos que guarda la infromacion de la solucion antes de empacar, el tipo y la rotacion que se va a empacar
                #Estos son apartir desde el cambio de caja
                Movimientos2[CajasAdentroAntes]= {"Contenedor": copy.deepcopy(ContenedorSolu), "Caja por meter":NTipoCaja , "Rotacion":Rotaciones[0] }
                
                #Se empaca la caja
                ContenedorSolu.EmpacarCaja(Rotaciones[0], ContenedorSolu.listaEM[EspacioMaximal],ContenedorSolu.listaTC[NTipoCaja][0])
                #Una vez se empaca la caja, se actualiza para la clase tipo de caja selecionada
                #la cantidad de cajas disponibles, Para la variable FaltanCajasPorEmpacar le reducimos en 1 su valor
                # y agregamos el %del volumen de la caja respecto al contenedor a la utilizacion del contenedor  
                
                ContenedorSolu.listaTC[NTipoCaja][1].q0 += (-1)
                ContenedorSolu.FaltanCajasPorEmpacar += (-1)
                ContenedorSolu.utilizacion =ContenedorSolu.utilizacion+(Rotaciones[0].x*Rotaciones[0].y*Rotaciones[0].z)/(DimensionesContenedor.px2*DimensionesContenedor.py2*DimensionesContenedor.pz2)
                  
    
                # Dada la caja empacada, actualizamos los espacios maximales donde si alguno de estos contiene la cajaempacada
                # se generan nuevos espacios maximales en los limites de ese espacio y se elimina (Si la caja se empaco
                # almenos debe haber 1 espacio maximal que lo contenga)  
               
                ContenedorSolu.ActualizarEspaciosMaximales(ContenedorSolu.listaCE[-1])
                  
                # Verificamos que dado los nuevos espacios maximales, eliminamos aquellos que estan contenidos
                # dentro de otro año
        
                ContenedorSolu.EliminarEspaciosContenidos()
                
                #Actualizamos la lista para organizarla de acuerdo a la que este mas cerca la base inferio del contenedor
                EMMayor = sorted(ContenedorSolu.listaEM, key=lambda x: (x.pz1))
                ContenedorSolu.listaEM=EMMayor
  
        #Agregamos la solucion al vecindario
        VecindarioSoluciones[PO]={"Contenedor":copy.deepcopy(ContenedorSolu), "Utilidad": ContenedorSolu.utilizacion, "Movimientos":Movimientos2}
   
    #Compararemos la mejor solucion del vecindario respecto a la solucion actual
    for i in VecindarioSoluciones:
        if VecindarioSoluciones[i]["Utilidad"] > MejorSolucionActualUtilidad:
            MejorSolucionActualUtilidad = VecindarioSoluciones[i]["Utilidad"]
            MejorSolucionActualContenedor=VecindarioSoluciones[i]["Contenedor"]
            MejorSolucionActualMovimientos = VecindarioSoluciones[i]["Movimientos"]
             
    #Analizaremos la solucion actual y si es mejor la que mejr soluciona actual, estas e comviertira en la mejor        
    if MejorSolucionActualUtilidad>SolucionGlobal:
        SolucionGlobal=MejorSolucionActualUtilidad
        ContendorGlobal=MejorSolucionActualContenedor
   
        

print("")
print("")
print("")
print("TIPOS DE CAJAS")
print("")
for u in listaVolumenMayor:
    print("Tipo de caja: ",u[0], " |  longitud incial x: ",  u[1].lx, " |  longitud incial y: ",u[1].ly , " |  longitud incial z: ", u[1].lz)


print("")
print("")
print("")
print("TABLA DE POSICIONES")
print("")
# Mostrar la tabla
def imprimir_linea_horizontal():
    print("|------|------|------|------|------|------|------|")
    
# Imprimir encabezados
print("| Tipo |  X1  |  X2  |  Y1  |  Y2  |  Z1  |  Z2  |")
imprimir_linea_horizontal()

# Imprimir datos de las cajas
for E in ContendorGlobal.listaCE:
    print(f"| {E.Tipo:^5}| {E.px1:^5} | {E.px2:^5} | {E.py1:^5} | {E.py2:^5} | {E.pz1:^5} | {E.pz2:^5} |")
    imprimir_linea_horizontal()

print("Instancia: ", InstanciaPrueba)
print("Solucion Deterministica: ", (ContenedorActual.utilizacion)*100, "%")
print("Solucion Heuristica: ", (ContendorGlobal.utilizacion)*100 , "%")
print("Tiempo de ejecucion en Segundos: ", time.time()-time1)
