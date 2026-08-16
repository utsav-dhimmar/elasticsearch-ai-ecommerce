import asyncio

from elasticsearch import AsyncElasticsearch

from app.core.config import settings

client = AsyncElasticsearch(hosts=settings.ELASRICSEARCH_URL)


async def main():
    if await client.ping():
        print("elasticsearch is connected")
        print(await client.info())
    else:
        print("elasricsearch is not connected")


if __name__ == "__main__":
    asyncio.run(main())
