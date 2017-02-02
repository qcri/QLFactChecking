from os import rename, listdir

def main():
    directory = '../../../data/features'
    fnames = listdir(directory)
    for filename in fnames:
        if filename.startswith('input-train1'):
            new_filename = filename.replace('input-train1', 'semeval2016-train1-with-annotations-clear-true-false-only', 1)
            print(new_filename)
            rename(directory+'/'+filename, directory+'/'+new_filename)

main()