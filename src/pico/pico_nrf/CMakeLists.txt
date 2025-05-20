
add_executable(pico_nrf
      src/pico_nrf.cpp
)

# pull in common dependencies
target_link_libraries(pico_nrf 
        pico_stdlib
	hardware_spi
        hardware_gpio
	RF24
        )

pico_enable_stdio_usb(pico_nrf 1)
pico_enable_stdio_uart(pico_nrf 0)

# create map/bin/hex/uf2 file etc.
pico_add_extra_outputs(pico_nrf)



