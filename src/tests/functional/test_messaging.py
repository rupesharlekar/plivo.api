import pytest
import random
import PlivoConfig
import requests

@pytest.fixture(scope='function')
def setup_teardown():

    print("\n--- starting test setup --- \n")

    get_numbers_response_status_code , get_numbers_response = callerRestClient.send_request(
        PlivoConfig.AUTH_ID + '/Number')
    assert get_numbers_response_status_code == requests.codes.ok
    print("\nget_numbers_response:\n",get_numbers_response)

    account_phone_numbers = [object['number'] for object in get_numbers_response['objects']]

    (sender, receiver) = tuple(random.sample(account_phone_numbers, 2))

    get_pricing_response_status_code, get_pricing_response = callerRestClient.send_request(
        PlivoConfig.AUTH_ID + '/PhoneNumber/?country_iso=' + PlivoConfig.COUNTRY_CODE)
    assert get_pricing_response_status_code == requests.codes.ok
    print("\nget_pricing_response:\n", get_pricing_response)

    msg_outbound_rate = get_pricing_response['message']['outbound']['rate']

    prereq_info = (sender, receiver).append(msg_outbound_rate)

    get_account_details_status_code , get_account_details = callerRestClient.send_request(PlivoConfig.AUTH_ID)
    assert get_account_details_status_code == requests.codes.ok
    print("\nget_account_details:\n", get_account_details)
    account_credits_at_start = get_account_details['cash_credits']

    prereq_info.append(account_credits_at_start)

    print("\n--- finishing test setup --- \n")

    yield prereq_info

    # print("\n--- starting test teardown --- \n")
    # # # Nothing to do here
    # print("\n--- finishing test teardown --- \n")

def test_message_pricing(setup_teardown):

    sender = setup_teardown[0]
    receiver = setup_teardown[1]
    expected_msg_outbound_rate = setup_teardown[2]
    account_credits_at_start = setup_teardown[3]

    send_message_response_response_code, send_message_response = callerRestClient.send_request(
        PlivoConfig.AUTH_ID + '/Message',
        src = sender,
        dst = receiver,
        text = "Hi, text from Plivo")
    assert send_message_response_response_code == requests.codes.accepted
    print("\nsend_message_response:\n",send_message_response)

    message_uuid = send_message_response['message_uuid']

    get_sent_message_details_status_code , get_sent_message_details = callerRestClient.send_request(
        PlivoConfig.AUTH_ID + '/Message/' + message_uuid)
    assert get_sent_message_details_status_code == requests.codes.ok
    print("\nget_sent_message_details:\n", get_sent_message_details)

    actual_msg_rate_deducted = get_sent_message_details['total_rate']
    actual_msg_amount_deducted = get_sent_message_details['total_amount']

    assert actual_msg_rate_deducted == expected_msg_outbound_rate

    get_account_details_status_code, get_account_details = callerRestClient.send_request(PlivoConfig.AUTH_ID)
    assert get_account_details_status_code == requests.codes.ok
    print("\nget_account_details:\n", get_account_details)

    account_credits_remaining = get_account_details['cash_credits']

    assert account_credits_remaining == (account_credits_at_start - actual_msg_amount_deducted)



