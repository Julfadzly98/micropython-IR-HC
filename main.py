from machine import Pin, time_pulse_us
import time
import urequests

def connect():
    import network
 
    ssid = "smartspacekk" 
    password = "smartspace09" 
 
    station = network.WLAN(network.STA_IF)
 
    if station.isconnected() == True:
        print("Already connected")
        return
 
    station.active(True)
    station.connect(ssid, password)
 
    while station.isconnected() == False:
        pass
 
    print("Connection successful")
    print(station.ifconfig())



# Ultrasonic sensor pins
trig = Pin(18, Pin.OUT)
echo = Pin(19, Pin.IN)

# IR sensor pin
ir_sensor = Pin(21, Pin.IN)

# Buzzer pin
buzzer = Pin(22, Pin.OUT)



# Telegram Bot Token and Chat ID
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = urequests.post(url, json=payload)
        response.close()
        print("Message sent to Telegram")
    except Exception as e:
        print("Failed to send message:", e)

def measure_distance():
    # Trigger the ultrasonic sensor
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # Measure the duration of the echo pulse
    duration = time_pulse_us(echo, 1, 1000000)
    
    # Calculate distance in centimeters
    distance = (duration / 2) / 29.1
    return distance

def main():
    while True:
        # Measure distance using the ultrasonic sensor
        distance = measure_distance()
        #https://docs.google.com/forms/d/e/1FAIpQLSeKT-7XwFW3nxrGBhprCks2jXZWOCj-UAm2gq1-jFEOyXSLLA/viewform?usp=pp_url&entry.108654085=1
        print("Ultrasonic Sensor Distance: {:.2f} cm".format(distance))

        # Send distance to Telegram
        send_telegram_message(f"Ultrasonic Sensor Distance: {distance:.2f} cm")

        # Check if the IR sensor detects an object
        if ir_sensor.value() == 0:  # Assuming 0 means object detected
            print("Object detected by IR sensor!")
            buzzer.value(1)  # Turn on the buzzer
        else:
            buzzer.value(0)  # Turn off the buzzer

        # Wait for a short time before the next measurement
        time.sleep(5)  # Send data every 5 seconds



        h = {'content-type' : 'application/x-www-form-urlencoded'}
        form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSeKT-7XwFW3nxrGBhprCks2jXZWOCj-UAm2gq1-jFEOyXSLLA/formResponse?usp=pp_url&'
        form_data = 'entry.108654085=' + str(distance)
        r = urequests.post(form_url, data=form_data, headers=h)
        r.status_code
        r.close()
        print("check google form")

if __name__ == "__main__":
    main()
