import aconsole
import asyncio

loop = asyncio.get_event_loop()
console = aconsole.AsyncConsole()

async def main():
    #You can have multiple incoming inputs:
    #Since the will be queued up, and processed one by one:
    first = console.input("First: ")
    second = console.input("Second: ")
    third = console.input("Third: ")

    await asyncio.wait([first, second, third])
    console.print('First: %s, Second: %s, Third: %s'%(first.result(), second.result(), third.result()))
    await asyncio.sleep(5)

console.run(loop)
loop.run_until_complete(main())
