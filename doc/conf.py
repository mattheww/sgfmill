import sgfmill

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]
templates_path = ['_templates']
source_suffix = '.rst'
source_encoding = 'utf-8'
master_doc = 'index'
project = u'Sgfmill'
copyright = u'2009-2018, Matthew Woodcraft and the sgfmill contributors'
version = sgfmill.__version__
release = sgfmill.__version__
exclude_patterns = ['_build']
pygments_style = 'vs'
modindex_common_prefix = ['sgfmill.']

html_theme = 'default'
html_theme_options = {
    'nosidebar'     : False,
    #'rightsidebar'  : True,
    'stickysidebar' : False,

    'footerbgcolor'    : '#3d3011',
    #'footertextcolor'  : ,
    'sidebarbgcolor'   : '#3d3011',
    #'sidebartextcolor' : ,
    'sidebarlinkcolor' : '#d8d898',
    'relbarbgcolor'    : '#523f13',
    #'relbartextcolor'  : ,
    #'relbarlinkcolor'  : ,
    #'bgcolor'          : ,
    #'textcolor'        : ,
    'linkcolor'        : '#7c5f35',
    'visitedlinkcolor' : '#7c5f35',
    #'headbgcolor'      : ,
    'headtextcolor'    : '#5c4320',
    #'headlinkcolor'    : ,
    #'codebgcolor'      : ,
    #'codetextcolor'    : ,

    'externalrefs'     : True,
    }

html_static_path = ['_static']
html_sidebars = { '**':[
    'wholetoc.html',
    'searchbox.html',
], }
html_style = "sgfmill.css"

intersphinx_mapping = {'python': ('http://docs.python.org/3',
                                  'python-inv.txt')}

rst_epilog = """
.. |gtp| replace:: :abbr:`GTP (Go Text Protocol)`
.. |sgf| replace:: :abbr:`SGF (Smart Game Format)`
"""

def setup(app):
    app.add_object_type('script', 'script',
                        indextemplate='pair: %s; example script',
                        objname="Example script")

