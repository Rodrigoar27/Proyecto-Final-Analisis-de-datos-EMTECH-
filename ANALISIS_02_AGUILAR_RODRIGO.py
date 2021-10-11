import csv

#register_id,direction,origin,destination,year,date,product,transport_mode,company_name,total_value
datos = []

#Definimos la variable lector para acceder a la información
with open("synergy_logistics_database.csv","r") as archivo_csv:
    lector = csv.DictReader(archivo_csv)
#Cargamos los datos a un nuevo arreglo llamado datos 
    for lectura in lector:
        datos.append(lectura)
        
#Opción 1 ---------------------------------------------------------
#Definimos la función que realizará las operaciones, únicamente con el parámetro de dirección    
def rutas_vigentes (direccion):
    contador = 0 
    rutas_registro = []
    rutas_conteo = []
#Realizamos una serie de bucles que identifiquen la ruta contada        
    for ruta in datos:
        if ruta["direction"] == direccion:
            ruta_actual = [ruta["origin"], ruta["destination"]]
            if ruta_actual not in rutas_registro:
                for ruta_datos in datos: 
                    if ruta_actual == [ruta_datos["origin"], ruta_datos["destination"]]:
                        contador += 1
#Añadimos la ruta contada a nuestro registro, así como incrementamos el contador por cada aparición                    
                rutas_registro.append(ruta_actual)
                rutas_conteo.append([contador,ruta["origin"], ruta["destination"]])
                contador = 0
#Ordenamos la lista y regresamos el valor al programa principal
    rutas_conteo.sort(reverse = True, key = lambda x:x[0])
    return rutas_conteo
#Para una mejor visualización, asignamos los valores a nuevas variables      
exportaciones = rutas_vigentes("Exports")
importaciones = rutas_vigentes("Imports")

#Imprimimos los resultados
print("\nOpción A \n")
#Imprimimos los resultados de las diez rutas más demandadas en exportaciones
print("Las diez rutas más demandadas para exportaciones son: \n")
for i in range(0,10):
        print (str(i+1) +  ". " + exportaciones[i][1] + " - " + exportaciones[i][2] )

#Imprimimos los resultados de las diez rutas más demandadas en exportaciones
print("\nLas diez rutas más demandadas para importaciones son: \n")
for i in range(0,10):
        print (str(i+1) +  ". " + importaciones[i][1] + " - " + importaciones[i][2] )


#print(exportaciones) #Descomentar para ver resultado completo
#print(importaciones) #Descomentar para ver resultado completo

#Opcion 2 ---------------------------------------------------------
#Definimos una función para dividir los datos de acuerdo a su forma de transporte
#De igual manera, definimos los parámetros de dirección
def transporte (modo_transporte,direccion = "Imports",direccion2 = "Exports"):
    transporte = []
    imp = 0
    exp = 0
    
#Realizamos una iteración para dividir de acuerdo al transporte
    for modo in datos: 
        if modo["transport_mode"] == modo_transporte:
            transporte.append([modo["direction"],modo["total_value"]])
#Realizamos una iteración para clasificar por la dirección                     
    for ops in transporte:
        if ops[0] == direccion:
            imp += int(ops[1])
        elif ops[0] == direccion2:
            exp += int(ops[1])
#Añadimos los resultados a una lista, modo de transporte, total de importaciones y total de exportaciones
    modos = [modo_transporte, imp, exp]
    return modos
#Para facilitar la visualización, añadimos los valores a diferentes variables    
Air = transporte("Air")
Road = transporte("Road")
Rail = transporte("Rail")
Sea = transporte ("Sea")
#Definimos una lista para añadir todos los resultados, para facilitar la impresión
transportes = [Air,Road,Rail, Sea]
transportes.sort(reverse = True, key = lambda x:x[2])

#Imprimimos los resultados
print("\n \nOpción B")
print("\nLos totales de exportaciones por medio de transporte son: \n")
for i in range(0,4):
     print (str(i+1) +  ". " + str(transportes[i][0]) + ". $" + str(transportes[i][2]) )

transportes.sort(reverse = True, key = lambda x:x[1])
print("\nLos totales de importaciones por medio de transporte son: \n")
for i in range(0,4):
     print (str(i+1) +  ". " + str(transportes[i][0]) + ". $" + str(transportes[i][1]) )

#print(transportes) #Descomentar para ver el resultado completo

#Opción 3  --------------------------------------------------------
#Definimos una función que realice la clasificación de datos de acuerdo al país de origen o destino    
def valor_operaciones (direccion):
    registro = []
    valores_paises = []
#Realizamos un bucle para realizar la clasificación      
    for viaje in datos:
        actual = [direccion, viaje["origin"]]
        valor = 0
        ops = 0
#Definimos un condicional que permita clasificar de acuerdo a si el país ya ha sido registrado        
        if actual in registro:
            continue
#Realizamos un bucle que permita sumar el valor del movimiento y que cuente el numero de operaciones        
        for mov in datos: 
            if actual == [mov["direction"], mov["origin"]]:
                valor += int(mov["total_value"])
                ops += 1
#Organizamos los datos en arreglos        
        registro.append(actual)
        valores_paises.append([direccion, viaje["origin"],valor,ops])
#Realizamos el ordenamiento y regresamos el arreglo    
    valores_paises.sort(reverse = True, key = lambda x:x[2])
    return valores_paises
#Para una mejor visualización, definimos variables para imp y exp    
valores_paises_exp = valor_operaciones("Exports")
valores_paises_imp = valor_operaciones("Imports")

#Definimos una función que calcule los porcentajes de cada país para importaciones y exportaciones
def porcentaje_exp_imp(valores_paises):
    porcentajes = []
    total = 0
    for pais in valores_paises:
        total += pais[2]
    for pais in valores_paises:
        porcentaje = round(pais[2] / total, 4)
        porcentajes.append([pais[1],porcentaje,pais[3]])
    return porcentajes
#Para mejor visualización, definimos variables para cada arreglo
porcentajes_exp = porcentaje_exp_imp(valores_paises_exp)
porcentajes_imp = porcentaje_exp_imp(valores_paises_imp)

#Definimos una función que designe que paises ocupan aproximadamente el 80% para exp e imp
def porcentajes (lista_paises,porcentaje):
    porcentaje_sum = 0
    paises = []
    for pais in lista_paises:
            porcentaje_sum += pais[1]
            if porcentaje_sum <= porcentaje:
                paises.append(pais[0])
            else:
                break
    return paises
 
#Definimos arreglos para los paises que representen el 80% de imp y exp    
sum_exp = porcentajes(porcentajes_exp,0.8)
sum_imp = porcentajes(porcentajes_imp,0.8)


#print(porcentajes_exp) #Descomentar para ver todos los porcentajes
#print(porcentajes_imp) #Descomentar para ver todos los porcentajes

#Imprimimos los resultados de forma amigable
print("\n \nOpción C")
print("\nLos Países que exportan aprox. el 80% son: \n")
for i in range(0,10):
     print (str(i+1) +  ". " + porcentajes_exp[i][0] + ", con " + str(porcentajes_exp[i][2]) + " operaciones")
     
print("\nLos Países que importan aprox. el 80% son: \n")
for i in range(0,10):
     print (str(i+1) +  ". " + porcentajes_imp[i][0] + ", con " + str(porcentajes_imp[i][2]) + " operaciones")




