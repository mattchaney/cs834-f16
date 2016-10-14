plotone <- function(data, outfile, title) {
    pdf(outfile)
    plot(data$V1, type='l', log='xy', main=title, 
        ylab='Frequency', xlab='Rank', col="black")
    dev.off()    
}

plottwo <- function(d1, d2, outfile, title) {
    pdf(outfile)    
    y_range <- range(1, d1$V1, d2$V1)
    plot(d1$V1, type='l', log='xy', main=title, ylim=y_range,
        ylab='Frequency', xlab='Rank', col="blue")
    lines(d2$V1, type="l", lty=2, col="red")
    legend(10000, y_range[2], c('Words', 'Bigrams'), cex=0.8,
        col=c('blue', 'red'), lty=1:2)
    dev.off()
}

d1 <- read.table('wordcount.dat')
d2 <- read.table('bigramcount.dat')
plotone(d1, 'wc.pdf', 'Word Counts')
plotone(d2, 'bg.pdf', 'Bigram Counts')
plottwo(d1, d2, 'both.pdf', 'Word and Bigram Counts')