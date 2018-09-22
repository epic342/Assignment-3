# Takes input form the command line and initiates the controller
# passing command line input to the controller which then uses
# the information to initiate the model which parses the require file/files
from src import command_interpreter as pc

def initiate_python_parser():
    interpreter = pc.CommandLine()
    interpreter.run_console()

    # controller.run_parser(command_line_args, True, True)


if __name__ == '__main__':
    initiate_python_parser()
    import doctest

    doctest.testmod()
