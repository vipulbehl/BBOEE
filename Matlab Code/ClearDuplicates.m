function [Population] = ClearDuplicates(Population, PopSize, dim, MaxParValue, MinParValue)

for i=1:PopSize
    Chrom1 = sort(Population(i,:)')';
    for j=i+1:PopSize
        Chrom2 = sort(Population(j,:)')';
        if Chrom1 == Chrom2
            parnum = ceil(dim*rand);
            tempVal = MinParValue + (MaxParValue - MinParValue) * rand;
            Population(j,parnum) = tempVal(1,1);
        end
    end
end
return;