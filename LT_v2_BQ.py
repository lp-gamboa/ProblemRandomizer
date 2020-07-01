#!/usr/bin/env python3

import BlackboardQuiz as bbq
import numpy as np

with bbq.Package("LinearTransformations_v2") as package: 
    with package.createPool('Fill in the blank questions.', description="Give a formula for the linear transformation given.", instructions="") as pool:
        
        Basis1 = ['-5 3; 3 -2', '1 5; 1 6', '-2 3; 1 -2', '-4 -1; 3 1', '7 3; 2 1', '5 2; 2 1']
        #Basis2 = ['5 2; 1 0', '2 4; 4 5', '7 10; 2 3', '-2 0; 5 1']
        Images1 = ['0 7; -1 2', '3 -1; 2 5', '4 1; -3 0', '1 -5; -2 2', '-1 4; 5 9', '5 1; -3 1']
        #Images2 = ['0 2; -4 10', '6 -2; 4 4', '8 2; -6 2', '2 8; -4 4']
        #f= open("LinearTrasnformations_v2_set.txt","w+")
        count = 0
        rep = 1
        while 2*count + rep < 12:
            b = np.matrix(Basis1[count])
            v1 = b[:,0]
            str_v1 = str(int(v1[0])) + ',' + str(int(v1[1]))
            v2 = b[:,1]
            str_v2 = str(int(v2[0])) + ',' + str(int(v2[1]))
            
            w = np.matrix(Images1[(count+3*rep)%6])
            w1 = w[:,0]
            str_w1 = str(int(w1[0])) + ',' + str(int(w1[1]))
            w2 = w[:,1]
            str_w2 = str(int(w2[0])) + ',' + str(int(w2[1]))
            
            str_body = 'Let $$F:\\mathbb{{R}}^2\\rightarrow\\mathbb{{R}}^2$$ be the linear transformation for which $$F({})=({})$$ and $$F({})=({})$$. Find a formula for F; that is, find F(a,b). F(a,b) = ([A],[B])'
            A = w*np.linalg.inv(b)
            r1 = A.T[:,0]
            str_r1 =str(int(bbq.roundSF(float(r1[0]),1))) + 'a + ' + str(int(bbq.roundSF(float(r1[1]),1))) + 'b'
            r2 = A.T[:,1]
            str_r2 = str(int(bbq.roundSF(float(r2[0]),1))) + 'a + ' + str(int(bbq.roundSF(float(r2[1]),1))) + 'b'
        #     print('Respuesta: F(a,b) = ' + str_r1 + str_r2 + '\n')
            pool.addFITBQ(title="LinearTransformations_v2_"+str(2*count + rep),
             text=str_body.format(str_v1, str_w1, str_v2, str_w2),
             answers={'A':[str_r1], 'B':[str_r2]})
            #f.write('ESS\t'+str_body.format(str_v1, str_w1, str_v2, str_w2)+'Find a formula for F; that is, find F(a,b). e.g. F(a,b)=(a+b, 3a)\tF(a,b) = ' + str_r1 + str_r2)
            
            if rep == 2:
                count, rep = count+1, 1
            else:
                rep = 2
