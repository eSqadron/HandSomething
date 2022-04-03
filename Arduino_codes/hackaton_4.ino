#include <Servo.h>

Servo door;

String value;
int a=0;
int b=90;
int state=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  door.attach(6);

} 

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    value=Serial.readString();
    if (value){
//      Serial.println(5);
      state=door.read();
      switch (state){
        case 90:
          door.write(0);
          break;
        case 0:
          door.write(90);
          break;
        default:
          door.write(0);
          break;
        }
      delay(1000);
    }
//    delay(500);
  }
}
