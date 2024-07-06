## Huffman Coding File Compression and Decompression Website

This website provides a user-friendly interface for compressing text files into binary files using Huffman coding, a popular algorithm for data compression. It also supports the decompression of binary files back into their original text format.

###  Features:
  - **File Compression** : Upload text files to the website, which then applies Huffman coding to generate compressed binary files. Huffman coding ensures efficient compression by assigning shorter codes to frequently occurring characters.

  - **File Decompression**: Upload previously compressed binary files to decompress them back into their original text format. The website reconstructs the original files using the same Huffman coding scheme used for compression.

  - **User Interface**: An intuitive web interface allows users to easily upload files, initiate compression or decompression processes, and download the resulting files.

### Usage:
  - **Upload Files**: Select a text file for compression or a binary file for decompression.

  - **Compression**: After uploading a text file, initiate the compression process. The website generates a binary file containing the compressed data.

  - **Decompression**: Upload a previously compressed binary file to decompress it back into its original text format. The website reconstructs the text file using the stored Huffman coding scheme.

### Technologies Used:
  - **Backend**: Python with Flask framework for handling file operations and implementing Huffman coding algorithms.

  - **Frontend**: HTML and CSS for creating an interactive user interface.

### Contact:
  - For questions, issues, or suggestions, please open an issue on GitHub.
