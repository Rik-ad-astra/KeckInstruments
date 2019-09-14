## Import General Tools
from .core import log
from pathlib import Path

from astropy.table import Table, Column


##-------------------------------------------------------------------------
## Define Mask Object
##-------------------------------------------------------------------------
class Mask(object):
    def __init__(self, input):
        self.slitpos = None
        self.alignmentStars = None
        self.scienceTargets = None
        self.xmlroot = None
        # from maskDescription
        self.name = None
        self.priority = None
        self.center_str = None
        self.center = None
        self.PA = None
        self.mascgenArguments = None

        xmlfile = Path(input)
        # Is the input OPEN mask
        if input.upper() in ['OPEN', 'OPEN MASK']:
            log.debug(f'"{input}" interpreted as OPEN')
            self.build_open_mask()
        elif input.upper() in ['RAND', 'RANDOM']:
            log.debug(f'"{input}" interpreted as RANDOM')
            self.build_random_mask()
        # try top open as XML mask design file
        elif xmlfile.exists():
            log.debug(f'"{input}" exists as file on disk')
            self.read_xml(xmlfile)
        # Try to parse input as long slit specification
        else:
            try:
                width, length = input.split('x')
                width = float(width)
                length = int(length)
                assert length <= 46
                assert width > 0
                self.build_longslit(input)
            except:
                log.debug(f'Unable to parse "{input}" as long slit')
                log.error(f'Unable to parse "{input}"')
                raise ValueError(f'Unable to parse "{input}"')


    def read_xml(self, xml):
        xmlfile = Path(xml)
        if xmlfile.exists():
            tree = ET.parse(xmlfile)
            self.xmlroot = tree.getroot()
        else:
            try:
                self.xmlroot = ET.fromstring(xml)
            except:
                log.error(f'Could not parse {xml} as file or XML string')
                raise
        # Parse XML root
        for child in self.xmlroot:
            if child.tag == 'maskDescription':
                self.name = child.attrib.get('maskName')
                self.priority = float(child.attrib.get('totalPriority'))
                self.PA = float(child.attrib.get('maskPA'))
                self.center_str = f"{child.attrib.get('centerRaH')}:"\
                                  f"{child.attrib.get('centerRaM')}:"\
                                  f"{child.attrib.get('centerRaS')} "\
                                  f"{child.attrib.get('centerDecD')}:"\
                                  f"{child.attrib.get('centerDecM')}:"\
                                  f"{child.attrib.get('centerDecS')}"
                self.center = SkyCoord(self.center_str, unit=(u.hourangle, u.deg))
            elif child.tag == 'mascgenArguments':
                self.mascgenArguments = {}
                for el in child:
                    if el.attrib == {}:
                        self.mascgenArguments[el.tag] = (el.text).strip()
                    else:
                        self.mascgenArguments[el.tag] = el.attrib
            elif child.tag == 'mechanicalSlitConfig':
                data = [el.attrib for el in child.getchildren()]
                self.slitpos = Table(data)
            elif child.tag == 'scienceSlitConfig':
                data = [el.attrib for el in child.getchildren()]
                self.scienceTargets = Table(data)
                ra = [f"{star['targetRaH']}:{star['targetRaM']}:{star['targetRaS']}"
                      for star in self.scienceTargets]
                dec = [f"{star['targetDecD']}:{star['targetDecM']}:{star['targetDecS']}"
                       for star in self.scienceTargets]
                self.scienceTargets.add_columns([Column(ra, name='RA'),
                                                 Column(dec, name='DEC')])
            elif child.tag == 'alignment':
                data = [el.attrib for el in child.getchildren()]
                self.alignmentStars = Table(data)
                ra = [f"{star['targetRaH']}:{star['targetRaM']}:{star['targetRaS']}"
                      for star in self.alignmentStars]
                dec = [f"{star['targetDecD']}:{star['targetDecM']}:{star['targetDecS']}"
                       for star in self.alignmentStars]
                self.alignmentStars.add_columns([Column(ra, name='RA'),
                                                 Column(dec, name='DEC')])
            else:
                mask[child.tag] = [el.attrib for el in child.getchildren()]


    def build_longslit(self, input):
        '''Build a longslit mask
        '''
        # parse input string assuming format similar to 0.7x46
        width, length = input.split('x')
        width = float(width)
        length = int(length)
        assert length <= 46
        self.name = f'LONGSLIT-{input}'
        slits_list = []
        # []
        # scale = 0.7 arcsec / 0.507 mm
        for i in range(length):
            # Convert index iteration to slit number
            # Start with slit number 23 (middle of CSU) and grow it by adding
            # a bar first on one side, then the other
            slitno = int( {0: -1, -1:1}[-1*(i%2)] * (i+(i+1)%2)/2 + 24 )
            leftbar = slitno*2
            leftmm = 145.82707536231888 + -0.17768476719087264*leftbar + (width-0.7)/2*0.507/0.7
            rightbar = slitno*2-1
            rightmm = leftmm - width*0.507/0.7
            slitcent = (slitno-23) * .490454545
            slits_list.append( {'centerPositionArcsec': slitcent,
                                'leftBarNumber': leftbar,
                                'leftBarPositionMM': leftmm,
                                'rightBarNumber': rightbar,
                                'rightBarPositionMM': rightmm,
                                'slitNumber': slitno,
                                'slitWidthArcsec': width,
                                'target': ''} )
        self.slitpos = Table(slits_list)

        # Alignment Box
        slit23 = self.slitpos[self.slitpos['slitNumber'] == 23][0]
        leftmm = slit23['leftBarPositionMM'] - 1.65*0.507/0.7
        rightmm = slit23['rightBarPositionMM'] + 1.65*0.507/0.7
        as_dict = {'centerPositionArcsec': 0.0,
                   'leftBarNumber': 46,
                   'leftBarPositionMM': leftmm,
                   'mechSlitNumber': 23,
                   'rightBarNumber': 45,
                   'rightBarPositionMM': rightmm,
                   'slitWidthArcsec': 4.0,
                   'targetCenterDistance': 0,
                   }
        self.alignmentStars = Table([as_dict])


    def build_open_mask(self):
        '''Build OPEN mask
        '''
        self.name = 'OPEN'
        slits_list = []
        for i in range(46):
            slitno = i+1
            leftbar = slitno*2
            leftmm = 270.400
            rightbar = slitno*2-1
            rightmm = 4.000
            slitcent = 0
            width  = (leftmm-rightmm) * 0.7/0.507
            slits_list.append( {'centerPositionArcsec': slitcent,
                                'leftBarNumber': leftbar,
                                'leftBarPositionMM': leftmm,
                                'rightBarNumber': rightbar,
                                'rightBarPositionMM': rightmm,
                                'slitNumber': slitno,
                                'slitWidthArcsec': width,
                                'target': ''} )
        self.slitpos = Table(slits_list)


    def build_random_mask(self, slitwidth=0.7):
        '''Build a Mask with randomly placed, non contiguous slits
        '''
        self.name = 'RANDOM'
        slits_list = []
        for i in range(46):
            slitno = i+1
            cent = random.randrange(54,220)
            # check if it is the same as the previous slit
            if i > 0:
                while cent == slits_list[i-1]['centerPositionArcsec']:
                    cent = random.randrange(54,220)
            leftbar = slitno*2
            leftmm = cent + slitwidth*0.507/0.7
            rightbar = slitno*2-1
            rightmm = cent - slitwidth*0.507/0.7
            width  = (leftmm-rightmm) * 0.7/0.507
            slits_list.append( {'centerPositionArcsec': cent,
                                'leftBarNumber': leftbar,
                                'leftBarPositionMM': leftmm,
                                'rightBarNumber': rightbar,
                                'rightBarPositionMM': rightmm,
                                'slitNumber': slitno,
                                'slitWidthArcsec': width,
                                'target': ''} )
        self.slitpos = Table(slits_list)
        
