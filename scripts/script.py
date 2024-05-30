# y hace algo que agarre la carpeta de tests, y por cada archivo nombre.clar 
# corra la funcion run_lints(path), capture el output y corra el comando diff sobre eso

# 6:40
# podes usar bash, python, make, lo que vos quieras
# 6:42
# los archivos nombre.out ahora van a estar vacios
# 6:43
# pero dejas un nombre.clar, nombre.stdout y dejas el script que corra stacy sobre nombre.clar, agarre el output y 
#lo compare contra nombre.stdout
# 6:43
# esa última explicación me gusta mas

import os
import stacks_analyzer.stacks_analyzer as stacy
import sys
path_to_tests = "tests"

directories = os.listdir(path_to_tests)

if not 'base_tests' in directories:
    os.mkdir('base_tests')

for dir in directories:

    path_to_particular_test = '/'.join([path_to_tests, dir])
    dir_to_types_of_tests = os.listdir(path_to_particular_test) #i.e. "[remediated-example, vulnerable-example]" 

    #.sort() asures that vulnerable-example always comes on 2nd place
    dir_to_types_of_tests.sort() 
    path_to_vul_ex = '/'.join([path_to_particular_test, dir_to_types_of_tests[1]])

    vul_contract = os.listdir(path_to_vul_ex)[0] #we know there-s only one example
    full_path_to_vul_contract = '/'.join([path_to_vul_ex, vul_contract])

    file_out = open('base_tests/' + os.path.basename(full_path_to_vul_contract)[:-5], "w")
    sys.stdout = file_out
    stacy.lint_file(full_path_to_vul_contract)


