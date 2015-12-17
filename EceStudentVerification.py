__author__ = 'codylallen'
#########################################################################
#   ECE Student Verification System
#
#   Date last modified: December 17, 2015
#
#   - Imports ECE student PUIDs from file set by PUIDIMPORTFILE
#   - Imports previous student check-in's from transcript log
#       file set by LOGFILE
#   - Verifies that student is an ECE student by ID
#   - Tracks the number of check-in's of each student
#   - If check-in limit is active, verifies check-in's not exceeded
#
#   - Questions? Contact codylallen@gmail.com
#
#               -   -   -   -   -   -   -   -   -   -
#          !-- TO EXIT PROGRAM SAFELY, TYPE 'exit' WHEN --!
#          !--         PROMPTED 'Swipe PUID...'         --!
#               -   -   -   -   -   -   -   -   -   -
#########################################################################

#####################################################################
#
#   CONSTANTS
#
#####################################################################

#   Activate and set a limit on student check-ins
LIMITCHECKINS = True
CHECKINLIMIT = 2

#   File to import PUIDs from
PUIDIMPORTFILE = 'studentIDs.txt'

#   Log file used to backup user data
LOGFILE = 'logfile.txt'

#####################################################################
#
#   GLOBALS
#
#####################################################################
EceStudents = dict()

#####################################################################
#
#   STRING TO INT
#
#   Purpose:
#   Cleans a string containing PUID, strips off whitespace and
#       leading zeros.
#   Returns clean string as an int
#
#####################################################################
def stringToInt(PUIDstring):
    PUIDstring = PUIDstring.strip()
    if PUIDstring:
        PUIDint = int(PUIDstring)
    else:
        PUIDint = -1

    return PUIDint


#####################################################################
#
#   IMPORT ECE STUDENTS
#
#   Purpose:
#   Imports student IDs from file set by PUIDIMPORTFILE
#
#   Usage:
#   The file of IDs should have one ID per line
#   Number of leading zeros ('0') does not matter. They will be
#       removed upon import
#
#####################################################################
def importEceStudents():
    try:
        with open(PUIDIMPORTFILE, 'r') as myFile:
            for line in myFile.readlines():
                # Clean string
                currentStudentInt = stringToInt(line)
                # Add to data structure
                EceStudents[currentStudentInt] = 0
    except IOError:
        print("\nERROR: Could not find PUID file " + PUIDIMPORTFILE)
        print("         Please ensure file is in the proper directory and")
        print("         is named correctly")
        exit(1)

#####################################################################
#
#   IMPORT PREVIOUS CHECK-INS
#
#   Purpose:
#   Imports previous check-in's from file set by LOGFILE
#
#   Usage:
#   The file of IDs should have one ID per line per check-in
#       recorded.
#
#####################################################################
def importPreviousCheckIns():
    try:
        with open(LOGFILE, 'r') as myFile:
            for line in myFile.readlines():
                PUIDint = stringToInt(line)
                if PUIDint in EceStudents.keys():
                    EceStudents[PUIDint] += 1
                else:
                    if PUIDint > 0:
                        print("WARNING: Imported student with unrecognized ID")
    except IOError:
        pass

#####################################################################
#
#   INITIALIZE
#
#   Purpose:
#   Initialize student data structure with IDs from file and update
#   previous visits from log
#
#####################################################################

def initialize():
    print('Populating ECE student data from ' + PUIDIMPORTFILE + ' ...')
    importEceStudents()

    print('Populating student visit history from ' + LOGFILE + ' ...')
    importPreviousCheckIns()

    print('System ready . . .')

#####################################################################
#
#   RECORD CHECK-IN
#
#   Purpose:
#   Upon valid check-in, record visit locally in data structure
#       and for backup in file specified by LOGFILE
#
#   Usage:
#   Assumes PUID has already been verified to be in data structure
#   Assumes PUID is already already type int
#
#####################################################################
def recordCheckIn(PUID):
    print("Valid ECE Student")

    EceStudents[PUID] += 1
    with open(LOGFILE, 'a') as myFile:
        myFile.writelines(str(PUID) + '\n')

#####################################################################
#
#   VERIFY STUDENT
#
#   Purpose:
#   Provided a PUID as a string, strip of whitespace and remove
#       leading zeros.
#   Cross-reference the PUID to the imported ECE Student PUIDS
#       returns True if ID is of an ECE Student
#       returns False if ID is not of an ECE Student
#
#####################################################################
def verifyStudent(PUIDstr):
    PUID = stringToInt(PUIDstr)

    # Check if ECE Student
    if PUID in EceStudents.keys():
        # Clear screen
        for lvc in range(50):
            print("\n")

        # If limit check is active, verify check-in limit not exceeded
        if LIMITCHECKINS:
            if(EceStudents[PUID] >= CHECKINLIMIT):
                # Check-In limit exceeded
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("!     **      CHECK-IN LIMIT EXCEEDED       **    !")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return

        # Valid check-in
        recordCheckIn(PUID)

    else:
        # Not an ECE Student
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!     **        NOT AN ECE STUDENT           **   !")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

#####################################################################
#
#   PROMPT FOR INPUT
#
#   Purpose:
#   Prompt user for PUID input
#
#   Usage:
#   Allows the user to swipe their ID or type in their ID manually
#
#   WARNING:
#   Current card reader (as of December 2015) injects multiple "="
#       into the input. Therefore this requires special parsing.
#   If a different card reader is used, the parsing section will need
#       to be modified accordingly
#
#####################################################################
def promptForInput():
    inputStr = ''

    while inputStr == '':
        inputStr = input("\nSwipt PUID or enter manually: ")
        if isinstance(inputStr, str):
            inputStr = inputStr.strip()

        # Check if need to parse for card reader described above
        if '=' in inputStr:
            inputStr = inputStr.split("=")
            if len(inputStr) < 3:
                print("ERROR: INVALID SWIPE ")
                print("Are you using a different card reader?")
                inputStr = ''
            else:
                PUIDstr = inputStr[2]
                return PUIDstr
        else:
            return inputStr

#####################################################################
#
#   MAIN
#
#####################################################################

if __name__ == "__main__":
    running = True
    initialize()

    while(running):
        inputString = ''

        inputString = promptForInput()

        if inputString == "exit":
            print("Closing script . . .")
            running = False
        else:
            verifyStudent(inputString)

    print("Exit successful . . .")