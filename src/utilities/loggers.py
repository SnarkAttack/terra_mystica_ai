import logging

LOG_TIMING = False

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

timer_logger = logging.getLogger('timer_log')
timer_logger.setLevel(logging.DEBUG)

timer_fh = logging.FileHandler('logs/timer.log')

timer_fh.setFormatter(formatter)
timer_logger.addHandler(timer_fh)

def log_timing_info(msg):
    if LOG_TIMING:
        timer_logger.debug(msg)

game_logger = logging.getLogger('game_log')
game_logger.setLevel(logging.INFO)

game_fh = logging.FileHandler('logs/games.log')

game_fh.setFormatter(formatter)
game_logger.addHandler(game_fh)
