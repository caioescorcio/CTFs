import telnetlib3, asyncio, re

host = "e6f33136be02690e.247ctf.com"
port = 50299
timeout = 100

async def shell(reader, writer):
    counter = 0
    while True:
        outp:str= await reader.read(1024)
        if counter > 500:
            break
        print(outp)
        counter += 1
        numbers_string:str = re.findall("\d+", outp)
        if numbers_string.__len__() > 2:
            r = int(numbers_string[2]) + int(numbers_string[3])
        else: 
            r = int(numbers_string[0]) + int(numbers_string[1])
        print(str(counter) + ": " + str(r) + "\n\n")
        writer.write(str(r)+ "\r\n")
        await writer.drain()
    # EOF
    print("end")

loop = asyncio.get_event_loop()
coro = telnetlib3.open_connection(host, port, shell=shell)
reader, writer = loop.run_until_complete(coro)
loop.run_until_complete(writer.protocol.waiter_closed)

