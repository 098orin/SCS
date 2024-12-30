import main
import value
import global_value as g

g.i2 = 2
main.main(value.project_id[g.i2])

"""
for i in range(60):
    
    for g.i2 in range(len(value.project_id)):
        #try:
            main.main(value.project_id[g.i2])
        #except Exception as error:
        #    print(error)
"""
    