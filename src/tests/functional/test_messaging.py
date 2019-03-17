import pytest
import random
from tests import PlivoConfig
import requests

@pytest.fixture(scope='function')
def setup_teardown():

    print("\n--- starting test setup --- \n")

    prereq_info = {}

    get_account_details_status_code , get_account_details = callerRestClient.send_request(PlivoConfig.AUTH_ID)
    print("\nget_account_details:\n", get_account_details)
    assert get_account_details_status_code == requests.codes.ok

    account_credits_at_start = get_account_details['cash_credits']
    prereq_info['account_credits_at_start'] = account_credits_at_start

    get_numbers_response_status_code , get_numbers_response = callerRestClient.send_request(
        PlivoConfig.AUTH_ID + '/Number')
    print("\nget_numbers_response:\n",get_numbers_response)
    assert get_numbers_response_status_code == requests.codes.ok

    account_phone_numbers = [object['number'] for object in get_numbers_response['objects']]
    (sender, receiver) = tuple(random.sample(account_phone_numbers, 2))
    prereq_info['numbers'] = [sender,receiver]

    get_pricing_response_status_code, get_pricing_response = callerRestClient.send_request(
                                            PlivoConfig.AUTH_ID + '/Pricing/?country_iso=' + PlivoConfig.COUNTRY_CODE)
    print("\nget_pricing_response:\n", get_pricing_response)
    assert get_pricing_response_status_code == requests.codes.ok

    msg_outbound_rate = get_pricing_response['message']['outbound']['rate']
    prereq_info['msg_outbound_rate'] = msg_outbound_rate

    print("\n--- finishing test setup --- \n")

    yield prereq_info

    # print("\n--- starting test teardown --- \n")
    # # # Nothing to do here
    # print("\n--- finishing test teardown --- \n")

@pytest.mark.functional
def test_message_pricing(setup_teardown):

    sender = setup_teardown['numbers'][0]
    receiver = setup_teardown['numbers'][1]
    expected_msg_outbound_rate = setup_teardown['msg_outbound_rate']
    account_credits_at_start = setup_teardown['account_credits_at_start']

    print("sender",sender)
    print("receiver",receiver)
    print("expected_msg_outbound_rate",expected_msg_outbound_rate)
    print("account_credits_at_start",account_credits_at_start)

    send_message_response_response_code, send_message_response = callerRestClient.send_request(
                                                                        PlivoConfig.AUTH_ID + '/Message',
                                                                        src = sender,
                                                                        dst = receiver,
                                                                        text = "Hi, text from Plivo")
    print("\nsend_message_response:\n", send_message_response)
    assert send_message_response_response_code == requests.codes.accepted
    assert len(send_message_response['message_uuid']) == 1

    message_uuid = send_message_response['message_uuid'][0]
    get_sent_message_details_status_code , get_sent_message_details = callerRestClient.send_request(
                                                                        PlivoConfig.AUTH_ID +'/Message/'+ message_uuid)
    print("\nget_sent_message_details:\n", get_sent_message_details)
    assert get_sent_message_details_status_code == requests.codes.ok

    actual_msg_rate_deducted = get_sent_message_details['total_rate']
    actual_msg_amount_deducted = get_sent_message_details['total_amount']
    assert actual_msg_rate_deducted == expected_msg_outbound_rate

    get_account_details_status_code, get_account_details = callerRestClient.send_request(PlivoConfig.AUTH_ID)
    print("\nget_account_details:\n", get_account_details)
    assert get_account_details_status_code == requests.codes.ok

    account_credits_remaining = get_account_details['cash_credits']
    assert account_credits_remaining == (account_credits_at_start - actual_msg_amount_deducted)



