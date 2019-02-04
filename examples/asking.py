import aconsole
import asyncio


async def main():
    console = aconsole.AsyncConsole()
    loop = asyncio._get_running_loop()

    loop.create_task(console.mainloop())
    while True:
        name = await console.input("What is your name: ")
        age = 0
        
        while True:
            try:
                age = int((await console.input("What is your age: ")))
                break
            except:
                console.set_foreground('red')
                await asyncio.sleep(1)
                console.set_foreground('green')

        await console.print("Name: {%s}, Age:  {%s}"%(name, age))
        await console.print("---------------------------------")
        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())