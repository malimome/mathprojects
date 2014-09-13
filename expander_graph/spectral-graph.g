#Read("/opt/gap-programs/spectral-graph.g");
RequirePackage("Grape");

grpAdjacencyMat := function(G)
	return (CollapsedAdjacencyMat(Group(()), G));
end;

grpEigenvalues := function(G)
	return (Eigenvalues(Rationals, grpAdjacencyMat(G)));
end;

grpEigenvectors := function(G)
	return (Eigenvectors(Rationals, grpAdjacencyMat(G)));
end;

grpPetersonGraph := function()
	return (Graph( SymmetricGroup(5), [[1,2]], OnSets,function(x,y) return Intersection(x,y)=[]; end));
end;

showinfo := function(grp)
  Print ("Generators : ", GeneratorsSmallest(grp), "\n");
  Print ("Size of automorph group : ", Size(grp), "\n");
  Print ("Center of group : ", Centre(grp), "\n");
  Print ("Elements of group : ", Elements(grp), "\n");
end;

findiso := function(g1, g2, autg1)
local i,j,k,t;
  for i in Elements(autg1) do
    k:=[];
    t:=false;
    for j in g1 do
      Add(k, j^i);
      #if (not(j^i in g2)) then
       # t:=true;
	#break;
      #fi;
    od;
    if (Set(k)=Set(g2)) then
      Print ("found isomorphism with :" , i, " \n");
    fi;
    #if (t=false) then
      Print ( k, "----->",i, "\n\n");
    #  return t;
    #fi;
  od;
end;

Read("fundamental.g");
Cgraph:=ComplementGraph(JohnsonGraph(7,2));;
F:=FundamentalRecordSimplicialComplex(Cgraph);;
G:=F.group; # the fundamental group
#<fp group on the generators [ _x1 ]>
Size(G);
Cgraph_cover:=CoveringGraph(Cgraph,G,F.edgeLabels,TrivialSubgroup(G));;
IsDistanceRegular(Cgraph_cover);
GlobalParameters(Cgraph_cover);
[ [ 0, 0, 10 ], [ 1, 3, 6 ], [ 2, 4, 4 ], [ 6, 3, 1 ], [ 10, 0, 0 ] ]



