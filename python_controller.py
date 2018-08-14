import model
import uml_output as uml_out
import python_code_validator as validate
import csv_plugin as csv
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
        
    def do_set_input_file(self, args):
        """
        Sets the input file that will be converted into a UML diagram.
        Author: Jake Reddock
        Syntax: set_input_file [file_name]
        """
        if len(args) == 0:
            root = Tk()
            root.filename = filedialog.askopenfilename(initialdir="C:/", title="Select Input File",
                                                       filetypes=(("Python Files", "*.py"), ("all files", "*.*")))
            self.args = root.filename
            root.withdraw()
        else:
            self.args = args
        print("Input file selected \"" + self.args + "\"")
        

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

    def do_validate_py(self, args):
        '''
        Validates a single file as executable python code.
        Author: Peter
        '''
        check_code = validate.CodeValidator()
        validated_file = check_code.validate_files(args)

    def do_save_to_csv(self, params):
        '''
        Saves specified file to csv.
        [command_line] input_file output_file
        Author: Peter
        '''
        # print(params, type(params))
        input_file = []
        if params == '':
            params = 'plants.py output.csv'
        args = params.split(' ')
        # print(args)
        if len(args) >= 1:
            input_file.append(args[0])
            output_file = 'output.csv'
        if len(args) >= 2:
            output_file = args[1]
        if input_file[0].endswith('.py'):
            fileprocessor = model.FileProcessor()
            fileprocessor.process_files(input_file)
            modules = fileprocessor.get_modules()
            # print(modules)
            csv_writer = csv.CSV_handler() 
            if csv_writer.write_csv_file(modules, output_file) == True:
                print('File successfully saved as {}'.format(output_file))

    def do_load_csv_for_uml(self, params):
        '''
        Loads csv file and creates UML diagram
        [command line] [file.csv]
        '''
        if params == '':
            params = 'output.csv'
        args = params.split(' ')
        print(args)
        if len(args) >= 1:
            input_file = args[0]
        if input_file.endswith('.csv'):
            csvloader = csv.CSV_handler()
            module = csvloader.open_file(input_file)
            makediagram = uml_out.MakeUML(True, True)
            if makediagram.create_class_diagram(module) == True:
                print("{} successfully converted to UML class diagram".format(input_file))

        

    def do_quit(self, other):
        '''
        Quits programme.
        Author: Peter
        '''
        print("Goodbye ......")
        return True