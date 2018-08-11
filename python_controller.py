import model
import uml_output as uml_out
from cmd import Cmd
from subprocess import call


class Controller(Cmd):

    def __init__(self, args):
        Cmd.__init__(self)
        self.args = args
        self.prompt = '> '
        self.cmdloop('Starting prompt...')

    def do_output_to_dot(self, args):
        """Parse and output the file into a UML diagram"""
        self.run_parser(self.args)

    def do_output_to_png(self, args):
        """Convert dot file into PNG"""
        call(['dot', '-Tpng', 'tmp/class.dot', '-o', 'tmp/class.png'])

    # Created and edited by Michael Huang, #2, #14
    def do_output_to_file(self, args):
        """
        Sets the output of the class diagram to a file location.
        Syntax: output_to_file
                output_to_file [path]


        """

        from shutil import copyfile
        if len(args) == 0:
            from tkinter import Tk
            from tkinter import filedialog

            root = Tk()
            root.filename = filedialog.askdirectory()
            print(root.filename)
            root.withdraw()

            copyfile('tmp/class.png', root.filename + '/class.png')
        else:
            copyfile('tmp/class.png', args + '/class.png')
            print('The output to the file destination was successful.')
        
    @staticmethod
    def run_parser(file_names):
        # Initiate processor
        processor = model.FileProcessor()
        processor.process_files(file_names)

        extracted_modules = processor.get_modules()

        new_uml = uml_out.MakeUML()
        return new_uml.create_class_diagram(extracted_modules)

