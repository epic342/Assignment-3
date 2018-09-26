import argparse
from cmd import Cmd

from src import controller
from src.database.statistics_creator import StatisticsCreator


class Controller(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        # Command line argument variables
        self.files = None
        self.statistics = None
        self.extracted_modules = None
        self.output = None
        self.args = self.register_arguments()
        self.parse_arguments()
        self.controller = controller.DataController(self)
        self.prompt = '> '

    def run_console(self):
        self.cmdloop('Starting prompt...\n'
                     'Type "help" for commands')

    def create_statistics(self, args):
        self.statistics = StatisticsCreator("statistics")
        self.statistics.create_tables()
        print("Now collecting statistics")

    def set_input_file_argument(self, files):
        self.files = files
        if not self.files:
            print("No input file selected.")
        else:
            print("Input file selected:")
            print(*self.files, sep="\n")

    def register_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-f",
            "--file",
            nargs="+",
            help="Multiple file input for parse")
        parser.add_argument(
            "-s",
            "--statistics",
            action='store_true',
            help="Print Statistics for classes uploaded")
        parser.add_argument(
            "-o",
            "--output",
            help="Setting name of the output location")
        return parser.parse_args()

    def parse_arguments(self):
        if self.args.statistics:
            self.create_statistics("statistics")

        if self.args.file is not None:
            self.set_input_file_argument(self.args.file)

        if self.args.output is not None:
            self.output = self.args.output
            print("Now setting names of output files")

    def do_change_python_files(self, args):
        """
        Change input files that are to be parsed by system
        Author: Braeden
        Syntax: change_python_files <filenames.py>
        """
        if self.controller.change_python_files(args):
            print("{}: {}".format("Success", "files have been set"))
        else:
            print("{}: {}".format("Error", "change_python_files <filenames.py>"))

    def do_enable_statistics(self, args):
        """
        Enabled statistics collection
        Author: Jake Reddock
        Syntax: enable_statistics
        """
        if self.controller.enable_statistics(args):
            print("{}: {}".format("Success", "Statistics collecting is turned on."))
        else:
            print("{}: {}".format("Error.", "Statistics collecting was not turned on."))

    def do_show_statistics(self, args):
        """
        Show statistics about the analysed classes
        Author: Jake Reddock
        Syntax: show_statistics
        Requires: enable_statistics, output_to_dot
        """
        if self.controller.show_statistics(args):
            print("Now showing statistics.")
            print("Creating graph, please wait...")
        else:
            print("Failed to show statistics.")

    def do_set_input_file(self, args):
        """
        Sets the input file that will be converted into a UML diagram.
        Author: Jake Reddock
        Syntax: set_input_file [file_name]
        """
        if self.controller.set_input_file(args) is not None:
            print("{}: {}".format("Success", "You have set the input file."))
        else:
            print("{}: {}".format("Error", "Failed to set an input file."))

    def do_output_to_dot(self, args):
        if self.controller.output_to_dot(args):
            print("{}: {}".format("Success", "You have outputted the file in dot format."))
        else:
            print("{}: {}".format("Error", "Failed to output the file into dot format."))

    def do_output_to_file(self, args):
        """
        Sets the output of the class diagram to a file location.
        Author: Michael Huang
        Syntax: output_to_file
                output_to_file [path]
        """
        if self.controller.copy_file_to_folder(args):
            ("{}: {}".format("Success", "You have successfully copied the file to your desired location."))
        else:
            print("{}: {}".format("Error", "Failed to copy the file to your location."))

    def do_output_to_png(self, args):
        """
        Converts dot file into PNG
        Author: Braeden
        """
        if self.controller.output_to_png(args) is not None:
            print("{}: {}".format("Success", "You have successfully outputted the file in png format."))
        else:
            print("{}: {}".format("Error", "Failed to output the file into png format."))

    def do_quit(self, other):
        '''
        Quits programme.
        Author: Peter
        '''
        print("Goodbye ......")
        return True
