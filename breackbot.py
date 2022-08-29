
import time
from binance.client import Client
from binance.enums import *
import config
from binance.um_futures import UMFutures
from math import dist, sqrt
import pandas as pd

client = Client(config.API_KEY, config.API_SECRET, tld='com')
um_futures_client = UMFutures(key='YOURAPIKEY', secret='YOURSECRETKEY')

BASE_URL = "https://api.binance.com"

def desviacion_estandar(valores, media):
    suma = 0
    for valor in valores:
        suma += (valor - media) ** 2

    radicando = suma /(len(valores)- 1)
    return sqrt(radicando)


def calculo_media(valores):
    suma = 0
    for valor in valores:
        suma += valor
    return suma / len(valores)

def RSI(precios, intervalo):
    delta = precios[4].diff()
    



print("------------CARGANDO DATOS-------------")
print("------------CARGANDO DATOS-------------")
print("------------CARGANDO DATOS-------------")


while True:

    Ticker = pd.DataFrame(um_futures_client.ticker_price())
    #Cambiar el valor de str.contains por el filtro que quieras
    #Ejemplo: si queres monedas que solamente sean con el par USDT:
    #asset = Ticker[Ticker["symbol"].str.contains("USDT")]
    #lo mismo para BUSD y otras "stables"
    #endswith es para filtrar por COMO quiero que TERMINE el simbolo
    #en este ejemplo es con "BUSD"
    asset = Ticker[Ticker["symbol"].str.endswith("BTCBUSD")]
    #print(asset)

    #filtrando por symbol solamente
    symbol = (asset["symbol"])
    #filtrando por precio
    precio = (asset["price"])

    intervalo = "15m" #Modificar a gusto [1m,5m,15m,30m,45m,1h,2h,4h,1d,1w,1M]
    cantvelas = 20  

    #IMPRIMIR LOS KLINE A TODOS LOS SIMBOLOS DE LA LISTA FILTRADA POR UNICAMENTE USDT

    for i in symbol:
        #19 porque sino me toma la ultima como para hacer la ruptura
        klines = pd.DataFrame(um_futures_client.klines(i,intervalo, **{"limit": cantvelas})).iloc[ :19,2].astype(float)
        klinesMin = pd.DataFrame(um_futures_client.klines(i,intervalo, **{"limit": cantvelas})).iloc[ :19,3].astype(float)

        price= um_futures_client.ticker_price(i)
        precios = float(price["price"])
        cantidad = round(10/float(precios))
        #print(cantidad)
        orders = um_futures_client.get_orders()
        #print(len(orders))
        #filtra por fila //no hace falta
        numeros= klines.tail(20).astype(float)
        #print(numeros)

        #llama a la funcion calculo_media(especificar de qué fila en la variante numeros)
        media = calculo_media(numeros)
        #print(media)
        #ema = calculo_media(numeros)

        #Muestra las medias de todas las monedas en la lista filtrada
        #print("Media de " + i + " es: "+ str(round(media,2)))
        #time.sleep (10)

        #Sacar la desviacion estandar para cada par
        resultado = desviacion_estandar(numeros, media)
        bandaalta = media + (resultado *2)
        bandabaja = media - (resultado *2)

        #Muestra la desviacion estandar para cada par
        #print("Desviación estandar de " + i + "es: " + str(round(resultado,10)))

        #Muestra la Banda alta y baja para cada par
        #print ("Banda alta y baja de " + i + " es: " + str(round(bandaalta,10)) ," " ,str(round(bandabaja,10)))
        #print ("Banda baja de " + i + " es: " + str(round(bandabaja,10)))


        #Muestra el precio Actual de cada par
        #print("Precio actual " + i +" es: " + precios)


        #Filtrar por maximo precio anterior del alto o bajo del precio
        maximoAnterior = klines.max()
        minimoAnterior = klinesMin.min()
        #print(minimoAnterior)
        #print(maximoAnterior)

        #calcula distancia entre precios y media
        distancia = (precios - media)/precios*100


        
            
        if  float(precios) > maximoAnterior:
            send_message(msg="Ruptura al alza de: " + i)
            print("Ruptura al alza de: " + i)
            time.sleep(10)
        
            #if distancia <= 1.5:
            #    send_message(msg="Ruptura en " + intervalo + " : "  + i )
            #    print("Ruptura en " + intervalo + " : "  + i )
            #    time.sleep(10)            
            #else:
            #    send_message(msg="Esperando ruptura " + intervalo + " : "  + i)
            #    print("Esperando ruptura en " + intervalo + " : "  + i)
            #send_message(msg="Banda Alta en " + intervalo + " = "  + i)
            #time.sleep(1)

        if float(precios) <=  float(maximoAnterior) and float(precios) >= float(maximoAnterior)*0.998:
            #send_message(msg="Posible Ruptura al alza en: " + intervalo + " : "  + i ) (P/ TELEGRAM)
            print("Posible ruptura al alza en: " + intervalo + " de " +  i + " " + (time.strftime("%H:%M:%S")))
            
            time.sleep(10)

        if float(precios) <  float(minimoAnterior) :#and float(precios) <= float(minimoAnterior)*1.005:
            #send_message(msg="Ruptura a la baja en " + intervalo + " : "  + i )
            print("Ruptura a la baja en: " + intervalo + " de " +  i + " " + (time.strftime("%H:%M:%S")))
            time.sleep(10)
        if float(precios) >  float(minimoAnterior) and float(precios) < (float(minimoAnterior)*1.002) :#and float(precios) <= float(minimoAnterior)*1.005:
            #send_message(msg="Posible ruptura a la baja o rango en: " + intervalo + " : "  + i )
            print("Posible ruptura a la baja o rango en: " + intervalo + " de " +  i + " " + (time.strftime("%H:%M:%S")))
            time.sleep(10)



