function calculateCorrelation(x, y) {
    const n = x.length;
    const meanX = x.reduce((a, b) => a + b, 0) / n;
    const meanY = y.reduce((a, b) => a + b, 0) / n;
    const covariance = x.map((xi, i) => (xi - meanX) * (y[i] - meanY)).reduce((a, b) => a + b, 0) / n;
    const stdDevX = Math.sqrt(x.map(xi => (xi - meanX) ** 2).reduce((a, b) => a + b, 0) / n);
    const stdDevY = Math.sqrt(y.map(yi => (yi - meanY) ** 2).reduce((a, b) => a + b, 0) / n);
    return covariance / (stdDevX * stdDevY);
}

function calculateSMA(data, windowSize) {
    let sma = [];
    for (let i = 0; i < data.length; i++) {
        if (i < windowSize - 1) {
            sma.push(null);
        } else {
            const window = data.slice(i - windowSize + 1, i + 1);
            const average = window.reduce((sum, value) => sum + value, 0) / windowSize;
            sma.push(average);
        }
    }
    return sma;
}