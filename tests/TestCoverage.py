import os


print("********* Coverage Testing ************")
cmd = "py.test --cov"
returned_value = os.system(cmd)
print(returned_value)
