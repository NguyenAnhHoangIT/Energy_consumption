function createSpiderChart(data) {
    console.log('Creating spider chart'); // Debug log
    const fields = [
        'solar', 'wind', 'geothermal', 'biomass', 'biogas', 'small_hydro',
        'coal', 'nuclear', 'natural_gas', 'large_hydro', 'batteries', 'imports'
    ];

    const averages = fields.map(field => {
        const values = data.map(d => d[field]);
        return values.reduce((a, b) => a + b, 0) / values.length;
    });

    const trace = {
        type: 'scatterpolar',
        r: averages,
        theta: fields,
        fill: 'toself',
        name: 'Average Energy'
    };

    const layout = {
        title: 'Spider Chart',
        polar: {
            radialaxis: {
                visible: true,
                range: [0, Math.max(...averages)]
            }
        }
    };

    Plotly.newPlot('spider-chart', [trace], layout);
}