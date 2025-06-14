import time, datetime, threading
from telegram_handler import check_telegram_messages, get_last_update_id, send_msg
from dhan_client import dhan
from logger_config import setup_logger
import kill_switch
from pnl_tracker import get_pnl

# Define profit/loss levels
profit = 2550
loss = -2250
sl_move = 2250
trail_sl = loss

logger = setup_logger("algo_logs")
last_update_id = get_last_update_id()

order_executed = False
start_time = time.time()
statement_interval = 180

universal_exit = False

# Start Telegram listener thread
telegram_thread = threading.Thread(target=check_telegram_messages, args=(lambda: order_executed, lambda: universal_exit), daemon=True)
telegram_thread.start()

# Startup messages
send_msg("Dhan Algo started.")
send_msg("Trade with 25 quantity.")  # Adjust as needed
send_msg("Accept Uncertainty.")
send_msg("You can't lose all the trades.")
send_msg("Take StopLoss with proud trader mindset.")
send_msg("It is all about PROBABILITY.")

logger.info("Dhan Algo Started.")

while datetime.datetime.now().time() < datetime.time(15, 15, 0):
    if time.time() - start_time >= statement_interval:
        logger.info("I am running. Relax Boss!")
        send_msg("I am running. Relax Boss!")
        start_time = time.time()

    if datetime.datetime.now().time() > datetime.time(9, 15, 0):
        try:
            total_pnl = get_pnl()
            logger.info("Total PnL: {}".format(round(total_pnl, 2)))

            if total_pnl > profit or total_pnl < trail_sl or universal_exit:
                universal_exit = True
                # cancel open orders + square off logic (to be added)
                logger.info("Exit condition met. Square off logic triggered.")
                break
        except Exception as e:
            logger.error(f"Error during loop: {e}")
    time.sleep(1)

logger.info(f"Booked PnL: {get_pnl():.2f} ₹")
send_msg(f"📊 Booked PnL: {get_pnl():.2f} ₹")

# Kill switch
kill_swith_res = kill_switch.main("PKR491")
if kill_swith_res:
    logger.info("Kill switch activated.")
    send_msg("Kill switch activated.")

time.sleep(20)
kill_swith_res = kill_switch.main("PKR491")
if kill_swith_res:
    logger.info("Kill switch activated-2.")
    send_msg("Kill switch activated-2.")

logger.info("Dhan Algo Stopped.")
send_msg("Algo Stopped.")
