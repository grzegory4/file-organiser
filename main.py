import os # os module is used to interact with the operating system
import shutil # shutil module is used to move files

# define the directory to organize
directory = os.path.join(os.path.expanduser('~'), 'Downloads')

# define the file extensions and their corresponding categories
extensions = {
    'Images': ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff', 'svg'],
    'Videos': ['mp4', 'mkv', 'webm', 'flv', 'avi', 'mov', 'wmv', 'mpg', 'mpeg', '3gp'],
    'Music': ['mp3', 'wav', 'flac', 'ogg', 'wma', 'aac'],
    'Documents': ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'rtf'],
    'Archives': ['zip', 'rar', '7z', 'tar', 'gz', 'iso', 'dmg'],
    'Executables': ['exe', 'msi'],
    'Scripts': ['py', 'sh', 'bat', 'ps1'],
    'Webpages': ['html', 'css', 'js', 'php', 'asp', 'aspx', 'jsp'],
    'Shortcuts': ['lnk'],
    'Others': []
}

# iterate over each file in the directory
for file_name in os.listdir(directory):
    file_path = os.path.join(directory, file_name) # get the full path of the file

    if os.path.isfile(file_path): # check if it is a file
        extension = os.path.splitext(file_name)[1][1:].lower() # Get the file extension

        folder_name = None
        # find the category for the file extension
        for category, ext_list in extensions.items():
            if extension in ext_list:
                folder_name = category
                break

        if folder_name:
            folder_path = os.path.join(directory, folder_name) # get the path of the category folder
            os.makedirs(folder_path, exist_ok=True) # create the category folder if it doesn't exist

            destination_path = os.path.join(folder_path, file_name) # get the destination path
            shutil.move(file_path, destination_path) # move the file to the category folder

            print(f'Moved {file_name} to {folder_name} folder') # print the action
        else:
            print(f'No destination folder found for {file_name}') # print if no category found

    else:
        print(f'Skipped {file_name}. It\'s a directory') # print if it is a directory

print('File organization completed') # print when the organization is complete