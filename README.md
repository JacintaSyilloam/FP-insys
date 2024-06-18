# Final Project Integrasi Sistem
## Kelompok 4

| NRP        | Nama                     |
| ---------- | ------------------------ |
| 5027221018 | Gabriella Erlinda Wijaya |
| 5027221036 | Jacinta Syilloam         |

## PROJECT 1
### Materials needed:
- DHT11 censor
- ESP32s Wi-Fi
- Jumper cables
- Breadboard

### Hardware Setup
1. Connect the ESP32s Wi-Fi to our laptop to confugure the settings using Arduino IDE
```
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
// #include <ESP8266WiFi.h>
#include <WiFi.h>
#include <PubSubClient.h>

#define BUILTIN_LED 21

// Update these with values suitable for your network.

const char* ssid = "Gabriella11";
const char* pswd = "gabriella1188";

const char* mqtt_server = "167.172.87.186"; //Broker IP/URL
const char* topic = "/gabjac/room/temperature";    //Topic
//const char* username="afzal";
//const char* password="temp123";

long timeBetweenMessages = 1000 * 20 * 1;

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
int value = 0;

int status = WL_IDLE_STATUS;     // the starting Wifi radio's status



#define DHTPIN 19    // Digital pin connected to the DHT sensor 

// Uncomment the type of sensor in use:
#define DHTTYPE    DHT11     // DHT 11
// #define DHTTYPE    DHT22     // DHT 22 (AM2302)



DHT_Unified dht(DHTPIN, DHTTYPE);

uint32_t delayMS;


void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, pswd);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is acive low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }
}

String macToStr(const uint8_t* mac)
{
  String result;
  for (int i = 0; i < 6; ++i) {
    result += String(mac[i], 16);
    if (i < 5)
      result += ':';
  }
  return result;
}

String composeClientID() {
  uint8_t mac[6];
  WiFi.macAddress(mac);
  String clientId;
  clientId += "esp-";
  clientId += macToStr(mac);
  return clientId;
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");

    String clientId = composeClientID() ;
    clientId += "-";
    clientId += String(micros() & 0xff, 16); // to randomise. sort of

    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      String subscription;
      subscription += topic;
      subscription += "/";
      subscription += composeClientID() ;
      subscription += "/in";
      client.subscribe(subscription.c_str() );
      Serial.print("subscribed to : ");
      Serial.println(subscription);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.print(" wifi=");
      Serial.print(WiFi.status());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void setup() {
  Serial.begin(115200);
  // Initialize device.
  dht.begin();

  //Setup WIFI & MQTT Broker connection
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
  Serial.println(F("DHTxx Unified Sensor Example"));
  // Print temperature sensor details.
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  Serial.println(F("------------------------------------"));
  Serial.println(F("Temperature Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("°C"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("°C"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("°C"));
  Serial.println(F("------------------------------------"));
  // Print humidity sensor details.
  dht.humidity().getSensor(&sensor);
  Serial.println(F("Humidity Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("%"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("%"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("%"));
  Serial.println(F("------------------------------------"));
  // Set delay between sensor readings based on sensor details.
  delayMS = 30000;
}

void loop() {
  // Delay between measurements.
  delay(delayMS);
  // Get temperature event and print its value.
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  float temp=0;
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));
  }
  else {
    Serial.print(F("Temperature: "));
    Serial.print(event.temperature);
    Serial.println(F("°C"));
    temp=event.temperature;
  }

  
  // Get humidity event and print its value.
  dht.humidity().getEvent(&event);
  float hum=0;
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!"));
  }
  else {
    Serial.print(F("Humidity: "));
    Serial.print(event.relative_humidity);
    Serial.println(F("%"));
    hum=event.relative_humidity;
  }


    // confirm still connected to mqtt server
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  String payload = "{\"Temp\":";
  payload += temp;
  payload += ",\"Hum\":";
  payload += hum;
  payload += "}";
  String pubTopic;
   pubTopic += topic;
  Serial.print("Publish topic: ");
  Serial.println(pubTopic);
  Serial.print("Publish message: ");
  Serial.println(payload);
  client.publish( (char*) pubTopic.c_str() , (char*) payload.c_str(), true );

  delay(5000);
}
```
   
2. Connect all hardware using the breadboard

| DHT11 pins | ESP32s pins |
| ---------- | ----------- |
| GND        | GND         |
| DATA       | GPIO 5      |
| VCC        | 3v3         |

![image](https://github.com/JacintaSyilloam/FP-insys/assets/128443451/7f2f1365-50da-4405-b231-6c5338a02add)


### Testing
Open the HTML file from the Project 1 directory and run the file using Live Server
![image](https://github.com/JacintaSyilloam/FP-insys/assets/121095246/422dba1f-384c-4003-8350-8fa9b5e1c708)


## PROJECT 2
### Materials needed
- RaspberryPi
- LED lamp
- hardware from project 1

### Hardware Setup
1. Connect the power cable from Project 1 hardware to the Raspberry Pi
2. Connect the Raspberry Pi to a monitor using VGA to HDMI cable (VGA to RaspPi, HDMI to monitor)
3. Connect the LED to the Raspberry Pi, (+) to pin 12, (-) to pin 14

![image](https://github.com/JacintaSyilloam/FP-insys/assets/128443451/275af062-aa0f-4681-9e8f-1ba94279c51c)

### Testing
Once the Raspberry Pi is connected to the monitor, we can start testing our project by running the HTML file from the Project 2 directory and run it using the live server

#### Lights OFF
![image](https://github.com/JacintaSyilloam/FP-insys/assets/128443451/b9f34337-a7dc-4929-93d4-835988951fe2)
![image](https://github.com/JacintaSyilloam/FP-insys/assets/128443451/a4091aea-ee1c-44be-a812-3423fb2881fd)

#### Lights ON
![image](https://github.com/JacintaSyilloam/FP-insys/assets/128443451/04ece15e-a8e1-4a90-be55-f9fcb7858bda)
![image](https://github.com/JacintaSyilloam/FP-insys/assets/128443451/1756848b-fb75-4164-85cd-f16329971a0b)
