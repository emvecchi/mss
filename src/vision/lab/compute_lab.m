function compute_lab

conf.calDir = '/Users/eliabruni/data/esp/test/input/esp_sample' ;
conf.dataDir = '/Users/eliabruni/data/esp/test/ouput/lab' ;
conf.numClasses = 1 ;

conf.prefix = 'baseline' ;
conf.randSeed = 1 ;

conf.modelPath = fullfile(conf.dataDir, [conf.prefix '-model.mat']) ;
conf.resultPath = fullfile(conf.dataDir, [conf.prefix '-result']) ;


% --------------------------------------------------------------------
%                                                           Setup data
% --------------------------------------------------------------------
classes = dir(conf.calDir) ;
classes = classes([classes.isdir]) ;
classes = {classes.name} ;

colorNodes = load('/Users/eliabruni/data/farhadi/feature_extraction/colorClusters.mat') ;

images = {} ;
imageClass = {} ;
for ci = 1:length(classes)
  ims = dir(fullfile(conf.calDir, classes{ci}, '*.jpg'))' ; 
  ims = cellfun(@(x)fullfile(classes{ci},x),{ims.name},'UniformOutput',false) ;
  images = {images{:}, ims{:}} ;
  imageClass{end+1} = ci * ones(1,length(ims)) ;
end
imageClass = cat(2, imageClass{:}) ;
model.classes = classes ;

% --------------------------------------------------------------------
%                                           Compute spatial histograms
% --------------------------------------------------------------------

  blockSize = 1000 ;
  listLength = length(images)/blockSize ;
  histsNames = [] ;
  for jj = 1:listLength
     histsNames{jj} = randseq(30) ;
  end
  histsNames = sort(histsNames) ;


  hists = {} ;
  iter = 0 ;
  for ii = 1:length(images)
    if mod(ii, 10) == 0
      fprintf('Processing %s (%.2f %%)\n', images{ii}, 100 * ii / length(images)) ;
    end

    im = imread(fullfile(conf.calDir, images{ii}));
    im = standardizeImage(im) ;
    
    hists{ii - (iter * blockSize)} = getColorImage(im, colorNodes);
    
    if mod(ii, blockSize) == 0
        tmpHists = cat(1, hists{:}) ;
        tmpHists = rot90(tmpHists) ;
        histName = histsNames{ii/blockSize} ;
        eval([histName ' = tmpHists;' ]) ;
        conf.prefix = histsNames{ii/blockSize} ;
        conf.histPath = fullfile(conf.dataDir, [conf.prefix '.mat']) ;
        save(conf.histPath, strcat(histsNames{ii/blockSize})) ;
        eval([histName ' = {};' ]) ;
        hists = {} ;
        tmpHists = {} ;
        histName = {} ;
        iter = iter + 1 ;
    end
  end
  
  tmpHists = cat(1, hists{:}) ;
  tmpHists = rot90(tmpHists) ;

  eval(['ZZZZZZZZZZZZZZZZZZZZ' '= tmpHists;' ]) ;
  % hists = cat(2, hists{:}) ;
  conf.prefix = 'ZZZZZZZZZZZZZZZZZZZZ' ;
  conf.histPath = fullfile(conf.dataDir, [conf.prefix '.mat']) ;
  save(conf.histPath,'ZZZZZZZZZZZZZZZZZZZZ') ;
  

% -------------------------------------------------------------------------
function im = standardizeImage(im)
% -------------------------------------------------------------------------

im = im2double(im) ;
if size(im,1) > 480, im = imresize(im, [480 NaN]) ; end

% -------------------------------------------------------------------------
function counts = getColorImage(im, colorNodes)
% -------------------------------------------------------------------------

if(size(im,3)==3)
    [L, a, b] = rgb2lab(im);

    %L = (L - mean(L(:)));% / std(L);
    %a = (a - mean(a(:)));% / std(a);
    %b = (b - mean(b(:)));% / std(b);        

    feat = single(cat(2, L(:)/2, a(:), b(:))/100); 

    %idx = getNearestHierarchy(feat, colorNodes);
    % leafnum = zeros(numel(colorNodes), 1);
    % leafnum([colorNodes.isleaf]) = 1:sum([colorNodes.isleaf]);
    % idx = leafnum(idx);
    
    idx = getNearest(feat, colorNodes.centers);

    colorim = reshape(idx, [size(im, 1) size(im, 2)]);
else 
    colorim = [] ; 
end

% Count how many times each cluster has been encountered in the image.
counts = zeros(1,128) ;
for i = 1:numel(colorim)
    counts(colorim(i)) = counts(colorim(i)) + 1 ;
end
% Normalization
counts = single(counts/sum(counts)) ;

% -------------------------------------------------------------------------
function idx = getNearest(data, centers)
% -------------------------------------------------------------------------

if 0 && exist('getNearest_mex', 'file')
    idx = getNearest_mex(int32(size(data, 1)), int32(size(data, 2)), ...
        int32(size(centers, 1)), double(data)', double(centers)');
    idx = idx(:);
else

    if 0   
        idx = kdtreeidx(double(centers), double(data));
    end
        
    centers = centers';
    centerssq = sum(centers.^2, 1);

    idx = zeros(size(data, 1), 1);
    for k = 1:size(data, 1)
        dist = centerssq - 2*data(k, :) * centers;
        [tmp, idx(k)] = min(dist);
    end

end
