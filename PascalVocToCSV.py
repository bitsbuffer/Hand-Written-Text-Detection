import xmltodict
import pandas as pd
import os

dir_name = './Annotations'

def xml_to_csv(dir_name):
    results = []
    for file_name in os.listdir(dir_name):
        try:
            with open(os.path.join(dir_name, file_name)) as fd:
                doc = xmltodict.parse(fd.read())
            objects = doc['annotation']['object']
            path = doc['annotation']['path']
            if type(objects) == list:
                for obj in objects:
                    row = [path]
                    row.append(obj['bndbox']['xmin'])
                    row.append(obj['bndbox']['ymin'])
                    row.append(obj['bndbox']['xmax'])
                    row.append(obj['bndbox']['ymax'])
                    row.append(obj['name'])
                    results.append(row)
            else:
                row = [path]
                row.append(objects['bndbox']['xmin'])
                row.append(objects['bndbox']['ymin'])
                row.append(objects['bndbox']['xmax'])
                row.append(objects['bndbox']['ymax'])
                row.append(objects['name'])
                results.append(row)
        except KeyError as e:
            print("Exception for file name {0} for key not found {1}".format(file_name, str(e)))
    return results

def str_change(string):
    return string.replace("C:\\Users\\tinzha\\Documents\\EY\\handwriting\\trainjpg_output\\JPEGImages\\", "train_images/")


if __name__ == "__main__":
    results = xml_to_csv(dir_name)
    df = pd.DataFrame(data=results, columns=['File_Name', 'xmin', 'ymin', 'xmax', 'ymax', 'class'])
    df['File_Name'] = df['File_Name'].apply(str_change)
    df.to_csv('annotate.txt', header=None, index=None, sep=',')
