const static int NUM_LIGHTS = 6;
int ledpin[6] = {3, 5, 6, 9, 10, 11};
char cur;
int index;
int i;
int speed;
String str;
char array[20];

void setup() 
{ 
  initializeLights();
  Serial.begin(115200);
  for(i = 0; i < NUM_LIGHTS; ++i) setLightLevel(i, 255);
  delay(500);
  for(i = 0; i < NUM_LIGHTS; ++i) setLightLevel(i, 0);
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

void loop() 
{ 
  while(Serial.available())
  {
    cur = Serial.read();
    if(cur == '{') {
      str = String();
      continue;
    }
    else if(cur == ',') {
      str.toCharArray(array, 20);
      index = atoi(array);
      str = String();
      continue;
    }
    else if(cur != '}') {
      str = str + String(cur);
      continue;
    }
    str.toCharArray(array, 20);
    speed = atoi(array);
    str = String();
    setLightLevel(index, speed);
  }
}
