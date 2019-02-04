# aconsole

Asynchorous Commandline like GUI for Python3. Uses asyncio and async await.
Controls

Mouse for navigating the output.
Keys for input:

    [Enter] submits input
    [Up/Down] navigates input history
<hr>

## Depencies

None. For GUI it uses Tkinter. But you need atleast Python 3.6
<hr>

## Simple Example

```py
import asyncio
import aconsole


async def main():
    loop = asyncio.get_event_loop()
    console = aconsole.AsyncConsole()

    loop.create_task(console.mainloop()) #Updates the GUI
    while True:
        while True:
            i = await console.input("echo to out: ")
            if i:
                break #None or empty string, we wont print that.
            
        await console.print("echo: %s"%i)
        #Lets sleep for half a second, so we see how console's input looks when there is no on going inputs.
        await asyncio.sleep(0.5) 
        
        #Console's input will be disabled and empty if there is no inputs requested.
        #There can be multiple awaiting inputs, they will be queued and processed in order.
        #You also can cancel on going input using console.cancel_input().


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

![image](https://raw.githubusercontent.com/theMINAD/aconsole/master/examples/images/echo.gif)
<hr>

## Other Example
 * [Async Chat Client](https://github.com/theMINAD/aconsole/blob/master/examples/chat_client.py)
 * [Async Chat Server](https://github.com/theMINAD/aconsole/blob/master/examples/chat_server.py)
 * [Simple Math Game](https://github.com/theMINAD/aconsole/blob/master/examples/game.py)
 * [Simple asking program](https://github.com/theMINAD/aconsole/blob/master/examples/asking.py)
 * [Simple asking program using sql](https://github.com/theMINAD/aconsole/blob/master/examples/asking_sql.py)