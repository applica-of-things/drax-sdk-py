import aiohttp
import asyncio

async def get_page(session, url):
    async with session.get(url) as r:
        return await r.text()

async def get_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def main(urls):
    async with aiohttp.ClientSession() as session:
        data = await get_all(session, urls)
        return data

if __name__== '__main__':
    urls = [
        "https://github.com/applica-of-things/drax-ecdh-py",
        "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token"
    ]
    results = asyncio.run(main(urls))
    print(results)