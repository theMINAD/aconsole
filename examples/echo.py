import asyncio
import aconsole


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    
    console = aconsole.AsyncConsole()
    console.title('echo test')
    console.set_alpha(0.9)

    async def echo():
        while True:
            result = await console.input('echo: ')
            console.print('you typed:', result)

    run_task = console.run()
    loop.create_task(echo())
    loop.run_until_complete(run_task)
