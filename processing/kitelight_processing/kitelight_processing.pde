const static int NUM_LIGHTS = 6;
int ledpin[6] = {3, 5, 6, 9, 10, 11};                           // light connected to digital pin 9
int ledspeed[6] = {0,0,0,0,0,0};
int index;
int speed;
int sep;

void setup() 
{ 
  initializeLights();
  initializeSerial();
}

void initializeLights()
{

  //Bank 1
  //Uses ground pin as ground
  //Pins 5 and 6 run higher than normal, so set to input when we want off
  analogWrite(3, 0);
  pinMode(5, INPUT);
  pinMode(6, INPUT);

  //Bank 2
  //Uses pin 12 as ground.
  analogWrite(9, 0);
  analogWrite(10, 0);
  analogWrite(11, 0);
  analogWrite(12, 0);
}

void initializeSerial()
{
  Serial.begin(9600);
}

void setLightLevel(int index, int speed)
{

  //Special case for turning pins 5 and 6 off
  if(ledpin[index] == 5 || ledpin[index] == 6 && speed == 0)
  {
    if(speed == 0)
    {
       pinMode(ledpin[index], INPUT);
       return;
    }
    else
    {
      pinMode(ledpin[index], OUTPUT);
    }
  }
  analogWrite(ledpin[index], speed);
}

void confirmRealignment()
{
  for(int i = 0; i < NUM_LIGHTS; ++i)
  {
    setLightLevel(i, 0);
  }
  setLightLevel(3, 255);
  delay(250);
  for(int i = 0; i < NUM_LIGHTS; ++i)
  {
    setLightLevel(i, ledspeed[i]);
  }  
}

void processSerial()
{
  index = Serial.read();
  if(index >= 6)
  {
    index = Serial.read();
    index = Serial.read();
    confirmRealignment();
    return;
  }
  speed = Serial.read();
  ledspeed[index] = speed;
  sep = Serial.read();
  setLightLevel(index, speed);   
}

void loop() 
{ 
  if(!(Serial.available() % 3))
  {
    processSerial();
  }
}
