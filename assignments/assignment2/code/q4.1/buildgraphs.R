#! /usr/bin/Rscript

plotgraph <- function(infile, outfile, title) {
    data <- read.table(infile)
    x <- seq(1, length(data$V1))
    y <- data$V1

    pdf(outfile)
    plot(x, y, type='l', log='xy', main=title, 
        ylab='Frequency', xlab='Rank')
    dev.off()    
}

plotgraph('wordcount', 'wc.pdf', 'Word Counts')
plotgraph('bigramcount', 'bg.pdf', 'Bigram Counts')