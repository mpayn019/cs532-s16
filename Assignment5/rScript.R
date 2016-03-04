library(igraph)
g <- read.graph("karate.gml", format="gml")

print('Edges will be deleted in the following order : ')
	
repeat{
	edges_betweenness <- edge.betweenness(g)
	max_value <- max(edges_betweenness)
	edge_to_delete <- match(c(max_value),edges_betweenness)
	print(paste(paste(paste(get.edgelist(g)[edge_to_delete,1]," -> "),get.edgelist(g)[edge_to_delete,2]),paste("  -- Betweenness = ",max_value)))
	g <- delete.edges(g, E(g, P=c(get.edgelist(g)[edge_to_delete,1],get.edgelist(g)[edge_to_delete,2])))
	cluster_no <- clusters(g)['no']

	if(cluster_no == 5)

	{
		break
	}
	cs <- leading.eigenvector.community(g, steps=1)
	V(g)$color <- ifelse(cs$membership==1, "pink", "green")
	scale <- function(v, a, b) {
  	v <- v-min(v) ; v <- v/max(v) ; v <- v * (b-a) ; v+a
	}
	#V(g)$size <- scale(abs(cs$eigenvectors[[1]]), 10, 20)
	E(g)$color <- "grey"
	E(g)[ V(g)[ color=="pink" ] %--% V(g)[ color=="green" ] ]$color <- "red"
	tkplot(g, layout=layout.kamada.kawai, vertex.label.font=2)
}

cs <- leading.eigenvector.community(g, steps=1)
V(g)$color <- ifelse(cs$membership==1, "pink", "green")
scale <- function(v, a, b) {
v <- v-min(v) ; v <- v/max(v) ; v <- v * (b-a) ; v+a
}
V(g)$size <- scale(abs(cs$eigenvectors[[1]]), 10, 20)
E(g)$color <- "grey"
E(g)[ V(g)[ color=="pink" ] %--% V(g)[ color=="green" ] ]$color <- "red"
tkplot(g, layout=layout.kamada.kawai, vertex.label.font=2)
