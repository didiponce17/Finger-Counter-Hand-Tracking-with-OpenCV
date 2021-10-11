 #include <Servo.h>
#define numOfValsRec 5
#define digitsPerValRec 1

Servo servoThumb;
Servo servoIndex;                                                                                                                                                       
Servo servoMiddle;


Servo servoRing;
Servo servoPinky;

int valsRec[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1; //$00000
int counter = 0;
bool counterStart = false;
bool newData = false;
String receivedString;                                                            
void setup() {
  Serial.begin(9600);
  servoThumb.attach(5);  
  servoIndex.attach(6);
  servoMiddle.attach (9);
  servoRing.attach(10);
  servoPinky.attach(11);


}

void receiveData() {
  while (Serial.available())
  {

    char c = Serial.read();

    if (c == '$') {
      counterStart = true;
      newData = true;
    }

    if (counterStart) {
      if (counter < stringLength) {
        receivedString = String(receivedString + c);
        counter++;

      }

      if (counter >= stringLength) {
        //$00000
        for (int i = 0; i < numOfValsRec; i++)
        {
          int num = (i * digitsPerValRec) + 1;
          valsRec[i] = receivedString.substring(num, num + digitsPerValRec).toInt();
        }

        receivedString = "";
        counter = 0;
        counterStart = false;
      }
    }
  }
}

void loop() {


  receiveData();
 // if (newData){
    
  if (valsRec[0] == 1){servoThumb.write(90);}else{servoThumb.write(0);}
  if (valsRec[1] == 1){servoIndex.write(180);}else{servoIndex.write(0);}
  if (valsRec[2] == 1){servoMiddle.write(180);}else{servoMiddle.write(0);}
  if (valsRec[3] == 1){servoRing.write(180);}else{servoRing.write(0);}
  if (valsRec[4] == 1){servoPinky.write(180);}else{servoPinky.write(0);}
 // newData = false;
 // }
  
}
