import segno, shutil


class QRCodeGenerator:

    @classmethod
    def makeRoomQRCode(cls, room_id):
        qr_code = segno.make_qr(room_id)
        filename = f'room_{room_id}_qr_code.png'
        qr_code.save(filename)
        shutil.move(filename, f'qr_codes/{filename}')
