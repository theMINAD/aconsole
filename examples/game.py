import aconsole
import asyncio
import random
from random import randint


loop = asyncio.get_event_loop()
main_console = aconsole.AsyncConsole()

game_answer = None
game_points = 0

async def game_output():
    global game_answer
    global game_points

    await main_console.print("TRY TYPE CALCULATE NUMBER BEFORE IT DISSAPEARS!")
    await asyncio.sleep(2)

    while True:
        main_console.clear_output()

        num1 = random.randint(0, 10)
        num2 = random.randint(0, 10)

        await main_console.print("WHAT IS: %d + %d"%(num1,  num2))
        await asyncio.sleep(2)
        
        main_console.clear_output()
        main_console.cancel_input()

        if game_answer == None:
            await main_console.print("TOO SLOW!, answer: %d"%(num1 + num2))
        elif game_answer == str(num1 + num2):
            await main_console.print("CORRECT!, answer: %d"%(num1 + num2))
            game_points += 1
        else:
            await main_console.print("WRONG!, answer: %d"%(num1 + num2))

        main_console.title("POINTS: %d"%(game_points))
        await asyncio.sleep(2)
        

async def game_input():
    global game_answer

    while True:
        game_answer = await main_console.input(">")

        if game_answer:
            await main_console.print("=>%s"%game_answer)
        

async def color_slider():
    r = 0
    g = 255
    b = 0

    r_inc = 30
    g_inc = 30
    b_inc = 30

    while True:
        r += r_inc
        g += g_inc
        b += b_inc

        if r >= 255:
            r = 255
            r_inc = -randint(20, 50)
        if g >= 255:
            g = 255
            g_inc = -randint(20, 50)
        if b >= 255:
            b = 255
            b_inc = -randint(20, 50)

        if r <= 0:
            r = 0
            r_inc = randint(20, 50)
        if g <= 0:
            g = 0
            g_inc = randint(20, 50)
        if b <= 0:
            b = 0
            b_inc = randint(20, 50) 

        main_console.set_foreground('#%02x%02x%02x' % (r, g, b))
        
        await asyncio.sleep(1/20)


if __name__ == '__main__':
    t1 = loop.create_task(main_console.mainloop())
    t2 = loop.create_task(game_output())
    t3 = loop.create_task(game_input())
    t4 = loop.create_task(color_slider())

    loop.run_until_complete(asyncio.gather(t1, t4))

#Simple calculating game. If user is too slow input is canceled.