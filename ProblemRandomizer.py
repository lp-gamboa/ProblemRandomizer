import sys
import MyBlackboardQuiz as bbq 
import RandomMathObjects as rmo 
from numpy import random as nr 
import json 
from sympy import * 

# ------------------------------------------------------------------------
def gen_variable(k, desc, var_values): 
    var_type = list(desc.keys())[0]
    var_params = desc[var_type] 
    optional = list(var_params.keys()) 
    subs_values = [(sympify(kk), vv) for kk,vv in var_values.items()] 
    
    if var_type=="ENTERO": 
        min_v, max_v = var_params["min"], var_params["max"]
        nuevo_entero = nr.choice(max_v+1-min_v)+min_v
        var_values[k] = nuevo_entero
        
    elif var_type=="PUNTO":
        coords = var_params.keys()
        val_coords = [sympify(var_params[a]).subs(subs_values) for a in coords] 
        var_values[k] = tuple(val_coords) 
        
    elif var_type=="VECTOR_COLUMNA": 
        params = { "size": var_params["num_coords"] } 
        params["max_val"] = (4 if not "max_val" in optional 
                    else sympify(var_params["max_val"]).subs(subs_values))
        params["max_denom"] = (1 if not "max_denom" in optional 
                    else sympify(var_params["max_denom"]).subs(subs_values))
        var_values[k] = rmo.gen_column_vector( size=params["size"], 
            max_val=params["max_val"], max_denom=params["max_denom"] ) 
            
    elif var_type=="VECTOR_FILA": 
        params = { "size": var_params["num_coords"] } 
        params["max_val"] = (4 if not "max_val" in optional 
                    else sympify(var_params["max_val"]).subs(subs_values))
        params["max_denom"] = (1 if not "max_denom" in optional 
                    else sympify(var_params["max_denom"]).subs(subs_values))
        var_values[k] = rmo.gen_row_vector( size=params["size"], 
            max_val=params["max_val"], max_denom=params["max_denom"] ) 
        
    elif var_type=="COMBINACION_LINEAL":
        params = { "vectors": var_params["vectores"] } 
        params["max_val"] = (4 if not "max_val" in optional 
                    else sympify(var_params["max_val"]).subs(subs_values))
        params["max_denom"] = (1 if not "max_denom" in optional 
                    else sympify(var_params["max_denom"]).subs(subs_values))
        var_values[k] = rmo.gen_lin_comb( vectors=params["vectors"], 
            max_val=params["max_val"], max_denom=params["max_denom"] ) 
        
    elif var_type=="POLINOMIO_MONICO":
        params = {"degree": var_params["degree"]}
        later_sub_needed = False 
        if "variable" in optional and len(var_params["variable"])>1:
            later_sub_needed = True 
        params["lin_factors"] = ( False if not "lin_factors" in optional 
                else sympify(var_params["lin_factors"]).subs(subs_values) )
        params["variable"] = ('x' if not "variable" in optional else 
            (var_params["variable"] if len(var_params["variable"])==1 else 
            't' ))
        params["max_val"] = (4 if not "max_val" in optional 
                    else sympify(var_params["max_val"]).subs(subs_values))
        params["max_denom"] = (1 if not "max_denom" in optional 
                    else sympify(var_params["max_denom"]).subs(subs_values))
        poly = rmo.gen_monic_poly( params["degree"],
            lin_factors=params["lin_factors"], variable=params["variable"],
            max_val=params["max_val"], max_denom=params["max_denom"] ) 
        if later_sub_needed: 
            poly = poly.subs(
            [ ('t',sympify(var_params["variable"]).subs(subs_values)) ] )
        var_values[k] = poly 
        
    elif var_type=="POLINOMIO":
        params = {"degree": var_params["degree"]}
        later_sub_needed = False 
        if "variable" in optional and len(var_params["variable"])>1:
            later_sub_needed = True 
        params["lin_factors"] = ( False if not "lin_factors" in optional 
                else sympify(var_params["lin_factors"]).subs(subs_values) )
        params["variable"] = ('x' if not "variable" in optional else 
            (var_params["variable"] if len(var_params["variable"])==1 else 
            't' ))
        params["max_val"] = (4 if not "max_val" in optional 
                    else sympify(var_params["max_val"]).subs(subs_values))
        params["max_denom"] = (1 if not "max_denom" in optional 
                    else sympify(var_params["max_denom"]).subs(subs_values))
        poly = rmo.gen_poly( params["degree"],
            lin_factors=params["lin_factors"], variable=params["variable"],
            max_val=params["max_val"], max_denom=params["max_denom"] ) 
        if later_sub_needed: 
            poly = poly.subs(
            [ ('t',sympify(var_params["variable"]).subs(subs_values)) ] )
        var_values[k] = poly
        
    elif var_type=="MATRIZ_RANGO": 
        params = {
            "size": ( 
                sympify(var_params["num_filas"]).subs(subs_values), 
                sympify(var_params["num_columnas"]).subs(subs_values) ), 
            "rank": sympify(var_params["rank"]).subs(subs_values) }
        params["max_val"] = (3 if not "max_val" in optional 
                    else sympify(var_params["max_val"]).subs(subs_values))
        params["max_denom"] = (1 if not "max_denom" in optional 
                    else sympify(var_params["max_denom"]).subs(subs_values))
        var_values[k] = rmo.gen_matrix_rank(size=params["size"], 
                        rank=params["rank"], max_val=params["max_val"],
                        max_denom=params["max_denom"])
                        
    elif var_type=="MATRIZ_DIAGONAL": 
        params = { "size":
                        sympify(var_params["dimension"]).subs(subs_values), 
            "det": sympify(var_params["determinante"]).subs(subs_values) }
        params["max_denom"] = (1 if not "max_denom" in optional 
                    else sympify(var_params["max_denom"]).subs(subs_values))
        var_values[k] = rmo.gen_diagonal_matrix(size=params["size"], 
                        det=params["det"], max_denom=params["max_denom"])
                        
    elif var_type=="MATRIZ_TRIANGULAR":
        params = { "size":
                        sympify(var_params["dimension"]).subs(subs_values), 
            "det": sympify(var_params["determinante"]).subs(subs_values) }
        params["upper"] = (True if not "superior" in optional 
                    else sympify(var_params["superior"]).subs(subs_values))
        params["max_val"] = (7 if not "max_val" in optional 
                    else sympify(var_params["max_val"]).subs(subs_values))
        params["max_denom"] = (1 if not "max_denom" in optional 
                    else sympify(var_params["max_denom"]).subs(subs_values))
        var_values[k] = rmo.gen_triang_matrix(size=params["size"], 
                        det=params["det"], upper=params["upper"],
                    max_denom=params["max_denom"], max_val=params["max_val"])
                        
    elif var_type=="MATRIZ_DETERMINANTE":
        params = { "size":
                        sympify(var_params["dimension"]).subs(subs_values), 
            "det": sympify(var_params["determinante"]).subs(subs_values) }
        params["max_val"] = (3 if not "max_val" in optional 
                    else sympify(var_params["max_val"]).subs(subs_values))
        params["max_denom"] = (1 if not "max_denom" in optional 
                    else sympify(var_params["max_denom"]).subs(subs_values))
        var_values[k] = rmo.gen_diagonal_matrix(size=params["size"], 
                        det=params["det"], max_denom=params["max_denom"],
                        max_val=params["max_val"])
                        
    elif var_type=="MATRIZ_SIMETRICA": 
        params = { "size":
                        sympify(var_params["dimension"]).subs(subs_values)}
        params["sym"] = (True if not "simetrica" in optional 
                    else sympify(var_params["simetrica"]).subs(subs_values))
        params["max_val"] = (3 if not "max_val" in optional 
                    else sympify(var_params["max_val"]).subs(subs_values))
        var_values[k] = rmo.gen_sym_matrix(size=params["size"], 
                        sym=params["sym"], max_val=params["max_val"])
                        
    elif var_type=="EVALUAR_FUNCION":
        punto = var_params["punto"]
        fun_vars = list(punto.keys())
        val_fun_vars = [(sympify(a), var_values[punto[a]]) for a in fun_vars]
        expr_fun = var_values[var_params["function"]] 
        var_values[k] = expr_fun.subs(val_fun_vars)
    
    elif var_type=="DERIVAR_FUNCION":
        foo, vars_diff = var_values[var_params["function"]], var_params["variables"] 
        for a in vars_diff:
            foo = diff(foo, symbols(a))
        var_values[k] = foo
        
    elif var_type=="EVALUAR_EXPRESION":
        var_values[k] = sympify(var_params["expr"]).subs(subs_values)
        
    elif var_type=="OPERACION_MATRICIAL":
        matriz = sympify(var_params["matriz"]).subs(subs_values)
        if var_params["operacion"]=="CALC_NUL":
            var_values[k]= len(matriz.nullspace())
        elif var_params["operacion"]=="CALC_RANK":
            var_values[k]=matriz.rank()
        else:
            print("operacion no implementada :c") 
    else: 
        print("caso no implementado... :c") 
    return var_values 
    
# ---------------------------------------------------------------

def eval_answer(ans_type, ans_desc, var_values): 
    if ans_type=="NUM":
        return sympify(ans_desc).subs(var_values)
    elif ans_type=="ESS":
        answer = ans_desc
        for k,v in var_values.items():
            answer = answer.replace("["+k+"]", latex(v))
        return answer
    elif ans_type=="FIBS":
        answer = {}
        for k,v in ans_desc.items():
            answer[k] = [str(sympify(v).subs(var_values))]
        return answer
    elif ans_type=="MCQ":
        answers, correct = ans_desc["opciones"], ans_desc["correcta"]
        return ["$$"+latex(sympify(a).subs(var_values))+"$$" for a in answers], correct 
    else:
        return 0


def gen_num_qs(pool, q_object): # acá q_object se maneja como un diccionario 
    for i in range(q_object["cantidad"]):
        nombre, cuerpo = q_object["id"]+"_"+str(i+1), q_object["cuerpo"]
        variables, val_variables = q_object["variables"].items(), {} 
        for k, v in variables:
            val_variables = gen_variable(k, v, val_variables) 
            cuerpo = cuerpo.replace("["+k+"]", latex(val_variables[k]))
        ans_desc_object = q_object["respuesta"]
        ans_type = q_object["tipo"]
        respuesta = eval_answer(ans_type, ans_desc_object, 
                                val_variables) 
        pool.addNumQ(nombre, cuerpo, respuesta, erramt=0.001) 


def gen_ess_qs(pool, q_object):
    for i in range(q_object["cantidad"]):
        nombre, cuerpo = q_object["id"]+"_"+str(i+1), q_object["cuerpo"]
        variables, val_variables = q_object["variables"].items(), {} 
        for k, v in variables:
            val_variables = gen_variable(k, v, val_variables) 
            cuerpo = cuerpo.replace("["+k+"]", latex(val_variables[k]))
        ans_desc_object = q_object["respuesta"]
        ans_type = q_object["tipo"]
        respuesta = eval_answer(ans_type, ans_desc_object,     val_variables) 
        pool.addEssQ(nombre, cuerpo, respuesta) 


def gen_file_qs(pool, q_object):
    for i in range(q_object["cantidad"]):
        nombre, cuerpo = q_object["id"]+"_"+str(i+1), q_object["cuerpo"]
        variables, val_variables = q_object["variables"].items(), {} 
        for k, v in variables:
            val_variables = gen_variable(k, v, val_variables) 
            cuerpo = cuerpo.replace("["+k+"]", latex(val_variables[k])) 
        pool.addFileQ(nombre, cuerpo) 
        
        
def gen_fib_qs(pool, q_object):
    for i in range(q_object["cantidad"]):
        nombre, cuerpo = q_object["id"]+"_"+str(i+1), q_object["cuerpo"]
        variables, val_variables = q_object["variables"].items(), {} 
        for k, v in variables:
            val_variables = gen_variable(k, v, val_variables) 
            cuerpo = cuerpo.replace("["+k+"]", latex(val_variables[k]))
        ans_desc_object = q_object["respuesta"]
        ans_type = q_object["tipo"]
        respuesta = eval_answer(ans_type, ans_desc_object,     val_variables) 
        pool.addFITBQ(nombre, cuerpo, respuesta) 

        
def gen_multchoice_qs(pool, q_object):
    for i in range(q_object["cantidad"]):
        nombre, cuerpo = q_object["id"]+"_"+str(i+1), q_object["cuerpo"]
        variables, val_variables = q_object["variables"].items(), {} 
        for k, v in variables:
            val_variables = gen_variable(k, v, val_variables) 
            cuerpo = cuerpo.replace("["+k+"]", latex(val_variables[k]))
        ans_desc_object = q_object["respuesta"]
        ans_type = q_object["tipo"]
        respuestas, correcta = eval_answer(ans_type, 
                                ans_desc_object, val_variables) 
        pool.addMCQ(nombre, cuerpo, respuestas, correcta) 


# ----------------------------------------------------------------------------
qt_switcher = { "NUM": gen_num_qs, "ESS": gen_ess_qs, 
                "FIL": gen_file_qs, "FIBS": gen_fib_qs, 
                "MCQ": gen_multchoice_qs }
path_json = sys.argv[1] 
with open(path_json,"r") as read_file:  
    test_info = json.load(read_file)
    # test_info is a json object that contains all data needed for the test.
    qs_info = test_info["preguntas"] # <- this is a list of json objects.
    with bbq.Package(test_info["nombre"]) as package: 
        for i in range(len(qs_info)): 
            q_actual = qs_info[i] # <- objeto de 'tipo' pregunta 
            q_type = q_actual["tipo"] 
            with package.createPool(pool_name = q_actual["id"], description = q_actual["descripcion"], instructions = q_actual["instrucciones"]) as q_pool: 
                qt_switcher[q_type](q_pool, q_actual) 
            
