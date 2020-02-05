import inspect
import ktl

from .core import *


##-----------------------------------------------------------------------------
## get filter
##-----------------------------------------------------------------------------
def filter(skipprecond=False, skippostcond=False):
    '''Query for the current filter.
    
    This returns a single value which is the result of the pair of filter wheels
    in the instrument.  If you want to know the position of one filter wheel in
    particular, see filter1 and filter2 below
    '''
    
    ##-------------------------------------------------------------------------
    ## Pre-Condition Checks
    def precondition(skipprecond=False):
        '''docstring
        '''
        if skipprecond is True:
            log.debug('Skipping pre condition checks')
        else:
            filter1_ok()
            filter2_ok()
    
    ##-------------------------------------------------------------------------
    ## Post-Condition Checks
    def postcondition(skippostcond=False):
        '''docstring
        '''
        if skippostcond is True:
            log.debug('Skipping post condition checks')
        else:
            filter1_ok()
            filter2_ok()
    
    ##-------------------------------------------------------------------------
    ## Script Contents
    this_function_name = inspect.currentframe().f_code.co_name
    log.debug(f"Executing: {this_function_name}")
    precondition(skipprecond=skipprecond)

    filterkw = ktl.cache(service='mosfire', keyword='FILTER')
    filterkw.monitor()

    postcondition(skippostcond=skippostcond)

    return str(filterkw)


##-----------------------------------------------------------------------------
## isdark
##-----------------------------------------------------------------------------
def isdark(skipprecond=False, skippostcond=False):
    '''Return True if the current observing mode is dark
    '''
    
    ##-------------------------------------------------------------------------
    ## Pre-Condition Checks
    def precondition(skipprecond=False):
        '''docstring
        '''
        if skipprecond is True:
            log.debug('Skipping pre condition checks')
        else:
            filter1_ok()
            filter2_ok()
    
    ##-------------------------------------------------------------------------
    ## Post-Condition Checks
    def postcondition(skippostcond=False):
        '''docstring
        '''
        if skippostcond is True:
            log.debug('Skipping post condition checks')
        else:
            filter1_ok()
            filter2_ok()
    
    ##-------------------------------------------------------------------------
    ## Script Contents
    this_function_name = inspect.currentframe().f_code.co_name
    log.debug(f"Executing: {this_function_name}")
    precondition(skipprecond=skipprecond)

    filterkw = ktl.cache(service='mosfire', keyword='FILTER')
    filterkw.monitor()

    postcondition(skippostcond=skippostcond)

    return (str(filterkw) == 'Dark')


##-----------------------------------------------------------------------------
## waitfordark
##-----------------------------------------------------------------------------
def waitfordark(timeout=60, skipprecond=False, skippostcond=False):
    '''Wait for the instrument to be in a dark state.
    '''
    ##-------------------------------------------------------------------------
    ## Pre-Condition Checks
    def precondition(skipprecond=False):
        '''docstring
        '''
        if skipprecond is True:
            log.debug('Skipping pre condition checks')
        else:
            filter1_ok()
            filter2_ok()
    
    ##-------------------------------------------------------------------------
    ## Post-Condition Checks
    def postcondition(skippostcond=False):
        '''docstring
        '''
        if skippostcond is True:
            log.debug('Skipping post condition checks')
        else:
            filter1_ok()
            filter2_ok()
    
    ##-------------------------------------------------------------------------
    ## Script Contents
    this_function_name = inspect.currentframe().f_code.co_name
    log.debug(f"Executing: {this_function_name}")
    precondition(skipprecond=skipprecond)

    endat = dt.utcnow() + tdelta(seconds=timeout)
    filterkw = ktl.cache(service='mosfire', keyword='FILTER')
    filterkw.monitor()

    while dt.utcnow() < endat and str(filterkw) != 'Dark':
        sleep(1)
    if str(filterkw) != 'Dark':
        raise TimeoutError('Timed out waiting for instrument to be dark')

    postcondition(skippostcond=skippostcond)

    return None


##-----------------------------------------------------------------------------
## filter1
##-----------------------------------------------------------------------------
def filter1(skipprecond=False, skippostcond=False):
    '''Query for the filter in filter wheel 1.
    '''
    
    ##-------------------------------------------------------------------------
    ## Pre-Condition Checks
    def precondition(skipprecond=False):
        '''docstring
        '''
        if skipprecond is True:
            log.debug('Skipping pre condition checks')
        else:
            filter1_ok()
    
    ##-------------------------------------------------------------------------
    ## Post-Condition Checks
    def postcondition(skippostcond=False):
        '''docstring
        '''
        if skippostcond is True:
            log.debug('Skipping post condition checks')
        else:
            filter1_ok()
    
    ##-------------------------------------------------------------------------
    ## Script Contents
    this_function_name = inspect.currentframe().f_code.co_name
    log.debug(f"Executing: {this_function_name}")
    precondition(skipprecond=skipprecond)

    filter1kw = ktl.cache(service='mmf1s', keyword='POSNAME')
    filter1kw.monitor()

    postcondition(skippostcond=skippostcond)

    return str(filter1kw)


##-----------------------------------------------------------------------------
## filter2
##-----------------------------------------------------------------------------
def filter2(skipprecond=False, skippostcond=False):
    '''Query for the filter in filter wheel 1.
    '''
    
    ##-------------------------------------------------------------------------
    ## Pre-Condition Checks
    def precondition(skipprecond=False):
        '''docstring
        '''
        if skipprecond is True:
            log.debug('Skipping pre condition checks')
        else:
            filter2_ok()
    
    ##-------------------------------------------------------------------------
    ## Post-Condition Checks
    def postcondition(skippostcond=False):
        '''docstring
        '''
        if skippostcond is True:
            log.debug('Skipping post condition checks')
        else:
            filter2_ok()
    
    ##-------------------------------------------------------------------------
    ## Script Contents
    this_function_name = inspect.currentframe().f_code.co_name
    log.debug(f"Executing: {this_function_name}")
    precondition(skipprecond=skipprecond)

    filter2kw = ktl.cache(service='mmf2s', keyword='POSNAME')
    filter2kw.monitor()

    postcondition(skippostcond=skippostcond)

    return str(filter2kw)


##-----------------------------------------------------------------------------
## quick_dark
##-----------------------------------------------------------------------------
def quick_dark(wait=False, timeout=30,
               skipprecond=False, skippostcond=False):
    '''Set the instrument to a dark mode which is close to the specified filter.
    Modeled after darkeff script.
    '''
    
    ##-------------------------------------------------------------------------
    ## Pre-Condition Checks
    def precondition(skipprecond=False):
        '''docstring
        '''
        if skipprecond is True:
            log.debug('Skipping pre condition checks')
        else:
            filter1_ok()
            filter2_ok()
    
    ##-------------------------------------------------------------------------
    ## Post-Condition Checks
    def postcondition(wait, timeout, skippostcond=False):
        '''docstring
        '''
        if skippostcond is True:
            log.debug('Skipping post condition checks')
        else:
            if wait is True:
                waitfordark(timeout=timeout)
            filter1_ok()
            filter2_ok()
    
    ##-------------------------------------------------------------------------
    ## Script Contents
    this_function_name = inspect.currentframe().f_code.co_name
    log.debug(f"Executing: {this_function_name}")
    precondition(skipprecond=skipprecond)

    log.info('Setting quick dark')
    filter_combo = {'Y': ['H2', 'Y'],
                    'J': ['NB1061', 'J'],
                    'H': ['NB1061', 'H'],
                    'Ks': ['NB1061', 'Ks'],
                    'K': ['NB1061', 'K'],
                    'J2': ['J2', 'K'],
                    'J3': ['J3', 'K'],
                    'H1': ['H1', 'K'],
                    'H2': ['H2', 'K'],
                    None: ['NB1061', 'Ks'],
                    }
    f1dest, f2dest = filter_combo.get(filter())
    if filter1() != f1dest:
        f1targkw = ktl.cache(service='mmf1s', keyword='TARGNAME')
        f1targkw.write(f1dest)

    if filter2() != f2dest:
        f2targkw = ktl.cache(service='mmf2s', keyword='TARGNAME')
        f2targkw.write(f2dest)

    postcondition(wait, timeout, skippostcond=skippostcond)

    return None


##-----------------------------------------------------------------------------
## go_dark
##-----------------------------------------------------------------------------
def go_dark(wait=False, timeout=30,
             skipprecond=False, skippostcond=False):
    '''Alias for quick_dark
    '''
    quick_dark(wait=wait, timeout=timeout,
               skipprecond=skipprecond, skippostcond=skippostcond)
