#! /usr/bin/env python
'''Tool for analyzing images'''
from __future__ import print_function
from PIL import Image
import imagehash
import argparse
import shelve
import glob
import uuid
import random
import shutil
import os
import collections
import subprocess

import math
import numpy

def index(args):
    '''Process and index a dataset for futher inspection'''
    # open the shelve database
    db = shelve.open(args["shelve"], writeback=True)
    db['grayscale'] = db.get('grayscale', {})
    db['color'] = db.get('color', {})

    # loop over the image dataset
    for imagePath in glob.iglob(os.path.join(args['dataset'], '*.JPG')):
        # load the image and compute the difference hash
        image = Image.open(imagePath)
        ghash = str(imagehash.grayscale_hash(image))
        chash = str(imagehash.color_hash(image))

        # extract the filename from the path and update the database
        # using the hash as the key and the filename append to the
        # list of values
        filename = os.path.abspath(imagePath)
        db['grayscale'][ghash] = db['grayscale'].get(ghash, []) + [filename]
        db['color'][chash] = db['color'].get(chash, []) + [filename]

    print('{} files indexed'.format(len(db['color'].items())))

    # close the shelf database
    db.close()


def supersearch(args):
    '''Search the database for similar files'''
    # open the shelve database
    db = shelve.open(args["shelve"])

    query = Image.open(args["query"])

    if args['hash_name'] == 'grayscale':
        h = imagehash.grayscale_hash(query)
        db_hash = db['grayscale']
    elif args['hash_name'] == 'color':
        h = imagehash.color_hash(query)
        db_hash = db['color']

    print(collections.Counter(len(hex) for hex, image in db_hash.items()).most_common())
    l = [(h - imagehash.hex_to_hash(hex), hex)  for hex, image in db_hash.items()]

    c = collections.Counter(item[0] for item in l)
    print(sorted(c.most_common(), key=lambda item: item[0]))

    command = []
    for strength, item in sorted(l, key=lambda item: item[0]):
        if args['threshold'] < 0 or strength <= args['threshold']:
            print('{} count: {} stength: {}'.format(db_hash[item][0], len(db_hash[item]), strength))
            command.append(db_hash[item][0])
    if command:
        subprocess.call(['feh', '-t', '-F', '-y 150', '-E 150'] + command)


def search(args):
    '''Search the database for matching files'''
    # open the shelve database
    db = shelve.open(args["shelve"])

    # load the query image, compute the difference image hash, and
    # and grab the images from the database that have the same hash
    # value
    query = Image.open(args["query"])

    if args['hash_name'] == 'grayscale':
        h = imagehash.grayscale_hash(query)
        db_hash = db['grayscale']
    elif args['hash_name'] == 'color':
        h = imagehash.color_hash(query)
        db_hash = db['color']


    filenames = db_hash[str(h)]
    print("Found %d images" % (len(filenames)))

    # loop over the images
    for filename in filenames:
        print(filename)
        #image = Image.open(args["dataset"] + "/" + filename)
        #image.show()

    # close the shelve database
    db.close()


def gather(args):
    '''Grab subset of files from CALTECH or other dataset'''
    # open the output file for writing
    output = open(args["csv"], "w")

    # loop over the input images
    for imagePath in glob.iglob(os.path.join(args["input"], "*/*.jpg")):
        # generate a random filename for the image and copy it to
        # the output location
        filename = str(uuid.uuid4()) + ".jpg"
        shutil.copy(imagePath, os.path.join(args["output"], filename))

        # there is a 1 in 500 chance that multiple copies of this
        # image will be used
        if random.randint(0, 500) == 0:
            # initialize the number of times the image is being
            # duplicated and write it to the output CSV file
            numTimes = random.randint(1, 8)
            output.write("%s,%d\n" % (filename, numTimes))

            # loop over a random number of times for this image to
            # be duplicated
            for i in xrange(0, numTimes):
                image = Image.open(imagePath)

                # randomly resize the image, perserving aspect ratio
                factor = random.uniform(0.95, 1.05)
                width = int(image.size[0] * factor)
                ratio = width / float(image.size[0])
                height = int(image.size[1] * ratio)
                image = image.resize((width, height), Image.ANTIALIAS)

                # generate a random filename for the image and copy
                # it to the output directory
                adjFilename = str(uuid.uuid4()) + ".jpg"
                shutil.copy(imagePath, os.path.join(args["output"], adjFilename))

    # close the output file
    output.close()


def main():
    '''Main function'''
    # construct the argument parse and parse the arguments
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser_name")
    index_parser = subparsers.add_parser('index')
    index_parser.add_argument("-d", "--dataset",
                              required=True,
                              help="path to input dataset of images")
    index_parser.add_argument("-s", "--shelve",
                              required=True,
                              help="output shelve database")
    # construct the argument parse and parse the arguments
    search_parser = subparsers.add_parser('search')
    search_parser.add_argument("-s", "--shelve",
                               required=True,
                               help="output shelve database")
    search_parser.add_argument("-q", "--query",
                               required=True,
                               help="path to the query image")
    search_parser.add_argument('--hash-name',
                               type=str, default='grayscale',
                               choices=('color', 'grayscale'),
                               help='set hash function to use for fingerprints')
    # construct the argument parse and parse the arguments
    super_search_parser = subparsers.add_parser('supersearch')
    super_search_parser.add_argument("-s", "--shelve",
                                     required=True,
                                     help="output shelve database")
    super_search_parser.add_argument("-q", "--query",
                                     required=True,
                                     help="path to the query image")
    super_search_parser.add_argument('-t', '--threshold',
                                     type=int, default=12,
                                     help='minimum match threshold')
    super_search_parser.add_argument('--hash-name',
                                     type=str, default='color',
                                     choices=('color', 'grayscale'),
                                     help='set hash function to use for fingerprints')

    # construct the argument parse and parse the arguments
    gather_parser = subparsers.add_parser('gather')
    gather_parser.add_argument("-i", "--input",
                               required=True,
                               help="input directory of images")
    gather_parser.add_argument("-o", "--output",
                               required=True,
                               help="output directory")
    gather_parser.add_argument("-c", "--csv",
                               required=True,
                               help="path to CSV file for image counts")

    args = vars(parser.parse_args())

    if args['subparser_name'] == 'index':
        index(args)
    elif args['subparser_name'] == 'search':
        search(args)
    elif args['subparser_name'] == 'supersearch':
        supersearch(args)
    elif args['subparser_name'] == 'gather':
        gather(args)

if __name__ == '__main__':
    main()
