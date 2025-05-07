import os
import shutil

#recursively identify all file paths
def find_file_paths(source_file):
    #initiates: this is "source_file/..."
    file_paths = os.listdir(source_file)
    return_paths = []
    for i in file_paths:  
        file_path = source_file+"/"+i
        return_paths.append(file_path)
        if os.path.isdir(file_path):
            #print(os.listdir(file_path))
            #file_paths = file_paths + find_file_paths(file_path)
            return_paths = return_paths + find_file_paths(file_path)
    return return_paths


def print_to_public(source_file,destination_file):
    # delete the contents in public completely/recursively
    destination_files = find_file_paths(destination_file)
    if len(destination_files) != 0: 
        for x in reversed(destination_files):
            if os.path.isfile(x):
                os.remove(x)
            else: #it must be a directory
                #check if contents?
                os.rmdir(x)
    

    # identifies the file paths of everything in source_file
    source_file_paths = find_file_paths(source_file)
    
     
    # Copy the contents to public, replacing "static" in filepath name to "public"
    for x in source_file_paths:
        dest_file_path = destination_file + x[len(source_file):]
        print(dest_file_path)
        if os.path.isfile(x):
            if os.path.exists(dest_file_path):
                raise Exception("Public file not being cleared out correctly")
            else:
                shutil.copy(x,dest_file_path)
        else:
            os.mkdir(dest_file_path)
def main():
    print_to_public("static","public")


if __name__ == "__main__":
    main()