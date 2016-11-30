import os
#generar gif
## EDITAR DIRECTORIO
actual= 'TESTING'
directorio='./' + actual

directorio_clusters=directorio+'/clusters'
directorio_complexes=directorio+'/complexes'
directorio_imagenes=directorio+'/images'

delta_g = []
for file in os.listdir(directorio_clusters):
	f = open(directorio_clusters+'/'+file, 'r')
	for line in f:
		if line.startswith("* deltaG: "):
			delta_g.append([file,line[10:][:-1]])
			break
	f.close()

delta_g=sorted(delta_g, key=lambda delta_g: delta_g[1], reverse=True)

import __main__
__main__.pymol_argv = ['pymol','-qc'] # Pymol: quiet and no GUI
from time import sleep
import pymol
pymol.finish_launching()
indice=0

for dg in delta_g:
	f = open(directorio_clusters+'/'+dg[0], 'r')
	cluster=''
	cluster_rank=''
	
	for line in f:
		if line.startswith("* Cluster: "):
			cluster=line[11:][:-1]
		if line.startswith("* ClusterRank: "):
			cluster_rank=line[15:][:-1]
			
	f.close()
	pdb_file=directorio_complexes+'/complex.'+cluster+'_'+cluster_rank+'.pdb'
        # Load Structures
        pymol.cmd.reinitialize()
        pymol.cmd.load(pdb_file)
        pymol.cmd.bg_color('white')

	## EDITAR ROTACIONES
        pymol.cmd.rotate('x','90')
        pymol.cmd.rotate('y','90')
        pymol.cmd.rotate('z','0')

        pymol.cmd.show_as('ribbon','complex.'+cluster+'_'+cluster_rank)
	pymol.cmd.color('red','complex.'+cluster+'_'+cluster_rank)
        pymol.cmd.show_as('spheres', 'resn LIG')
	pymol.cmd.color('blue','resn LIG')
	
	print('Imprimiendo imagen '+str(indice+1))
        pymol.cmd.png(directorio_imagenes+'/imagen_'+str(indice+1)+'.png')
        
	sleep(0.5) # (in seconds)
        indice+=1

	## EDITAR NUMERO DE IMAGENES QUE RENDEREA
	if indice==10:
		break
        
# Get out!
pymol.cmd.quit()

