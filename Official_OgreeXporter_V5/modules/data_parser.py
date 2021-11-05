def write_data(path, data, name_file):
    f = open(path + name_file, "w")
    print("ALERT >> CREATING FILE AT " + path)
    f.write(data)
    f.close()

def read_data(path):
    f = open(path, "r")
    return f.read()