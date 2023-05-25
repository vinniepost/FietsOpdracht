test = "fiets 1000, fiets 1001, fiets 1002, fiets 1003,"
split = test.split(", ")
split[-1] = split[-1].strip(",")
print(split)