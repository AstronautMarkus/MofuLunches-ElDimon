#include <SPI.h>
#include <MFRC522.h>

// RC522 Pinout
#define RST_PIN 9    // Reset pin 9
#define SS_PIN 10    // SDA pin 10

MFRC522 mfrc522(SS_PIN, RST_PIN); // RC522 instance

void setup() {
  SPI.begin();        // Start SPI bus
  mfrc522.PCD_Init(); // Start RC522 module
  Serial.begin(9600); // Use 9600 baud rate
}

void loop() {
  // if no RFID detected return
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // Print UID Hex code
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) Serial.print("0");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    if (i < mfrc522.uid.size - 1) Serial.print(" "); // Space between bytes
  }
  Serial.println();

  mfrc522.PICC_HaltA(); // Stop reading
}