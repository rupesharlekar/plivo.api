import pytest
import random
from plivoConfig import PlivoConfig

@pytest.fixture(scope='function')
def test_setup_teardown():

    print("\n--- starting test setup --- \n")

    get_numbers_response = callerRestClient.send_request('Number')
    print("\nget_numbers_response:\n",get_numbers_response)

    account_phone_numbers = [object['number'] for object in get_numbers_response['objects']]

    (sender, receiver) = tuple(random.sample(account_phone_numbers, 2))

    get_pricing_response = callerRestClient.send_request('PhoneNumber/?country_iso='+ PlivoConfig.COUNTRY_CODE)
    print("\nget_pricing_response:\n", get_pricing_response)

    msg_outbound_rate = get_pricing_response['message']['outbound']['rate']

    prereq_info = (sender, receiver).append(msg_outbound_rate)

    get_account_details = callerRestClient.send_request()
    print("\nget_account_details:\n", get_account_details)
    account_credits_at_start = get_account_details['cash_credits']

    prereq_info.append(account_credits_at_start)

    print("\n--- finishing test setup --- \n")

    yield prereq_info

    # print("\n--- starting test teardown --- \n")
    # # # Nothing to do here
    # print("\n--- finishing test teardown --- \n")


@pytest.mark.functional
def test_message_pricing(test_setup_teardown):

    sender = test_setup_teardown[0]
    receiver = test_setup_teardown[1]
    expected_msg_outbound_rate = test_setup_teardown[2]
    account_credits_at_start = test_setup_teardown[3]


    send_message_response = callerRestClient.send_request('Message',
                                        src = sender,
                                        dst = receiver,
                                        text = "Hi, text from Plivo")
    print("\nsend_message_response:\n",send_message_response)

    message_uuid = send_message_response['message_uuid']

    get_sent_message_details = callerRestClient.send_request('Message' +'/'+ message_uuid)

    actual_msg_rate_deducted = get_sent_message_details['total_rate']
    actual_msg_amount_deducted = get_sent_message_details['total_amount']

    assert actual_msg_rate_deducted == expected_msg_outbound_rate

    get_account_details = callerRestClient.send_request()
    print("\nget_account_details:\n", get_account_details)

    account_credits_remaining = get_account_details['cash_credits']

    assert account_credits_remaining == (account_credits_at_start - actual_msg_amount_deducted)



