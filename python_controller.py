import model
import uml_output as uml_out
from cmd import Cmd
from subprocess import call


class Controller(Cmd):

    def __init__(self, args):
        Cmd.__init__(self)
        self.args = args
        self.prompt = '> '
        self.cmdloop('Starting prompt...\n'
                     'Type "help" for commands')

    def do_change_python_files(self, args):
        """
        Change input files that are to be parsed by system
        Author: Braeden
        Syntax: change_python_files <filenames.py>
        """
        user_args = args.split()
        if len(user_args) > 0:
            self.args = args.split()
        else:
            print("Syntax Error: change_python_files <filenames.py>")

    def do_output_to_dot(self, args):
        """
        Parse and output the file into a UML diagram
        Author: Braeden
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
    def do_output_to_png(args):
        """
        Converts dot file into PNG
        Author: Braeden
        """
        return call(['dot', '-Tpng', 'tmp/class.dot', '-o', 'tmp/class.png'])

    @staticmethod
    def run_parser(file_names, hide_attributes, hide_methods):
        if len(file_names) > 0:
            # Initiate processor
            processor = model.FileProcessor()
            processor.process_files(file_names)

            extracted_modules = processor.get_modules()

            new_uml = uml_out.MakeUML(hide_attributes, hide_methods)
            return new_uml.create_class_diagram(extracted_modules)
        else:
            print("Error: No files were set, use command change_python_files")
