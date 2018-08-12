import model
import uml_output as uml_out
from cmd import Cmd
from subprocess import call
import os

class Controller(Cmd):

    def __init__(self, args):
        Cmd.__init__(self)
        self.args = args
        self.prompt = '> '
        self.cmdloop('Starting prompt...\n'
                     'Type "help" for commands')

    def do_change_python_files(self, args):
        """
        Change input files to be parsed by system
        Syntax: change_python_files <filename or * for all>.py
        """
        self.args = args.split()

    def do_output_to_dot(self, args):
        """
        Parse and output the file into a UML diagram
        Syntax: output_to_dot [-a|-m]
        [-a] Hides all attributes on class diagram
        [-m] Hides all methods on class diagram
        """
        user_options = args.split()

        hide_attributes = False
        hide_methods = False

        if len(user_options) > 0:
            if "-a" in user_options:
                hide_attributes = True
            if "-m" in user_options:
                hide_methods = True

        self.run_parser(self.args, hide_attributes, hide_methods)

    def do_output_to_png(self, args):
        """
        Converts dot file into PNG
        """
        call(['dot', '-Tpng', 'tmp/class.dot', '-o', 'tmp/class.png'])

    @staticmethod
    def run_parser(file_names, hide_attributes, hide_methods):
        # Initiate processor
        processor = model.FileProcessor()
        processor.process_files(file_names)

        extracted_modules = processor.get_modules()

        new_uml = uml_out.MakeUML(hide_attributes, hide_methods)
        return new_uml.create_class_diagram(extracted_modules)

