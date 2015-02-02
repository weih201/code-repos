
## Data loading
rm(list=ls())
data(mtcars)

## Exploratory data analysis
dim(mtcars)
head(mtcars)
str(mtcars)

tapply(mtcars$mpg, mtcars$am, mean)

library(ggplot2)
library(gridExtra)

# density distribiution
g1<-ggplot(mtcars, aes(mpg, fill = as.factor(am))) + geom_density(alpha = 0.2)
 # box plotting
g2<-ggplot(mtcars, aes(x=am, y=mpg, fill=as.factor(am))) + geom_boxplot()

grid.arrange(g1,g2, ncol=2)

ya <- mtcars$mpg[mtcars$am == 0]
ym <- mtcars$mpg[mtcars$am == 1]
t<-t.test(ym, ya, paired=FALSE)
t$p.value; t$conf.int;t$estimate
## Models selection

## check the correlation between mpg and other fields
## mtcars[,-1] is the dataframe without mpg
cor(mtcars$mpg,mtcars[,-1])
## or
sort(cor(mtcars)[1,])

cormodel1 = lm(mpg ~ factor(am), data = mtcars)
cormodel2 = update(cormodel1, mpg ~ factor(am) + wt)
cormodel3 = update(cormodel2, mpg ~ factor(am) + wt + cyl)
cormodel4 = update(cormodel3, mpg ~ factor(am) + wt + cyl + hp)
anova(cormodel1, cormodel2, cormodel3, cormodel4)

summary(cormodel3)$coefficients

## Residuial plot
plot(predict(cormodel3), resid(cormodel3), pch = '.')
abline(cormodel3, lwd=2)

plot(cormodel3)


## Based on the anova results, model 3 is our beast canditate as 
## it is the last model with statisticaly significant variables (p < 0.05).

## Model selection by step function
stepmodel = step(lm(data = mtcars, mpg ~ .),trace=0, steps=10000)
summary(stepmodel)

par(mfrow= c(2,2))
plot(stepmodel)


model1 = lm(mpg ~ factor(am), data = mtcars)
model2 = update(model1, mpg ~ factor(am) + hp)
model3 = update(model2, mpg ~ factor(am) + hp + wt)
model4 = update(model3, mpg ~ factor(am) + hp + wt + carb)

anova(model1, model2, model3, model4)
summary(model3)