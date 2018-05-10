import re
from datetime import datetime as dt
from time import sleep

# Wrap ktl import in try/except so that we can maintain test case or simulator
# version of functions.
try:
    import ktl
    from ktl import Exceptions as ktlExceptions
except:
    ktl = None

from Keck.Instruments import AbstractInstrument

# -----------------------------------------------------------------------------
# HIRES
# -----------------------------------------------------------------------------
class HIRES(AbstractInstrument):
    def __init__(self):
        super().__init__()
        self.name = 'HIRES'
        self.optical = True
        self.allowed_sampmodes = [1]
        self.scripts = ["stare", "slit nod", "ABBA", "ABB'A'"]
        self.binnings = ["1x1", "1x2", "2x1", "2x2"]
        self.basename = f"h{dt.utcnow().strftime('%Y%m%d')}_"
        self.serviceNames = ["hires", "hiccd", "expo"]
        self.obstypes = ["object", "dark", "line", "intflat", "bias"]
    
    
    def get_collimator(self):
        collred = self.services['hires']['COLLRED'].read()
        collblue = self.services['hires']['COLLBLUE'].read()
        if collred == 'red' and collblue == 'not blue':
            collimator = 'red'
        elif collred == 'not red' and collblue == 'blue':
            collimator = 'blue'
        else:
            collimator = None
        return collimator
    
    
    def get_binning(self):
        if self.services is None:
            return None
        keywordresult = self.services['hiccd']['BINNING'].read()
        binningmatch = re.match('\\n\\tXbinning (\d)\\n\\tYbinning (\d)',
                                keywordresult)
        if binningmatch is not None:
            self.binning = (int(binningmatch.group(1)),
                            int(binningmatch.group(2)))
        else:
            print(f'Could not parse keyword value "{keywordresult}"')
    
    
    def get_DWRN2LV(self):
        if self.services is None:
            return None
        DWRN2LV = float(self.services['hiccd']['DWRN2LV'].read())
        return DWRN2LV
    
    
    def get_RESN2LV(self):
        if self.services is None:
            return None
        RESN2LV = float(self.services['hiccd']['RESN2LV'].read())
        return RESN2LV
    
    
    def fill_dewar(self, wait=True):
        '''Fill dewar using procedure in /local/home/hireseng/bin/filln2
        '''
        if self.services is None:
            return None
        if self.services['hiccd']['WCRATE'].read() != False:
            print('The CCD is currently reading out. Try again when complete.')
            return None
        print('Initiating camera dewar fill.')
        self.services['hiccd']['utbn2fil'].write('on')
        while self.services['hiccd']['utbn2fil'].read() != 'off':
            sleep(15)
        print('HIRES Dewar Fill is Complete.')
        return True
    
    
    def open_covers(self, wait=True):
        '''Use same process as: /local/home/hires/bin/open.red and open.blue
        
        modify -s hires rcocover = open \
                        echcover = open   xdcover  = open \
                        co1cover = open   co2cover = open \
                        camcover = open   darkslid = open     wait

        modify -s hires bcocover = open \
                        echcover = open   xdcover  = open \
                        co1cover = open   co2cover = open \
                        camcover = open   darkslid = open     wait
        '''
        collimator = self.get_collimator()

        if collimator == 'red':
            self.services['hires']['rcocover'].write('open')
        elif collimator == 'blue':
            self.services['hires']['bcocover'].write('open')
        else:
            print('Collimator is unknown.  Collimator cover not opened.')
        self.services['hires']['echcover'].write('open')
        self.services['hires']['co1cover'].write('open')
        self.services['hires']['xdcover'].write('open')
        self.services['hires']['co2cover'].write('open')
        self.services['hires']['camcover'].write('open')
        self.services['hires']['darkslid'].write('open')
    
        if wait is True:
            if collimator == 'red':
                self.services['hires']['rcocover'].write('open', wait=True)
            elif collimator == 'blue':
                self.services['hires']['bcocover'].write('open', wait=True)
            else:
                print('Collimator is unknown.  Collimator cover not opened.')
            self.services['hires']['echcover'].write('open', wait=True)
            self.services['hires']['co1cover'].write('open', wait=True)
            self.services['hires']['xdcover'].write('open', wait=True)
            self.services['hires']['co2cover'].write('open', wait=True)
            self.services['hires']['camcover'].write('open', wait=True)
            self.services['hires']['darkslid'].write('open', wait=True)
    
    
    def close_covers(self, wait=True):
        collimator = self.get_collimator()

        if collimator == 'red':
            self.services['hires']['rcocover'].write('closed')
        elif collimator == 'blue':
            self.services['hires']['bcocover'].write('closed')
        else:
            print('Collimator is unknown.  Collimator cover not opened.')
        self.services['hires']['echcover'].write('closed')
        self.services['hires']['co1cover'].write('closed')
        self.services['hires']['xdcover'].write('closed')
        self.services['hires']['co2cover'].write('closed')
        self.services['hires']['camcover'].write('closed')
        self.services['hires']['darkslid'].write('closed')
    
        if wait is True:
            if collimator == 'red':
                self.services['hires']['rcocover'].write('closed', wait=True)
            elif collimator == 'blue':
                self.services['hires']['bcocover'].write('closed', wait=True)
            else:
                print('Collimator is unknown.  Collimator cover not opened.')
            self.services['hires']['echcover'].write('closed', wait=True)
            self.services['hires']['co1cover'].write('closed', wait=True)
            self.services['hires']['xdcover'].write('closed', wait=True)
            self.services['hires']['co2cover'].write('closed', wait=True)
            self.services['hires']['camcover'].write('closed', wait=True)
            self.services['hires']['darkslid'].write('closed', wait=True)
    
    
    def iodine_start(self):
        '''Use same process as in /local/home/hires/bin/iod_start
        
        modify -s hires moniodt=1
        modify -s hires setiodt=50.
        modify -s hires iodheat=on
        '''
        if self.services is None:
            return None
        self.services['hires']['moniodt'].write(1)
        self.services['hires']['setiodt'].write(50)
        self.services['hires']['iodheat'].write('on')
    
    
    def iodine_stop(self):
        '''Use same process as in /local/home/hires/bin/iod_stop
        
        modify -s hires moniodt=0
        modify -s hires iodheat=off
        '''
        if self.services is None:
            return None
        self.services['hires']['moniodt'].write(0)
        self.services['hires']['iodheat'].write('off')
    
    
    def take_exposure(self, obstype=None, exptime=None, nexp=1):
        if obstype is None:
            obstype = self.services['hiccd']['OBSTYPE'].read()

        if obstype.lower() not in self.obstypes:
            print(f'OBSTYPE "{obstype} not understood"')
            return

        if self.services['hiccd']['OBSERVIP'].read() == 'true':
            print('Waiting up to 300s for current observation to finish')
            if not ktl.waitFor('($hiccd.OBSERVIP == False )', timeout=300):
                raise Exception('Timed out waiting for OBSERVIP')

        if exptime is not None:
            self.services['hiccd']['TTIME'].write(int(exptime))

        if obstype.lower() in ["dark", "bias", "zero"]:
            self.services['hiccd']['AUTOSHUT'].write(False)
        else:
            self.services['hiccd']['AUTOSHUT'].write(True)

        for i in range(nexp):
            exptime = int(self.services['hiccd']['TTIME'].read())
            print(f"Taking exposure {i:d} of {nexp:d}")
            print(f"  Exposure Time = {exptime:d} s")
            self.services['hiccd']['EXPOSE'].write(True)
            exposing = ktl.Expression("($hiccd.OBSERVIP == True) and ($hiccd.EXPOSIP == True )")
            reading = ktl.Expression("($hiccd.OBSERVIP == True) and ($hiccd.WCRATE == True )")
            obsdone = ktl.Expression("($hiccd.OBSERVIP == False)")

            if not exposing.wait(timeout=30):
                raise Exception('Timed out waiting for EXPOSING state to start')
            print('  Exposing ...')

            if not reading.wait(timeout=exptime+30):
                raise Exception('Timed out waiting for READING state to start')
            print('  Reading out ...')

            if not obsdone.wait(timeout=90):
                raise Exception('Timed out waiting for READING state to finish')
            print('Done')


#     def expo_get_power_on(self):
#         return True
#     
#     
#     def expo_toggle_power(self):
#         new_state = not self.expo_get_power_on()
#         print(f'Setting power on exposure meter {{True: "ON", False: "OFF"}[new_state]}')



# -----------------------------------------------------------------------------
# HIRES
# -----------------------------------------------------------------------------
def PRV_Afternoon_Setup():
    '''Configure the instrument for afternoon setup (PRV mode).
    '''
    h = HIRES()
    h.connect()
    # Check dewar level, if below threshold, fill
    if h.getDWRN2LV() < 20:
        h.fill_dewar()
    # Start iodine cell
    h.iodine_start()
    # Open covers
    
    # Set filename root
    # Set binning to 3x1
    # Set full frame
    # Confirm gain=low
    # Confirm Speed = fast
    # m slitname=opened
    # m fil1name=clear
    # m fil2name=clear
    # Confirm collimator = red
    # m cafraw=0
    # set ECHANG
    # set XDANG
    # tvfilter to BG38
    # Confirm tempiod1
    # Confirm tempiod2
    # Obstype = object
    ## Focus
    # Exposure meter off
    # ThAr2 on
    # Lamp filter=ng3
    # m deckname=D5
    # iodine out
    # texp = 10 seconds
    # expose
    # -> run IDL focus routine and iterate as needed
    ### Calibrations
    ## THORIUM Exposures w/ B5
    # Exposure meter off
    # ThAr2 on
    # lamp filter = ng3
    # m deckname=B5
    # iodine out
    # texp=1 second
    # two exposures
    ## THORIUM Exposure w/ B1
    # Exposure meter off
    # ThAr2 on
    # lamp filter = ng3
    # m deckname=B1
    # iodine out
    # texp=3 second
    # one exposure
    # -> check saturation: < 20,000 counts on middle chip?
    # -> Check I2 line depth. In center of chip, it should be ~30%
    ## Iodine Cell Calibrations B5
    # Make sure cell is fully warmed up before taking these
    # Exposure meter off
    # Quartz2 on
    # Lamp filter=ng3
    # m deckname=B5
    # iodine in
    # texp=2 second
    # one exposure
    # -> check saturation: < 20,000 counts on middle chip?
    # -> Check I2 line depth. In center of chip, it should be ~30%
    ## Wide Flat Fields
    # Exposure meter off
    # Quartz2 on
    # Lamp filter=ng3
    # m deckname=C1
    # iodine out
    # texp=1 second
    # Take 1 exposures
    # -> Check one test exp for saturation (<20k counts)
    # Take 49 exposures
    # m lampname=none
    # m deckname=C2
    # Check dewar level, if below threshold, fill


