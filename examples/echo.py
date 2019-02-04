import asyncio
import aconsole


async def main():
    loop = asyncio.get_event_loop()
    console = aconsole.AsyncConsole()

    loop.create_task(console.mainloop())
    while True:
        while True:
            i = await console.input("echo to out: ")
            if i:
                break #Not none or empty string.
            
        await console.print("echo: %s"%i)
        await asyncio.sleep(0.5)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
