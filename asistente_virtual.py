import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import pyaudio
import webbrowser
import datetime
import wikipedia


id1 = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"
id2 = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"


# Escuchar nuestro micro y devolver el audio en txt
def transformar_audio_en_txt():
    # almacenar el recognizer en una variable
    reco = sr.Recognizer()
    # configurar el micro
    with sr.Microphone() as origin:
        # tiempo de espera
        reco.pause_threshold = .8
        # informar que comenzó la grabación
        print("Ya puedes hablar")
        # guardar lo escuchado en una variable
        audio = reco.listen(origin)

        try:
            # buscar en google lo que haya escuchado
            pedido = reco.recognize_google(audio, language="es-ES")
            # prueba de que ingresó bien
            print("Dijiste: " + pedido)
            # devolver pedido
            return pedido
        except sr.UnknownValueError:
            print("No entendí lo que dijiste")
            return "sigo esperando..."
        except sr.RequestError:
            print("Ups, no hay servicio")
            return "sigo esperando..."
        except:
            print("Algo fue mal")
            return "sigo esperando"


# funcion para que se el asistente pueda hablar
def hablar(m):
    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", id1)
    # pronunciar mensaje
    engine.say(m)
    engine.runAndWait()


# informar del dia de la semana
def pedir_dia():
    # variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # variable para dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario días
    calendario = {0: "Lunes",
                  1: "Martes",
                  2: "Miércoles",
                  3: "Jueves",
                  4: "Viernes",
                  5: "Sábado",
                  6: "Domingo"}

    # decir día de la semana
    hablar(f"Hoy es {calendario[dia_semana]}")


# informar de la hora
def pedir_hora():
    # crear variable con datos de la hora
    hora = datetime.datetime.now()

    # decir hora
    hablar(f"En este momento son las: {hora.hour} y {hora.minute} minutos")


# funcion saludo inicial
def saludo_inicial():
    # crear variables con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif hora.hour >= 6 or hora.hour < 13:
        momento = "Buenos días"
    else:
        momento = "Buenas tardes"
    hablar(f"{momento}. Soy Helena, tu asistente virtual. En que te puedo ayudar?")


# funcion central del asistente
def central():
    # activar el saludo inicial
    saludo_inicial()
    comandos = {
        "youtube": ["abrir youtube", "ir a youtube", "abre youtube", "llevame a youtube"],
        "google": ["abrir navegador", "abre google", "ir a google", "llevame a google"],
        "hora": ["qué hora es", "dime la hora", "qué hora tenemos"],
        "dia": ["en qué día estamos", "qué día es hoy", "hoy es"],
        "wikipedia": ["busca en wikipedia"]
    }
    # variable de corte
    comenzar = True
    while comenzar:
        # activar micro y guardar pedido en un string
        pedido = transformar_audio_en_txt().lower()
        if any(frase in pedido for frase in comandos["youtube"]):
            hablar("Por supuesto")
            webbrowser.open("https://www.youtube.com")
            continue
        elif any(frase in pedido for frase in comandos["google"]):
            hablar("Por supuesto")
            webbrowser.open("https://www.google.com")
            continue
        elif any(frase in pedido for frase in comandos["hora"]):
            pedir_hora()
            continue
        elif any(frase in pedido for frase in comandos["dia"]):
            pedir_dia()
            continue
        elif "busca en wikipedia" in pedido:
            hablar("Okey")
            pedido = pedido.replace("wikipedia", "")
            wikipedia.set_lang("es")
            res = wikipedia.summary(pedido, sentences=1)
            hablar(f"Según wikipedia: {res}")
            continue
        elif "busca en internet" in pedido:
            hablar("Ahora lo busco")
            pedido = pedido.replace("busca en internet", "")
            pywhatkit.search(pedido)
            hablar("Esto es lo que encontrado")
            continue
        elif "reproducir" in pedido:
            hablar("Reproduciendo canción")
            pywhatkit.playonyt(pedido)
            continue
        elif "broma" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue

        # ARREGLAR ELIF ACCIONES
        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strip()
            cartera = {"apple": "AAPL",
                       "amazon": "AMZN",
                       "google": "GOOGL"}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_accion = accion_buscada.info["regularMarketPrice"]
                hablar(f"El precio de {accion} es {precio_accion}")
                continue
            except:
                hablar("Perdón, no encontré nada")
                continue
        # HASTA AQUÍ

        elif "adiós" in pedido:
            hablar("Okey, me voy a descansar, cualquier cosa me avisas")
            break





central()
