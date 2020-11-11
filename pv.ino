float val[9]; // variável para guardar o valor lido
int i,j,medias=192;

void setup() {
  Serial.begin(115200);// configura a porta serial
  analogReadResolution(12);
}

void loop() {
  i=0;
  j=0;
  while (j<9){
    val[j]=0;
    j+=1;
  }
  while(i<medias){
    val[0]+=analogRead(A0);// lê o pino de entrada
    val[1]+=analogRead(A1);
    val[2]+=analogRead(A2);
    val[3]+=analogRead(A3);
    val[4]+=analogRead(A4);
    val[5]+=analogRead(A5);
    val[6]+=analogRead(A6);
    val[7]+=analogRead(A7);
    val[8]+=analogRead(A8);
    i++;
    delay(5);
  }
  j=0;
  while (j<9){
    val[j]=val[j]/medias;
    j+=1;
  }
  Serial.print(val[0],1);
  Serial.print(' ');
  Serial.print(val[1],1);
  Serial.print(' ');
  Serial.print(val[5],1);
  Serial.print(' ');
  Serial.print(val[2],1);
  Serial.print(' ');
  Serial.print(val[6],1);
  Serial.print(' ');
  Serial.print(val[3],1);
  Serial.print(' ');
  Serial.print(val[7],1);
  Serial.print(' ');
  Serial.print(val[4],1);
  Serial.print(' ');
  Serial.println(val[8],1);
}
