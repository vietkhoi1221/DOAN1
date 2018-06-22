#include <Wire.h>
#include "MAX30100_PulseOximeter.h"
#include <LiquidCrystal_I2C.h>

#define REPORTING_PERIOD_MS     1000
LiquidCrystal_I2C lcd(0x27, 16, 2);
// PulseOximeter is the higher level interface to the sensor
// it offers:
//  * beat detection reporting
//  * heart rate calculation
//  * SpO2 (oxidation level) calculation
PulseOximeter pox;

uint32_t tsLastReport = 0;
int h,bpm;

// Callback (registered below) fired when a pulse is detected
void onBeatDetected()
{
    Serial.println("Beat!");
}

void setup()
{
    // initialize the LCD
    lcd.begin();

  // Turn on the blacklight and print a message.
    lcd.backlight();
    lcd.clear();
    Serial.begin(9600);
    pox.begin();

   // Serial.print("Initializing pulse oximeter..");

    if (!pox.begin()) {
        //Serial.println("FAILED");
        for(;;);
    } else {
       // Serial.println("SUCCESS");
    }
}

void loop()
{
    // Make sure to call update as fast as possible
    pox.update();
    int tong =0;
    // Asynchronously dump heart rate and oxidation levels to the serial
    // For both, a value of 0 means "invalid"
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        lcd.clear();
        h = pox.getHeartRate();
        Serial.print("Heart rate:");
        Serial.print(h);
        lcd.setCursor(1,0);
        lcd.print("Heart rate:");
        lcd.print(h);
        if (pox.getSpO2()<100)
        bpm = pox.getSpO2();
        Serial.print("bpm/SpO2:");
        Serial.print(bpm);
        Serial.println("%");
        lcd.setCursor(1,1);
        lcd.print("bpm/SpO2:");
        lcd.print(bpm);
        tsLastReport = millis();
        //lcd.print("Heart rate:");
        //lcd.print(pox.getHeartRate());
    }
}
