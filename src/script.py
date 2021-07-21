from functions import *
import os

#print( os.getcwd() )
if __name__ == "__main__":

    path = ""
    for V , E in graphs_from_file( path ):

        print( "-"*100 )
        print( "\nAdjency Table\n" )
        tab = adj_tab( V , E )
        print_adj( tab )

        print( "\nDepth Table\n" )
        tab = depth_tab( tab )
        print_dtab( tab )

        print( "\nStrongly Connected Components\n" )
        for comp in SCC( V , E ):
            comp.sort()
            print( *comp )


