function compute_textons

% Add texton path where to find anigauss
%path(path, '/home/elia.bruni/google/data_sets/mir/1m/scripts/texton')


conf.calDir = '/Users/eliabruni/data/esp/test/input' ;
conf.dataDir = '/Users/eliabruni/data/esp/test/ouput/texton' ;
conf.autoDownloadData = false ;
conf.numTrain = 4 ;
conf.numTest = 4 ;
conf.numClasses = 1 ;
conf.numWords = 256 ;
conf.numSpatialX = 1 ;
conf.numSpatialY = 1 ;
conf.quantizer = 'kdtree' ;
%conf.phowOpts = {'Verbose', 2, 'Step', 5} ;

conf.prefix = 'baseline' ;
conf.randSeed = 1 ;


conf.vocabPath = fullfile(conf.dataDir, [conf.prefix '-vocab.mat']) ;
conf.modelPath = fullfile(conf.dataDir, [conf.prefix '-model.mat']) ;
conf.resultPath = fullfile(conf.dataDir, [conf.prefix '-result']) ;

randn('state',conf.randSeed) ;
rand('state',conf.randSeed) ;
vl_twister('state',conf.randSeed) ;

% --------------------------------------------------------------------
%                                                           Setup data
% --------------------------------------------------------------------
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
model.numSpatialX = conf.numSpatialX ;
model.numSpatialY = conf.numSpatialY ;
model.quantizer = conf.quantizer ;
model.vocab = [] ;

% --------------------------------------------------------------------
%                                                     Train vocabulary
% --------------------------------------------------------------------


if ~exist(conf.vocabPath) 
  
  singleDescrs = {} ;
  
  for ii = 1:conf.numTrain 
      
    im = imread(fullfile(conf.calDir, images{ii}));
    im = standarizeImage(im) ;
    descrs = MR8fast(im);
    singleDescrs{ii} = vl_colsubset(single(descrs), length(descrs)) ;
    
  end
  
  % Quantize the descriptors to get the visual words
  singleDescrs = vl_colsubset(cat(2, singleDescrs{:}), 10e4) ;
  singleDescrs = single(singleDescrs) ;
  
  vocab = vl_kmeans(singleDescrs, conf.numWords, 'verbose','algorithm', 'lloyd') ;
  
  save(conf.vocabPath, 'vocab') ;
else
  load(conf.vocabPath) ;
end

model.vocab = vocab ;

if strcmp(model.quantizer, 'kdtree')
  model.kdtree = vl_kdtreebuild(vocab) ;
end
  
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
    if mod(ii, 100) == 0
      fprintf('Processing %s (%.2f %%)\n', images{ii}, 100 * ii / length(images)) ;
    end

    im = imread(fullfile(conf.calDir, images{ii})) ;
    hists{ii - (iter * blockSize)} = getImageDescriptor(model, im);


    if mod(ii, blockSize) == 0
        tmpHists = cat(2, hists{:}) ;
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
  tmpHists = cat(2, hists{:}) ;
  tmpHists = rot90(tmpHists) ;

  eval(['ZZZZZZZZZZZZZZZZZZZZ' '= tmpHists;' ]) ;
  % hists = cat(2, hists{:}) ;
  conf.prefix = 'ZZZZZZZZZZZZZZZZZZZZ' ;
  conf.histPath = fullfile(conf.dataDir, [conf.prefix '.mat']) ;
  save(conf.histPath,'ZZZZZZZZZZZZZZZZZZZZ') ;





% -------------------------------------------------------------------------
function im = standarizeImage(im)
% -------------------------------------------------------------------------

% im = rgb2gray(im) ;
im = im2bw(im) ;

if size(im,1) > 480, im = imresize(im, [480 NaN]) ; end

% -------------------------------------------------------------------------
function hist = getImageDescriptor(model, im)
% -------------------------------------------------------------------------

im = standarizeImage(im) ;
%width = size(im,2) ;
%height = size(im,1) ;
numWords = size(model.vocab, 2) ;

% get Textons
descrs = MR8fast(im);

% quantize appearance
switch model.quantizer
  case 'vq'
    [drop, binsa] = min(vl_alldist(model.vocab, single(descrs)), [], 1) ;
  case 'kdtree'
    binsa = double(vl_kdtreequery(model.kdtree, model.vocab, ...
                                  single(descrs),...
                                  'MaxComparisons', 15)) ;
end


bins = sub2ind([model.numSpatialY, model.numSpatialX, numWords], ...
               binsa) ;


hist = zeros(model.numSpatialY * model.numSpatialX * numWords, 1) ;
hist = vl_binsum(hist, ones(size(bins)), bins) ;
hist = single(hist / sum(hist)) ;
