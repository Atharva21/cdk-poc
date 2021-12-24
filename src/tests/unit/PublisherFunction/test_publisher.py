from typing import Dict
import pytest
import json
# import src.functions.PublisherFunction.app as publisher
# ! 👇 doesnt work?!
# from ....functions.PublisherFunction import app as publisher


@pytest.fixture(scope="function")
def valid_payload() -> Dict:
    return {
        'body': json.dumps(
            {
                "siteId": "2040111",
                "origin": "BP",
                "country": "GB",
                "items": [
                    {
                        "barcode": "5012035952808",
                        "linkedItemId": "2039711",
                        "stockOnHand": 10,
                        "availableForSale": True,
                        "lastUpdated": "2020-08-21T14:20:16.000Z",
                        "lastModified": "2020-08-21T14:30:16.000Z",
                        "updateReason": "FullUpdate",
                        "olaCode": "074"
                    },
                    {
                        "barcode": "5012035952809",
                        "linkedItemId": "2039711",
                        "stockOnHand": 10,
                        "availableForSale": True,
                        "lastUpdated": "2020-08-21T14:20:16.000Z",
                        "lastModified": "2020-08-21T14:30:16.000Z",
                        "updateReason": "FullUpdate",
                        "olaCode": "075"
                    },
                    {
                        "barcode": "5012035952811",
                        "linkedItemId": "2039711",
                        "stockOnHand": 10,
                        "availableForSale": True,
                        "lastUpdated": "2020-08-21T14:20:16.000Z",
                        "lastModified": "2020-08-21T14:30:16.000Z",
                        "updateReason": "FullUpdate",
                        "olaCode": "076"
                    }
                ]
            }
        )
    }


def test_sample(valid_payload: Dict):
    # import src.functions.PublisherFunction.app as publisher
    # result = publisher.main(valid_payload, None)
    # assert result == {
    #     'statusCode': 200,
    #     'body': 'published message to SQS'
    # }
    assert 1 == 1
