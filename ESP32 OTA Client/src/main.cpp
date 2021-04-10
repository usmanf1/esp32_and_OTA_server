#include <Arduino.h>
#include <HTTPClient.h>
#include <HTTPUpdate.h>
#include <WiFi.h>

#include "base64.h"


#define VERSION "1.0.3"
#define HOST "esp32"

const char* ssid = "SSID";
const char* password = "PSK";

const char* urlBase = "server_address";
// Authorization credentials
const String& authUsername = "username";
const String& authPassword = "password";

WiFiClient client;

void getLatest() {
  String checkUrl = String( urlBase);
  checkUrl.concat("/latest");
  checkUrl.concat( "?ver=" + String(VERSION) );
  checkUrl.concat( "&dev=" + String(HOST) );
  Serial.println("INFO: Checking for updates at URL: " + String( checkUrl ) );

  String auth = base64::encode(authUsername + ":" + authPassword);
  Serial.println(auth);

  t_httpUpdate_return ret = httpUpdate.update( client, checkUrl, auth );

  switch (ret) {
    default:
      break;
    case HTTP_UPDATE_FAILED:
      Serial.println("ERROR: HTTP_UPDATE_FAILD Error (" + String(httpUpdate.getLastError()) + "): " + httpUpdate.getLastErrorString().c_str());
      break;
    case HTTP_UPDATE_NO_UPDATES:
      Serial.println("INFO: HTTP_UPDATE_NO_UPDATES");
      break;
    case HTTP_UPDATE_OK:
      Serial.println("INFO status: HTTP_UPDATE_OK");
      break;
  }

}
void getList() {
  String checkUrl = String( urlBase);
  checkUrl.concat("/list");
  checkUrl.concat( "?ver=" + String(VERSION) );
  checkUrl.concat( "&dev=" + String(HOST) );
  Serial.println("INFO: Checking for updates at URL: " + String( checkUrl ) );
  HTTPClient http;
  http.begin(client, checkUrl);

  String auth = base64::encode(authUsername + ":" + authPassword);
  Serial.println(auth);
  http.addHeader("Authorization", auth);
  // Send HTTP GET request
  int httpResponseCode = http.GET();
  if (httpResponseCode > 0) {
    Serial.print("Available Firmwares are: ");
    String payload = http.getString();
    Serial.println(payload);

  }

  http.end();
}
void getUpdate(String to_update) {
  String checkUrl = String( urlBase);
  checkUrl.concat("/update");
  checkUrl.concat("?ver=" + String(VERSION) );
  checkUrl.concat("&dev=" + String(HOST) );
  checkUrl.concat("&update=" + String(to_update));


  String auth = base64::encode(authUsername + ":" + authPassword);
  Serial.println(auth);

  t_httpUpdate_return ret = httpUpdate.update( client, checkUrl, auth );

  switch (ret) {
    default:
      break;
    case HTTP_UPDATE_FAILED:
      Serial.println("ERROR: HTTP_UPDATE_FAILD Error (" + String(httpUpdate.getLastError()) + "): " + httpUpdate.getLastErrorString().c_str());
      break;
    case HTTP_UPDATE_NO_UPDATES:
      Serial.println("INFO: HTTP_UPDATE_NO_UPDATES");
      break;
    case HTTP_UPDATE_OK:
      Serial.println("INFO status: HTTP_UPDATE_OK");
      break;
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println("Welcome to HTTP Server");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  WiFi.setSleep(false);
  delay(2000);

}

void loop() {
  Serial.println("Welcome to OTA Operation, press 1 for available list or press 2");
  Serial.print("for latest firmware update or press 3 for any available firmware update: ");
  while (Serial.available() == 0) {}
  
  String choice = Serial.readString();
  Serial.println(choice);
  if(choice == "1"){
    getList();
  }
  else if(choice == "2"){
    getLatest();
  }
  else if(choice == "3"){
    Serial.print("Enter the firmware version: ");
    while (Serial.available() == 0) {}
    
    String to_update = Serial.readString();
    Serial.println(to_update);
    getUpdate(to_update);
  }
  else{
    Serial.println("Invalid Selection");
  }  
    
}