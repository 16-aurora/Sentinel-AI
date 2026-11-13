const SentinelApp = {

    API_BASE: window.location.origin,

    async request(endpoint) {
        const response = await fetch(`${this.API_BASE}${endpoint}`);

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        return await response.json();
    },

    setText(id, value) {
        const element = document.getElementById(id);

        if (element) {
            element.textContent = value ?? "--";
        }
    },

    formatNumber(value) {
        return new Intl.NumberFormat("en-US").format(value || 0);
    },

    async loadDashboard() {
        try {
            const [health, intelligence] = await Promise.all([
                this.request("/health"),
                this.request("/domains")
            ]);

            this.updateStatus(health);
            this.updateOverview(intelligence);
            this.updateDomains(intelligence.domains);
            this.updateSystemDetails(health, intelligence);

            if (window.SentinelCharts) {
                const cyber = intelligence.domains?.cybersecurity;

                window.SentinelCharts.renderCyberRiskDistribution(
                    cyber?.categories
                );

                window.SentinelCharts.renderDomainCoverage(
                    intelligence.domains
                );
            }

            if (window.SentinelPanels?.refresh) {
                await window.SentinelPanels.refresh();
                console.info("Sentinel AI detailed panels refreshed.");
            }

            this.setText(
                "last-updated",
                `Last updated: ${new Date().toLocaleTimeString()}`
            );

            console.info("Sentinel AI dashboard connected successfully.");

        } catch (error) {
            console.error("Sentinel AI connection error:", error);

            this.setText("system-status", "API CONNECTION ERROR");
            this.setText("global-status", "OFFLINE");
            this.setText("last-updated", "Unable to retrieve live data");

            this.showConnectionError();
        }
    },

    updateStatus(health) {
        const operational = health.status === "OPERATIONAL";

        this.setText(
            "system-status",
            operational ? "SYSTEM OPERATIONAL" : "SYSTEM DEGRADED"
        );
    },

    updateOverview(data) {
        const domains = data.domains || {};

        const available = Object.values(domains).filter(
            domain => domain.status === "AVAILABLE"
        );

        const totalRecords = Object.values(domains).reduce(
            (total, domain) => total + (Number(domain.records) || 0),
            0
        );

        this.setText(
            "domains-online",
            `${data.domains_available}/${data.domains_total}`
        );

        this.setText(
            "total-records",
            this.formatNumber(totalRecords)
        );

        this.setText(
            "cyber-records",
            this.formatNumber(
                domains.cybersecurity?.records
            )
        );

        this.setText(
            "global-status",
            data.system_status || "UNKNOWN"
        );
    },

    updateDomains(domains) {
        const configuration = [
            {
                key: "cybersecurity",
                statusId: "cyber-status",
                summaryId: "cyber-summary"
            },
            {
                key: "climate",
                statusId: "climate-status",
                summaryId: "climate-summary"
            },
            {
                key: "economy",
                statusId: "economy-status",
                summaryId: "economy-summary"
            }
        ];

        configuration.forEach(item => {
            const domain = domains?.[item.key];

            if (!domain) {
                this.setText(item.statusId, "UNAVAILABLE");
                this.setText(item.summaryId, "No domain information");
                return;
            }

            this.setText(item.statusId, domain.status);

            this.setText(
                item.summaryId,
                `${this.formatNumber(domain.records)} records · ${domain.unit || "Data"}`
            );

        });
    },

    updateSystemDetails(health, intelligence) {
        const detail = document.getElementById("system-detail");

        if (!detail) return;

        detail.textContent =
            `System: ${health.system} | ` +
            `Status: ${health.status} | ` +
            `Available domains: ${intelligence.domains_available}/` +
            `${intelligence.domains_total}`;
    },

    showConnectionError() {
        const status = document.getElementById("system-detail");

        if (status) {
            status.textContent =
                "Unable to connect to the Sentinel AI API. " +
                "Check that the backend is running on port 8000.";
        }
    },

    start() {
        this.loadDashboard();

        // Refresh live data every 60 seconds.
        this.refreshInterval = setInterval(
            () => this.loadDashboard(),
            60000
        );
    }
};

document.addEventListener("DOMContentLoaded", () => {
    SentinelApp.start();
});

window.SentinelApp = SentinelApp;