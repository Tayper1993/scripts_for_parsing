import asyncio
from time import perf_counter

from parsers.igromania import parse_igromania_news
from parsers.noob_club import parse_noob_club


if __name__ == '__main__':
    start = perf_counter()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(parse_noob_club())
    loop.run_until_complete(parse_igromania_news())
    print(f"Время выполнения: {(perf_counter() - start):.02f}")
