import asyncio
import aconsole


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    
    console = AsyncConsole()
    console.title('echo test')
    console.set_alpha(0.9)

    async def echo():
        while True:
            result = await console.input('echo: ')
            console.print('you typed:', result)

    with suppress(asyncio.CancelledError):
        console.run()
        loop.run_until_complete(echo())
