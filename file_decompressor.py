import os
from flask import session

current_directory = os.getcwd()


class HuffmanDecompressor:
    def __init__(self,data,encoding_dict):
        self.encoding_dict = encoding_dict
        self.decoding_dict = {}
        self.data = data

    def __file_to_bits(self,content):
        bits_string = ''
        for byte in content:
            bits = bin(byte)[2:].zfill(8)  # Convert byte to bits (string) and zero-pad to 8 bits
            bits_string += bits
        return bits_string
    
    def __generate_decoding_dict(self):
        self.decoding_dict = {v: k for k, v in self.encoding_dict.items()}
    

    def __decode_data(self,data):
        decoded_data = ''
        current_bits = ''
        for char in data:
            current_bits += char
            if current_bits in self.decoding_dict:
                decoded_data += self.decoding_dict[current_bits]
                current_bits = ''

        return decoded_data

    def decompression(self):
        bits_string = self.__file_to_bits(self.data)
        if bits_string != '':
            padding_info = bits_string[0:8]
        else :
            print('Error Occured')
            return 'Error'
        decimal_value = int(padding_info, 2)

        removed_padding_meta = bits_string[8:]
        data = removed_padding_meta[:-decimal_value]
        self.__generate_decoding_dict()
        decoded_data = self.__decode_data(data)
        return decoded_data

