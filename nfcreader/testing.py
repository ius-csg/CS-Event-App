# import nfc
# import struct

# ndef_data_area = bytearray(64 * 16)
# ndef_data_area[0] = 0x10  # NDEF mapping version '1.0'
# ndef_data_area[1] = 12    # Number of blocks that may be read at once
# ndef_data_area[2] = 8     # Number of blocks that may be written at once
# ndef_data_area[4] = 63    # Number of blocks available for NDEF data
# ndef_data_area[10] = 1    # NDEF read and write operations are allowed
# ndef_data_area[14:16] = struct.pack('>H', sum(ndef_data_area[0:14]))  # Checksum

# def ndef_read(block_number, rb, re):
#     if block_number < len(ndef_data_area) / 16:
#         first, last = block_number*16, (block_number+1)*16
#         block_data = ndef_data_area[first:last]
#         return block_data

# def ndef_write(block_number, block_data, wb, we):
#     global ndef_data_area
#     if block_number < len(ndef_data_area) / 16:
#         first, last = block_number*16, (block_number+1)*16
#         ndef_data_area[first:last] = block_data
#         return True

# def on_startup(target):
#     idm, pmm, sys = '03FEFFE011223344', '01E0000000FFFF00', '12FC'
#     target.sensf_res = bytearray.fromhex('01' + idm + pmm + sys)
#     target.brty = "106A"
#     print(target)
#     return target

# def on_connect(tag):
#     print("tag activated")
#     tag.add_service(0x0009, ndef_read, ndef_write)
#     tag.add_service(0x000B, ndef_read, lambda: False)
#     return True

# with nfc.ContactlessFrontend('usb:002:004') as clf:
#     print(clf.connect(card={'on-startup': on_startup, 'on-connect': on_connect}))
#     while clf.connect(card={'on-startup': on_startup, 'on-connect': on_connect}):
#         print("tag released")

# import nfc

# def on_connect(llc):
#     print(llc)
#     return True
# clf = nfc.ContactlessFrontend('usb:002:002')

# llc = clf.connect(llcp={'on_connect': on_connect})
# print(llc)
# clf.close()

from smartcard.scard import *
from smartcard.util import     toHexString

class printobserver( CardObserver ):
    def update( self, observable, addedcards, removedcards):
        for card in addedcards:
         if addedcards:
            hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
            assert hresult==SCARD_S_SUCCESS
            hresult, readers = SCardListReaders(hcontext, [])
            assert len(readers)>0
            reader = readers[0]
            hresult, hcard, dwActiveProtocol = SCardConnect(
             hcontext,
             reader,
             SCARD_SHARE_SHARED,
             SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
            hresult, response = SCardTransmit(hcard,dwActiveProtocol,[0xFF,0xCA,0x00,0x00,0x04])
            uid = toHexString(response, format=0)
            print (response) #cards ATR
            print (uid) #Cards UID

print( "place card on reader")
while 1:
    cardmonitor = CardMonitor()
    cardobserver = printobserver()
    cardmonitor.addObserver( cardobserver )
    cardmonitor.deleteObserver( cardobserver )
    time.sleep( 2 )