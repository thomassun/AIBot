import asyncio


async def main():
    print("Hello ...")
    await asyncio.sleep(100)
    print("... World!")


asyncio.run(main())
