import asyncio
import json

from app.core.embeddings.main import emd
from app.els.main import INDEX_NAME, elsearch_client
from app.els.main import main as els_main
from app.schemas.products import Product


async def main() -> None:
    await els_main()
    print("setting up index")
    with open("products.json", mode="r") as f:
        raw_data: list[Product] = json.load(fp=f)

        product_data_bulk: list = []

        for d in raw_data:
            p = Product.model_validate(d)
            p.description_vector = emd.embed(p.description).tolist()
            action = {
                "_index": INDEX_NAME,
                "_id": p.id,
                "_source": p.model_dump(),
            }
            product_data_bulk.append(action)

        print(product_data_bulk[0].values())
        res = await elsearch_client.insert_document_bulk(
            index_name=INDEX_NAME, documents=product_data_bulk
        )
        print(res)
        await elsearch_client.close()


if __name__ == "__main__":
    asyncio.run(main())
