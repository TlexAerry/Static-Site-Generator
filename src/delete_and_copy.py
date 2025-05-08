import os
import shutil

#recursively identify all file paths
def find_file_paths(source_directory_path):
    #initiates: this is "source_file/..."
    file_paths = os.listdir(source_directory_path)
    return_paths = []
    for i in file_paths:  
        file_path = source_directory_path+"/"+i
        return_paths.append(file_path)
        if os.path.isdir(file_path):
            #print(os.listdir(file_path))
            #file_paths = file_paths + find_file_paths(file_path)
            return_paths = return_paths + find_file_paths(file_path)
    return return_paths

def copy_to_dest(source_dir_path,dest_dir_path):
    # delete the contents in destination completely/recursively
    destination_files = find_file_paths(dest_dir_path)
    if len(destination_files) != 0: 
        for x in reversed(destination_files):
            if os.path.isfile(x):
                os.remove(x)
            else: #it must be a directory
                os.rmdir(x)

    # identifies the file paths of everything in source_file
    source_file_paths = find_file_paths(source_dir_path)
     
    # Copy the contents to dest, replacing <source> in filepath name to <dest>
    for x in source_file_paths:
        dest_file_path = dest_dir_path + x[len(source_dir_path):]
        if os.path.isfile(x):
            if os.path.exists(dest_file_path):
                raise Exception("Public file not being cleared out correctly")
            else:
                shutil.copy(x,dest_file_path)
        else:
            os.mkdir(dest_file_path)

