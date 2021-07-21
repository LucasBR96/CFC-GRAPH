START = 0
END   = 1
DEPTH = 2

def adj_tab( V , E , key_s = lambda x : x ):

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
    components = { x: set( [x] ) for x in V1 }

    i , j = 0 , 0
    while i < len( V1 ):
        
        x = V1[ i ]
        ex = e_fun( x )

        while j < len( V2 ):

            y = V2[ j ]
            sy = s_fun( y )

            if not ( sy < ex ):
                break

            components[ x ].add( y )
            j += 1
        i += 1
    return map( list, components.values() )

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

        n = int( fptr.readline().split() )
        E = set()
        for i in range( n ):
            tup = tuple( fptr.readline().split() )
            E.add( tup )

        yield V , E

    fptr.close()


