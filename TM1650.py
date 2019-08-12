import smbus
import traceback


####################################################################################################
#
#  TM1650 i2c for 7 segment display
#
####################################################################################################
class TM1650:
    def __init__(self, bus = smbus.SMBus(1)):
        self.display_base_address = 0x34
        self.dctrl_base_address = 0x24
        self.bus = bus
        self.mask_bright = 7 #0b00000111
        self.dot_mask = 0x80
        self.misses = 0
                                #0x00  0x01  0x02  0x03  0x04  0x05  0x06  0x07  0x08  0x09  0x0A  0x0B  0x0C  0x0D  0x0E  0x0F
        self.TM1650_CDigits =  [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # 0x00
                                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # 0x10
                                0x00, 0x82, 0x21, 0x00, 0x00, 0x00, 0x00, 0x02, 0x39, 0x0F, 0x00, 0x00, 0x00, 0x40, 0x80, 0x00, # 0x20
                                0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7f, 0x6f, 0x00, 0x00, 0x00, 0x48, 0x00, 0x53, # 0x30
                                0x00, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71, 0x6F, 0x76, 0x06, 0x1E, 0x00, 0x38, 0x00, 0x54, 0x3F, # 0x40
                                0x73, 0x67, 0x50, 0x6D, 0x78, 0x3E, 0x00, 0x00, 0x00, 0x6E, 0x00, 0x39, 0x00, 0x0F, 0x00, 0x08, # 0x50
                                0x63, 0x5F, 0x7C, 0x58, 0x5E, 0x7B, 0x71, 0x6F, 0x74, 0x02, 0x1E, 0x00, 0x06, 0x00, 0x54, 0x5C, # 0x60
                                0x73, 0x67, 0x50, 0x6D, 0x78, 0x1C, 0x00, 0x00, 0x00, 0x6E, 0x00, 0x39, 0x30, 0x0F, 0x00, 0x00] # 0x70

    def testDisplay(self):
        self.write8(self.dctrl_base_address,0x17)
        #self.write8(self.dctrl_base_address+1,0x1F)

        self.write8(self.display_base_address,0xF7)
        self.write8(self.display_base_address+1,0x77)
        self.write8(self.display_base_address+2,0x77)
        self.write8(self.display_base_address+3,0x77)

    def setBrightness(self,nPosition, nValue):
        if((nValue >=0) and (nValue <8) and (nPosition >=0) and (nPosition < 4)):
            #print nValue
            nShift = nValue <<4
            #print nShift
            nBright = self.mask_bright | nShift
            #print nBright
            self.write8(self.dctrl_base_address +nPosition,nBright)

    def setNumber(self, nPosition, nNumber, bShowDot):
        if( (nPosition >=0) and (nPosition < 4)):
            nData = str(nNumber)
            if(len(nData) == 1):
                nAscii = self.TM1650_CDigits[ord(nData)]
                #print nAscii
                if(bShowDot != 0):
                    nAscii |= self.dot_mask
                self.write8(self.display_base_address+nPosition,nAscii)

    def clearNumber(self, nPosition):
        if( (nPosition >=0) and (nPosition < 4)):
            nAscii = 0
            self.write8(self.display_base_address+nPosition,nAscii)
    def write8(self,currentAddress, reg):
        #"Writes an 8-bit value to the specified register/address"
        nError = 0
        while True:
            try:
                if nError <20:
                    self.bus.read_byte_data(currentAddress, reg)
                    #self.bus.write_byte_data(currentAddress, reg, value)
                    break
            except IOError as err:
                self.misses += 1
                nError +=1
                traceback.print_exc()
