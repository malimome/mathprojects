check:=function(n)
  local i, t, g;
  Print ("test");
  
  for i in [1..n] do
    g:= DihedralGroup(IsPermGroup,i*2);
    
    for t in Elements(g) do
      if IsAbelian(Centralizer(g, t)) then
        Print("Group  ", i, "\n");
        Print(t, "\n");
      fi;
    od;
    
  od;
  end;

findel := function(n1,n2)
  local i,j,k,t,grpset,g,z;
  for i in [n1..n2] do
    grpset := AllSmallGroups(i, IsAbelian, false);
    for g in grpset do
      z:= Elements(Centre(g));
	  Print("Centre:", z, "\n");
      k:= Difference(Elements(g),z);
      for j in k do
        for t in k do
          if ((j*t in z) and (not (t*j in z))) then
	    Print("j:" , j, "\t  t:", t , "\n");
	  else
	    Print("j:" , j, "\t  t:", t , "\n");
	  fi;
        od;
      od;
    od;
  od;
end;

  
symdel := function(n1,n2)
  local i,j,k,t,grpset,g,z;
  for i in [n1..n2] do
    g := DihedralGroup(IsPermGroup,i*2);
      z:= Elements(Centre(g));
	  #Print("Centre:", z, "\n");
      k:= Difference(Elements(g),z);
	  #Print("kentre:", k, "\n");
      for j in k do
        for t in k do
          if ((j*t in z)) then
	    Print("@@@@@in@@@@j*t:=" , j*t, " = ", t*j,"\n");
	  else
	    Print("####out####j:" , j, "t:", t , "\n");
	  fi;
        od;
      od;
  od;
end;


