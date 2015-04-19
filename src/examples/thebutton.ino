//Simple sketch to set RGB light based on predefined
// serial inputs.
const int RED = 9;
const int GREEN = 10;
const int BLUE = 11;
const int red[] = {0xe5,0,0};
const int orange[] = {0xff,0xf,0};
const int yellow[] = {0xff,0x77,0};
const int green[] = {0x2,0xbe,0x1};
const int blue[] = {0,0x83,0xc7};
const int purple[] = {0x82,0,0x80};
const int off[] = {0,0,0};
char colorCode;
char color[3];
int numBytes = 0;


void setup() {
  Serial.begin(9600);
  pinMode(RED,OUTPUT);
  pinMode(GREEN,OUTPUT);
  pinMode(BLUE,OUTPUT);
}

void loop () {
  numBytes = Serial.available();
  if (numBytes >= 1) {
    Serial.readBytes(color,numBytes);
    colorCode = color[0];
    switch (colorCode) {
      case 'R':
        setColor(red);
        break;
      case 'O':
        setColor(orange);
        break;
      case 'Y':
        setColor(yellow);
        break;
      case 'G':
        setColor(green);
        break;
      case 'B':
        setColor(blue);
        break;
      case 'P':
        setColor(purple);
        break;
      case 'K':
        setColor(off);
        break;
      default:
        setColor(off);
    }
  }
}
void setColor(const int* color) {
  analogWrite(RED,color[0]);
  analogWrite(GREEN,color[1]);
  analogWrite(BLUE,color[2]);
}
