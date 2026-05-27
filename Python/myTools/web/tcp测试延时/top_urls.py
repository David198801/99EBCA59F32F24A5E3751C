import asyncio
import aiohttp
import time


async def fetch_with_timeout(url, timeout=3):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            start = time.monotonic()
            response = await session.get(url)
            response_time = (time.monotonic() - start)*1000
            return response_time, url
    except Exception as e:
        return None, url
        


async def main():
    tasks = []
    results = []

    with open('url.txt', 'r') as f:
        urls = [x.replace('\n','') for x in f.readlines()]

    for url in urls:
        if url:
            tasks.append(fetch_with_timeout(url))

    for task in asyncio.as_completed(tasks):
        result, url = await task
        if result:
            results.append((url, result))

    sorted_results = sorted(results, key=lambda x: x[1])

    print("Top 5 fastest URLs:")
    for idx, (url, response_time) in enumerate(sorted_results[:5], 1):
        print(f"{idx}. {response_time:.2f}ms {url} ")

if __name__ == "__main__":
    asyncio.run(main())