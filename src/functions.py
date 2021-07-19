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

# returns the set of strongly connected components of a Di-Graph
def SCC( V , E ):

    dept = search_in_depth( V , E )

    E_t = transpose_graph( E )
    m = max( dept[ u ][ END ] for u in dept ) + 1
    f = lambda x : m - dept[ x ]
    dept_prime = search_in_depth( V , E_t , f )

    pass

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


