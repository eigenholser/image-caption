from __future__ import print_function
import argparse
import logging
import os
from PIL import (Image, ImageDraw, ImageFont, ImageEnhance)
import sys


logger = logging.getLogger(__name__)


def caption(index_filename, caption_font_filename, caption_text):
    """
    Read the source file. Create a caption with semi-transparent backcground
    for contrast. Paste the caption over the source image. Flatten and save.
    This offers the illusion of transparency in the RGB image that does not
    support transparency.
    """
    # Want just the base portion of the filename without extension. Will also
    # be used to name the target file.
    index_filename_base = os.path.splitext(os.path.basename(index_filename))[0]
    if not caption_text:
        caption_text = index_filename_base
    target_basename = "{}.jpg".format(index_filename_base)
    index_dirname = os.path.dirname(index_filename)
    target_filename = os.path.join(index_dirname, target_basename)

    # Initialize some symbolic color names.
    black = (0, 0, 0)
    white = (255, 255, 255)
    transparent = (0, 0, 0, 0)

    # Create an RGBA image object from the source file.
    index_img = Image.open(index_filename).convert('RGBA')
    width, height = index_img.size

    # Caption height is 5% of total image height.
    caption_bg_color = (0, 0, 0, 100)   # Semi-transparent caption background
    caption_bg_height = int(height / 20)
    caption_font_size = int(caption_bg_height * 0.5)
    caption_font = ImageFont.truetype(
            caption_font_filename, caption_font_size)

    # New RGBA image object for the caption.
    wm = Image.new('RGBA',(width, caption_bg_height), caption_bg_color)
    draw = ImageDraw.Draw(wm)
    caption_color = "white"
    caption_width, caption_height = draw.textsize(caption_text, caption_font)
    draw.text(((width-caption_width)/2, (caption_bg_height-caption_height)/2),
            caption_text, caption_color, caption_font)

    # Paste the caption on the lower end of the source image object.
    en = ImageEnhance.Brightness(wm)
    opacity=0.50    # TODO: Clumsy
    mask = en.enhance(1-opacity)
    index_img.paste(wm, (0, height-caption_bg_height), mask)

    # Flatten alpha channel and save.
    index_img.convert("RGB").save(target_filename)


class FormArgumentParser(argparse.ArgumentParser):
    """
    Custom argparser.
    """
    def error(self, message):
        sys.stderr.write('error: {}\n'.format(message))
        self.print_help()
        sys.exit(2)


    def usage_message(self):
        """
        Print a message and exit.
        """
        sys.stderr.write("error: Missing required arguments.\n")
        self.print_help()
        sys.exit(3)


def main():
    """
    Parse command-line arguments. Process form.
    """
    parser = FormArgumentParser()
    parser.add_argument("-i", "--index-file",
            help="Index file to which the caption will be applied.")
    parser.add_argument("-f", "--caption-font-file",
            help="Font to use in caption.")
    parser.add_argument("-c", "--caption-text",
            help="Caption text to use on index image.")
    parser.add_argument("-v", "--verbose", help="Log level to DEBUG.",
            action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    error = False
    index_file = args.index_file
    caption_font_filename = args.caption_font_file
    caption_text = args.caption_text

    if not index_file:
        logger.error("Index file is required.")
        error = True
    elif not os.path.exists(index_file):
        logger.error("Index file {} does not exist!".format(index_file))
        error = True

    if not caption_font_filename:
        logger.error("Caption font is required.")
        error = True
    elif not os.path.exists(caption_font_filename):
        logger.error(
                "Caption font {} does not exist!".format(caption_font_file))
        error = True

    if error:
        logger.error("Exiting due to errors.")
        parser.usage_message()
        sys.exit(1)

    caption(index_file, caption_font_filename, caption_text)


if __name__ == "__main__": # pragma: no cover
    main()
