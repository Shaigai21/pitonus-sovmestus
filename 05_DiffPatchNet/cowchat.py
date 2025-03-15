#!/usr/bin/env python3
import asyncio
import cowsay

clients = {}
cow_names = set(cowsay.list_cows())

async def chat(reader, writer):
    me = None
    queue = asyncio.Queue()
    writer.write(b"Please login using 'login <cow_name>'\n")
    await writer.drain()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(queue.get())
    online = True
    while not reader.at_eof():

        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                data = q.result().decode().strip()
                if not data:
                    continue
                command = data.split()
                if command[0] == 'who':
                    writer.write(f"Registered users: {', '.join(clients.keys())}\n".encode())
                    await writer.drain()
                elif command[0] == 'cows':
                    writer.write(f"Available cow names: {', '.join(cow_names)}\n".encode())
                    await writer.drain()
                elif len(command) == 2 and command[0] == 'login':
                    cow_name = command[1]
                    if cow_name not in cowsay.list_cows():
                        writer.write(f"Error: Cow name '{cow_name}' does not exist.\n".encode())
                    elif cow_name not in cow_names:
                        writer.write(f"Error: Cow name '{cow_name}' is already taken.\n".encode())
                    else:
                        if me:
                            clients.pop(me, None)
                            cow_names.add(me)
                        me = cow_name
                        clients[me] = queue
                        cow_names.remove(me)
                        writer.write(f"Logged in as {me}\n".encode())
                    await writer.drain()
                elif command[0] == 'say' and len(command) > 2:
                    if not me:
                        writer.write("Login to send and receive messages.\n".encode())
                        await writer.drain()
                    target = command[1]
                    if target in clients:
                        message = ' '.join(command[2:])
                        print(f"put {message} to {target}")
                        await clients[target].put(f"Message from {me}:\n{cowsay.cowsay(message, cow=me)}")
                    else:
                        writer.write(f"Error: No such user: {target}\n".encode())
                        await writer.drain()
                elif command[0] == 'yield' and len(command) > 1:
                    if not me:
                        writer.write("Login to send and receive messages.\n".encode())
                        await writer.drain()
                    message = ' '.join(command[1:])
                    for out in clients.values():
                        if out is not queue:
                            print(f"put {message} to {out}")
                            await out.put(f"Broadcast from {me}:\n{cowsay.cowsay(message, cow=me)}")
                elif command[0] == 'quit':
                    writer.write(b"Goodbye!\n")
                    await writer.drain()
                    online = False
                    break
                else:
                    writer.write(b"Error: Invalid command or invalid usage!\n")
                    await writer.drain()
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                if me: 
                    writer.write(f"{q.result()}\n".encode())
                    await writer.drain()
        if not online: break
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    if me:
        clients.pop(me, None)
        cow_names.add(me)
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())