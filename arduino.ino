long duration;
int distance;
const int MR1=7, MR2=8, ML1=9, ML2=10, TRIG=5, ECHO=6 ;  // MR-right motor,ML-left motor:
char receivedChar;                               // s-stop,f-front,l=left,r=right( from eye movement):
boolean newData = false;

void setup() {
  pinMode(LED_BUILTIN,OUTPUT);
  pinMode(MR1, OUTPUT);
  pinMode(MR2, OUTPUT);
   pinMode(ML1, OUTPUT);      // declaration of all pin:
  pinMode(ML2, OUTPUT);
  pinMode(TRIG,OUTPUT);
  pinMode(ECHO,INPUT);
  Serial.begin(9600);
  
   //  setup code here, to run once:

}

void loop() 
{
  recvOneChar();
  runNewData();
  digitalWrite(MR1,LOW);
  digitalWrite(ML1,LOW);
  digitalWrite(TRIG,LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG,HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG,LOW);
    duration = pulseIn(ECHO,HIGH);
    distance = duration * 0.034 /2;
  
  //  main code here, to run repeatedly:
}

 void recvOneChar() 
 {
  if(Serial.available()>0)
   {  receivedChar = Serial.read();   // read character recieved from laptop ( i.e s,f,l,r):
      newData = true;
   }
 }
 void runNewData() 
 {
  if(newData == true)
  {
    digitalWrite(LED_BUILTIN,LOW);
    if(receivedChar=='s')           // condition for stop:
     {
//      digitalWrite(LED_BUILTIN,LOW);
      digitalWrite(ML2,LOW);       
      digitalWrite(MR2,LOW);
     }
     
     else if(receivedChar=='r')         // contidion for turning right:
     {digitalWrite(ML2,HIGH);
      digitalWrite(MR2,LOW);
     }
     
     else if(receivedChar=='l')         // condition for turning left:
     {digitalWrite(ML2,LOW);
      digitalWrite(MR2,HIGH);
     }
     
     else if(receivedChar=='f')         // condition for moving forward:
      {
//        digitalWrite(LED_BUILTIN,HIGH);
        digitalWrite(ML2,HIGH);
        digitalWrite(MR2,HIGH);
        
//        if(distance < 40)            // stop if finds obstacle in front:
//          {
////             digitalWrite(ML2,LOW);
////             digitalWrite(MR2,LOW);
//          }
//        else
//          {
//             digitalWrite(ML2,HIGH);
//             digitalWrite(MR2,HIGH);
//          }
       }
       else{
        digitalWrite(ML2,LOW);
        digitalWrite(MR2,LOW);
        
//        digitalWrite(LED_BUILTIN,HIGH);
       }
  }
 }
