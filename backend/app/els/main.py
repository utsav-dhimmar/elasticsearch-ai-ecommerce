import asyncio
from typing import Any

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from app.core.config import settings

client = AsyncElasticsearch(hosts=settings.ELASRICSEARCH_URL)

INDEX_NAME = "products"
MAPPINGS = {
    "properties": {
        "id": {"type": "keyword"},
        "title": {"type": "text"},
        "description": {"type": "text"},
        "category": {"type": "keyword"},
        "description_vector": {
            "type": "dense_vector",
            "dims": 384,
            "index": True,
            "similarity": "cosine",
        },
    }
}


class ElasticsearchClient:
    def __init__(self):
        self.client: AsyncElasticsearch = client

    async def ping(self):
        return await self.client.ping()

    async def info(self):
        return await self.client.info()

    async def close(self):
        await self.client.close()

    async def create_index(
        self, index_name: str = INDEX_NAME, mappings: dict = MAPPINGS
    ):
        res = await self.client.indices.create(
            index=index_name, mappings=mappings
        )

        return res

    async def check_index(self, index_name: str = INDEX_NAME):
        res = await self.client.indices.exists(index=index_name)

        return res

    async def get_document(self, index_name: str, doc_id: str):
        res = await self.client.get(index=index_name, id=doc_id)

        return res

    async def search(self, index_name: str, query: dict):
        res = await self.client.search(index=index_name, body=query)

        return res

    async def insert_document_bulk(self, index_name: str, documents: list[Any]):
        success, fail = await async_bulk(self.client, actions=documents)
        return {
            "success_count": success,
            "failed_count": len(str(fail)),
            "errors": fail,
        }


elsearch_client = ElasticsearchClient()


async def main():
    if not await elsearch_client.ping():
        print("elasricsearch is not connected")
        return

    print(await elsearch_client.info())
    print("elasticsearch is connected")

    if await elsearch_client.check_index(INDEX_NAME):
        print("index is already created")
        return
    print("creating index")
    await elsearch_client.create_index(INDEX_NAME, MAPPINGS)

    await elsearch_client.close()


if __name__ == "__main__":
    asyncio.run(main())
