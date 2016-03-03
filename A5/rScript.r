library(igraph) #loads graph
g <- read.graph("karate.gml", format="gml") #loadnetworkdata

print('Edges will be deleted in the following order : ')
	
repeat{
	edges_betweenness <- edge.betweenness(g) #detects edge betweenness
	max_value <- max(edges_betweenness) #find the max
	edge_to_delete <- match(c(max_value),edges_betweenness) #removes the edge max
	print(paste(paste(paste(get.edgelist(g)[edge_to_delete,1]," -> "),get.edgelist(g)[edge_to_delete,2]),paste("  -- Betweenness = ",max_value))) #prints the edge with the max betweeness
	g <- delete.edges(g, E(g, P=c(get.edgelist(g)[edge_to_delete,1],get.edgelist(g)[edge_to_delete,2]))) 	#stops the graph and makes 2 clusters
	cluster_no <- clusters(g)['no']

	if(cluster_no == 5)

	{
		break
	}
	cs <- leading.eigenvector.community(g, steps=1)
	V(g)$color <- ifelse(cs$membership==1, "cornflowerblue", "coral")
	scale <- function(v, a, b) {
  	v <- v-min(v) ; v <- v/max(v) ; v <- v * (b-a) ; v+a
	}
	#V(g)$size <- scale(abs(cs$eigenvectors[[1]]), 10, 20)
	E(g)$color <- "deeppink"
	E(g)[ V(g)[ color=="cornflowerblue" ] %--% V(g)[ color=="coral" ] ]$color <- "midnightblue"
	tkplot(g, layout=layout.kamada.kawai, vertex.label.font=2)
}

cs <- leading.eigenvector.community(g, steps=1)
V(g)$color <- ifelse(cs$membership==1, "cornflowerblue", "coral")
scale <- function(v, a, b) {
v <- v-min(v) ; v <- v/max(v) ; v <- v * (b-a) ; v+a
}
V(g)$size <- scale(abs(cs$eigenvectors[[1]]), 10, 20)
E(g)$color <- "deeppink"
E(g)[ V(g)[ color=="cornflowerblue" ] %--% V(g)[ color=="coral" ] ]$color <- "midnightblue"
tkplot(g, layout=layout.kamada.kawai, vertex.label.font=2)
