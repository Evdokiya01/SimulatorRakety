# -*- coding: utf-8 -*-

"""
Created on 2013-02-23
:author: Andreas Kaiser (disko)
"""

from fanstatic import Library
from fanstatic import Resource


library = Library(
    'javascript_load_image',
    'resources'
    )
load_image = Resource(
    library,
    'load-image.js',
    minified='load-image.min.js'
    )
