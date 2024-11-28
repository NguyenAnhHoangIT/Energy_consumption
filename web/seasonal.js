function createSeasonalChart(elementId, data, title, xAxisTitle = 'Date') {
    console.log(`Creating seasonal chart for ${elementId} with title ${title}`); // Debug log
    const traces = [
        { name: 'Solar', field: 'solar' },
        { name: 'Wind', field: 'wind' },
        { name: 'Geothermal', field: 'geothermal' },
        { name: 'Biomass', field: 'biomass' },
        { name: 'Biogas', field: 'biogas' },
        { name: 'Small Hydro', field: 'small_hydro' },
        { name: 'Coal', field: 'coal' },
        { name: 'Nuclear', field: 'nuclear' },
        { name: 'Natural Gas', field: 'natural_gas' },
        { name: 'Large Hydro', field: 'large_hydro' },
        { name: 'Batteries', field: 'batteries' },
        { name: 'Imports', field: 'imports' }
    ].map(trace => ({
        x: data.map(d => d.date),
        y: data.map(d => d[trace.field]),
        type: 'scatter',
        mode: 'lines+markers',
        name: trace.name
    }));

    const layout = {
        title: title,
        xaxis: { title: xAxisTitle },
        yaxis: { title: 'Energy (MWh)' }
    };

    Plotly.newPlot(elementId, traces, layout);
}