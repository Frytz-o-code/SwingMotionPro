import bcrypt

# Passwort eingeben
password = "admin123".encode()
# Salt generieren und Passwort hashen
#hashed = bcrypt.hashpw(password, bcrypt.gensalt())
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# Ergebnis anzeigen
print(hashed.decode())