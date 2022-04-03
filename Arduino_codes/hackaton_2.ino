#define red 6
#define green 5
#define blue 3
#include <Servo.h>
Servo door;

int dane=0;
String value;
char *pch;
char *tab[2];
int i=0;
int state=0;
int privious_time = 0;
int current_time = 0;

 
void setup() {
  // put your setup code here, to run once:
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(blue, OUTPUT);
  Serial.begin(9600);
  door.attach(11);
  

}

void loop() {
//  if(Serial.available()){
//    dane=Serial.parseInt();
//  Serial.println(dane,DEC);
//  }
  if(Serial.available()){
    value=Serial.readString();
    int str_len = value.length()+1;
    char g[str_len];
    value.toCharArray(g,str_len);
    Serial.println(g);
    pch=strtok(g,"b, '");
    int i=0;
    while (pch != NULL){
      tab[i]=pch;
      i=i+1;
//      Serial.println(atoi(tab[i-1]));
      pch=strtok(NULL,", ");
  }
    int brightness_per = atoi(tab[1]);
    int brightness=map(brightness_per,0,100,0,255);
    Serial.println(tab[0]);
    Serial.println(brightness_per);
    Serial.println(brightness);
    switch (*tab[0]){
      case 'R':
        analogWrite(red,255-brightness);
        analogWrite(blue,255);
        analogWrite(green,255);
        Serial.println("Red");
        break;
      case 'G':
        analogWrite(green,255-brightness);
        analogWrite(blue,255);
        Serial.println("green");
        analogWrite(red,255);
        break;
      case 'B':
        analogWrite(blue,255-brightness);
        analogWrite(red,255);
        Serial.println("Blue");
        analogWrite(green,255);
        break;
      case 'D':
//        current_time = millis();
//        if (current_time - privious_time > 5000){
          state=door.read();
          switch (state){ 
            case 0:
              door.write(90);
//              privious_time = current_time;
              break;
            default:
              door.write(0);
//              privious_time = current_time;
              break;
//          }
          
        }
      
      default:
        break;
    }
  }
//    Serial.println(tab[0]);
//    Serial.println(atoi(tab[1]));
//    analogWrite(red,255);
//    analogWrite(green,d);
//    analogWrite(blue,255);
  // put your main code here, to run repeatedly:

}
//void serialEvent(){
//  if(Serial.available()){
//    value=Serial.readString();
//    int str_len = value.length()+1;
//    char g[str_len];
//    Serial.println(g);
//    value.toCharArray(g,str_len);
//    pch=strtok(g,"b, '");
//    int i=0;
//    while (pch != NULL){
//      tab[i]=pch;
//      i=i+1;
////      Serial.println(atoi(tab[i-1]));
//      pch=strtok(NULL,", ");
//  }
//  }
//  }
