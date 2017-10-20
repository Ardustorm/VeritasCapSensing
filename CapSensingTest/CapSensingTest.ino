#include <CapacitiveSensor.h>

/*
 * CapitiveSense Library Demo Sketch
 * Paul Badger 2008
 * Uses a high value resistor e.g. 10M between send pin and receive pin
 * Resistor effects sensitivity, experiment with values, 50K - 50M. Larger resistor values yield larger sensor values.
 * Receive pin is the sensor pin - try different amounts of foil/metal on this pin
 */


CapacitiveSensor   cs_2_4 = CapacitiveSensor(4,3);        // 10M resistor between pins 4 & 2, pin 2 is sensor pin, add a wire and or foil if desired

CapacitiveSensor   cs_2_6 = CapacitiveSensor(11,12);      
void setup() {
   /* cs_4_2.set_CS_AutocaL_Millis(0xFFFFFFFF);     // turn off autocalibrate on channel 1 - just as an example */
   Serial.begin(115200);
}

void loop() {
   
    long start = millis();
    long total1 =  cs_2_4.capacitiveSensor(30);
    long total2 =  cs_2_6.capacitiveSensor(30);

    Serial.print(millis() - start);        // check on performance in milliseconds
    Serial.print("\t");                    // tab character for debug windown spacing

    Serial.print(total1);                  // print sensor output 1

    Serial.print("\t");

    Serial.print(total2);                  // print sensor output 2

    Serial.print("\t");

    for(int i = 50; i < total1; i+= 40) {
           Serial.print("#");
    }

    /* add another for loop here to show other side */
    
    Serial.print("\n");
    
    delay(40);                             // arbitrary delay to limit data to serial port 
}


/* 
arduino communicates which button is pressed to a computer (rasp pi maybe?)
which is connected to a display that can show questions. maybe also have
led strips so it's more 'flashy.'






 */