# aconsole

Asynchorous Commandline like GUI for Python 3.

Provides async await for print and input. It also supports having multiple awaiting inputs, which are queued and then processed one by one.

You can now get this lib from pip: https://pypi.org/project/aconsole/0.0.3/

See: [Multiple inputs awaiting](https://github.com/theMINAD/aconsole/blob/master/examples/multi.py).<br>

Other supported features:
 * Canceling input.
 * Changing color theme
 * Chaging transparency
<hr>

## Controls
Mouse for navigating the output.
Keys for input:

    [Enter] Submits input.
    [Up/Down] Navigates input history.

Keys for output:

    [Ctrl+C] Copy selected content.
    [Ctrl+R] Clears output.
<hr>

## Depencies
Just Python 3.5 or above. For GUI it uses Tkinter, which is built-in module in Python.<br>
Tested on: Mac, Linux and Windows.
<hr>

## A Simple Example
```py
import asyncio
import aconsole

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    
    console = AsyncConsole()
    console.title('echo test')

    async def echo():
        while True:
            result = await console.input('echo to out: ')
            console.print('echo:', result)

    run_task = console.run(loop)
    loop.create_task(echo())
    loop.run_until_complete(run_task) # wait until window closed
```

![image](https://raw.githubusercontent.com/theMINAD/aconsole/master/examples/images/echo.gif)
<hr>

## Other Examples
 * [Async Chat Client](https://github.com/theMINAD/aconsole/blob/master/examples/chat_client.py)
 * [Async Chat Server](https://github.com/theMINAD/aconsole/blob/master/examples/chat_server.py)
 * [Simple Math Game](https://github.com/theMINAD/aconsole/blob/master/examples/game.py)
 * [Simple asking program](https://github.com/theMINAD/aconsole/blob/master/examples/asking.py)
 * [Simple asking program using sql](https://github.com/theMINAD/aconsole/blob/master/examples/asking_sql.py)
 * [Multiple inputs awaiting](https://github.com/theMINAD/aconsole/blob/master/examples/multi.py)
