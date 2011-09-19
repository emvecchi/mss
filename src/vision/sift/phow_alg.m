function phow_alg(low, high)

% PHOW_ALG 
% Color version SIFT descriptors are extracted on a regular grid with five pixels spacing, 
% at four multiple scales (10, 15, 20, 25 pixel radii), zeroing the low contrast ones. 
% Descriptors are then quantized on a number of visual words that we varied between 250 and 
% 2000 in steps of 250. We then computed a one-level 4x4 pyramid of spatial histograms, 
% consequently increasing the features dimensions 16 times, for a number that varies between 
% 4K and 32K, in steps of 4K.
%
% This program requires vlfeat toolbox (http://www.vlfeat.org/). 

run('VLFEATROOT/toolbox/vl_setup'')

conf.calDir = 'input_dir' ;
conf.dataDir = 'output_dir' ;
cnf.numTrain = 1000 ;
conf.numClasses = 1 ;
conf.numWords = 2000 ;
conf.numSpatialX = 4 ;
conf.numSpatialY = 4 ;
conf.quantizer = 'kdtree' ;
conf.phowOpts = {'Sizes', [10, 15, 20, 25], 'Step', 5, 'Color', true} ;
%conf.phowOpts = {'Step', 5} ;

conf.prefix = 'baseline' ;
conf.randSeed = 1 ;

conf.vocabPath = 'vocabulary_dir' ; 
%conf.vocabPath = fullfile(conf.dataDir, [conf.prefix '-vocab.mat']) ;
conf.modelPath = fullfile(conf.dataDir, [conf.prefix '-model.mat']) ;
conf.resultPath = fullfile(conf.dataDir, [conf.prefix '-result']) ;

randn('state',conf.randSeed) ;
rand('state',conf.randSeed) ;
vl_twister('state',conf.randSeed) ;

% --------------------------------------------------------------------
%                                                           Setup data
% --------------------------------------------------------------------
mkdir(conf.dataDir) ;
classes = dir(conf.calDir) ;
classes = classes([classes.isdir]) ;
classes = {classes.name} ;

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

model.classes = classes ;
model.phowOpts = conf.phowOpts ;
model.numSpatialX = conf.numSpatialX ;
model.numSpatialY = conf.numSpatialY ;
model.quantizer = conf.quantizer ;
model.vocab = [] ;

% --------------------------------------------------------------------
%                                                     Train vocabulary
% --------------------------------------------------------------------


if ~exist(conf.vocabPath) 
  
  % TODO:  
  % Preallocate singleDescrs for efficiency!
  singleDescrs = {} ;
  
  for ii = 1:conf.numTrain 
      
    im = imread(fullfile(conf.calDir, images{randsample(conf.numTrain,1)}));
 	im = standarizeImage(im) ;
    [drop, descrs] = vl_phow(im, model.phowOpts{:}) ;
    % singleDescrs{ii} = descrs(:,randsample(1:length(descrs), 1)) ; 
    % singleDescrs{ii} = vl_colsubset(single(descrs), 1) ;
	singleDescrs{ii} = vl_colsubset(single(descrs), length(descrs)) ;
  end
  
  % Quantize the descriptors to get the visual words
  
  singleDescrs = vl_colsubset(cat(2, singleDescrs{:}), 10e4) ;
  singleDescrs = single(singleDescrs) ;
  
  
  vocab = vl_kmeans(singleDescrs, conf.numWords, 'verbose','algorithm', 'elkan') ;
  save(conf.vocabPath, 'vocab') ;
  
else
  fprintf('Vocab found!') ;
  load(conf.vocabPath) ;
end

model.vocab = vocab ;

if strcmp(model.quantizer, 'kdtree')
  model.kdtree = vl_kdtreebuild(vocab) ;
end


% --------------------------------------------------------------------
%                                           Compute spatial histograms
% --------------------------------------------------------------------
  high = str2num(high) ;
  low = str2num(low) ;   
  intervalSize = 400000 ;
  % fprintf('low: ', num2str(low), ' high: ', num2str(high), ' intervaliSize: ',  num2str(intervalSize))
  blockSize = 2000 ;
  listLength = intervalSize/blockSize ;
  histsNames = [] ;
  for jj = 1:listLength
     histsNames{jj} = randseq(30) ;
  end
  histsNames = sort(histsNames) ;

  
  hists = {} ;
  for ii = low:high
    if mod(ii, 100) == 0
      fprintf('Processing %s (%.2f %%)\n', images{ii}, 100 * ii / intervalSize) ;
    end

    im = imread(fullfile(conf.calDir, images{ii})) ;
    hists{ii} = getImageDescriptor(model, im);
    
    
    if mod(ii, blockSize) == 0
        tmpHists = cat(2, hists{:}) ;
	tmpHists = rot90(tmpHists) ;
        histName = histsNames{(ii - (low-1)) / blockSize} ;
 	eval([histName ' = tmpHists;' ]) ;
        conf.prefix = histsNames{(ii - (low-1)) / blockSize} ;
        conf.histPath = fullfile(conf.dataDir, [conf.prefix '.mat']) ;
	save(conf.histPath, strcat(histsNames{(ii - (low-1)) / blockSize})) ; 
        eval([histName ' = {};' ]) ;
        hists = {} ;
        tmpHists = {} ;
        histName = {} ;
    end

  end
  tmpHists = cat(2, hists{:}) ;
  tmpHists = rot90(tmpHists) ;

  eval(['ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ' '= tmpHists;' ]) ;
  % hists = cat(2, hists{:}) ;
  conf.prefix = 'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ' ;
  conf.histPath = fullfile(conf.dataDir, [conf.prefix '.mat']) ;
  save(conf.histPath,'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ') ; 

% -------------------------------------------------------------------------
function im = standarizeImage(im)
% -------------------------------------------------------------------------

im = im2single(im) ;
if size(im,1) > 480, im = imresize(im, [480 NaN]) ; end

% -------------------------------------------------------------------------
function hist = getImageDescriptor(model, im)
% -------------------------------------------------------------------------

im = standarizeImage(im) ;
width = size(im,2) ;
height = size(im,1) ;
numWords = size(model.vocab, 2) ;

% get PHOW features
[frames, descrs] = vl_phow(im, model.phowOpts{:}) ;

% quantize appearance
switch model.quantizer
  case 'vq'
    [drop, binsa] = min(vl_alldist(model.vocab, single(descrs)), [], 1) ;
  case 'kdtree'
    binsa = double(vl_kdtreequery(model.kdtree, model.vocab, ...
                                  single(descrs), ...
                                  'MaxComparisons', 15)) ;
end
    
% quantize location
width = size(im, 2) ;
height = size(im, 1) ;

binsx = vl_binsearch(linspace(1,width,model.numSpatialX+1), frames(1,:)) ;
binsy = vl_binsearch(linspace(1,height,model.numSpatialY+1), frames(2,:)) ;

bins = sub2ind([model.numSpatialY, model.numSpatialX, numWords], ...
               binsy,binsx,binsa) ;
         

hist = zeros(model.numSpatialY * model.numSpatialX * numWords, 1) ;
hist = vl_binsum(hist, ones(size(bins)), bins) ;
hist = single(hist / sum(hist)) ;


