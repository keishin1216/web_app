#include <LiquidCrystal_I2C.h> 
LiquidCrystal_I2C lcd(0x27,16,2);
const int trigPin = 2;
const int echoPin = 3;

double duration = 0;
double distance = 0;

int ledlight = 5;
int count = 0;
void setup() {
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Count");
 pinMode(trigPin, OUTPUT); 
 pinMode(echoPin, INPUT); 
  pinMode(ledlight, OUTPUT);
 
}


const int a = 5; 
int l[a];
int t = 0;
int pre_l = 0;
boolean approaching = false;

void loop() {
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration / 2 * 340.0 /1000;
   
 l[t] = distance;
 t = ++t % a;
 int sum = 0;
 for (int i = 0; i < a; i++) {
   sum += l[t];
 }
 int l_ma = sum / a;

 int dl = pre_l - l_ma;
 if (l_ma < 1200) {
   if (millis() > 1000) { 
     if (dl < 0 && approaching == false) {
       approaching = true;
       count++;
        digitalWrite(ledlight, HIGH);
        delay(100);
     digitalWrite(ledlight, LOW);
      lcd.setCursor(0, 1);
     lcd.print(count);
     lcd.print(" times ");
     }
   }
  }else{
   approaching = false;
   
 }
 
 pre_l = l_ma;
   
 delay(70);
}
