from passlib.hash import sha256_crypt

enteredPassword = "web101project"
pw = sha256_crypt.hash(enteredPassword)
print(pw)

