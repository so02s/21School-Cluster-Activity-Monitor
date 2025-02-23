import time
import ADS1x15

class ADC:
    def __init__(self, pin) -> None:
        self.adc = ADS1x15.ADS1115()
        self.GAIN = 1
        self.pin = pin
    def read_pin(self, pin):
        return self.adc.read_adc(pin, gain=self.GAIN)
    def adc_test(self):
    # Read all the ADC channel values in a list.
        values = [0]*4
        for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
            values[i] = self.read_pin(i)
        # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 12 or 16 bit signed integer value depending on the
        # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
    # Print the ADC values.
            print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    # Pause for half a second.
            time.sleep(0.5)