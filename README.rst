Image Caption
=============

Place semi-transparent image caption on top of a source image and save as
JPEG.


Installation
------------

Install for developers:

    $ mkvirtualenv --python python3 image-caption
    $ setvirtualenvproject
    $ pip install -r requirements.txt
    $ python setup.py develop


Invocation
----------

Effortlessly add your caption to images like this:

    $ caption --index-file test.tif --font-file lucon.ttf --caption-text "Hello World"

You will need to dig up a font file in order to do this.
