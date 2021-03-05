# define an empty list
lista = []

# open file and read the content in a list
with open('lista_rec_2.txt', 'r') as f:
    for line in f:
        # remove linebreak which is the last character of the string
        word = line[:-1]

        # add item to the list
        lista.append(word)

print(lista)