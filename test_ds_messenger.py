import ds_messenger

dm = ds_messenger.DirectMessenger("168.235.86.101", "wlay", "123")
dm2 = ds_messenger.DirectMessenger("168.235.86.101", "wlay2", "123")

# dm.send("test 1", "wlay2")

# dm2.send("test 2", "wlay")
# dm2.send("test 3", "wlay")

print(dm2.retrieve_new())
print(dm.retrieve_all())