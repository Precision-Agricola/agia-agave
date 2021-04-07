# disease detection
# N X M matrix, detect spots, get the percentage of these spots


# básicamente el algoritmo determinístico para encontrar manchas es: por cada pixel P 
# en M X N, si P == <VALOR OBJETIVO> (valor objetivo sería el valor de las manchas,
# el blanco o cercano a blanco) Valida Mancha(P), la función valida mancha 
# realizaría 4 comparaciones, navegaría los pixeles hacia arriba, abajo, izquierda
# y derecha y si encuentra algún VALOR PLANTA regresa T, si regresa 4 Trues entonces 
# es un pixel de mancha e incrementa la cuenta de pixeles. 


plant.t <- read.csv("plantzero.csv",stringsAsFactors = F, header = F)
dim(plant.t)
colnames(plant.t)
str(plant.t)
# clean extra character 
plant.t[0,]
plant.t[1,1] <- 0
plant.t$V1 <- as.numeric(plant.t$V1)
class(plant.t)
plant.t.m <- as.matrix(plant.t)
dim(plant.t.m)
image(plant.t.m)

max(plant.t.m)
min(plant.t.m)

# resaltar para validar. 

plant.aux <- plant.t.m
plant.aux[1:10,1:10] <- 7
image(plant.aux)
# togetherness, thick barrier

existence.treshold <- 1
thickness <- 8
min.size <- 5   
desease.indicator <- 7

test.matrix <- matrix(rep(0,100),nrow=10,ncol=10)
test.matrix[4,4] <- 1 
test.matrix[5,4] <- 1 
test.matrix[6,4] <- 1 
test.matrix[7,4] <- 1 
test.matrix[4,7] <- 1 
test.matrix[5,7] <- 1 
test.matrix[6,7] <- 1 
test.matrix[7,7] <- 1 

test.matrix[4,5] <- 1 
test.matrix[4,6] <- 1 

test.matrix[7,5] <- 1 
test.matrix[7,6] <- 1 

image(test.matrix)

# clean function
validate.border <- function(row,column,matrix,direction,threshold,thickness) {
  if (direction=="U") {
    #print("up")
    vector <- matrix[,column]
    sign <- -1
    current <- row - 1
    limit <- current - proximity.nbr
  } else if (direction=="D") {
    #print("down")
    vector <- matrix[,column]
    sign <- 1
    current <- row + 1
    limit <- current + proximity.nbr
  } else if (direction=="L") {
    #print("left")
    vector <- matrix[row,]
    sign <- -1
    current <- column - 1
    limit <- current - proximity.nbr
  } else {
    #print("right")
    vector <- matrix[row,]
    sing <- 1
    current <- column + 1
    limit <- current + proximity.nbr
  }
  #print(paste("The vector:",vector,sep=" "))
  ## boders
  if (current < 1 | current > nrow(matrix) | current > ncol(matrix)) {
    return(FALSE)
  }
  
  if (limit < 1 | limit > nrow(matrix) | limit > ncol(matrix)) {
    return(FALSE)
  }
  
  ## validate
  # proximity of limits!!!
  
  
  target.sequence <- current:limit
  #print(target.sequence)
  # while 
  evidence <- 0
  for (i in target.sequence) {
    #print(paste("index",i,sep=" "))
    pixel <- vector[i]
    #print(paste("value",vector[i],sep=" "))
    if (pixel >= threshold) {
      #print("HIT")
      evidence <- evidence + 1
    }
  }
  if (evidence >= thickness) {
    return(TRUE)
  } else {
    return(FALSE)
  }
}


validate.border(3,4,test.matrix,"U",1,1)
validate.border(3,4,test.matrix,"D",1,1)
validate.border(8,4,test.matrix,"U",1,1)

getwd()
setwd("/Users/adeobeso/Downloads/agave2021")

class(image.data)
dim(image.data)
str(image.data)


uperlimits <- c(250,110,120,110,190,250,160,250,110,150) # 135
lowerlimits <- c(120,80,100,90,160,140,140,1,80,120)   
filenames <- c("3.28.20_T8.xlsx","3.26.20_T8.xlsx","3.25.20_T8.xlsx","3.24.20_T8.xlsx","3.20.20_T8.xlsx",
               "3.19.20_T8.xlsx","3.18.20_T8.xlsx","3.14.20_T8.xlsx","3.12.20_T8.xlsx","3.11.20_T8.xlsx")
proximities <- c(15,15,15,15,20,15,15,15,8,15)
thicknesses <- c(5,5,5,5,8,5,8,5,8,5)


current.plan <- 10
library(xlsx)
uperlimit <- uperlimits[current.plan] # 250
lowerlimit <- lowerlimits[current.plan] # 
file.name <- filenames[current.plan]
image.data <- read.xlsx(file.name, sheetName = "Sheet1")
proximity.nbr <- proximities[current.plan]
thickness <- thicknesses[current.plan]

plant.t.m <- as.matrix(image.data)
dim(plant.t.m)
# identify limits
plant.t.m[1:10,120] <- 7  # help identify thresholds. 

image(plant.t.m)

resulting.matrix <- plant.t.m
apply.filter <- c(F,T,T,F,T,T,F,F,F,F,F)
 if (apply.filter[current.plan]==T) {
resulting.matrix[resulting.matrix < 1.5] <- 0 ## if there is noise
}
for (i in 1:nrow(resulting.matrix)) {
  print(i)
  #for (j in 1:ncol(resulting.matrix)) {
    for (j in lowerlimit:uperlimit) {
    if ( resulting.matrix[i,j] == 0 &
      validate.border(i,j,resulting.matrix,"U",existence.treshold,thickness) &
      validate.border(i,j,resulting.matrix,"D",existence.treshold,thickness) &
      validate.border(i,j,resulting.matrix,"R",existence.treshold,thickness) &
      validate.border(i,j,resulting.matrix,"L",existence.treshold,thickness)) {
      resulting.matrix[i,j] <- desease.indicator
    }
    
  }
}

image(resulting.matrix)

plant.count <- length(resulting.matrix[resulting.matrix >= 1])
disease.count <- length(resulting.matrix[resulting.matrix >= 7])

## Add to final table
new.row <- data.frame(date=file.name,total=plant.count,disease=disease.count)
# agave.disease.set <- new.row


write.csv()

agave.disease.set <- rbind(agave.disease.set, new.row)
write.csv(agave.disease.set, file="agave.disease.set.csv")



# write.csv(agave.disease.set, file="agave.disease.set.first.csv")


