import re # Regualar expressions
import gi # Gtk

gi.require_version("Gtk", "3.0") 
from gi.repository import Gtk

class Control:
    """Control class for business logic."""
    
    def __init__(self, ratio=0.5):
        self.ratio = ratio
        self.control_window = None

    def update_numbers_in_string(self, input_string):

        # Convert special characters to their actual numbers (So that they can be multiplied)
        input_string = input_string.replace('¼', '0.25').replace('½', '0.5').replace('¾', '0.75')

        # Split into lines to be able to keep format in the end
        output_lines = []
        input_lines = input_string.split("\n")
        
        # Find all numbers
        for input_line in input_lines:
            numbers = re.findall(r'\d+\.\d+|\d+', input_line)

            # Make a new list of all the numbers multiplied by the selected ratio
            updated_numbers = []
            for num in numbers:
                if '.' in num:
                    updated_numbers.append(str(float(num) * self.ratio))
                else:
                    updated_numbers.append(str(int(num) * self.ratio))

            # Split the input_line into words
            words = input_line.split()

            output_words = []
            for word in words:
                # Check if the word contains any digits
                if any(char.isdigit() for char in word):
                    # Loop over each updated number to replace the original number with the updated one
                    for i in range(len(numbers)):
                        # Replace the original number with the updated number of the same index
                        if numbers[i] in word:
                            # Fix unwanted decimals, for example 150.0 g
                            if '.' in updated_numbers[i]:
                                updated_numbers[i] = updated_numbers[i].rstrip('0').rstrip('.')
                            word = word.replace(numbers[i], updated_numbers[i])
                            break

                # Stiching everying up again!
                output_words.append(word)

            output_lines.append(" ".join(output_words))

        output_string = "\n".join(output_lines)

        return output_string

class ControlWindow:
    """ControlWindow class for GUI logic."""

    def __init__(self, control):
        self.control = control
        self.control.control_window = self
        self.builder = Gtk.Builder()
        self.builder.add_from_file("scale.ui")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("window")
        self.window.set_title("Scale your recipes")
        self.window.show_all()
        self.window.connect("destroy", Gtk.main_quit)

    """ Buttons things """
    def on_close_clicked(self, clicked):
        Gtk.main_quit()

    def on_apply_clicked(self, clicked):
        # Define and get text from input_box
        input_buffer = self.builder.get_object("input_box").get_buffer()
        input_string = input_buffer.get_text(input_buffer.get_start_iter(), input_buffer.get_end_iter(), True)

        # Call the method to convert the input string
        output_string = self.control.update_numbers_in_string(input_string)

        # Define the output_box and set the text with the output_string
        output_buffer = self.builder.get_object("output_box").get_buffer()
        output_buffer.set_text(output_string)

    """ Radio buttons """
    def on_radio1_toggled(self, toggled):
        self.control.ratio = 0.5

    def on_radio2_toggled(self, toggled):
        self.control.ratio = 0.75

    def on_radio3_toggled(self, toggled):
        self.control.ratio = 1

    def on_radio4_toggled(self, toggled):
        self.control.ratio = 1.25

    def on_radio5_toggled(self, toggled):
        self.control.ratio = 1.5

    def on_radio6_toggled(self, toggled):
        self.control.ratio = 1.75

    def on_radio7_toggled(self, toggled):
        self.control.ratio = 2

if __name__ == "__main__":
    control = Control()
    ControlWindow(control)
    Gtk.main()

