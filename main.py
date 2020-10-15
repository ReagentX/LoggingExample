import time
from multiprocessing import Process


def write_logs() -> None:
    # We can import the logger above and pickle the single instance across the processes
    #   but by importing it here each thread creates its own instance of the logger.
    # This is analogous to starting an instance of an app in each process.
    from lib.logger import LOGGER
    while True:
        LOGGER.error('Something weird happened.')
        LOGGER.info('A normal thing happened.')
        LOGGER.debug('Got HTTP response 200.')
        time.sleep(2)


processes = [Process(target=write_logs) for _ in range(4)]
proc_identifier = 0
for process in processes:
    proc_identifier += 1
    process.name = f'Logging Process #{proc_identifier}'
    process.start()
    # Prevent race condition where processes try and listen on the same port
    time.sleep(0.5)
write_logs()
