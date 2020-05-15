import sys
import requests    
  
# Данные авторизации в API Trello  
auth_params = {    
    'key': "XXXXXXXXXXXXXXXXX",    
    'token': "XXXXXXXXXXXXXXXXXXX", }  
  
# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}"  
board_id = "pOJclpUc"

def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        k=0
        for count in task_data:
            if count['name'] != "Нет задач!":
                k+=1
        print(column['name'] + '. Количество задач:' + str(k))    
        # Получим данные всех задач в колонке и перечислим все названия      
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:     
            print('\t' + task['name'] + '\n' + 'id:' + task['id'])  
            
def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break

def new_column(column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': column_name, **auth_params})
    

def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None
    task_dict = {}
    i=0
    task_ids = []    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:
            task_ids.append(task['name'])
            if task['name'] == name and task_ids.count(task['name'])==1:
                task_id = task['id']    
            elif task['name'] == name and task_ids.count(task['name'])>1:
                task_dict.update([(task['id'],task['name'])])
        if task_id:
            break    
    
    print('Были найдены потворяющиеся задачи' + '\n')
    for key in task_dict:
        task_column_name = requests.get(base_url.format('lists') + '/' + task['idList'], params=auth_params).json()['name']
        print("id: {}      Задача: {}       Находится в колонке:   {}".format(key, task['name'], task_column_name))
    task_id = input("Пожалуйста, введите ID задачи, которую нужно переместить: ")   
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            break  


if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])  
    elif sys.argv[1] == 'column':    
        new_column(sys.argv[2])    

