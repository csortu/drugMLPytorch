setwd('/home/ortutay/Dropbox/Misc/HiDucator/DataScienceAcademy/Courses/Advanced_Python_for_datascience/AdvancedPythonPractice/data')

sourcefile <- 'drug_consumption.data'

drugData <- read.csv(sourcefile, header = FALSE)
table(drugData$V6)
headerNames <- c('id','age','sex','edu','country','ethnicity',
                 'neuroticism','extraversion','openness','agreeableness',
                 'conscientiousness','impulsiveness','sensationseeking',
                 "Alcohol","Amphet","Amyl","Benzos","Caff","Cannabis",
                 "Choc","Coke","Crack","Ecstasy","Heroin","Ketamine",
                 "Legalh","LSD","Meth","Mushrooms","Nicotine","Semeron",
                 "VSA")

names(drugData) <- headerNames

# Recover original category labels
# Age
read.table('metadata.txt', skip = 6, nrows = 6, sep = ' ')

drugData$age <- factor(drugData$age,
                       levels = c(-0.95197,-0.07854,0.49788,
                                  1.09449,1.82213,2.59171),
                       labels = c("18-24","25-34","35-44","45-54","55-64","65+"))

# Gender
read.table('metadata.txt', skip = 18, nrows = 2, sep = ' ')

drugData$sex <- factor(drugData$sex,
                       levels = c(0.48246,-0.48246),
                       labels = c("Female","Male"))

# Education
#read.table('metadata.txt', skip = 26, nrows = 9, sep = ' ')

drugData$edu <- factor(drugData$edu,
                       levels = c(-2.43591,-1.7379,-1.43719,-1.22751,
                                  -0.61113,-0.05921,0.45468,1.16365,1.98437),
                       labels = c("left<16","left16","left17","left18","someuninodiploma",
                                  "cert","uni","msc","dr"))


# Ethnicity
read.table('metadata.txt', skip = 54, nrows = 5, sep = ' ')

drugData$ethnicity <- factor(drugData$ethnicity,
                             levels = c(-0.50212,-1.10702,1.90725,0.12600,-0.22166,
                                        0.11440,-0.31685),
                             labels = c("Asian","Black","Mixed-Black/Asian","Mixed-White/Asian","Mixed-White/Black",
                                        "Other","White"))

# Country
#read.table('metadata.txt', skip = 41, nrows = 3, sep = ' ')

drugData$country <- factor(drugData$country,
                           levels = c(-0.57009,-0.46841,-0.28519,-0.09765,0.21128,0.24923,0.96082),
                           labels = c("Australia","Canada","New Zealand","Other",
                                      "Ireland","UK","USA"))

# Psycho measurements
#Neuroticism
as.numeric(levels(as.data.frame(table(drugData$neuroticism))$Var1))

drugData$neuroticism <- factor(drugData$neuroticism,
                               levels=c(-3.46436,-3.15735,-2.75696,-2.52197,-2.42317,-2.34360,-2.21844,-2.05048,-1.86962,-1.69163,
                                        -1.55078,-1.43907,-1.32828,-1.19430,-1.05308,-0.92104,-0.79151,-0.67825,-0.58016,-0.46725,
                                        -0.34799,-0.24649,-0.14882,-0.05188,0.04257,0.13606,0.22393,0.31287,0.41667,0.52135,
                                        0.62967,0.73545,0.82562,0.91093,1.02119,1.13281,1.23461,1.37297,1.49158,1.60383,
                                        1.72012,1.83990,1.98437,2.12700,2.28554,2.46262,2.61139,2.82196,3.27393),
                               labels = c(12:60))

#Extraversion

drugData$extraversion <- factor(drugData$extraversion,
                                levels = c(-3.27393,-3.00537,-2.72827,-2.53830,-2.44904,-2.32338,-2.21069,-2.11437,-2.03972,-1.92173,
                                           -1.76250,-1.63340,-1.50796,-1.37639,-1.23177,-1.09207,-0.94779,-0.80615,-0.69509,-0.57545,
                                           -0.43999,-0.30033,-0.15487,0.00332,0.16767,0.32197,0.47617,0.63779,0.80523,0.96248,
                                           1.11406,1.28610,1.45421,1.58487,1.74091,1.93886,2.12700,2.32338,2.57309,2.85950,
                                           3.00537,3.27393),
                                labels = c(16,18:56,58,59))

#Openness

drugData$openness <- factor(drugData$openness,
                            levels = c(-3.27393,-2.85950,-2.63199,-2.39883,-2.21069,-2.09015,-1.97495,-1.82919,-1.68062,-1.55521,
                                       -1.42424,-1.27553,-1.11902,-0.97631,-0.84732,-0.71727,-0.58331,-0.45174,-0.31776,-0.17779,
                                       -0.01928,0.14143,0.29338,0.44585,0.58331,0.72330,0.88309,1.06238,1.24033,1.43533,
                                       1.65653,1.88511,2.15324,2.44904,2.90161),
                            labels = c(24,26,28:60))

#Agreeableness

drugData$agreeableness <- factor(drugData$agreeableness,
                                 levels = c(-3.46436,-3.15735,-3.00537,-2.90161,-2.78793,-2.70172,-2.53830,-2.35413,-2.21844,-2.07848,
                                            -1.92595,-1.77200,-1.62090,-1.47955,-1.34289,-1.21213,-1.07533,-0.91699,-0.76096,-0.60633,
                                            -0.45321,-0.30172,-0.15487,-0.01729,0.13136,0.28783,0.43852,0.59042,0.76096,0.94156,
                                            1.11406,1.28610,1.45039,1.61108,1.81866,2.03972,2.23427,2.46262,2.75696,3.15735,
                                            3.46436),
                                 labels = c(12,16,18,23:60))

#Conscientiousness

drugData$conscientiousness <- factor(drugData$conscientiousness,
                                     levels = c(-3.46436,-3.15735,-2.90161,-2.72827,-2.57309,-2.42317,-2.30408,-2.18109,-2.04506,-1.92173,
                                                -1.78169,-1.64101,-1.51840,-1.38502,-1.25773,-1.13788,-1.01450,-0.89891,-0.78155,-0.65253,
                                                -0.52745,-0.40581,-0.27607,-0.14277,-0.00665,0.12331,0.25953,0.41594,0.58489,0.75830,
                                                0.93949,1.13407,1.30612,1.46191,1.63088,1.81175,2.04506,2.33337,2.63199,3.00537,
                                                3.46436),
                                     labels = c(17,19:57,59))

#Impulsiveness

drugData$impulsiveness <- factor(drugData$impulsiveness,
                                 levels = c(-2.55524,-1.37983,-0.71126,-0.21712,0.19268,0.52975,0.88113,1.29221,1.86203,2.90161),
                                 labels = 1:10)

#Sensation seeing

drugData$sensationseeking <- factor(drugData$sensationseeking,
                                    levels = c(-2.07848,-1.54858,-1.18084,-0.84637,-0.52593,-0.21575,
                                               0.07987,0.40148 ,0.76540,1.22470,1.92173),
                                    labels = 1:11)


# Export data

write.csv(drugData,"drug_consumption_original.csv")

