int speedPin = 5; // PWM control (speed)
int dir1 = 4;     // Direction pin 1
int dir2 = 3;     // Direction pin 2
int mSpeed = 255; // Maximum speed
unsigned long startTime;
int runDuration = 15000; // Duration to run the motor in milliseconds
bool isHalfwayCommand = false; // Flag to track if the command is for half backward movement

void setup() {
  pinMode(speedPin, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
  Serial.begin(9600);
  startTime = 0; // Initialize start time
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming character

    switch (command) {
      case 'f': // Forward
        digitalWrite(dir1, HIGH);
        digitalWrite(dir2, LOW);
        analogWrite(speedPin, mSpeed);
        startTime = millis(); // Record start time
        isHalfwayCommand = false; // Reset the halfway flag
        break;
      case 'b': // Backward
        digitalWrite(dir1, LOW);
        digitalWrite(dir2, HIGH);
        analogWrite(speedPin, mSpeed);
        startTime = millis(); // Record start time
        isHalfwayCommand = false; // Reset the halfway flag
        break;
      case 's': // Stop
        analogWrite(speedPin, 0);
        isHalfwayCommand = false; // Reset the halfway flag
        break;
      case 'h': // Halfway backward
        digitalWrite(dir1, LOW);
        digitalWrite(dir2, HIGH);
        analogWrite(speedPin, mSpeed);
        startTime = millis(); // Record start time
        isHalfwayCommand = true; // Set the halfway flag
        break;
    }
  }

  // Check if the motor has been running for the specified duration
  if ((millis() - startTime) >= (isHalfwayCommand ? (runDuration / 2) : runDuration) && 
      (digitalRead(dir1) == HIGH || digitalRead(dir2) == HIGH)) {
    analogWrite(speedPin, 0); // Stop the motor
    isHalfwayCommand = false; // Reset the halfway flag
  }
}
