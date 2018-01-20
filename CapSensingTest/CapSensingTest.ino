#include <CapacitiveSensor.h>

/*
 * CapitiveSense Library Demo Sketch
 * Paul Badger 2008
 * Uses a high value resistor e.g. 10M between send pin and receive pin
 * Resistor effects sensitivity, experiment with values, 50K - 50M. Larger resistor values yield larger sensor values.
 * Receive pin is the sensor pin - try different amounts of foil/metal on this pin
 */
/*
  #### WIRING DIAGRAM ############
  .SEND PIN -------o			     +--------------------+
  .                |			     |     	          |
  .                <			     |	   	          |
  .                 > (~1 MOhm)		     |	  METAL PLATE     |
  .                <			     |	    OR WIRE	  |
  .                |			     |	                  |
  .RECIEVE PIN-----o-------------------------|		          |
  .                                          |                    |
  .                                          +--------------------+

*/

const int NUM_SENSORS = 4;

CapacitiveSensor sensors[NUM_SENSORS] = {
   /* (send, recieve) */
   CapacitiveSensor(10, 12),
   CapacitiveSensor(10, 11),
   CapacitiveSensor(10, 9),
   CapacitiveSensor(10, 8)

};



void setup() {
   pinMode(13, OUTPUT);		/* pin 13 is gnd pin */
   digitalWrite(13, LOW);
   
   delay(100);
   Serial.begin(115200);
   delay(100);
}

void loop() {

   for(int i=0; i < NUM_SENSORS; i++) {

      Serial.print(sensors[i].capacitiveSensor(30) );
      Serial.print("\t");
   }
   Serial.print("\n");

   delay(40);                             // arbitrary delay to limit data to serial port
}


/*
   arduino communicates which button is pressed to a computer (rasp pi maybe?)
   which is connected to a display that can show questions. maybe also have
   led strips so it's more 'flashy.'






*/