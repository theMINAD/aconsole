import aconsole
import asyncio

loop = asyncio.get_event_loop()
console = aconsole.AsyncConsole()

#You can have multiple incoming inputs:
#Since the will be queued up, and processed one by one:
first = loop.create_task(console.input("First: "))
second = loop.create_task(console.input("Second: "))
third = loop.create_task(console.input("Third: "))

#Gui loop, so our application responds:
mainloop = loop.create_task(console.mainloop())

loop.run_until_complete(asyncio.gather(first, second, third))
console.print_no_wait('First: %s, Second: %s, Third: %s'%(first.result(), second.result(), third.result()))
loop.run_until_complete(asyncio.sleep(5)) #After 5 seconds kill the app