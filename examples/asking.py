import aconsole
import asyncio

console = aconsole.AsyncConsole()

async def main():    
    while True:
        name = await console.input("What is your name: ")
        age = 0
        
        while True:
            try:
                age = int((await console.input("What is your age: ")))
                break
            except asyncio.CancelledError:
                break
            except:
                console.set_colors('black', 'red')
                await asyncio.sleep(1)
                console.set_colors('black', 'green')

        console.print("Name: {%s}, Age:  {%s}"%(name, age))
        console.print("---------------------------------")
        await asyncio.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run_task = console.run()
    loop.run_until_complete(main())
