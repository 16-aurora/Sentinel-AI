
const SentinelCharts = {

    colors: {
        blue: "#168BFF",
        cyan: "#39DDF5",
        purple: "#b380e9",
        red: "#FF557A",
        orange: "#FFAA55",
        yellow: "#EEDB5E",
        green: "#36E6A7",
        text: "#A9BCD5",
        grid: "rgba(90, 145, 200, 0.12)"
    },

    layoutBase: {
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: {
            family: "Montserrat, sans-serif",
            color: "#A9BCD5",
            size: 11
        },
        margin: {
            l: 35,
            r: 20,
            t: 25,
            b: 35
        },
        showlegend: true,
        legend: {
            orientation: "h",
            y: -0.18,
            font: { color: "#A9BCD5" }
        }
    },

    config: {
        responsive: true,
        displayModeBar: false
    },

    renderCyberRiskDistribution(categories) {
        const container = document.getElementById("cyber-chart");

        if (!container || !categories) return;

        const labels = Object.keys(categories);
        const values = Object.values(categories);

        if (!labels.length) return;

        const colorMap = {
            CRITICAL: this.colors.red,
            HIGH: this.colors.orange,
            MEDIUM: this.colors.yellow,
            LOW: this.colors.green
        };

        const trace = {
            type: "bar",
            x: labels,
            y: values,
            marker: {
                color: labels.map(
                    label => colorMap[label.toUpperCase()] || this.colors.cyan
                ),
                line: { width: 0 },
                cornerradius: 6
            },
            hovertemplate: "%{x}<br>Records: %{y}<extra></extra>"
        };

        const layout = {
            ...this.layoutBase,
            barcornerradius: 9,
            bargap: 10,
            showlegend: false,
            xaxis: {
                showgrid: false,
                zeroline: false
            },
            yaxis: {
                showgrid: true,
                gridcolor: this.colors.grid,
                zeroline: false,
                title: "Records"
            }
        };

        Plotly.react(container, [trace], layout, this.config);
    },

    renderDomainCoverage(domains) {
        const container = document.getElementById("coverage-chart");

        if (!container || !domains) return;

        const available = Object.values(domains).filter(
            domain => domain.status === "AVAILABLE"
        );

        if (!available.length) return;

        const labels = available.map(domain => domain.domain.toUpperCase());
        const values = available.map(domain => domain.records || 0);

        const trace = {
            type: "bar",
            orientation: "h",
            x: values,
            y: labels,
            marker: {
                color: [this.colors.blue, this.colors.cyan, this.colors.purple],
                line: { width: 0 }
            },
            hovertemplate: "%{y}<br>Records: %{x}<extra></extra>"
        };

        const layout = {
            ...this.layoutBase,
            barcornerradius: 9,
            showlegend: false,
            margin: { l: 110, r: 20, t: 15, b: 35 },
            xaxis: {
                showgrid: true,
                gridcolor: this.colors.grid,
                zeroline: false,
                title: "Records"
            },
            yaxis: {
                showgrid: false,
                zeroline: false,
                automargin: true,
                tickfont: {
                    family: "Montserrat, sans-serif",
                    size: 11
                }
            }
        };

        Plotly.react(container, [trace], layout, this.config);
    }
};

window.SentinelCharts = SentinelCharts;
