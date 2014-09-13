
aut := function(G, n)
return (AsGroup(Filtered(SymmetricGroup(n), f -> Set(G) = Set(G,e->e^f))));
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

