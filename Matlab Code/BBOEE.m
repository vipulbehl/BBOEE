function [MinCost]= BBOEE(fhd,dim,PopSize,iters,lb,ub,varargin)
rand('state',sum(100*clock));

%Initilaizations
pmutate = 0.01; % initial mutation probability
Keep = 2; % elitism parameter: how many of the best habitats to keep from one generation to the next
EvolConst = 50; % Evolution Constant

% Initializing the parameters with default values
fit = zeros(1,PopSize);
EliteSolution = zeros(Keep,dim);
EliteCost = zeros(1,Keep);
Island = zeros(PopSize,dim);
mu = zeros(1,PopSize);
lambda1 = zeros(1,PopSize);
MinCost = zeros(1,iters);
Bestpopulation = zeros(1,dim);
partition = 20;
    

% Initalizing population
if length(lb)==1
    lb=repmat(lb,1,dim);
    ub=repmat(ub,1,dim);
end

lb=repmat(lb,PopSize,1);
ub=repmat(ub,PopSize,1);
population=lb+(ub-lb).*rand(PopSize,dim);
%disp(population)

%Check Bounds Clip
for i=1:PopSize
    temp = population(i,:);
    for j=1:dim
        temp2=temp(j);
        if(temp2>ub)
            temp2=ub;
        end
        if(temp2<lb)
            temp2= lb;
        end
        temp(j)=temp2;
    end
    population(i,:) = temp;
end
        
%Calculation of fitness
fit=feval(fhd,population',varargin{:});

% Calculation of Growth and Decline Rate
for i=1:PopSize
    % Decline Rate
    mu(i) = (1 - ((i+1)/PopSize)) + EvolConst/(i+1);
    % Growth Rate
    lambda1(i) = ((i+1)/PopSize)*((i+1)*(PopSize-(i+1))/PopSize.^2) + 2*((PopSize*(i+1)).^0.5);
end

% Defining the loop
for l=1:iters  
    selected = 0;
    selectedList = [];
    while selected < partition
        index = randi([1 PopSize]);
        if ~ismember(index,selectedList)
            selectedList = [selectedList,index];
            selected = selected + 1;
        end
        
    end
    
    % Defining the Elite Solutions
    for j=1:Keep
        EliteSolution(j,:)=population(j,:);
        EliteCost(j)=fit(j);
    end

    % Performing Migration operation on Group A
    for k=1:PopSize
        if ~ismember(k,selectedList)
            for j=1:dim
                if rand() < lambda1(k)
                    RandomNum = rand()*sum(mu);
                    Select = mu(1);
                    SelectIndex = 1;
                    while (RandomNum > Select) && (SelectIndex < (PopSize-1))
                     SelectIndex = SelectIndex + 1;
                     Select = Select + mu(SelectIndex);
                    end
                    r = randi([1 PopSize]);
                    while r == k || r == SelectIndex
                        r = randi([1 PopSize]);
                    end
                     Island(k,j) = population(SelectIndex,j);
                else
                    Island(k,j) = population(k,j);
                end
            end
        end
    end
    
    % Performing Migration operation on Group B
    selectedList = selectedList(randperm(partition));
    for k=1:partition
        for j=1:dim
            if rand() < lambda1(k)
                if k==1
                    previous = partition;
                    next1 = k+1;
                elseif k == partition
                    previous = k-1;
                    next1 = 1;
                else
                    previous = k-1;
                    next1 = k+1;
                end
                
                if mu(selectedList(previous)) > mu(selectedList(next1))
                    SelectIndex = selectedList(previous);
                else
                    SelectIndex = selectedList(next1);
                end
                
                if rand() < mu(SelectIndex)
                    r = randi([1 PopSize]);
                    while r == k || r == SelectIndex
                        r = randi([1 PopSize]);
                    end
                    tempRange = population(SelectIndex,j)-population(r,j);
                    tempRand = -tempRange+rand(1,1)*(2*tempRange);
                    Island(k,j) = population(SelectIndex,j) + tempRand;
                else
                    Island(k,j) = population(k,j);
                end
            else
                Island(k,j) = population(k,j);
            end
        end
    end
    
   % Performing Mutation
%       for k=1:PopSize
%           for parnum=1:dim
%               if pmutate > rand
%                   tempRand = lb + (ub-lb) * rand;
%                   Island(k,parnum) = tempRand(1,1);
%               end
%           end
%       end
      
      
    % Mutation
    PopA = PopSize*(3/4);
    for k=1:PopA
          for parnum=1:dim
              if pmutate > rand
                  tempRand = median(population(k,:));
                  Island(k,parnum) = tempRand(1,1);
              end
          end
    end
     
    % Part B mutation
    for k=PopA:PopSize
        randIndex = randi([1 dim]);
        tempRand = median(population(k,:));
        Island(k,randIndex) = tempRand(1,1);
    end
      

    % Performing the bound checking
    for i=1:PopSize
        temp = Island(i,:);
        for j=1:dim
            temp2=temp(j);
            if(temp2>ub)
                temp2=ub;
            end
            if(temp2<lb)
                temp2= lb;
            end
            temp(j)=temp2(1,1);
        end
        Island(i,:) = temp;
    end
    

    % Replace the habitats with their new versions.
    for k=1:PopSize
        population(k,:) = Island(k,:);
    end

    %Calculate objective function for each individual
    fit=feval(fhd,population',varargin{:});
    
    % Sort the fitness
    fitness_sorted=sort(fit')';

    % Sort the population on fitness
    [Out,I] = sort(fit,2);
    population=population(I',:);

    % Replacing the individual of population with EliteSolution
    for k=1:Keep
        population((PopSize-1)-k,:) = EliteSolution(k,:);
        fit((PopSize-1)) = EliteCost(k);
    end

    % Removing the duplicate individuals
    population = ClearDuplicates(population,PopSize,dim,ub,lb);

    %Calculate objective function for each individual
    fit=feval(fhd,population',varargin{:});

    % Sort the fitness
    fitness_sorted=sort(fit);

    % Sort the population on fitness
    [Out,I] = sort(fit,2);
    population=population(I',:);

    % Saving the best individual
    MinCost(l) = fit(1);
    Bestpopulation=population(1,:);
    gBestScore=fit(1);
    
    % Displaying the best fitness of each iteration
    fprintf('Iteration: %i Best Fitness: %i\n',l,gBestScore);
    
    end
end