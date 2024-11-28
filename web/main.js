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
        const dailySelect = document.getElementById('daily-select');
        dailySelect.addEventListener('change', function() {
            const days = parseInt(this.value);
            const filteredData = data.slice(-days);
            createChart('daily-chart', filteredData, 'Daily Energy Data');
        });

        createChart('daily-chart', data.slice(-7), 'Daily Energy Data');
    }

    function createWeeklyChart(data) {
        const weeklySelect = document.getElementById('weekly-select');
        const months = [...new Set(data.map(d => d.date.slice(0, 7)))];
        months.forEach(month => {
            const option = document.createElement('option');
            option.value = month;
            option.textContent = month;
            weeklySelect.appendChild(option);
        });

        weeklySelect.addEventListener('change', function() {
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
});