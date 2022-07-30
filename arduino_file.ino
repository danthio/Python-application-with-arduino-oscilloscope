

int pin = A0;
int val;

void setup() {
  Serial.begin(9600);
}

void loop() {
  val = analogRead(pin);

  Serial.print(val);
  Serial.print("\n");
}
