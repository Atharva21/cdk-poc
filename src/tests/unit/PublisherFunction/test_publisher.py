import src.functions.PublisherFunction.app as publisher


def test_sample():
    tmp = publisher.main(None, None)
    assert tmp == 'hi'
