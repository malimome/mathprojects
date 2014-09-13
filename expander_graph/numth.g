znOrders:=function(n, b)
  local m, g;
  g:= PrimeResidues(n); 
  Print("Elemes:\t");
  if (b = 0) then
    for m in Elements(g) do
      Print(m, ":",OrderMod(m, n), "\t");
    od;
  else
    for m in Elements(g) do
      Print(m, "\t");
    od;
    Print("\nOrders:\t");
    for m in Elements(g) do
      Print(OrderMod(m, n), "\t");
    od;
  fi;
  Print("\nSize Of G: ", Size(g),"\t\t", "Lambda(n): " ,Lambda(n), "\n" , "Elements:\t\n");
    
end;


powersofPrimElem:=function(n)
	local m,g;
	g := PrimitiveRootMod(n);
	for m in [1..Phi(n)] do
		Print(m, ":", g^m mod n, "\t");
	od;
	Print("\n");

end;

squarePowersofElem:=function(n)
	local m,g;
	g := PrimitiveRootMod(n);
	for m in [1..(n-1)/2] do
		Print(m, ":", m^2 mod n, "\t");
	od;
	Print("\n");

end;


