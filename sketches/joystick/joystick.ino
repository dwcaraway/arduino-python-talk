const int SW_PIN = 2; //Digital pin connected to the switch output
const int X_PIN = 0; //Analog pin connected to the X output
const int Y_PIN = 1; //Analog pin connected to the Y output

void setup() {
  pinMode(SW_PIN, INPUT);
  digitalWrite(SW_PIN, HIGH);
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("Switch:   ");
  Serial.print(digitalRead(SW_PIN));

  Serial.print("\n");
  Serial.print("X-axis:   ");
  Serial.print(analogRead(X_PIN));

  Serial.print("\n");
  Serial.print("Y-axis:   ");
  Serial.print(analogRead(Y_PIN));

  Serial.print("\n\n");
  delay(500);
}
