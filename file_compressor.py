import heapq
import os
from flask import session

current_directory = os.getcwd()

class Node:
    def __init__(self,frequency,character,left_node=None,right_node=None):
        self.frequency = frequency
        self.character = character
        self.left_node = left_node
        self.right_node = right_node
        self.huff = ''

    def __lt__(self,nxt):       # Less than method that is used while pushing into heapq
        return self.frequency < nxt.frequency       
    

class HuffmanCompressor:
    def __init__(self,data):
        #self.source_path = source_path
        self.dest_path = ''
        self.freqeuency_dict = {}
        self.encoding_dict = {}
        self.encoded_text = ''
        self.padded_text = ''
        self.decoding_dict = {}
        self.data = data

    def __generate_freq_dict(self,text):
        for character in text:
            if character not in self.freqeuency_dict:
                self.freqeuency_dict[character] = 0   # character is the key, 0 is frequency
            self.freqeuency_dict[character] += 1

    def __generate_encoding_dict(self,node, val=''): 

        newVal = val + str(node.huff) 
        if(node.left_node): 
            self.__generate_encoding_dict(node.left_node, newVal) 
        if(node.right_node): 
            self.__generate_encoding_dict(node.right_node, newVal) 
 
        if(not node.left_node and not node.right_node):
            self.encoding_dict[node.character] = newVal

    def __encode_text(self,text):
        for character in text:
            self.encoded_text += self.encoding_dict[character]

    def __generate_padded_text(self):
        if self.encoded_text != '':
            padding_value = 8 - len(self.encoded_text)%8
            
            for _ in range(padding_value):
                self.encoded_text += '0'

            padding_meta = format(padding_value,'08b')
            self.padded_text = padding_meta + self.encoded_text

    def __generate_byte_data(self):
        byte_values = []
        for i in range(0, len(self.padded_text), 8):
            
            byte_value = int(self.padded_text[i:i+8], 2)
            byte_values.append(byte_value)

        return bytes(byte_values)
    
    def __write_to_file(self,byte_data):
        file_name = os.path.splitext(self.source_path)[0]
        file_name += '_compressed.bin'
        file_path = os.path.join(current_directory,file_name)
        self.dest_path = file_path
        try:
            with open(self.dest_path, 'wb') as file:
                file.write(byte_data)
            print("Binary Data successfully written to file path")
        except Exception as e:
            print(f"Error in writing to file: {e}")

    def compression(self):
        text = self.data

        if text != '':
            self.__generate_freq_dict(text)
        else:
            print('Empty Text File')

        if len(self.freqeuency_dict)>0:
            min_heap = []
            for char, freq in self.freqeuency_dict.items():
                heapq.heappush(min_heap,Node(freq,char))

            while len(min_heap) > 1:
                left_node = heapq.heappop(min_heap)
                right_node = heapq.heappop(min_heap)

                left_node.huff = 0
                right_node.huff = 1 
                parent_node = Node(left_node.frequency + right_node.frequency, left_node.character+right_node.character, left_node, right_node)
                heapq.heappush(min_heap, parent_node)

            self.__generate_encoding_dict(min_heap[0])
            self.__encode_text(text)

            #str_encoding_dict = str(self.encoding_dict)
        
            ## padding
            self.__generate_padded_text()
            byte_data = self.__generate_byte_data()
            meta_data = str(self.encoding_dict)
            metadata_bytes = meta_data.encode('utf-8')

            session['encoding_dict'] = self.encoding_dict
            
            return metadata_bytes,byte_data

    

