TABLES = {}

TABLES['users'] = (
    "CREATE TABLE users ("
    "  userId INT NOT NULL AUTO_INCREMENT,"
    "  name NVARCHAR(180) NOT NULL,"
    "  email NVARCHAR(255) NOT NULL UNIQUE,"
    "  password NVARCHAR(180) NOT NULL,"
    "  legalPerson BIT NOT NULL,"
    "  cpf NCHAR(11),"
    "  cnpj NCHAR(14),"
    "  isTenant BIT NOT NULL,"
    "  PRIMARY KEY (userId))")

TABLES['offices'] = (
    "CREATE TABLE offices ("
    "  officeId INT NOT NULL AUTO_INCREMENT,"
    "  ownerId INT NOT NULL,"
    "  address NVARCHAR(300) NOT NULL,"
    "  district NVARCHAR(300) NOT NULL,"
    "  number NVARCHAR(5) NOT NULL,"
    "  extra NVARCHAR(300) NOT NULL,"
    "  scoring INT NOT NULL,"
    "  nScore INT NOT NULL,"
    "  PRIMARY KEY (officeId))")

TABLES['rents'] = (
    "CREATE TABLE rents ("
    "  rentId INT NOT NULL AUTO_INCREMENT,"
    "  userId INT NOT NULL,"
    "  bookingStart DATETIME NOT NULL,"
    "  bookingEnd DATETIME NOT NULL,"
    "  checkIn DATETIME,"
    "  checkOut DATETIME,"
    "  PRIMARY KEY (rentId))")