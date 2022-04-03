/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>
#include <LiquidCrystal.h>
LiquidCrystal lcd(2, 4, 8, 9, 12, 13);

Servo finger_1;
Servo finger_2;
Servo finger_3;
Servo finger_4;
Servo finger_5;
// twelve servo objects can be created on most boards


int pos = 0;   
int i=0;
int j=0;
//char str[] ="1,150,95,44,85";
//char g[20];
char *pch;
char *tab[5];
//int a;
//int a;
//int b;
//int c;
//int d;
//int e;
String value;

void setup() {
  finger_1.attach(3);
  finger_2.attach(5);
  finger_3.attach(6);
  finger_4.attach(10);
  finger_5.attach(11);
  Serial.begin(9600);
  lcd.begin(16,2);
  // attaches the servo on pin 9 to the servo object
}

void loop() {
    if (Serial.available()){
    value=Serial.readString();
    int str_len = value.length()+1;
    char g[str_len];
    value.toCharArray(g,str_len);
//    Serial.println(g);
//    Serial.println(tab[1]);
//    delay(500); 
//    Serial.println(g);
//     delay(1000);
    pch=strtok(g,"b, '");
    int i=0;
    while (pch != NULL){
      tab[i]=pch;
      i=i+1;
//      Serial.println(atoi(tab[i-1]));
      pch=strtok(NULL,", ");
    }
//  }
//    delay(2000);
//    Serial.println(value[0]);

    //if (Serial.available()){
//    Serial.println(a);
//    delay(100);
//    Serial.println(b);
//    delay(100);
//    Serial.println(c);
//    delay(100);
  //}
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("T");
    lcd.setCursor(1, 0);
    lcd.print(tab[0]);
    lcd.setCursor(5, 0);
    lcd.print("I");
    lcd.setCursor(6, 0);
    lcd.print(tab[1]);
    lcd.setCursor(10, 0);
    lcd.print("M");
    lcd.setCursor(11, 0);
    lcd.print(tab[2]);
    lcd.setCursor(0, 1);
    lcd.print("R:");
    lcd.setCursor(1, 1);
    lcd.print(tab[3]);
    lcd.setCursor(5, 1);
    lcd.print("P:");
    lcd.setCursor(6, 1);
    lcd.print(atoi(tab[4]));
    
    Serial.println(atoi(tab[0]));
    Serial.println(atoi(tab[1]));
    Serial.println(atoi(tab[2]));
    Serial.println(atoi(tab[3]));
    Serial.println(atoi(tab[4]));
    finger_1.write(180-atoi(tab[0]));
    finger_2.write(atoi(tab[1]));
    finger_3.write(atoi(tab[2]));
    finger_4.write(180-atoi(tab[3]));
    finger_5.write(180-atoi(tab[4]));
//    delay(150);
    }
//  
//  for (pos = 0; pos <= 140; pos += 1) { // goes from 0 degrees to 180 degrees
//    // in steps of 1 degree
//    finger_1.write(pos);
//    finger_2.write(pos);
//    finger_3.write(pos);
//    finger_4.write(pos);
//    finger_5.write(pos);// tell servo to go to position in variable 'pos'
//    delay(15);                       // waits 15ms for the servo to reach the position
//  }
//  for (pos = 140; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
//    finger_1.write(pos);
//    finger_2.write(pos);
//    finger_3.write(pos);
//    finger_4.write(pos);
//    finger_5.write(pos);              // tell servo to go to position in variable 'pos'
//    delay(15);                       // waits 15ms for the servo to reach the position
//  }
}
//void serialEvent(){
//      while (Serial.available()){
//       a = Serial.readStringUntil(",").toInt();
//       b = Serial.readStringUntil(",").toInt();
//       c = Serial.readStringUntil(",").toInt();
//       d = Serial.readStringUntil(",").toInt();
//       e = Serial.readStringUntil(",").toInt();
//    }
//}
