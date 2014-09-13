RequirePackage("grape");

commutingGraph:=function(g)
  local v;
  v:=Difference(AsSet(g),AsSet(Centre(g)));
  return (Graph(Group(()), v, OnPoints, function(x,y) return x<>y and x*y=y*x; end));
end;

noncommutingGraph:=function(g)
  local v;
  v:=Difference(AsSet(g),AsSet(Centre(g)));
  return (Graph(Group(()), v, OnPoints, function(x,y) return x<>y and x*y<>y*x; end,true));
end;

acentralGraph := function(g)
  local v,z;
  z:=AsSet(Centre(g));
  v:=Difference(AsSet(g), z);
  return (Graph(Group(()), v, OnPoints, function(x,y) return ((x<>y) and not(x*y in z)); end));
end;

centralGraph := function(g)
  local v,z;
  z:=AsSet(Centre(g));
  v:=Difference(AsSet(g), z);
  return (Graph(SmallGroup(1,1), v, OnPoints, function(x,y) return ((x<>y) and (x*y in z)); end));
end;
  
findexample:= function(n1,n2)
  local count,graphset,gr,graph,grpset,g, num1, num2;
  graphset:=[];
  #TODO:Generate all nonableian group with permutations, subgroup testing of sym(n) 
  for count in [n1..n2] do
    num1:=0;
    Print("Count: ", count, "\n");
    grpset := Elements(AllSmallGroups(count, IsAbelian, false));
    for g in grpset do
      Print("num1: ", num1, "\n");
      num1 := num1 +1;
      num2:=0;
      gr:=noncommutingGraph(g);
      for graph in graphset do
        num2:=num2+1;
        if (IsIsomorphicGraph(gr, graph)) then
	  Print("***Count : ", count, "\tnum1 = ", num1, "\tnum2 = ", num2, "\n");
	  Print("graph1: ", graph , "\n");
	  Print("graph2: ", gr, "\n");
	fi;
      od;
      Add(graphset, gr);
    od;
  od;
  
end;
      


