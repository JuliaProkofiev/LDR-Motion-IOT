import network
from machine import ADC, Pin
import math, time
import ujson
from umqtt.simple import MQTTClient
import _thread

# MQTT Server Parameters
mqtt_server = "broker.mqttdashboard.com"
mqtt_port = 1883
mqtt_user = ""
mqtt_password = ""
mqtt_client_id = "clientId-LaRNzQtOBj"
mqtt_topic = "pucpr/iot/ilum-motion-node"

# Connect to WiFi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    time.sleep(0.1)
print("WiFi Connected!")

# Setup LEDs
led_pins = [13, 12, 14, 27, 26, 25, 33, 32, 23, 22]
leds = [Pin(pin, Pin.OUT) for pin in led_pins]

# Função para desligar todos os LEDs
def clear_leds():
    for led in leds:
        led.value(0)

# Função para acender LEDs de acordo com o valor de 'n'
def light_up_to(n):
    clear_leds()
    for i in range(min(n, len(leds))):  # Garantir que n não exceda o número de LEDs
        leds[i].value(1)
    return n  # Retorna o número de LEDs acesos

# Setup LDR on ADC
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)

# Setup PIR Sensor
pir_pin = Pin(35, Pin.IN)

rl10 = 50e3
gamma = 0.7

# Função para calcular a resistência a partir do valor do ADC
def calculate_resistance():
    value = adc.read()
    if value == 4095:
        return float('inf')
    voltage_ratio = value / 4095
    return 10e3 * (1 / voltage_ratio - 1)

# Função para converter resistência em lux
def calculate_lux(resistance):
    if resistance == float('inf'):
        return 0.0
    return 10 * math.pow(rl10 / resistance, 1 / gamma)

# Função para interpolação linear corrigida
points = [
    (0.1, 1.25e6),  # (lux, resistência)
    (1, 250e3),
    (10, 50e3),
    (50, 16.2e3),
    (100, 9.98e3),
    (400, 3.78e3),
    (1000, 1.99e3),
    (10000, 397),
    (100000, 79)
]

def linear_interpolation(resistance):
    if resistance >= 1.25e6:
        return 0.1  # Mínimo lux
    elif resistance <= 79:
        return 100000  # Máximo lux

    for i in range(len(points) - 1):
        if points[i + 1][1] <= resistance <= points[i][1]:
            lux1, res1 = points[i]
            lux2, res2 = points[i + 1]
            return lux1 + ((resistance - res1) / (res2 - res1)) * (lux2 - lux1)

# Variável global para o cliente MQTT
client = None

# Função MQTT no núcleo 1
def mqtt_task():
    global client
    client = MQTTClient(mqtt_client_id, mqtt_server, mqtt_port, user=mqtt_user, password=mqtt_password)

    # Função para conectar ao MQTT e garantir reconexões
    def connect_mqtt():
        while True:
            try:
                client.connect()
                print("MQTT Connected!")
                break
            except OSError as e:
                print("Failed to connect to MQTT, retrying in 5 seconds...")
                time.sleep(5)

    connect_mqtt()  # Tenta conectar inicialmente

    prev_message = ""
    while True:
        try:
            if pir_pin.value():  # Se o sensor de movimento for ativado
                resistance = calculate_resistance()
                lux = round(calculate_lux(resistance), 1)
                interpolated_lux = round(linear_interpolation(resistance), 1)

                num_leds_on = light_up_to(min(10, int(interpolated_lux / 10000 * 10)))  # Baseado no valor interpolado, acende LEDs

                print(f'Lux: {lux}, Interpolated Lux: {interpolated_lux}, LEDs On: {num_leds_on}')

                message = ujson.dumps({
                    "Lux": lux,
                    "Interpolated Lux": interpolated_lux,
                    "LEDs On": num_leds_on  # Envia o número de LEDs acesos
                })

                # Publica a mensagem a cada vez que o sensor é ativado
                if message != prev_message or lux != prev_message:
                    try:
                        client.publish(mqtt_topic, message)
                        prev_message = message
                    except OSError as e:
                        print(f"Publish failed: {e}")
                        connect_mqtt()  # Reconecta caso a publicação falhe
                time.sleep(1)
            else:
                print("No motion detected")
                clear_leds()
                time.sleep(0.5)
        except OSError as e:
            print(f"Error in MQTT task: {e}")
            connect_mqtt()  # Reconecta caso ocorra um erro

# Inicia a thread do MQTT no núcleo 1
_thread.start_new_thread(mqtt_task, ())

# Loop principal para o ADC rodando no núcleo 0
while True:
    if pir_pin.value():
        resistance = calculate_resistance()
        lux = round(calculate_lux(resistance), 1)
        linear_interpolation(calculate_resistance())

    time.sleep(2)
