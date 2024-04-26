import pandas

# data = pandas.read_csv('data.csv')
#
# grey_count = len(data[data['Primary Fur Color'] == 'Gray'])
# black_count = len(data[data['Primary Fur Color'] == 'Black'])
# red_count = len(data[data['Primary Fur Color'] == 'Cinnamon'])
#
# squirrels_dict = {
#     "Fur Color": ['gray', 'black', 'red'],
#     'Count': [grey_count, black_count, red_count]
# }
#
# data_table = pandas.DataFrame(squirrels_dict)
# data_table.to_csv('color_data.csv')
# print(data_table)

data = pandas.read_csv('data.csv')

running_count = len(data[data['Running'] == True])
chasing_count = len(data[data['Chasing'] == True])
climbing_count = len(data[data['Climbing'] == True])
eating_count = len(data[data['Eating'] == True])
foraging_count = len(data[data['Foraging'] == True])

squirrel_action_dict = {
    'Action When Seen': ['running', 'chasing', 'climbing', 'eating', 'foraging'],
    'Count': [running_count, chasing_count, climbing_count, eating_count, foraging_count]
}

table = pandas.DataFrame(squirrel_action_dict)
table.to_csv('action_data.csv')