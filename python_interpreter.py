# Takes input form the command line and initiates the controller 
# passing command line input to the controller which then uses
# the information to initiate the model which parses the require file/files

import sys
import python_controller as pc


def initiate_python_parser(command_line_args):
    controller = pc.Controller(command_line_args)
    controller.run_parser(command_line_args)


if __name__ == '__main__' :
    # USAGE: python_parser.py <"filename or * for all">.py
    #import doctest
    #doctest.testmod()

    #parser = argparse.ArgumentParser()

   # parser.add_argument("-f", "--file", nargs='+', help="Multiple file input for parse", required=True)

    #args = parser.parse_args()

    #if len(args.file) > 0:
    #    initiate_python_parser(args.file)

    import doctest
    doctest.testmod()

    if len(sys.argv) == 1:
        print("USAGE: " + sys.argv[0] + " <pythonfiles>")
    else:
        initiate_python_parser(sys.argv[1:])