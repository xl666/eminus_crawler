import login 
import cursos as cr
import evaluaciones as ev
import actividades as ac
import os
import config

if __name__ == '__main__':            
    driver = config.configure()
    login.login(driver, os.environ.get('user'), os.environ.get('pass'))
    cursos = cr.regresar_cursos(driver)
    print(cr.ver_cursos(cursos))
    cr.extraer_evidencias_lista_cursos(driver, cursos, ['94668','94369'], '/tmp/evidencias')
    #cr.extraer_evidencias_curso(driver, cursos, '94369', '/tmp/cibercrimen')
    #cr.ir_a_curso(driver, cursos, '94368')
    #ev.ir_a_evaluaciones(driver)
    #ev.extraer_respuestas_evaluaciones_curso(driver, '/tmp/evaluaciones')
    
    #ac.ir_a_actividades(driver)
    #ac.extraer_respuestas_actividades_curso(driver, '/tmp/actividades')
    

