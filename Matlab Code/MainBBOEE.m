% mex cec17_func.cpp -DWINDOWS
func_num=1;
D=[10 30 50 100];
Xmin=-100;
Xmax=100;
pop_size=100;
iter_max=100;
runs=1;
fhd=str2func('cec17_func');
allFunc = zeros(30,iter_max);
results = zeros(30,5);
fileNames = ["10dim","30dim","50dim","100dim"];

% Defining F(x*) constants
fx = [100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2100 2200 2300 2400 2500 2600 2700 2800 2900 3000];

% Loop for various dimensions
for k=1:4
    % Loop for cec functions
    for i=1:30
        func_num=i;
        for j=1:runs
            fprintf('Function: %i Run: %i \n',i,j);
            [MinCost]= BBOEE(fhd,D(k),pop_size,iter_max,Xmin,Xmax,func_num) - fx(i);
            allFunc(i,:) = MinCost;
            results(i,1) = min(MinCost); % Min Value
            results(i,2) = max(MinCost); % Max Value
            results(i,3) = median(MinCost); % Meadian
            results(i,4) = mean(MinCost); % Mean
            results(i,5) = std(MinCost); % Standard Deviation
        end
    end
    save(fileNames(k),'results');
end