La herramienta que hemos desarrollado combina Scapy, una poderosa librería de Python para la manipulación de paquetes, con Tkinter, una biblioteca para la creación de interfaces gráficas. Esta combinación nos permite crear una aplicación intuitiva que facilita la gestión y análisis de la red.

![imagen](https://github.com/user-attachments/assets/afe2073d-8518-4fff-ad74-95beac013fb6)

Funcionamiento:

Interfaz Gráfica Intuitiva:
     La aplicación cuenta con una interfaz amigable donde los usuarios pueden interactuar fácilmente con las funcionalidades de Scapy. A través de botones y cuadros de texto, se pueden ingresar parámetros y ejecutar acciones sin necesidad de tener conocimientos avanzados de programación.

Envío de Paquetes ARP:
     Utilizando Scapy, la herramienta permite enviar paquetes ARP (Address Resolution Protocol) a dispositivos en la red. Esto es fundamental para detectar dispositivos conectados y verificar su estado. Al enviar estos paquetes, podemos recopilar información sobre la dirección IP y la dirección MAC de cada dispositivo en nuestra red local.

Detección de Intrusos:
    La herramienta analiza las respuestas de los paquetes ARP para identificar dispositivos que no deberían estar conectados a la red. Esto ayuda a detectar posibles intrusos o dispositivos no autorizados que podrían comprometer la seguridad de la red.

Expulsión de Intrusos:
    En caso de detectar un dispositivo no autorizado, la herramienta permite enviar paquetes ARP maliciosos para "expulsar" a esos intrusos de la red. Esta técnica, aunque debe usarse con responsabilidad y en entornos controlados, es efectiva para mantener la seguridad de la red local.

Visualización de Resultados:
    La interfaz gráfica muestra información en tiempo real sobre los dispositivos detectados, así como alertas si se identifica un intruso. Esto permite a los usuarios tener un control más efectivo sobre su red y actuar rápidamente ante cualquier amenaza.

Consideraciones:

Es importante recordar que el uso de herramientas de análisis de red debe realizarse de manera ética y responsable. Esta aplicación es una demostración educativa y debe utilizarse únicamente en entornos donde tengas permiso para realizar pruebas de seguridad.


