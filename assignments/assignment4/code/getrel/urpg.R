args = commandArgs(trailingOnly=TRUE)
data <- read.table(paste('urpg',args[1],'.dat',sep=''))

ploturpg <- function(data) {
    pdf(paste('urpg.pdf', sep=''))
    plot(data, type='o', ylim=c(0,1), xlim=c(0,1), pch=15)
    dev.off()
}

ploturpg(data)