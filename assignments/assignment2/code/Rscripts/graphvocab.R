data <- read.table('vocab')

pdf("vocab.pdf")
plot(data$V2, data$V1, type="l", main="Vocabulary Growth",
    ylab="Words in Vocabulary", xlab="Words in Collection")
dev.off()
