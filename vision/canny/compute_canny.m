function compute_canny


conf.calDir = '/Users/eliabruni/data/esp/test/input/esp_sample' ;
conf.dataDir = '/Users/eliabruni/data/esp/test/ouput/canny' ;
conf.autoDownloadData = false ;
conf.numTrain = 9 ;
conf.numClasses = 1 ;
conf.numWords = 4 ;
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
    
    hists{ii - (iter * blockSize)} = canny(im);
    
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
  tmpHists = cat(2, hists{:}) ;
  tmpHists = rot90(tmpHists) ;

  eval(['ZZZZZZZZZZZZZZZZZZZZ' '= tmpHists;' ]) ;
  % hists = cat(2, hists{:}) ;
  conf.prefix = 'ZZZZZZZZZZZZZZZZZZZZ' ;
  conf.histPath = fullfile(conf.dataDir, [conf.prefix '.mat']) ;
  save(conf.histPath,'ZZZZZZZZZZZZZZZZZZZZ') ;


% -------------------------------------------------------------------------
function im = standardizeImage(im)
% -------------------------------------------------------------------------

if size(im,1) > 480, im = imresize(im, [480 NaN]) ; end



