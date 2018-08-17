import model
import uml_output as uml_out
import python_code_validator as validate
import csv_plugin as csv
import pickle_modules
from cmd import Cmd
from subprocess import call



class Controller(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.args = self.register_arguments()
        self.parse_arguments()
        self.prompt = '> '
        # Command line argument variables
        self.files = None
        self.statistics = False
        self.output = None

        self.cmdloop('Starting prompt...\n'
                     'Type "help" for commands')

    #Created by Jake
    def register_arguments(self):
        #Create your commands in here
        parser = argparse.ArgumentParser()
        #Created by Braeden
        parser.add_argument("-f", "--file", nargs="+", help="Multiple file input for parse")
        # Created By Jake Reddock
        parser.add_argument("-s", "--statistics", action='store_true', help="Print Statistics for classes uploaded")
        # Created By Michael Huang
        parser.add_argument("-o", "--output", help="Shows name of the output file")
        return parser.parse_args()

    # Created By Jake Reddock
    def parse_arguments(self):
        #Create Logic for your arguments here
        #Created by Jake
        if self.args.statistics:
            self.statistics = self.args.statistics
            print("Statistics collecting is turned on")
        #Created by Braeden
        if self.args.file is not None:
            self.files = self.args.file
            print("Files selected: ")
            print(*self.files, sep="\n")
        # Created by Michael Huang
        if self.args.output is not None:
            self.output = self.args.output
            print("Now showing names of output files")    

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
        files = []
        if type(args) == str:
            files.append(args)
        elif type(args) == list:
            files = args
        
        check_code = validate.CodeValidator()
        validated_file = check_code.validate_files(files)
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
        Author: Peter
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

    def do_pickle_modules(self, filename = 'plants.py'):
        '''
        Load modules from single file and save them using pickle
        Author: Peter

        Command:
        pickle_modules filename
        eg pickle_modules plants.py
        '''
        file = [filename]
        parser = model.FileProcessor()
        parser.process_files(file)
        modules = parser.get_modules()
        pickler = pickle_modules.PickleModules()
        return pickler.save(modules)

    def load_pickle(self):
        '''
        Loads previously saved module using pickle
        Author: Peter
        
        Command:
        load_pickle
        '''
        pickler = pickle_modules.PickleModules()
        return pickler.load()

    def do_quit(self, other):
        '''
        Quits programme.
        Author: Peter
        '''
        print("Goodbye ......")
        return True
