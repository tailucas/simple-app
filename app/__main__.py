#!/usr/bin/env python
import asyncio
import configparser
import locale
import logging
import os
import threading


from tailucas_pylib import app_config, log, WORK_DIR
from tailucas_pylib.process import SignalHandler
from tailucas_pylib import threads
from tailucas_pylib.threads import thread_nanny, die, bye
from tailucas_pylib.zmq import zmq_term


async def main():
    log.setLevel(logging.DEBUG)
    # ensure proper signal handling; must be main thread
    signal_handler = SignalHandler()
    nanny = threading.Thread(
        name="nanny", target=thread_nanny, args=(signal_handler,), daemon=True
    )
    # test inherited locale settings
    if "LC_ALL" in os.environ.keys():
        locale.setlocale(locale.LC_ALL, os.environ["LC_ALL"])
        conv = locale.localeconv()
        int_curr_symbol = str(conv["int_curr_symbol"]).rstrip()
        currency_symbol = str(conv["currency_symbol"])
        if int_curr_symbol is None or len(int_curr_symbol) == 0:
            raise AssertionError(
                "Locale settings are incomplete. Local currency configuration is not available."
            )
        log.info(
            f"Locale is {locale.getlocale()} using currency symbols [{int_curr_symbol}] => [{currency_symbol}]"
        )
    else:
        log.warning("No locale settings found for currency and date configurations.")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # startup completed
    # back to INFO logging
    log.setLevel(logging.INFO)
    try:
        # start thread nanny
        nanny.start()
        config_value = None
        try:
            config_value = app_config.getint("app", "simple_config")
        except configparser.NoSectionError:
            log.warning(
                "No configuration found, likely due to being run outside of the container context."
            )
        env_vars = list(os.environ)
        env_vars.sort()

        log.info(
            f"Startup complete with {config_value=!s} and {len(env_vars)} environment variables visible: {env_vars}. {WORK_DIR=}."
        )
        threads.interruptable_sleep.wait()
        log.info("Shutting down...")
    finally:
        die()
        zmq_term()
        loop.close()
    bye()


if __name__ == "__main__":
    asyncio.run(main())
