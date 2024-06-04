'''Module for testing ds_messenger.py'''

import ds_messenger

def test_ds_messenger():
    '''Function for testing ds_messenger.py'''
    wlay, wlay2 = instance_direct_messengers()
    assert wlay is not None
    assert wlay.token is not None
    assert wlay.sent is not None
    assert wlay.recv is not None
    assert wlay2 is not None
    assert wlay2.token is not None
    assert wlay2.sent is not None
    assert wlay2.recv is not None

    # Testing if retrieve_new() returns an empty list before messages are sent
    list_of_new = wlay2.retrieve_new()
    assert isinstance(list_of_new, list)
    assert len(list_of_new) == 0

    # Testing if send() returns True for a proper message and the msg is appended to dms_out
    len_before = len(wlay.dms_out)
    assert wlay.send("test sending", "wlay2") is True
    assert len(wlay.dms_out) > len_before

    # Testing if retrieve_new() returns a list of DirectMessages
    list_of_new = wlay2.retrieve_new()
    assert isinstance(list_of_new, list)
    for dm in list_of_new:
        assert isinstance(dm, ds_messenger.DirectMessage)

    # Testing if retrieve_all() returns a list of DirectMessages
    assert wlay.send("second test sending", "wlay2") is True
    list_of_all = wlay2.retrieve_all()
    assert isinstance(list_of_all, list)
    for dm in list_of_all:
        assert isinstance(dm, ds_messenger.DirectMessage)
    list_of_new = wlay2.retrieve_new()
    assert isinstance(list_of_new, list)

    # Testing if faulty DirectMessengers can be instantiated and if they have tokens, sent, and recv
    invalid_server, wrong_pd = instance_faulty_messengers()
    assert invalid_server is not None
    assert invalid_server.token is None
    assert invalid_server.sent is None
    assert invalid_server.recv is None
    assert wrong_pd is not None
    assert wrong_pd.token is None
    assert wrong_pd.sent is not None
    assert wrong_pd.recv is not None

    # Testing if send() returns False when a DirectMessenger without a server attempts to send
    len_before = len(invalid_server.dms_out)
    assert invalid_server.send("test sending with invalid server", "wlay2") is False
    assert len(invalid_server.dms_out) == len_before

    # Testing if send() returns False when a DirectMessenger without a token attempts to send
    len_before = len(wrong_pd.dms_out)
    assert wrong_pd.send("test sending with wrong password", "wlay2") is False
    assert len(wrong_pd.dms_out) == len_before

    # Testing if retrieve_new() returns an empty list for a faulty DirectMessenger
    list_of_new = invalid_server.retrieve_new()
    assert isinstance(list_of_new, list)
    assert len(list_of_new) == 0

    # Testing if retrieve_all() returns an empty list for a faulty DirectMessenger
    list_of_all = invalid_server.retrieve_new()
    assert isinstance(list_of_all, list)
    assert len(list_of_all) == 0


def instance_direct_messengers():
    '''Function for instantiating DirectMessengers'''
    wlay = ds_messenger.DirectMessenger("168.235.86.101", "wlay", "123")
    wlay2 = ds_messenger.DirectMessenger("168.235.86.101", "wlay2", "123")
    return wlay, wlay2

def instance_faulty_messengers():
    '''Function for instantiating faulty DirectMessengers'''
    invalid_server = ds_messenger.DirectMessenger("", "wlay no server", "123")
    wrong_pwd = ds_messenger.DirectMessenger("168.235.86.101", "wlay", "111")
    return invalid_server, wrong_pwd
