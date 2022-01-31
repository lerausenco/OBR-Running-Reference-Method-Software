#    "OBR_analyzer_move_vertical_cursor" (v1.0)
#	 This programme is based on OBR_analyzer_simple written by Soren Heinze in 2016.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


# A small program to automatically press the correct buttons that a proprietary
# OBR-measurement/analyzing program analyzes the OBR rawdata.
# The files will also be saved automatically, assuming that CTRL + S
# is the shortcut to open the "save-file" dialogue of OBR-measurement program.
# For each analyzes the reference file will be changed.
#
# It assumes that a "Load Reference File ..." option can be found 70 pixels
# below the "File" button in the menu bar.
# This is the case for a certain version of the proprietary
# OBR-measurement/analyzing program (stated in the accompanying manual to this
# program) for which the OBR_analyzer_simple program was tested for.
#

from time import sleep

from pykeyboard import PyKeyboard
from pymouse import PyMouse

# Instantiate a mouse and a keyboard.
# A PyMouse() and a PyKeyboard() have certain methods that allow
# easy access to typical features of such peripherals like moving the
# pointer to a certain position or pressing keyboard buttons.
mouse = PyMouse()
keyboard = PyKeyboard()

# Just reminding the user of sth. very important.
print '''\n\n
ATTENTION:
DON'T MOVE THE WINDOW OF THE OBR-PROGRAM, AFTER THE POSITION OF THE <FILE> BUTTON
WAS DETERMINED!

See the instructions that accompany this program, how to use it.\n
'''

# Don't do more analyses than the number stated here.
#
# Users tend to make mistakes. E.g. pressing too fast ENTER before
# actually entering a number.
# I catch the most common mistakes by using the while-loop, the try-except
# statement and by trying to convert to a number at once.
correct_input = False
# Continue until the input given by the user is a number.
while not correct_input:
    # Try to do sth. specific ...
    try:
        # Get the input from the user. If raw_input() contains a string
        # between the brackets, this string will be printed on the
        # shell to give the user some more information.
        input_from_user = raw_input('Highest measurement file number: ')
        # raw_input() returns a string. But a number is required. Hence I
        # convert the string to a number.
        #
        # These two statements are summed up into one line in the while-loops
        # below.
        highest_number = int(input_from_user)
        # If everything is correct, set correct_input to True, which means
        # that the while-loop will NOT start again.
        correct_input = True
    # ... unless the user gives wrong input. ...
    except ValueError:
        # ... If this is the case just ignore it and start the loop
        # again.
        pass

# Reset correct_input for the next user-input.
correct_input = False

# An analysis of many files may take a lot of time.
# To allow the user to abort this process anywhere and continue from this point
# I ask for the file which shall be analyzed first.
while not correct_input:
    try:
        message_1 = 'Number of first file to be analyzed (must be > 1): '
        start_here = int(raw_input(message_1))
        if start_here > 1:
            correct_input = True
    except ValueError:
        pass

correct_input = False

# The time one analysis takes
while not correct_input:
    try:
        analysis_time = int(raw_input('Time for ONE analysis in full SECONDS: '))
        correct_input = True
    except ValueError:
        pass

# An analysis sometimes needs more time then anticipated.
# Here I try to compensate a bit for such cases.
analysis_time += 10
correct_input = False

# The time it takes to save the files.
while not correct_input:
    try:
        save_time = int(raw_input('Time it takes to SAVE in full SECONDS: '))
        correct_input = True
    except ValueError:
        pass
save_time += 5

# The base-filename. e.g. 2017-05-23_Sample_E23_"
# The name will be "filled up" by the measurement-number in the
# analysis-loop below.
message_2 = '"Base" for filenames WITHOUT the numbers at the end (e.g. "Sample_01_"): '
base_filename = raw_input(message_2)

vertical_cursor_pos_msg = 'Enter where to position cursor for first iteration in m: e.g. 15.900 '
vertical_cursor_pos = float(raw_input(vertical_cursor_pos_msg))

# A visual separator to make the use of this program easier for the user.
print "\n\n<<<<<<<< Basic user input complete >>>>>>>>"

# Instructions for the user what to do, so that the program can determine the
# position of the <FILE> Button
print """\n
Move the mouse pointer over the <FILE> Button in the MENU BAR of the OBR program.

DON'T click the mouse! 
The console must remain the active window!

Once this is done, press ENTER (the position of the <FILE> Button will
be detected).

DON'T MOVE THE WINDOW OF THE OBR-PROGRAM AFTERWARDS!\n
"""

# Using raw_input() I make sure that the program will halt here and wait
# for ENTER.
raw_input('Press ENTER when the mouse is over the <FILE> Button.')

print "\n\n<<<<<<<< <FILE> Button position determined >>>>>>>>"

# Here the position of the mouse pointer is determined.
# .position() returns a tuple that contains the x- and y-coordinates
# of the pointer at the time this method is called.
file_button_position = mouse.position()
# file_button_position[0] / file_button_position[1] retrieves the first / second
# entry of the tuple that contains the x- and y-coordinates of the
# <FILE> Button
load_reference_button_position = (file_button_position[0], (file_button_position[1] + 70))

# Do the same for the X1 vertical cursor position.
raw_input('Press ENTER when mouse is over X1 value')
X1_value_screen_pos = mouse.position()
print "\n\n<<<<<<<< X1 field position determined >>>>>>>>"

# Some more information for the user.
print """\n
ATTENTION: DON'T MOVE THE WINDOW OF THE OBR-PROGRAM

After pressing ENTER again the OBR window will become active and the 
automatic analysis will start.
DON'T make this console the active window after pressing ENTER.
It will work even if you can't see this console.\n
"""

# Wait here for the user to start the automatic measurements.
raw_input('Press ENTER now to start the automatic measurements. >>>')

# Give the user a summary of the input information.
print "\n-----------------------\n"
print "ATTENTION: DON'T MOVE THE WINDOW OF THE OBR-PROGRAM!\n"
print "Automated Measurements have started.\n"
print "Highest file number: %s" % highest_number
print "Starting with measurement: %s" % start_here
print "Time for ONE analysis: %s seconds" % (analysis_time - 10)
print "Time it takes to SAVE: %s seconds" % (save_time - 5)
print "Base-filename: %s" % base_filename
print "\n-----------------------\n"

## ## ## ## ## Here the analysis-loop starts ## ## ## ## ##
# This counter counts presents the number of the file to be analyzed.
# counter = start_here - 1

for counter in range(start_here, highest_number + 1):

    # First of all I need to make the OBR measurement/analyze program
    # the active window. I do this by simply clicking it at a position the
    # does not contain anything.
    mouse.click(load_reference_button_position[0], load_reference_button_position[1])

    # The numbering of the files should be with four leading zeros but counter
    # is just a regular number.
    # .zfill() puts leading zeros in front of a number. However, .zfill() can
    # be used just on a string. Thus I first convert the number to a string.
    load_file_number = str(counter).zfill(4)
    # Make the correct filename, by concatenating the base-filename and
    # the number for the measurement that is performed.
    load_file = base_filename + load_file_number

    # Load the new file to be analyzed.
    # .press_key() is a method of a PyKeyboard-instance that presses and holds
    # the given key and does NOT release it until release_key() is called.
    # keyboard.control_l_key selects the left CTRL-key
    keyboard.press_key(keyboard.control_l_key)
    # .tap_key() taps the given key.
    keyboard.tap_key('l')
    # Don't forget to release the pressed CTR-key.
    keyboard.release_key(keyboard.control_l_key)
    # I put in sleep() statements all over this loop to give the
    # analysis-PC some time to "settle" between commands.
    sleep(1)

    keyboard.tap_key(keyboard.return_key)
    sleep(1)
    keyboard.tap_key('y')
    sleep(2)

    keyboard.type_string(load_file)
    sleep(1)
    keyboard.tap_key(keyboard.return_key)
    sleep(2)

    vertical_cursor_increment = 5.0 / 1000

    for i in range(10):  # iterate though different cursor positions

        adj_vertical_cursor_pos = vertical_cursor_pos - vertical_cursor_increment * i

        # double click on X1 value to be able to change it
        mouse.click(X1_value_screen_pos[0], X1_value_screen_pos[1])
        mouse.click(X1_value_screen_pos[0], X1_value_screen_pos[1])

        # convert float input to string and write in
        adj_vertical_cursor_pos_string = str(adj_vertical_cursor_pos)
        adj_vertical_cursor_pos_string = adj_vertical_cursor_pos_string.replace(".", ",")

        keyboard.type_string(adj_vertical_cursor_pos_string)
        keyboard.tap_key(keyboard.enter_key)
        sleep(2)

        suffix = "pos_" + str(i)
        processed_file_name = load_file + "_" + suffix
        sleep(analysis_time)

        # Now save the file.
        keyboard.press_key(keyboard.control_l_key)
        keyboard.tap_key('s')
        keyboard.release_key(keyboard.control_l_key)
        sleep(1)

        keyboard.type_string(processed_file_name)
        sleep(1)
        keyboard.tap_key(keyboard.return_key)
        sleep(save_time)

    print "Analyzed %s" % load_file

    # To give the user some time to abort the program.
    sleep(5)
