function createCorrelationMatrix(data) {
    console.log('Creating correlation matrix'); // Debug log
    const fields = [
        'solar', 'wind', 'geothermal', 'biomass', 'biogas', 'small_hydro',
        'coal', 'nuclear', 'natural_gas', 'large_hydro', 'batteries', 'imports'
    ];

    const matrix = fields.map(field1 => {
        return fields.map(field2 => {
            const values1 = data.map(d => d[field1]);
            const values2 = data.map(d => d[field2]);
            return calculateCorrelation(values1, values2);
        });
    });

    const layout = {
        title: 'Correlation Matrix',
        xaxis: { title: 'Variables', tickvals: fields, ticktext: fields },
        yaxis: { title: 'Variables', tickvals: fields, ticktext: fields },
        margin: { t: 50, b: 100, l: 100, r: 50 }
    };

    const trace = {
        z: matrix,
        x: fields,
        y: fields,
        type: 'heatmap',
        colorscale: 'Viridis'
    };

    Plotly.newPlot('correlation-matrix', [trace], layout);
}