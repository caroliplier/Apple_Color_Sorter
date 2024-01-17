#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Servo.h>

// Replace the next variables with your SSID/Password combination
const char* ssid = "DeterministicOptimization";
const char* password = "KomsiyahC4n5";

// Add your MQTT Broker IP address, example:
//const char* mqtt_server = "192.168.1.144";
const char* mqtt_server = "192.168.222.178";

WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
char msg[50];
int value = 0;

unsigned long previousMillis = 0;  // will store the last time the command was executed
const long interval = 1000;  // interval at which to execute command (1 second)

const int servoPin = 18;
const int irkanan = 23;
const int irkiri = 22;

int redCount = 0;
int greenCount = 0;
char charRedCount[30];
char charGreenCount[30];

bool next = true;

Servo servo;
int pos = 0;

bool servoMove(String arah) {
  if (arah.equals("kiri")) {
    for (pos = 90; pos <= 135; pos += 1) {
      servo.write(pos);
      delay(10);
    }
    while (digitalRead(irkiri) != 1) {
      Serial.print("waiting\n");
      delay(500);
    }
    return true;
  }
  if (arah.equals("kanan")) {
    for (pos = 90; pos >= 45; pos -= 1) {
      servo.write(pos);
      delay(10);
    }
    while (digitalRead(irkanan) != 1) {
      Serial.print("waiting\n");
      delay(500);
    }
    return true;
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  servo.attach(servoPin, 500, 2400);
  pinMode(irkanan, INPUT);          // IR Sensor pin INPUT
  pinMode(irkiri, INPUT);           // IR Sensor pin INPUT
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off".
  // Changes the output state according to the message
  if (String(topic) == "iloveapple") {
    Serial.print("Changing output to ");
    if (messageTemp == "green") {
      Serial.println("green");
      Serial.print("memutar servo ke kiri\n");
      next = servoMove("kiri");
      Serial.print("Servo Dikiri\n");
      servo.write(90);
      greenCount++;
      String(greenCount).toCharArray(charGreenCount,30);
      client.publish("greenCount",charGreenCount);
      delay(100);
    } else if (messageTemp == "red") {
      Serial.println("red");
      Serial.print("memutar servo ke kanan\n");
      next = servoMove("kanan");
      Serial.print("Servo Dikanan\n");
      servo.write(90);
      redCount++;
      String(redCount).toCharArray(charRedCount,30);

      client.publish("redCount",charRedCount);
      delay(100);
    }
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("iloveapple");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
    // put your main code here, to run repeatedly:
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    // save the last time the command was executed
    previousMillis = currentMillis;

    client.publish("greenCount",charGreenCount);
    client.publish("redCount",charRedCount);
  }
}