import pytest


def test_messaging_price():

    get_numbers_response = callerRestClient.send_request('number')

    print("\nget_numbers_response:",get_numbers_response)