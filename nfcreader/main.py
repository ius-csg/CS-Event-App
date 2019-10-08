import nfc
from nfc.clf import RemoteTarget

import sys, os


clf = nfc.ContactlessFrontend('usb:001:002')

target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
print(target)


tag = clf.connect(rdwr={'on_connect': lambda tag: False})
print(tag)
assert tag.ndef is not None
assert tag.ndef.records[0].type == 'urn:nfc:wkt:T'
print(tag.ndef.records[0].text)

clf.close()