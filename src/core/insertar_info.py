from dis import dis
#from msilib.schema import Class
from src.core.methods import permisoMethod, rolMethod
from src.core.models.rol import Rol
from src.core.models.socio import Socio
from src.core.methods import socioMethod
from src.core.methods import personalMethod
from src.core.models.personal import Personal
from src.core.models.disciplina import Disciplina
from src.core.methods import disciplinaMethod
from werkzeug.security import generate_password_hash
from src.core.methods import configuracionMethod
from random import randrange


def insertar():
    ### CREAR CONFIG
    configuracionMethod.create_configuracion(paginacion=10, monto_base=1500, porcentaje_recargo=10)

    ### CREAR ROL
    rolMethod.create_rol('Administrador')
    rolMethod.create_rol('Operador')
    print('CREAR ROL')

    ### CREAR PERSONAL
    password_hash = generate_password_hash('1234', method='sha256')
    personalMethod.create_personal('Juan','Fazzano','juan@fazzano.com',password_hash, 1)  
    personalMethod.create_personal('Gisela','Fernandez','gisela@fernandez.com',password_hash, 1)  
    personalMethod.create_personal('Facundo','Alcorta','facundo@alcorta.com',password_hash, 1)  
    personalMethod.create_personal('Admin0','Admin0','admin0@mail.com',password_hash, 1)  
    personalMethod.create_personal('Operador0','Operador0','operador0@mail.com',password_hash, 2)  
    print('CREAR PERSONAL')

    ### CREAR SOCIO

    for i in range(20):
          socioMethod.create_socio('socio'+str(i),'socio'+str(i),password_hash,'DNI',str(i),'xx','calle '+ str(i) ,str(i)+str(i)+str(i)+str(i)+str(i),'socio'+str(i)+'@mail.com')
    print('CREAR SOCIO')

    ### CREAR DISCIPLINAS
    disciplinaMethod.create_disciplina('Futbol','sub 15', 'Lunes', '14hs', 2500, 'Juan Perez')
    disciplinaMethod.create_disciplina('Futbol','sub 17', 'Lunes', '16hs', 2500, 'Juan Perez')
    disciplinaMethod.create_disciplina('Futbol','sub 19', 'Lunes', '18hs', 2500, 'Juan Perez')

    disciplinaMethod.create_disciplina('Voley','sub 15', 'Martes', '14hs', 2000, 'Juan Perez')
    disciplinaMethod.create_disciplina('Voley','sub 17', 'Martes', '16hs', 2000, 'Juan Perez')
    disciplinaMethod.create_disciplina('Voley','sub 19', 'Martes', '18hs', 2000, 'Juan Perez')

    disciplinaMethod.create_disciplina('Hockey','sub 15', 'Miercoles', '14hs', 4000, 'Juan Perez')
    disciplinaMethod.create_disciplina('Hockey','sub 17', 'Miercoles', '16hs', 4000, 'Juan Perez')
    disciplinaMethod.create_disciplina('Hockey','sub 19', 'Miercoles', '18hs', 4000, 'Juan Perez')

    disciplinaMethod.create_disciplina('Patín','sub 15', 'Jueves', '14hs', 3000, 'Juan Perez')
    disciplinaMethod.create_disciplina('Patín','sub 17', 'Jueves', '16hs', 3000, 'Juan Perez')
    disciplinaMethod.create_disciplina('Patín','sub 19', 'Jueves', '18hs', 3000, 'Juan Perez')
    print('CREAR DISCIPLINAS')

    ### AGREGO DISCIPLINAS A SOCIOS
    for i in range(1,11):
        socioMethod.agregar_disciplina(randrange(1,21),i)
        
    print('AGREGO DISCIPLINAS A SOCIOS')

    # socioMethod.disciplina_practicada(1)
    #disciplinaMethod.list_socios(1)
    
    ### CREAR PERMISOS
    permisoMethod.create_permiso('disciplina_index')      #1      # A/O
    permisoMethod.create_permiso('disciplina_show')       #2      # A/O
    permisoMethod.create_permiso('disciplina_new')        #3      # A/O
    permisoMethod.create_permiso('disciplina_update')     #4      # A/O
    permisoMethod.create_permiso('disciplina_destroy')    #5      # A
    permisoMethod.create_permiso('disciplina_export') 
          #6      personal
    permisoMethod.create_permiso('personal_index')        #7      # A/O
    permisoMethod.create_permiso('personal_show')         #8      # A/O
    permisoMethod.create_permiso('personal_new')          #9      # A/O
    permisoMethod.create_permiso('personal_update')       #10     # A/O
    permisoMethod.create_permiso('personal_destroy')      #11     # A

    permisoMethod.create_permiso('socio_index')           #12     # A/O
    permisoMethod.create_permiso('socio_show')            #13     # A/O
    permisoMethod.create_permiso('socio_new')             #14     # A/O
    permisoMethod.create_permiso('socio_update')          #15     # A/O
    permisoMethod.create_permiso('socio_destroy')         #16     # A
    

    permisoMethod.create_permiso('pagos_index')           #17     # A/O
    permisoMethod.create_permiso('pagos_show')            #18     # A/O
    permisoMethod.create_permiso('pagos_import')          #19     # A/O
    permisoMethod.create_permiso('pagos_destroy')         #20     # A

    permisoMethod.create_permiso('config_update')         #21     #A
    permisoMethod.create_permiso('config_show')           #22     #A

    permisoMethod.create_permiso('cuota_generate')       #23     #A

    print('CREAR PERMISOS')


    ### AGREGO PERMISOS A ROL
    #PERMISOS PARA ROL ADMINISTRADOR
    rolMethod.agregar_permiso(1,1)  #Rol administrador permiso 'disciplina_index'
    rolMethod.agregar_permiso(1,2)  #Rol administrador permiso 'disciplina_show'
    rolMethod.agregar_permiso(1,3)  #Rol administrador permiso 'disciplina_new'
    rolMethod.agregar_permiso(1,4)  #Rol administrador permiso 'disciplina_update'
    rolMethod.agregar_permiso(1,5)  #Rol administrador permiso 'disciplina_destroy'
    rolMethod.agregar_permiso(1,6)  #Rol administrador permiso 'disciplina_export'
    rolMethod.agregar_permiso(1,7)  #Rol administrador permiso 'personal_index'
    rolMethod.agregar_permiso(1,8)  #Rol administrador permiso 'personal_show'
    rolMethod.agregar_permiso(1,9)  #Rol administrador permiso 'personal_new'
    rolMethod.agregar_permiso(1,10) #Rol administrador permiso 'personal_update'
    rolMethod.agregar_permiso(1,11) #Rol administrador permiso 'personal_destroy'
    rolMethod.agregar_permiso(1,12) #Rol administrador permiso 'socio_index'
    rolMethod.agregar_permiso(1,13) #Rol administrador permiso 'socio_show'
    rolMethod.agregar_permiso(1,14) #Rol administrador permiso 'socio_new'
    rolMethod.agregar_permiso(1,15) #Rol administrador permiso 'socio_update'
    rolMethod.agregar_permiso(1,16) #Rol administrador permiso 'socio_destroy'
    rolMethod.agregar_permiso(1,17) #Rol administrador permiso 'pagos_index'
    rolMethod.agregar_permiso(1,18) #Rol administrador permiso 'pagos_show'
    rolMethod.agregar_permiso(1,19) #Rol administrador permiso 'pagos_import'
    rolMethod.agregar_permiso(1,20) #Rol administrador permiso 'pagos_destroy'
    rolMethod.agregar_permiso(1,21) #Rol administrador permiso 'config_update'
    rolMethod.agregar_permiso(1,22) #Rol administrador permiso 'config_show'
    rolMethod.agregar_permiso(1,23) #Rol administrador permiso 'cuota_generate'

    #PERMISOS PARA ROL PERSONAL
    rolMethod.agregar_permiso(2,1)  #Rol operador permiso 'disciplina_index'
    rolMethod.agregar_permiso(2,2)  #Rol operador permiso 'disciplina_show'
    rolMethod.agregar_permiso(2,3)  #Rol operador permiso 'disciplina_new'
    rolMethod.agregar_permiso(2,4)  #Rol operador permiso 'disciplina_update'
    rolMethod.agregar_permiso(2,12) #Rol operador permiso 'socio_index'
    rolMethod.agregar_permiso(2,13) #Rol operador permiso 'socio_show'
    rolMethod.agregar_permiso(2,14) #Rol operador permiso 'socio_new'
    rolMethod.agregar_permiso(2,15) #Rol operador permiso 'socio_update'
    rolMethod.agregar_permiso(2,17) #Rol operador permiso 'pagos_index'
    rolMethod.agregar_permiso(2,18) #Rol operador permiso 'pagos_show'
    rolMethod.agregar_permiso(2,19) #Rol operador permiso 'pagos_import'

    print('AGREGO PERMISOS A ROL')

    # listar permisos de rol 1
    print("permisos asignados al rol admin:")
    print(rolMethod.permisos_asignados(1))


    ### AGREGO ROL A PERSONALO
    #admin
    personalMethod.asignar_rol(1,1)
    personalMethod.asignar_rol(2,1)
    personalMethod.asignar_rol(3,1)
    personalMethod.asignar_rol(4,1)

    #operador
    personalMethod.asignar_rol(5,2)
    print('AGREGO ROL A PERSONALO')

    # print(personalMethod.get_by_id(1).rol_id)
    # print(personalMethod.get_by_id(2).rol_id)
    

