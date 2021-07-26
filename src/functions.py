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
    essa lista é ordenada crescentemente dada alguma função
    '''

    tab = { u:[] for u in V }
    for u , v in E:
        tab[ u ].append( v )

    for u in V:
        tab[ u ].sort( key = key_s, reverse = True )
    return tab

def print_adj( adj ):
    pass

def depth_tab( adj ):
    
    seq = [ -1 ]*3
    dtab = { u : seq.copy() for u in V }

    stack = []
    unvisited = V.copy()
    global clock
    clock = -1

    def mark_visit( v ):

        global clock
        clock += 1
        dtab[ v ][ START ] = clock
        dtab[ v ][ DEPTH ] = len( stack )
        stack.append( v )
        if dtab[ v ][ DEPTH ]:
            unvisited.remove( v )

    while unvisited:

        v = unvisited.pop()
        mark_visit( v )

        while stack:

            u = stack.pop()
            if not adj[ u ]:
                clock += 1
                dtab[ u ][ END ] = clock
                continue

            stack.append( u )
            v = adj[ u ].pop()
            if not( v in unvisited ):
                continue

            mark_visit( v )

    return dtab

def print_dtab( dtab ):
    pass

def search_in_depth(  V , E , key_s = lambda x : x ):
    
    adj = adj_tab( V , E , key_s )
    return depth_tab( adj )

def transpose_graph( E ):
    return { ( v , u ) for u , v in E }

def forest( d_tab ):
    
    V = set( d_tab.keys() )
    s_fun = lambda x : d_tab[ x ][ START ]
    e_fun = lambda x : d_tab[ x ][ END ]
    d_fun = lambda x : d_tab[ x ][ DEPTH ]
    
    V1 = [ x for x in V if d_fun( x ) == 0 ]
    V2 = list( V - set( V1 ) )

    V1.sort( key = s_fun )
    V2.sort( key = s_fun )
    components = { x: [x] for x in V1 }

    i , j = 0 , 0
    while i < len( V1 ):
        
        x = V1[ i ]
        ex = e_fun( x )

        while j < len( V2 ):

            y = V2[ j ]
            sy = s_fun( y )

            if not ( sy < ex ):
                break

            components[ x ].append( y )
            j += 1
        i += 1
    return tuple( components.values() )

# returns the set of strongly connected components of a Di-Graph
def SCC( V , E ):

    dept = search_in_depth( V , E )

    E_t = transpose_graph( E )
    m = max( dept[ u ][ END ] for u in dept ) + 1
    end_fun = lambda x : m - dept[ x ][ END ]
    dept_prime = search_in_depth( V , E_t , end_fun )
    
    return forest( d_tab )

# yields graphs from a source file ----------------------------
def graphs_from_file( path ):
    
    fptr = open( path , "r" )
    num_g = int( fptr.readline().split() ) # num of graphs
    for i in range( num_g ):
        
        n = fptr.readline().split()
        V = set( fptr.readline().split() )

        n = int( fptr.readline())
        E = set()
        for i in range( n ):
            tup = tuple( fptr.readline().split() )
            E.add( tup )

        yield V , E

    fptr.close()


