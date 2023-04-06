# Population Protocol Visualiser
This software is used to visualise population protocols.

# Requirements
This project requires `python >= 3.0`. The recommended version is 3.9.13.

# Installation
Download the package as a zip file and extract all project files to a folder.

The required external libraries can be downloaded with:

`python -m pip install -r requirements.txt`

# Usage

## Using the Graphical User Interface (GUI)

To run the GUI, navigate to the directory of the software in your terminal and run the following command

`python main.py`

Alternatively you can run the GUI by opening the `main.py` file

To create a new network, navigate to `File -> Create protocol..`. This will open a dialog where you can specify the parameters of the network. When a network has been created, the controls on the right of the interface can be used to control the simulation.

## Using the Command-line Interface (CLI)

The CLI can be accessed through the terminal.

The CLI takes in a number of arguments in the following form:

`python main.py -arg1 val1 -arg2 val2 -flag1`

Arguments can be provided with values as shown above. The above command would set the argument `arg1` to `val1`.

Flags are not provided with values, but work as switches that can be omitted/included. 

### Help
To view a list of all available arguments and flags, the help command may be used. This can be run with the following command:

`python main.py -h`

This displays detailed information on all arguments and their uses.
# License
This software is available under the MIT license.
