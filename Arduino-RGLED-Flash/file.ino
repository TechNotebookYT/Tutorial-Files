// Project By Tech Notebook
int R = 11;
int G = 4;
void setup() {
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT); 
}
// Tech Notebook
void loop() {
  digitalWrite(G, HIGH);
  delay(1000);
  digitalWrite(G, LOW);
  digitalWrite(R, HIGH);
  delay(1000);
  digitalWrite(R, LOW);
  // Tech Notebook
  // http://bit.ly/33QiRmF
}
