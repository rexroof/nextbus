// This #include statement was automatically added by the Particle IDE.
#include <adafruit-led-backpack.h>

Adafruit_7segment matrix = Adafruit_7segment();

// for blinking the colon on the display
int colon = false;
// number of seconds until bus
int bus_time = 3559;
// the last value we got from the api
String previous_time = "unset";
// how often we check for times:
int check_interval = 20;
// global for tracking when to check
int check_again = 0;

// the route and stop I care about
int route = 31;
int stop = 2091;
String publish_data = String::format("{ \"bus\": \"%d\", \"stop\": \"%d\" }",route,stop);

// should return four digits to display
int seconds_tochars(int _secs) {
    
    int hours = (_secs/3600);
    _secs = _secs - ( hours * 3600 );
    
    int minutes = (_secs / 60);
    _secs = _secs - (minutes * 60);

    // our output only has 4 digits.
    if (hours > 0) {
        minutes = 59;
    }
    
    _secs = _secs + (minutes*100);
    return(_secs);
}

// should parse string into seconds
int nextbus_toseconds(String _data) {
    int result = 0;
    
    // input should look like 00:20:01
    int firstColon  = _data.indexOf(':');
    int secondColon = _data.indexOf(':', firstColon + 1);
    String hoursString   = _data.substring(0,firstColon);
    String minutesString = _data.substring(firstColon+1,secondColon);
    String secondsString = _data.substring(secondColon+1);
    
    result = result + secondsString.toInt();
    result = result + (60 * minutesString.toInt());
    result = result + (3600 * hoursString.toInt());
    
    return(result);
}

void setup() {
  matrix.begin(0x70);
  matrix.setBrightness(12);
  Particle.subscribe(System.deviceID() + "/hook-response/nextbus/", nextbus, MY_DEVICES);
}

void check_time() {
   Particle.publish("nextbus", publish_data, PRIVATE);
}

void nextbus(const char *event, const char *data) {
    String _indata = String(data);

    // if result contains a :
    if ( _indata.indexOf(':') > -1 ) {
            // if this is a new result
            if ( _indata.compareTo(previous_time) != 0 ) {
               bus_time = nextbus_toseconds(_indata);
               previous_time = _indata;
            }
    }
}

void loop() {
  int _output = seconds_tochars(bus_time);
  matrix.printNumber(_output,DEC);
  colon = ! colon;
  matrix.drawColon(colon);
  matrix.writeDisplay();
  
  // sleep half a second to blink colon
  delay(500);
  colon = ! colon;
  matrix.drawColon(colon);
  matrix.writeDisplay();
 
  // check our api every check_interval
  if (check_again == 0) {
      check_time();
      check_again = check_interval;
  } else {
      check_again--;
  }
  
   // sleep another half second
  delay(500);
  bus_time--;
 
}
