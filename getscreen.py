import pyperclip

with open('./screens/congrats.txt','r') as file:
    data=file.read()

#x=str(repr(data))
#print(x)

x=''.join(data.split('\n'))
pyperclip.copy(x)