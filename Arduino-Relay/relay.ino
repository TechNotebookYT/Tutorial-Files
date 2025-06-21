int in1 = 8;
int in2 = 7;

void setup() {
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
}

void loop() {
  digitalWrite(in1, HIGH);
  delay(1000);
  digitalWrite(in2, HIGH);
  delay(1000);
  digitalWrite(in1, LOW);
  delay(1000);
  digitalWrite(in2, LOW);
  delay(1000);
  
}
