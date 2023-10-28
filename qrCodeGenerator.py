import segno

class QRCodeGenerator:

    @classmethod
    def makeRoomQRCode(cls, room_id):
        qr_code = segno.make_qr(room_id)
        qr_code.save(f'room_{room_id}_qr_code.png')
