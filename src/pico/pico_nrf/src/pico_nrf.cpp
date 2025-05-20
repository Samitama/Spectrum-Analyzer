#include <stdio.h>
#include <RF24.h>
#include "pico/stdlib.h"
#include "hardware/spi.h"

#define CE_PIN 6
#define CSN_PIN 1

#define NRF24_SCK 2
#define NRF24_TX 3
#define NRF24_RX 0

RF24 radio(CE_PIN,CSN_PIN);

SPI spi;

const uint8_t adres[6] = "00001";


void power_up();

int main(){
    stdio_init_all();
    gpio_init(25);
    gpio_set_dir(25,GPIO_OUT);
    power_up();
    spi.begin(spi0,NRF24_SCK,NRF24_TX,NRF24_RX);
    radio.begin(&spi);
    radio.setPayloadSize(32);    
    radio.setPALevel(RF24_PA_MIN);
    radio.openWritingPipe(adres);
    radio.stopListening();
 
    while (1){
        const char text[] = "Hello";
        bool report = radio.write(&text,sizeof(text));
        if (report) gpio_put(25,1);
        else gpio_put(25,0);
        sleep_ms(1000);
    }
}

void power_up(){
    for (int i = 0; i < 3; i++)
    {
        gpio_put(25,1);
        sleep_ms(100);
        gpio_put(25,0);
        sleep_ms(100);
    }
}
