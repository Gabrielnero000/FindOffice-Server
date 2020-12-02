TABLES = {}

TABLES['tenant'] = (
    "CREATE TABLE tenant ("
    "  tenantId INT NOT NULL AUTO_INCREMENT,"
    "  name NVARCHAR(180) NOT NULL,"
    "  email NVARCHAR(255) NOT NULL UNIQUE,"
    "  password NVARCHAR(180) NOT NULL,"
    "  PRIMARY KEY (tenantId))")

TABLES['landmaster'] = (
    "CREATE TABLE landmaster ("
    "  landmasterId INT NOT NULL AUTO_INCREMENT,"
    "  name NVARCHAR(180) NOT NULL,"
    "  email NVARCHAR(255) NOT NULL UNIQUE,"
    "  password NVARCHAR(180) NOT NULL,"
    "  PRIMARY KEY (landmasterId))")

TABLES['offices'] = (
    "CREATE TABLE offices ("
    "  officeId INT NOT NULL AUTO_INCREMENT,"
    "  landmasterId INT NOT NULL,"
    "  city NVARCHAR(300) NOT NULL,"
    "  district NVARCHAR(300) NOT NULL,"
    "  address NVARCHAR(300) NOT NULL,"
    "  number NVARCHAR(5) NOT NULL,"
    "  description NVARCHAR(300) NOT NULL,"
    "  daily_rate FLOAT NOT NULL,"
    "  capacity INT NOT NULL,"
    "  scoring INT NOT NULL,"
    "  nScore INT NOT NULL,"
    "  type VARCHAR(100) NOT NULL,"
    "  PRIMARY KEY (officeId))")

TABLES['rents'] = (
    "CREATE TABLE rents ("
    "  rentId INT NOT NULL AUTO_INCREMENT,"
    "  officeId INT NOT NULL,"
    "  tenantId INT NOT NULL,"
    "  bookingStart DATETIME NOT NULL,"
    "  bookingEnd DATETIME NOT NULL,"
    "  checkIn DATETIME,"
    "  checkOut DATETIME,"
    "  PRIMARY KEY (rentId))")
