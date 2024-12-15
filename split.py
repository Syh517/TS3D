import re
from faker import Faker


# with open("/home/yyy/mysql/data/logs/sqls.txt", "r") as fileHandler:
#     # Read next line
#     line = fileHandler.readline()
#     # check line is not empty
#     while line:
#         print(line.split("\t")[-1])
#         line  =  fileHandler.readline()


fake = Faker()
while True:
    addr=fake.address()
    print(re.sub(r'\s+', ' ', addr).strip())
    print("\n")

