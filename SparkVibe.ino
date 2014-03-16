String poker = "";

int pokeFunction(String args) {
    poker = args;
    return 1;
}

void setup() {
    Spark.function("poke", pokeFunction);
    pinMode(0,OUTPUT);
}

void loop() {
    if(!poker.equals("")){
        analogWrite(0, 128);
        poker = "";
    }
}
