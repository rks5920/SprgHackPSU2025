#include <WiFi.h>
#include <HTTPClient.h>
#include <Keypad.h>

// WiFi credentials
const char* ssid     = "Tom_iPhone";
const char* password = "hackpsu!";

// Define the number of rows and columns for a 3x4 keypad (3 columns and 4 rows)
const byte ROWS = 4;
const byte COLS = 3;

// Define the keymap according to the typical telephone keypad layout
char keys[ROWS][COLS] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};

// Assign ESP32 pins to the keypad rows and columns
// (Update these pin numbers based on your wiring)
byte rowPins[ROWS] = {12, 14, 26, 27}; // Rows 1 to 4
byte colPins[COLS] = {25, 33, 32};      // Columns 1 to 3

// Create the Keypad object
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  Serial.begin(9600);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Check if a key is pressed
  char key = keypad.getKey();
  if (key) {
    Serial.print("Key Pressed: ");
    Serial.println(key);
    
    // Map the key to the correct URL endpoint
    String endpoint;
    if (key == '*') {
      endpoint = "c";
    } else if (key == '#') {
      endpoint = "ent";
    } else {
      endpoint = String(key);
    }
    
    // Construct the full URL
    String url = "http://172.20.10.7:5000/" + endpoint;
    
    // Send a GET request if WiFi is connected
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(url);
      int httpCode = http.GET();
      
      if (httpCode > 0) {
        Serial.printf("GET request sent to: %s, Code: %d\n", url.c_str(), httpCode);
      } else {
        Serial.printf("GET failed for: %s, Error: %s\n", url.c_str(), http.errorToString(httpCode).c_str());
      }
      http.end();
    } else {
      Serial.println("WiFi not connected!");
    }
    
    // Delay to help debounce the key press
    delay(200);
  }
}



