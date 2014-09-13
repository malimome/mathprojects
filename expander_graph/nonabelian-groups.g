
listofnonabelian := function(n)
local i,j,nagrp;
nagrp :=[];

for i in AllSmallGroups(n) do
  if (IsAbelian(i)=false) then
    Add(nagrp, i);
  fi;
od;

return nagrp;
end;

