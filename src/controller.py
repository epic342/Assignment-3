import os
from shutil import copyfile
from subprocess import call
from tkinter import filedialog, Tk

import src.strategy.bar_graph as bardisplay
import src.strategy.graph_strategy as strategy
import src.strategy.horizontal_bar as hdisplay
import src.strategy.stacked_bar as stackdisplay
from src import model, uml_output as uml_out
from src.output import csv_plugin as csv
from src.pickle_modules import PickleModules


class DataController:
    def __init__(self, controller):
        self.controller = controller

    def enable_statistics(self, args):
        self.controller.create_statistics(args)
        return True

    def show_statistics(self, args):
        if self.controller.statistics is not None:
            if self.controller.extracted_modules is not None:
                strategy.GraphManager(bardisplay.BarGraphCreator('tester')).make_graph(self.controller.statistics)
                return True
            else:
                print("Please run the \"output_to_dot\" to command")
                return False
        else:
            print(
                "Statistics collecting is not enabled, "
                "type \"enable_statistics\" to enable")
            return False

    def show_stacked_statistics(self, args):
        if self.controller.statistics is not None:
            if self.controller.extracted_modules is not None:
                strategy.GraphManager(stackdisplay.StackedGraphCreator('tester')).make_graph(self.controller.statistics)
                return True
            else:
                print("Please run the \"output_to_dot\" to command")
                return False
        else:
            print(
                "Statistics collecting is not enabled, "
                "type \"enable_statistics\" to enable")
            return False

    def show_horizontal_statistics(self, args):
        if self.controller.statistics is not None:
            if self.controller.extracted_modules is not None:
                strategy.GraphManager(hdisplay.HorizontalGraphCreator('tester')).make_graph(self.controller.statistics)
                return True
            else:
                print("Please run the \"output_to_dot\" to command")
                return False
        else:
            print(
                "Statistics collecting is not enabled, "
                "type \"enable_statistics\" to enable")
            return False

    def change_python_files(self, args):
        user_args = args.split()
        if len(user_args) > 0:
            self.controller.files = [args]
            return True

        return False

    def output_to_dot(self, args):

        user_options = args.split()

        hide_attributes = False
        hide_methods = False

        if len(user_options) > 0:
            if "-a" in user_options:
                hide_attributes = True
            if "-m" in user_options:
                hide_methods = True

        self.run_parser(self, hide_attributes, hide_methods)
        return True

    def set_input_file(self, args):
        if len(args) == 0:
            root = Tk()
            self.controller.files = filedialog.askopenfilenames(
                initialdir="C:/",
                title="Select Input File",
                filetypes=(
                    ("Python Files",
                     "*.py"),
                    ("all files",
                     "*.*")))
            root.withdraw()
            return True
        else:
            self.controller.set_input_file_argument([args])
            return True

    def copy_file_to_folder(self, args):
        if len(args) == 0:

            root = Tk()
            root.filename = filedialog.askdirectory()
            print(root.filename)
            root.withdraw()

            copyfile('../tmp/class.png', root.filename + '/class.png')
            return True
        else:
            try:
                copyfile('../tmp/class.png', args + '/class.png')
                print('The output to the file destination was successful.')
                return True
            except FileNotFoundError as f:
                print("{}: {}".format(f, 'Failed to find a file path.'))
                print('Please specify a valid file path.')
                return False
            except:
                print('Unexpected error has occurred.')
                return False

    @staticmethod
    def output_to_png(args):
        # TODO Not working with ARA computers
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
        return call(['dot', '-Tpng', 'tmp/class.dot', '-o', 'tmp/class.png'])

    @staticmethod
    def run_parser(self, hide_attributes, hide_methods):
        if len(self.controller.files) > 0:
            processor = model.FileProcessor(self.controller.statistics)
            processor.process_files(self.controller.files)

            self.controller.extracted_modules = processor.get_modules()

            new_uml = uml_out.MakeUML(hide_attributes, hide_methods)
            return new_uml.create_class_diagram(self.controller.extracted_modules)
        else:
            print("Error: No files were set, use command change_python_files")

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
            if csv_writer.write_csv_file(modules, output_file):
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
            if makediagram.create_class_diagram(module):
                print(
                    "{} successfully converted to UML class diagram".format(input_file))

    def do_pickle_modules(self, filename='plants.py'):
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
        pickler = PickleModules()
        return pickler.save(modules)

    def load_pickle(self):
        '''
        Loads previously saved module using pickle
        Author: Peter

        Command:
        load_pickle
        '''
        pickler = PickleModules()
        return pickler.load()
