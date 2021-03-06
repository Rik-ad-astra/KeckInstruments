import inspect
from datetime import datetime as dt
from datetime import timedelta as tdelta
from time import sleep

try:
    import ktl
except ModuleNotFoundError as e:
    pass

from .core import *


##-----------------------------------------------------------------------------
## Rotator Control
##-----------------------------------------------------------------------------
def rotpposn(skipprecond=False, skippostcond=False):
    '''Return ROTPPOSN in degrees.
    '''
    this_function_name = inspect.currentframe().f_code.co_name
    log.debug(f"Executing: {this_function_name}")

    ##-------------------------------------------------------------------------
    ## Pre-Condition Checks
    if skipprecond is True:
        log.debug('Skipping pre condition checks')
    else:
        instrument_is_MOSFIRE()

    ##-------------------------------------------------------------------------
    ## Script Contents
    ROTMODEkw = ktl.cache(service='dcs', keyword='ROTMODE')
    log.info(f'Rotator mode is {ROTMODEkw.read()}')
    ROTPPOSNkw = ktl.cache(service='dcs', keyword='ROTPPOSN')
    ROTPPOSN = float(ROTPPOSNkw.read())
    log.info(f'Drive angle (ROTPPOSN) = {ROTPPOSN:.1f} deg')
    
    ##-------------------------------------------------------------------------
    ## Post-Condition Checks
    if skippostcond is True:
        log.debug('Skipping post condition checks')
    else:
        pass

    return ROTPPOSN


def drive_angle(skipprecond=False, skippostcond=False):
    '''Alias for rotpposn
    '''
    return rotpposn(skipprecond=skipprecond, skippostcond=skippostcond)


def _set_rotpposn(rotpposn, skipprecond=False, skippostcond=False):
    '''Set the rotator position in stationary mode.
    
    This only tries to set the position once, use `set_rotpposn` in practice
    as it makes multiple attempts which seems to be more reliable.
    '''
    this_function_name = inspect.currentframe().f_code.co_name
    log.debug(f"Executing: {this_function_name}")

    ##-------------------------------------------------------------------------
    ## Pre-Condition Checks
    if skipprecond is True:
        log.debug('Skipping pre condition checks')
    else:
        instrument_is_MOSFIRE()
    
    ##-------------------------------------------------------------------------
    ## Script Contents

    log.info(f'Setting ROTPPOSN to {rotpposn:.1f}')
    ROTDESTkw = ktl.cache(service='dcs', keyword='ROTDEST')
    ROTDESTkw.write(float(rotpposn))
    sleep(1)
    ROTMODEkw = ktl.cache(service='dcs', keyword='ROTMODE')
    ROTMODEkw.write('stationary')
    sleep(1)
    
    ##-------------------------------------------------------------------------
    ## Post-Condition Checks
    if skippostcond is True:
        log.debug('Skipping post condition checks')
    else:
        log.info(f'Waiting for rotator to be "in position"')
        ROTSTATkw = ktl.cache(service='dcs', keyword='ROTSTAT')
        ROTSTATkw.monitor()
        while str(ROTSTATkw) != 'in position':
            log.debug(f'ROTSTAT = "{ROTSTATkw}"')
            sleep(2)

    return None


def set_rotpposn(rotpposn):
    '''Set the rotator position in stationary mode.  Performs a single retry if
    a ktlError is raised.
    '''
    try:
        _set_rotpposn(rotpposn)
    except ktlExceptions.ktlError as e:
        log.warning(f"Failed to set rotator")
        log.warning(e)
        sleep(2)
        log.info('Trying again ...')
        _set_rotpposn(rotpposn)

