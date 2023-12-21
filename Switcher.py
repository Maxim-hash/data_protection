from lab3 import *

def read_file(filename, ext):
    with open(filename + '.' + ext, 'rb') as file:
        return bytearray(file.read())
    
def write_file(filename, ext, encoded, sign):
    with open(f"encoded_file/{filename}.{ext}", 'w') as encode_file:
            encode_file.write(str(encoded))
            encode_file.write(str(sign))

class Switcher:

    def method(self, mode):
        default = "Invalid method"
        
        filename = "text"
        ext = "txt"
        self.mode = mode
        self.file = read_file(filename, ext)

        return getattr(self, "method_" + str(mode), lambda:default)()
    
    def method_elgamal(self):
        encoded = elgamal_encode(self.file)
        sign = el_gamal_sign(bytearray("".join(str(i) + " " for i in encoded), encoding='utf-8'))



        write_file(self.mode, "txt", encoded, sign)

    def method_rsa(self):
        encoded = rsa_encode(self.file)
        sign = rsa_sign(bytearray("".join(str(i) + " " for i in encoded), encoding='utf-8'), bytearray("".join(str(i) + " " for i in encoded), encoding='utf-8') + bytearray(1))


        write_file(self.mode, "txt", encoded, sign)

    def method_gost(self):
        encoded = rsa_encode(self.file)
        sign = gost_sign(bytearray("".join(str(i) + " " for i in encoded), encoding='utf-8'))

        write_file(self.mode, "txt", encoded, sign)
