'''
As funções abaixo contém o Código para a resolução do seguinte problema: Dado um grafo dirigido, retorne as suas componetes fortemente conexas. Para quem não sabe uma componente
fortemente conexa de um grafo é um subconjunto de seus vértices onde é possível acessar qualquer nó desse subconjunto a partir de qualquer outro usando as arestas deste grafo.

A solução desse problema é, em linhas gerais, descrita pelas seguintes etapas:

    1 - faça uma busca em profundidade no grafo e retorne os instantes de saida de cada no.
    2 - gere o transposto do grafo original.
    3 - faça uma busca em profundidade no grafo transposto, priorizando os instantes de saida da primeira busca em ordem decrescente
    4 - as árvores resultantes dessa busca representam as componentes fortemente conexas do grafo.

É recomendado ter um conhecimento prévio em busca de profundidade para entender a prova desta solução. Para provar que a supracitada  funciona, vamos considerar C1 e C2 duas 
componentes fortemente conexas distintas de um di-grafo G. Respectivamente, v e u são vértices específicos de cada componente, enquanto v' e u' são os demais. Além disso, T1 e T2 
são os instantes quando cada uma das componentes terminam de ser exploradas. Estabelecidos esses termos, conclui-se que:

    A) se uma aresta v -> u existir, então não pode existir uma aresta que ligue algum elemento de C2 em direção à C1. A existência dessa aresta v -> u existir implica que qualquer
    elemento de C2 pode ser acessado a partir de C1 ( qualquer v' pode chegar em v, v liga para u, u alcança qualquer u' ), a existência de qualquer aresta na direção oposta torna 
    a premissa inversa verdadeira. Logo C1 e C2 foram nunca componentes distintas mas sim partes de uma mesma componente.

    B) Com essa ponte unidirecional existindo, é certo que T1 > T2. Ora, se a busca começar em C1, em algum momento essa busca irá passar por v, que por sua vez irá iciar a 
    busca em profundidade em C2 com início em u. Como C2 é fortemente conexa e não existe nenhuma aresta de C2 para C1, C2 vai ser totalmente explorada antes da dfs voltar à 
    v. O outro caso é mais trivial, começando em C2, a exploração dessa componente vai terminar antes da de C1 sequer começar. Ambos os casos concluem com T1 > T2. Contudo, no
    segundo, a arvore de busca de C2 será distinta da de C1, enquanto no primeiro esta será uma sub árvore dessa.

    C) Agora vem o pulo do gato. Ao transpor C1 e C2, essas componentes manterão a propriedade de serem fortemente conexas, mas a aresta v -> u se tornará u -> v. Ao priorizar
    o tempo de término da busca anterior em ordem decrescente, a nova busca sempre começará pela Componente que está sendo apontada( desta vez, C1 ), fazendo que cada arvore result
    -ante da busca represente um conjunto fortemente conexo.
'''

START = 0
END   = 1
DEPTH = 2

def adj_tab( V , E , key_s = lambda x : x ):
    
    '''
    Tabaela de adjacência:
    Cada entrada é um nó do grafo e o valor correspondente é uma lista contendo os nós para os quais a
    entrada aponta.
    essa lista é ordenada decrescentemente dada alguma função
    '''

    tab = { u:[] for u in V }
    for u , v in E:
        tab[ u ].append( v )

    for u in V:
        tab[ u ].sort( key = key_s, reverse = True )
    return tab


def depth_tab( adj ):

    '''
    tabela de profundidade, obtida após uma busca de profudindade.
    Assim como a de adjacência, cada entrada é um nó de um grafo. Os valores correspondentes são
    a tripla ordenada:

        START - Momento que o nó começa a ser explorado
        END   - Momento que termina
        DEPTH - Profundidade da busca
    '''
    
    seq = [ -1 ]*3
    dtab = { u : seq.copy() for u in adj.keys() }

    stack = []
    unvisited = set( adj.keys() )
    global clock
    clock = -1

    def mark_visit( v ):

        global clock
        clock += 1
        dtab[ v ][ START ] = clock
        dtab[ v ][ DEPTH ] = len( stack )
        stack.append( v )

        unvisited.remove( v )

    while unvisited:

        v = min( unvisited )
        mark_visit( v )

        while stack:

            u = stack.pop()

            # u termina de ser explorado ------------------------------------------------------
            if not adj[ u ]:
                clock += 1
                dtab[ u ][ END ] = clock
                continue

            stack.append( u )
            v = adj[ u ].pop()

            # v ja foi explorado --------------------------------------------------------------
            if not( v in unvisited ):
                continue

            mark_visit( v )

    return dtab

def print_tab( adj ):
    
    '''
    serve tanto para tab de profundidade quanto de adjacência
    '''
    
    seq = ( list( adj.keys() ) )
    seq.sort()
    for u in seq:
        s1 = str( u )
        s2 = " ".join( map( str , adj[ u ] ) )
        print( s1 , '|' , s2 )

def search_in_depth(  V , E , key_s = lambda x : x ):
    
    adj = adj_tab( V , E , key_s )
    return depth_tab( adj )

def transpose_graph( E ):
    return { ( v , u ) for u , v in E }

def forest( d_tab ):

    '''
    divide os nos em arvores de busca de profundidade distintas.
    O numero de arvores é o numero de nos que tem profundidade zero, vamos chamar esses nos de raiz. Um no de profundiadade diferente de 
    zero pertence a uma arvore se seu valor Start for menor que o valor End da raiz.
    '''

    # Para ficar mais legível-----------------------------------------------------------------------------
    V = set( d_tab.keys() )
    s_fun = lambda x : d_tab[ x ][ START ]
    e_fun = lambda x : d_tab[ x ][ END ]
    d_fun = lambda x : d_tab[ x ][ DEPTH ]
    
    # separando os nós de profundidade zero ( raiz ) dos demais -----------------------------------------
    V1 = [ x for x in V if d_fun( x ) == 0 ]
    trees = { x: [x] for x in V1 }
    V2 = list( V - set( V1 ) )
    
    # --------------------------------------------------------------------------------------------------
    # Otimizando a busca:
    # Uma forma ingenua de obter as raizes seria testar todos os nos de V1 contra todos os nos de V2, o 
    # que daria uma complexidade temporal de O( |V1|*|V2| ) = O( n² ). Melhor seria ordenar V1 e V2 de
    # forma crescente quanto a Start. Se um V2[ j ] ( de um V2 ordenado ) tiver um Start maior que o End
    # de um V1[ i ], então nenhum V2[ k ] com k >= j pertence à arvore com raiz em V1[ i ].
    V1.sort( key = s_fun )
    V2.sort( key = s_fun )
    i , j = 0 , 0
    while i < len( V1 ):
        x = V1[ i ]
        ex = e_fun( x )
        while j < len( V2 ):
            y = V2[ j ]
            sy = s_fun( y )
            if not ( sy < ex ):
                break
            trees[ x ].append( y )
            j += 1
        i += 1
    #---------------------------------------------------------------------------------------------------


    return tuple( trees.values() )

def label_edge( E , d_tab ):
    
    E_list = list( E )
    E_list.sort()

    s_fun = lambda x : d_tab[ x ][ START ]
    e_fun = lambda x : d_tab[ x ][ END ]
    
    print( "\nEdge labeling\n" )
    for u , v in E_list:

        label = "CRUZAMENTO"
        if s_fun( u ) < s_fun( v ) < e_fun( u ):
            label = "AVANÇO"
        elif s_fun( v ) < s_fun( u ) < e_fun( v ):
            label = "RETORNO"

        s = "{} -> {} : {}".format( u , v , label )
        print( s )


def SCC( V , E ):
   
    '''
    soluçaõ descrita no inicio do arquivo
    '''

    dept = search_in_depth( V , E )

    E_t = transpose_graph( E )
    m = max( dept[ u ][ END ] for u in dept ) + 1
    end_fun = lambda x : m - dept[ x ][ END ]
    dept_prime = search_in_depth( V , E_t , end_fun )
    
    return forest( dept_prime )

def graphs_from_file( path ):
    
    fptr = open( path , "r" )
    num_g = int( fptr.readline() ) 
    for i in range( num_g ):
        n = int( fptr.readline())
        V , E = set() , set()
        for j in range( n ):
            u , v = fptr.readline().split()

            V.add( u )
            V.add( v )

            tup = ( u , v )
            E.add( tup )

        yield V , E

    fptr.close()


