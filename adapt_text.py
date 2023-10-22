full_text = []

def split_text():
    with open("tables.txt") as f:
        text = f.readlines()

        j = 0
        for i in range(len(text)):
            if text[i] == '\n':
                full_text.append(text[j:i])
                j = i + 1

def refactor_text(table):
    res = "{"
    
    for line in table:
        res += f"{line[:line.find(':') + 1]} \"{line[line.find(' '):].rstrip().lower().lstrip()}\", "
    
    res = res[:len(res) - 2] + '}'
    return res

def create_voc(names_table, names_var):
    res = "{"
    
    for i in range(len(names_table)):
        res += f"\"{names_table[i]}\": {names_var[i]}, "
    
    res = res[:len(res) - 2] + '}'

    with open("vocs.txt", "w") as f:
        f.writelines(res) 

def create_vars():
    res = ""
    names = []
    names_var = []
    
    for i in range(len(full_text)):
        name = input()
        name_var = "self." + name + "_table"
        names.append(name)
        names_var.append(name_var)
        
        res += name_var + " = " + refactor_text(full_text[i]) + '\n' * 2 
    
    with open("formatted_tables.txt", "w") as f:
        f.writelines(res.rstrip()) 

    create_voc(names, names_var)

split_text()
create_vars()
        