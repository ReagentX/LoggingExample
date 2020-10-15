import time 
from multiprocessing import Process 

from lib.logger import LOGGER


def write_logs() -> None: 
    while True:
        LOGGER.error('Oops, something weird happened.')
        LOGGER.info('Hey, something happened.')
        LOGGER.debug('Got http code 200.')
        time.sleep(1)


processes = [Process(target=write_logs) for _ in range(4)]
proc_identifier = 0
for process in processes:
    proc_identifier += 1
    process.name = f'Logging Process #{proc_identifier}'
    process.start()
    # Prevent race condition where processes try and listen on the same port
    time.sleep(1)
write_logs()