# append token to a file newline
def append_to_file(file, token):
    file_object = open(file, "a")
    file_object.write(token + "\n")
    file_object.close()