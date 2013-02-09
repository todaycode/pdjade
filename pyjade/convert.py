import logging
import codecs
from optparse import OptionParser
from pyjade.utils import process
import os

def convert_file():
    support_compilers_list = ['django', 'jinja', 'underscore', 'mako', 'tornado']
    available_compilers = {}
    for i in support_compilers_list:
        try:
            compiler_class = __import__('pyjade.ext.%s' % i, fromlist=['pyjade']).Compiler
        except ImportError, e:
            logging.warning(e)
        else:
            available_compilers[i] = compiler_class

    usage = "usage: %prog [options] file [output]"
    parser = OptionParser(usage)
    parser.add_option("-o", "--output", dest="output",
                    help="Write output to FILE", metavar="FILE")
    parser.add_option("-c", "--compiler", dest="compiler",
                    choices=available_compilers.keys(),
                    default=available_compilers.keys()[0],
                    type="choice",
                    help="COMPILER must be one of %s, default is django" % ','.join(available_compilers.keys()))
    parser.add_option("-e", "--ext", dest="extension",
                    help="Set import/extends default file extension", metavar="FILE")

    options, args = parser.parse_args()
    if len(args) < 1:
        print "Specify the input file as the first argument."
        exit()
    file_output = options.output or (args[1] if len(args) > 1 else None)
    compiler = options.compiler

    if options.extension:
        extension = '.%s'%options.extension
    elif options.output:
        extension = os.path.splitext(options.output)[1]
    else:
        extension = None

    if compiler in available_compilers:
        template = codecs.open(args[0], 'r', encoding='utf-8').read()
        output = process(template, compiler=available_compilers[compiler], staticAttrs=True, extension=extension)
        if file_output:
            outfile = codecs.open(file_output, 'w', encoding='utf-8')
            outfile.write(output)
        else:
            print output
    else:
        raise Exception('You must have %s installed!' % compiler)

if __name__ == '__main__':
    convert_file()
