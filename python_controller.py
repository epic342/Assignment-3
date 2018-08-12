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

    @staticmethod
    def run_parser(file_names):
        # Initiate processor
        processor = model.FileProcessor()
        processor.process_files(file_names)

        extracted_modules = processor.get_modules()

        new_uml = uml_out.MakeUML()
        return new_uml.create_class_diagram(extracted_modules)

