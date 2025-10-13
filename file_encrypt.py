a= input("Enter the data you wnat to convert into a cipher: ")
# key is generated here:
key=Fernet.generate_key()

#now, let us assign the value of key to a variable:
f=Fernet(key)

#let us now convert the decrypted string into an incryptrd one:
token=f.encrypt(b'a')


#display the cipher text:
print("the incrypted data is : ", token)

d=f.decrypt(token)

print(d.decode())
