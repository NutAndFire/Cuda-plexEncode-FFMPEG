from os import path, listdir
from sys import argv
from plexEncode import Encoder


if __name__ == '__main__':
    if len(argv) < 2:
        print('Please provide directory to encode')
        exit(1)

    plexEn = Encoder()
    inputDirectory = path.join(argv[1], '')
    outputDirectory = path.join(inputDirectory, plexEn.OUTPUT_DIRECTORY, '')

    plexEn.clean_directory(outputDirectory)
    filesInInputDirectory = [inputDirectory + fileName for fileName in listdir(inputDirectory)]
    filesToEncode = filter(path.isfile, filesInInputDirectory)

    for file in filesToEncode:
        plexEn.plex_encoder(file, outputDirectory)
