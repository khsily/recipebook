import pandas as pd

data = pd.read_csv('C:/Users/Administrator/Desktop/name.csv', header=None, names=['name', 'id'])


def id_2_class_name(predicted_class):
    id = {}
    for i in range(len(data['id'])):
        ids = str('id_' + str(data['id'][i]))
        name = str(data['name'][i])
        id_dict = dict(zip([ids], [name]))
        id.update(id_dict)
    return id[predicted_class]


