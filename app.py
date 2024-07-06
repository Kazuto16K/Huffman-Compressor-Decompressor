from flask import Flask, request, url_for, send_from_directory, render_template,redirect,session
import os,struct
from file_compressor import HuffmanCompressor
from file_decompressor import HuffmanDecompressor

app = Flask(__name__)
app.secret_key = 'hnjxnsjnanmxklnmaxomamlkxa'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['COMPRESSED_FOLDER'] = 'compressed'
app.config['DECOMPRESSED_FOLDER'] = 'decompressed'

os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)
os.makedirs(app.config['COMPRESSED_FOLDER'],exist_ok=True)
os.makedirs(app.config['DECOMPRESSED_FOLDER'],exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and file.filename.endswith('.txt'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
        file.save(filepath)

        compressed_filepath = compress_file(filepath)
        file_size = os.path.getsize(compressed_filepath)
        file_size = file_size / 1024.0
        file_size = "{:.2f}".format(file_size)

        download_link = url_for('download_file', filename = os.path.basename(compressed_filepath))
        return render_template('processed.html', link=download_link, file_size=file_size)
    else:
        return 'Invalid file type. Please upload text file'
    
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['COMPRESSED_FOLDER'],filename)

@app.route('/decompress/<filename>')
def download_decompressed_file(filename):
    return send_from_directory(app.config['DECOMPRESSED_FOLDER'],filename,as_attachment = True)

def compress_file(filepath):
    with open(filepath,'r') as file:
        text = file.read()

    hc = HuffmanCompressor(text)
    metadata_bytes,compressed_data = hc.compression()
    print('Compressing Done')
    
    compress_filename = os.path.splitext(os.path.basename(filepath))[0] + '_compressed.bin'
    compressed_filepath = os.path.join(app.config['COMPRESSED_FOLDER'],compress_filename)

    with open(compressed_filepath, 'wb') as file:
        file.write(struct.pack('I', len(metadata_bytes)))  
        file.write(metadata_bytes)
        file.write(compressed_data)

    return compressed_filepath


@app.route('/decompress',methods=['POST'])
def decompress_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and file.filename.endswith('.bin'):
        filepath = os.path.join(app.config['COMPRESSED_FOLDER'],file.filename)
        if os.path.exists(filepath):
            decompressed_filepath = decompress_file_function(filepath)
        else:
            return 'File doesnt exist in directory'
        
        file_size = os.path.getsize(decompressed_filepath)
        file_size = file_size / 1024.0
        file_size = "{:.2f}".format(file_size)
        
        download_link = url_for('download_decompressed_file', filename = os.path.basename(decompressed_filepath),folder = 'decompressed')
        return render_template('processed.html', link=download_link, file_size=file_size)
    else:
        return 'Invalid file type, Please Upload .bin file'
    

def decompress_file_function(filepath):
    with open(filepath, 'rb') as file:
        metadata_length = struct.unpack('I', file.read(4))[0]
        metadata_bytes = file.read(metadata_length)
        metadata_str = metadata_bytes.decode('utf-8')
        compressed_data = file.read()

    metadata = eval(metadata_str)
    hd = HuffmanDecompressor(data=compressed_data,encoding_dict=metadata)

    decompressed_text = hd.decompression()

    decompressed_filename = os.path.splitext(os.path.basename(filepath))[0] + '.txt'
    decompressed_filepath = os.path.join(app.config['DECOMPRESSED_FOLDER'], decompressed_filename)
    with open(decompressed_filepath, 'w') as file:
        file.write(decompressed_text)
    
    return decompressed_filepath

if __name__ == '__main__':
    app.run(debug=True)