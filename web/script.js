document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:8000/get_energy_data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Fetched data:', data); // Debug log
            const dailyData = processData(data, 'day');
            const weeklyData = processData(data, 'week');
            const monthlyData = processData(data, 'month');

            console.log('Daily data:', dailyData); // Debug log
            console.log('Weekly data:', weeklyData); // Debug log
            console.log('Monthly data:', monthlyData); // Debug log

            createDailyChart(dailyData);
            createWeeklyChart(weeklyData);
            createMonthlyChart(monthlyData);

            createTrendChart('daily-trend-chart', dailyData, 'Daily Energy Trend');
            createTrendChart('weekly-trend-chart', weeklyData, 'Weekly Energy Trend');
            createTrendChart('monthly-trend-chart', monthlyData, 'Monthly Energy Trend', 'Month');

            createSeasonalChart('daily-seasonal-chart', dailyData, 'Daily Energy Seasonal');
            createSeasonalChart('weekly-seasonal-chart', weeklyData, 'Weekly Energy Seasonal');
            createSeasonalChart('monthly-seasonal-chart', monthlyData, 'Monthly Energy Seasonal', 'Month');

            createCorrelationMatrix(data);
            createSpiderChart(data);
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });

    function processData(data, period) {
        const groupedData = {};

        data.forEach(record => {
            const date = new Date(record.interval_start_utc);
            let key;

            if (period === 'day') {
                key = date.toISOString().split('T')[0];
            } else if (period === 'week') {
                const startOfWeek = new Date(date.setDate(date.getDate() - date.getDay()));
                key = startOfWeek.toISOString().split('T')[0];
            } else if (period === 'month') {
                key = `${date.getFullYear()}-${date.getMonth() + 1}`;
            }

            if (!groupedData[key]) {
                groupedData[key] = {
                    solar: 0,
                    wind: 0,
                    geothermal: 0,
                    biomass: 0,
                    biogas: 0,
                    small_hydro: 0,
                    coal: 0,
                    nuclear: 0,
                    natural_gas: 0,
                    large_hydro: 0,
                    batteries: 0,
                    imports: 0,
                    other: 0,
                    count: 0
                };
            }

            Object.keys(groupedData[key]).forEach(field => {
                if (field !== 'count') {
                    groupedData[key][field] += record[field] || 0;
                }
            });

            groupedData[key].count += 1;
        });

        return Object.keys(groupedData).map(key => {
            const avgData = groupedData[key];
            Object.keys(avgData).forEach(field => {
                if (field !== 'count') {
                    avgData[field] /= avgData.count;
                }
            });
            avgData.date = key;
            return avgData;
        });
    }

    function createDailyChart(data) {
        const dailyChartContainer = document.getElementById('daily-chart');
        const select = document.createElement('select');
        select.innerHTML = `
            <option value="7">Last 7 Days</option>
            <option value="30">Last 30 Days</option>
        `;
        dailyChartContainer.appendChild(select);

        select.addEventListener('change', function() {
            const days = parseInt(this.value);
            const filteredData = data.slice(-days);
            createChart('daily-chart', filteredData, 'Daily Energy Data');
        });

        createChart('daily-chart', data.slice(-7), 'Daily Energy Data');
    }

    function createWeeklyChart(data) {
        const weeklyChartContainer = document.getElementById('weekly-chart');
        const select = document.createElement('select');
        const months = [...new Set(data.map(d => d.date.slice(0, 7)))];
        months.forEach(month => {
            const option = document.createElement('option');
            option.value = month;
            option.textContent = month;
            select.appendChild(option);
        });
        weeklyChartContainer.appendChild(select);

        select.addEventListener('change', function() {
            const month = this.value;
            const filteredData = data.filter(d => d.date.startsWith(month));
            createChart('weekly-chart', filteredData, 'Weekly Energy Data');
        });

        createChart('weekly-chart', data.filter(d => d.date.startsWith(months[0])), 'Weekly Energy Data');
    }

    function createMonthlyChart(data) {
        data.forEach(d => {
            d.date = new Date(d.date).toLocaleString('default', { month: 'long' });
        });
        createChart('monthly-chart', data, 'Monthly Energy Data', 'Month');
    }

    function createChart(elementId, data, title, xAxisTitle = 'Date') {
        console.log(`Creating chart for ${elementId} with title ${title}`); // Debug log
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
            { name: 'Imports', field: 'imports' },
            { name: 'Other', field: 'other' }
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

    function createTrendChart(elementId, data, title, xAxisTitle = 'Date') {
        console.log(`Creating trend chart for ${elementId} with title ${title}`); // Debug log
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
            { name: 'Imports', field: 'imports' },
            { name: 'Other', field: 'other' }
        ].map(trace => ({
            x: data.map(d => d.date),
            y: calculateSMA(data.map(d => d[trace.field]), 7), // Simple Moving Average with window size 7
            type: 'scatter',
            mode: 'lines',
            name: `${trace.name} Trend`,
            line: { dash: 'dot' }
        }));

        const layout = {
            title: title,
            xaxis: { title: xAxisTitle },
            yaxis: { title: 'Energy (MWh)' }
        };

        Plotly.newPlot(elementId, traces, layout);
    }

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
            { name: 'Imports', field: 'imports' },
            { name: 'Other', field: 'other' }
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

    function createCorrelationMatrix(data) {
        console.log('Creating correlation matrix'); // Debug log
        const fields = [
            'solar', 'wind', 'geothermal', 'biomass', 'biogas', 'small_hydro',
            'coal', 'nuclear', 'natural_gas', 'large_hydro', 'batteries', 'imports', 'other'
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
            yaxis: { title: 'Variables', tickvals: fields, ticktext: fields }
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

    function createSpiderChart(data) {
        console.log('Creating spider chart'); // Debug log
        const fields = [
            'solar', 'wind', 'geothermal', 'biomass', 'biogas', 'small_hydro',
            'coal', 'nuclear', 'natural_gas', 'large_hydro', 'batteries', 'imports', 'other'
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
});