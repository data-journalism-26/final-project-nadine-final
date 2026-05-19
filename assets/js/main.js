const splitIndexData = [
    { year: 2015, all: 100.0, cyclists: 100.0 },
    { year: 2016, all: 92.68574732581672, cyclists: 102.61096605744125 },
    { year: 2017, all: 91.93408499566348, cyclists: 99.73890339425587 },
    { year: 2018, all: 94.68054350968488, cyclists: 116.18798955613576 },
    { year: 2019, all: 88.06013298641226, cyclists: 116.18798955613576 },
    { year: 2020, all: 78.60653368025442, cyclists: 111.22715404699738 },
    { year: 2021, all: 74.0676496097138, cyclists: 97.12793733681463 },
    { year: 2022, all: 80.60132986412259, cyclists: 123.7597911227154 },
    { year: 2023, all: 82.07574443480775, cyclists: 116.4490861618799 },
    { year: 2024, all: 80.08094825093957, cyclists: 116.18798955613576 },
    { year: 2025, all: 81.3529921942758, cyclists: 120.62663185378591 },
];

const splitSeries = {
    cyclists: { label: "Cyclist deaths", color: "#d84f8f", field: "cyclists", active: true },
    all: { label: "All traffic deaths", color: "#1f1f1f", field: "all", active: false },
};

const cyclistTypeData = [
    { year: 2015, total: 383, bicycle: 347, pedelec: 36 },
    { year: 2016, total: 393, bicycle: 331, pedelec: 62 },
    { year: 2017, total: 382, bicycle: 314, pedelec: 68 },
    { year: 2018, total: 445, bicycle: 356, pedelec: 89 },
    { year: 2019, total: 445, bicycle: 327, pedelec: 118 },
    { year: 2020, total: 426, bicycle: 284, pedelec: 142 },
    { year: 2021, total: 372, bicycle: 241, pedelec: 131 },
    { year: 2022, total: 474, bicycle: 266, pedelec: 208 },
    { year: 2023, total: 446, bicycle: 256, pedelec: 190 },
    { year: 2024, total: 445, bicycle: 250, pedelec: 195 },
    { year: 2025, total: 462, bicycle: 245, pedelec: 217 },
];

const ageGapData = [
    { label: "Conventional bicycles", value: 56.3, className: "age-bar-conventional" },
    { label: "All cyclist deaths", value: 61.5, className: "age-bar-all" },
    { label: "Pedelec users", value: 67.3, className: "age-bar-pedelec" },
];

function renderSplitIndexChart() {
    const container = document.querySelector("#split-index-figure");
    if (!container) return;

    const fallback = container.querySelector(".article-figure");
    const width = 1040;
    const height = 520;
    const margin = { top: 34, right: 190, bottom: 66, left: 68 };
    const plotWidth = width - margin.left - margin.right;
    const plotHeight = height - margin.top - margin.bottom;
    const minYear = 2015;
    const maxYear = 2025;
    const minValue = 68;
    const maxValue = 132;
    const yTicks = [70, 80, 90, 100, 110, 120, 130];

    const x = year => margin.left + ((year - minYear) / (maxYear - minYear)) * plotWidth;
    const y = value => margin.top + ((maxValue - value) / (maxValue - minValue)) * plotHeight;
    const lastDatum = splitIndexData[splitIndexData.length - 1];
    const pathFor = field => splitIndexData
        .map((d, i) => `${i === 0 ? "M" : "L"} ${x(d.year).toFixed(2)} ${y(d[field]).toFixed(2)}`)
        .join(" ");

    const chart = document.createElement("div");
    chart.className = "split-chart is-ready";
    chart.innerHTML = `
        <svg viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="split-title split-desc">
            <title id="split-title">Road deaths fell. Cyclist deaths did not.</title>
            <desc id="split-desc">Indexed deaths from 2015 to 2025. Overall traffic deaths fell, while cyclist deaths ended higher.</desc>
            <rect class="period-band" x="${x(2021)}" y="${margin.top - 12}" width="${x(2022) - x(2021)}" height="${plotHeight + 12}"></rect>
            <text class="chart-small-text" x="${x(2021.5)}" y="${margin.top + 17}" text-anchor="middle" font-size="14" fill="#333333">
                <tspan x="${x(2021.5)}">2022 marked</tspan>
                <tspan x="${x(2021.5)}" dy="17">a new high</tspan>
            </text>
            ${yTicks.map(tick => `
                <line class="${tick === 100 ? "baseline" : "grid-line"}" x1="${margin.left}" x2="${margin.left + plotWidth}" y1="${y(tick)}" y2="${y(tick)}"></line>
                <text class="chart-small-text" x="${margin.left - 10}" y="${y(tick) + 5}" text-anchor="end" font-size="16" fill="#151515">${tick}</text>
            `).join("")}
            <line class="axis-line" x1="${margin.left}" x2="${margin.left + plotWidth}" y1="${margin.top + plotHeight}" y2="${margin.top + plotHeight}"></line>
            ${splitIndexData.map(d => `
                <text class="chart-small-text" x="${x(d.year)}" y="${margin.top + plotHeight + 25}" text-anchor="middle" font-size="16" fill="#151515">${d.year}</text>
            `).join("")}
            <text class="chart-small-text" x="16" y="${margin.top + plotHeight / 2}" transform="rotate(-90 16 ${margin.top + plotHeight / 2})" text-anchor="middle" font-size="17" fill="#151515">Index</text>
            <path class="series-line series-muted" data-series="all" d="${pathFor("all")}"></path>
            <path class="series-line series-accent" data-series="cyclists" d="${pathFor("cyclists")}"></path>
            <path class="line-hit" data-series="all" d="${pathFor("all")}"></path>
            <path class="line-hit" data-series="cyclists" d="${pathFor("cyclists")}"></path>
            ${Object.entries(splitSeries).map(([key, series]) => splitIndexData.map(d => {
                const isEnd = key === "cyclists" && d.year === 2025;
                return `<circle class="point ${series.active ? "point-accent" : "point-muted"} ${isEnd ? "end-point" : ""}" data-series="${key}" data-year="${d.year}" cx="${x(d.year)}" cy="${y(d[series.field])}" r="${isEnd ? 6.5 : 4.2}"></circle>`;
            }).join("")).join("")}
            <text x="${x(2025) + 24}" y="${y(lastDatum.cyclists) - 10}" font-size="17" font-weight="700" fill="#d84f8f">Cyclist deaths</text>
            <text x="${x(2025) + 24}" y="${y(lastDatum.cyclists) + 12}" font-size="17" font-weight="700" fill="#d84f8f">+20.6%</text>
            <text x="${x(2025) + 24}" y="${y(lastDatum.all) + 2}" font-size="17" fill="#151515">All traffic deaths</text>
            <text x="${x(2025) + 24}" y="${y(lastDatum.all) + 24}" font-size="17" fill="#151515">-18.6%</text>
        </svg>
        <div class="split-tooltip" aria-hidden="true"></div>
    `;

    if (fallback) {
        container.replaceChildren(chart);
    } else {
        container.prepend(chart);
    }

    const tooltip = chart.querySelector(".split-tooltip");
    const lines = chart.querySelectorAll(".series-line");
    const lineHits = chart.querySelectorAll(".line-hit");
    const points = chart.querySelectorAll(".point");

    function setActive(seriesKey) {
        chart.classList.add("is-hovering");
        lines.forEach(line => line.classList.toggle("is-active", line.dataset.series === seriesKey));
        points.forEach(point => point.classList.toggle("is-active", point.dataset.series === seriesKey));
    }

    function clearActive() {
        chart.classList.remove("is-hovering");
        lines.forEach(line => line.classList.remove("is-active"));
        points.forEach(point => point.classList.remove("is-active"));
        tooltip.classList.remove("is-visible");
    }

    function showTooltip(event, seriesKey, year) {
        const series = splitSeries[seriesKey];
        const datum = splitIndexData.find(d => d.year === Number(year));
        if (!series || !datum) return;

        const value = datum[series.field];
        const change = value - 100;
        const sign = change >= 0 ? "+" : "-";
        tooltip.innerHTML = `
            <strong>${series.label}, ${datum.year}</strong>
            <span>Index: ${value.toFixed(1)}</span>
            <span>Change since 2015: ${sign}${Math.abs(change).toFixed(1)}%</span>
        `;

        const chartRect = chart.getBoundingClientRect();
        const pointerX = event.clientX - chartRect.left;
        const pointerY = event.clientY - chartRect.top;
        tooltip.style.left = `${Math.min(Math.max(pointerX, 110), chartRect.width - 110)}px`;
        tooltip.style.top = `${Math.max(pointerY, 72)}px`;
        tooltip.classList.add("is-visible");
    }

    function nearestYear(event) {
        const chartRect = chart.getBoundingClientRect();
        const svgX = ((event.clientX - chartRect.left) / chartRect.width) * width;
        const rawYear = minYear + ((svgX - margin.left) / plotWidth) * (maxYear - minYear);
        return splitIndexData.reduce((nearest, d) => (
            Math.abs(d.year - rawYear) < Math.abs(nearest.year - rawYear) ? d : nearest
        ), splitIndexData[0]).year;
    }

    points.forEach(point => {
        point.addEventListener("pointerenter", event => {
            setActive(point.dataset.series);
            point.setAttribute("r", point.classList.contains("end-point") ? "8" : "6");
            showTooltip(event, point.dataset.series, point.dataset.year);
        });
        point.addEventListener("pointermove", event => showTooltip(event, point.dataset.series, point.dataset.year));
        point.addEventListener("pointerleave", () => {
            point.setAttribute("r", point.classList.contains("end-point") ? "6.5" : "4.2");
            clearActive();
        });
        point.addEventListener("focus", event => {
            const rect = point.getBoundingClientRect();
            setActive(point.dataset.series);
            showTooltip({
                clientX: rect.left + rect.width / 2,
                clientY: rect.top + rect.height / 2,
            }, point.dataset.series, point.dataset.year);
        });
        point.addEventListener("blur", clearActive);
        point.setAttribute("tabindex", "0");
        point.setAttribute("aria-label", `${splitSeries[point.dataset.series].label}, ${point.dataset.year}`);
    });

    lineHits.forEach(line => {
        line.addEventListener("pointerenter", event => {
            setActive(line.dataset.series);
            showTooltip(event, line.dataset.series, nearestYear(event));
        });
        line.addEventListener("pointermove", event => {
            setActive(line.dataset.series);
            showTooltip(event, line.dataset.series, nearestYear(event));
        });
        line.addEventListener("pointerleave", clearActive);
    });
}

function renderCyclistTypesChart() {
    const container = document.querySelector("#cyclist-types-figure");
    if (!container) return;

    const fallback = container.querySelector(".article-figure");
    const startIndex = cyclistTypeData.length - 1;

    const chart = document.createElement("div");
    chart.className = "types-chart is-ready";
    chart.innerHTML = `
        <div class="types-chart-header">
            <div>
                <h3>Pedelecs became a larger share of cyclist deaths.</h3>
                <p>Move through the years to see how the fatality mix changed.</p>
            </div>
            <div class="types-summary-panel" aria-live="polite">
                <div class="types-year">${cyclistTypeData[startIndex].year}</div>
                <div class="summary-total">0 cyclist deaths</div>
                <div class="summary-share">0% involved pedelecs</div>
            </div>
        </div>
        <div class="types-bars" role="img" aria-label="Cyclist deaths by type and year">
            <div class="composition-bar">
                <div class="composition-segment segment-bicycle">
                    <span class="segment-text"></span>
                </div>
                <div class="composition-segment segment-pedelec">
                    <span class="segment-text"></span>
                </div>
            </div>
        </div>
        <div class="types-slider-wrap">
            <label for="cyclist-types-slider">Year</label>
            <input class="types-slider" id="cyclist-types-slider" type="range" min="0" max="${cyclistTypeData.length - 1}" step="1" value="${startIndex}">
            <output for="cyclist-types-slider">${cyclistTypeData[startIndex].year}</output>
        </div>
    `;

    if (fallback) {
        container.replaceChildren(chart);
    } else {
        container.prepend(chart);
    }

    const yearEl = chart.querySelector(".types-year");
    const output = chart.querySelector("output");
    const slider = chart.querySelector(".types-slider");
    const totalValue = chart.querySelector(".summary-total");
    const shareValue = chart.querySelector(".summary-share");
    const bicycleSegment = chart.querySelector(".segment-bicycle");
    const pedelecSegment = chart.querySelector(".segment-pedelec");
    const bicycleText = bicycleSegment.querySelector(".segment-text");
    const pedelecText = pedelecSegment.querySelector(".segment-text");

    function formatNumber(value) {
        return value.toLocaleString("en-US");
    }

    function update(index) {
        const d = cyclistTypeData[index];
        yearEl.textContent = d.year;
        output.textContent = d.year;

        const bicycleShare = (d.bicycle / d.total) * 100;
        const pedelecShare = (d.pedelec / d.total) * 100;
        totalValue.textContent = `${formatNumber(d.total)} cyclist deaths`;
        shareValue.textContent = `${pedelecShare.toFixed(0)}% involved pedelecs`;
        bicycleSegment.style.width = `${bicycleShare}%`;
        pedelecSegment.style.width = `${pedelecShare}%`;
        bicycleText.textContent = `${formatNumber(d.bicycle)} without motor`;
        pedelecText.textContent = `${formatNumber(d.pedelec)} pedelecs`;
    }

    slider.addEventListener("input", event => update(Number(event.target.value)));
    update(startIndex);
}

function renderAgeGapChart() {
    const container = document.querySelector("#age-gap-figure");
    if (!container) return;

    const fallback = container.querySelector(".article-figure");
    const chart = document.createElement("div");
    chart.className = "age-chart is-ready";
    chart.innerHTML = `
        <h3>The fatality gap is also an age gap.</h3>
        <p>In both bicycle categories, older riders made up more than half of deaths in 2025.</p>
        <div class="age-plot" role="img" aria-label="Share of killed cyclists aged 65 or older by bicycle type in 2025">
            ${ageGapData.map(d => `
                <div class="age-row">
                    <div class="age-label">${d.label}</div>
                    <div class="age-track">
                        <div class="age-bar age-under" style="--bar-width: ${100 - d.value}%"></div>
                        <div class="age-bar ${d.className}" style="--bar-width: ${d.value}%"></div>
                    </div>
                    <div class="age-value">${d.value.toFixed(1)}%</div>
                </div>
            `).join("")}
        </div>
        <div class="age-legend" aria-hidden="true">
            <span class="legend-under">Under 65</span>
            <span class="legend-over">65 or older</span>
        </div>
        <p class="age-note">About two in three killed pedelec users were 65 or older; among conventional bicycles, it was still just over half.</p>
    `;

    if (fallback) {
        container.replaceChildren(chart);
    } else {
        container.prepend(chart);
    }

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    chart.classList.add("is-visible");
                    observer.disconnect();
                }
            });
        }, { threshold: 0.35 });
        observer.observe(chart);
    } else {
        chart.classList.add("is-visible");
    }
}

async function renderBerlinWeather() {
    const widget = document.querySelector("#berlin-weather");
    if (!widget) return;

    const tempEl = widget.querySelector(".weather-temp");
    const nowEl = widget.querySelector(".weather-now");
    const rideNoteEl = widget.querySelector(".weather-ride-note");
    const dayEls = widget.querySelectorAll(".weather-days div");
    const url = "https://api.open-meteo.com/v1/dwd-icon?latitude=52.52&longitude=13.41&current=temperature_2m,weather_code,wind_speed_10m,precipitation&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Europe%2FBerlin";

    const weatherText = code => {
        if ([0].includes(code)) return "Clear";
        if ([1, 2].includes(code)) return "Partly cloudy";
        if ([3].includes(code)) return "Cloudy";
        if ([45, 48].includes(code)) return "Fog";
        if ([51, 53, 55, 56, 57].includes(code)) return "Drizzle";
        if ([61, 63, 65, 66, 67, 80, 81, 82].includes(code)) return "Rain";
        if ([71, 73, 75, 77, 85, 86].includes(code)) return "Snow";
        if ([95, 96, 99].includes(code)) return "Thunderstorm";
        return "Forecast";
    };

    const rideAdvice = (code, rain, wind, temp) => {
        if ([95, 96, 99].includes(code)) return "Not a good riding window: thunderstorm risk.";
        if ([61, 63, 65, 66, 67, 80, 81, 82].includes(code) || rain >= 50) {
            return "Ride with care: rain risk is high, so visibility and braking distance may be worse.";
        }
        if (wind >= 35) return "Ride with care: strong wind can make open streets and bridges uncomfortable.";
        if (temp <= 3) return "Ride with care: cold conditions can mean slippery patches, especially early or late.";
        return "Good riding window: conditions look manageable, but check the sky before you leave.";
    };

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error("Weather request failed");
        const data = await response.json();
        const current = data.current;
        const daily = data.daily;

        tempEl.textContent = `${Math.round(current.temperature_2m)}°`;
        nowEl.textContent = `${weatherText(current.weather_code)} now · wind ${Math.round(current.wind_speed_10m)} km/h`;
        rideNoteEl.textContent = rideAdvice(
            current.weather_code,
            daily.precipitation_probability_max?.[0] ?? 0,
            current.wind_speed_10m,
            current.temperature_2m
        );

        ["Today", "Tomorrow", "Day after"].forEach((label, index) => {
            const high = Math.round(daily.temperature_2m_max[index]);
            const low = Math.round(daily.temperature_2m_min[index]);
            const rain = daily.precipitation_probability_max?.[index];
            dayEls[index].innerHTML = `<span>${label}</span><strong>${high}° / ${low}°</strong><span>${weatherText(daily.weather_code[index])}${rain !== undefined ? ` · ${rain}% rain` : ""}</span>`;
        });
    } catch (error) {
        tempEl.textContent = "--°";
        nowEl.textContent = "Weather preview unavailable. Check conditions before riding.";
        rideNoteEl.textContent = "No live ride note available right now.";
    }
}

function renderCrashTypePrompt() {
    const prompt = document.querySelector("#crash-type-prompt");
    const chart = document.querySelector("#crash-type-chart");
    if (!prompt || !chart) return;

    const options = Array.from(prompt.querySelectorAll(".crash-option"));
    const reveal = prompt.querySelector(".crash-reveal");
    const result = prompt.querySelector(".crash-result");
    const correct = new Set(["turning", "crossing"]);
    const selected = new Set();
    chart.hidden = true;

    options.forEach(option => {
        option.dataset.correct = String(correct.has(option.dataset.answer));
        option.addEventListener("click", () => {
            const value = option.dataset.answer;
            if (selected.has(value)) {
                selected.delete(value);
                option.classList.remove("is-selected");
            } else {
                if (selected.size >= 2) {
                    const first = selected.values().next().value;
                    selected.delete(first);
                    const firstOption = options.find(item => item.dataset.answer === first);
                    firstOption?.classList.remove("is-selected");
                }
                selected.add(value);
                option.classList.add("is-selected");
            }
            reveal.disabled = selected.size !== 2;
        });
    });

    reveal.addEventListener("click", () => {
        options.forEach(option => {
            option.classList.add("is-revealed");
            option.disabled = true;
        });
        reveal.disabled = true;
        result.textContent = "The two largest categories were turning crashes and crossing/entering crashes. Together, they made up 57% of Berlin’s bicycle-involved injury crashes in 2024.";
        chart.hidden = false;
        prompt.scrollIntoView({ behavior: "smooth", block: "start" });
    });
}

renderSplitIndexChart();
renderCyclistTypesChart();
renderAgeGapChart();
renderCrashTypePrompt();
renderBerlinWeather();
