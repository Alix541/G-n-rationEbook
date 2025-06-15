import ClassTram
import getpass
import os
import inspect
import categorie

struct_roman=categorie.tirer_scenario()

SCHEMA_PRINCIPAL_CLASSES = {
    name: cls
    for name, cls in inspect.getmembers(ClassTram, inspect.isclass)
    if cls.__module__ == ClassTram.__name__
}

schema_principal_class = SCHEMA_PRINCIPAL_CLASSES[struct_roman["schema_principal"]]
#print("Classes trouvées dans ClassTram :", list(SCHEMA_PRINCIPAL_CLASSES.keys()))
#print("Classe principale :", schema_principal_class)
print(SCHEMA_PRINCIPAL_CLASSES)