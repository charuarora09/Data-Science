#Author: Charu Arora and Rohit Bhattacharjee
#install.packages("h2o")

#packages required
library("h2o")
require("h2o")

#location of the input file
dir <- dirname(parent.frame(2)$ofile)
setwd(dir)
localH2O = h2o.init(nthread=2,max_mem_size = "1G")
h2o.removeAll()

#read data file into package
cat("\nReading File")
df <- h2o.importFile(path = normalizePath("sample.csv"))

#Principal Component Analysis
df.new=h2o.scale(df[,2:370])
cat("\nPCA")
df.pca=h2o.prcomp(df.new,k=10)
features_pca=h2o.predict(df.pca,df,num_pc=10)
dat=h2o.cbind(features_pca,df[,ncol(df)])

#Splitting Data into Training, Validation and Testing Sets

splits <- h2o.splitFrame(dat, c(0.6,0.2), seed=1234)
train  <- h2o.assign(splits[[1]], "train.hex") # 60%
valid  <- h2o.assign(splits[[2]], "valid.hex") # 20%
test   <- h2o.assign(splits[[3]], "test.hex")  # 20%

response="TARGET"
predictors=setdiff(names(dat[,1:10]),response)


valid$TARGET <- as.factor(valid$TARGET)
train$TARGET <- as.factor(train$TARGET)

#Neutral Network
cat("\nTraining Neural Network")
m5 <- h2o.deeplearning(
  model_id="dl_model_first", 
  training_frame=train, 
  validation_frame=valid,   ## validation dataset: used for scoring and early stopping
  x=predictors,
  y="TARGET",
  activation="Maxout",
  adaptive_rate = TRUE,
  hidden=c(500,500),       ## default: 2 hidden layers with 200 neurons each
  epochs=100,
  stopping_metric = "MSE",
  stopping_tolerance = 0.01,
  stopping_rounds = 2,
  nfolds = 10
  
)
cat("\nPredicting Neural Network")
pred=h2o.predict(m5,test)
test$Accuracy <- pred$predict == test$TARGET
dnn_acc=mean(test$Accuracy)

cat("\nTraining GBM")


#Gradient Boosting
gbm1=h2o.gbm(
  training_frame = train,
  validation_frame = valid,
  x=predictors,
  y=response,
  ntrees = 200,
  learn_rate = 0.3,
  max_depth = 10,
  sample_rate = 0.7,
  col_sample_rate = 0.7,
  stopping_rounds = 2,
  stopping_tolerance = 0.01,
  model_id = "gbm_model_1",
  seed=2000000,
  nfolds = 10
  
  
)
cat("\nTraining RF")


#Random Forests
RF1= h2o.randomForest(
  training_frame = train,
  validation_frame = valid,
  x=predictors,
  y=response,
  ntrees=200,
  stopping_rounds = 2,
  score_each_iteration = T,
  seed=1000000,
  nfolds=10
)

cat("\nPredicitng RF")
pred_RF=h2o.predict(RF1,test)
cat("\nPredicitng GBM")
pred_GBM=h2o.predict(gbm1,test)

acc_RF=mean(pred_RF$predict==test$TARGET)
acc_GBM=mean(pred_GBM$predict==test$TARGET)

cat("\n Accuracy of Deep Neural Net:",dnn_acc)
cat("\n Accuracy of Gadient Boosting:",acc_GBM)
cat("\n Accuracy of Random Forest:",acc_RF)


h2o.shutdown(prompt = FALSE)
