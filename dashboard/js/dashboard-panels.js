
(() => {
"use strict";

const API = window.location.origin;
const C = {
    blue: "#168bff",
    purple: "#b380e9",
    cyan: "#39ddf5",
    orange: "#ffaa55",
    red: "#ff557a",
    green: "#36e6a7",
    yellow: "#eedb5e",
    slate: "#334B68"
};

const n = v => Number.isFinite(Number(v)) ? Number(v) : 0;
const avg = (rows,key) => rows.length
    ? rows.reduce((s,r)=>s+n(r[key]),0)/rows.length : 0;

const count = (rows,key) => rows.reduce((o,r)=>{
    const k=String(r[key]||"Unknown");
    o[k]=(o[k]||0)+1;
    return o;
},{});

const safe = v => String(v??"").replace(/[&<>"']/g,c=>({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
}[c]));

async function get(path) {
    const response=await fetch(API+path);
    if(!response.ok) throw new Error(`API ${response.status}`);
    return response.json();
}

async function records(domain) {
    const first=await get(`/domains/${domain}/records?limit=500`);
    const result=[...(first.records||[])];
    for(let offset=500;offset<first.total;offset+=500){
        const page=await get(`/domains/${domain}/records?limit=500&offset=${offset}`);
        result.push(...(page.records||[]));
    }
    return result;
}

function metric(label,value,detail,color="cyan"){
    return `<article class="intel-metric">
        <span>${safe(label)}</span>
        <strong class="${color}">${safe(value)}</strong>
        <small>${safe(detail)}</small>
    </article>`;
}

function chart(title,subtitle,id){
    return `<article class="intel-card">
        <h3>${safe(title)}</h3><small>${safe(subtitle)}</small>
        <div class="intel-chart" id="${id}"></div>
    </article>`;
}

function table(title,subtitle,id){
    return `<article class="intel-card intel-wide">
        <h3>${safe(title)}</h3><small>${safe(subtitle)}</small>
        <div class="intel-table-wrap" id="${id}"></div>
    </article>`;
}

function shell(kicker,description,metrics,content){
    return `<div class="intel-kicker">${safe(kicker)}</div>
        <p class="intel-description">${safe(description)}</p>
        <div class="intel-metrics">${metrics}</div>
        <div class="intel-grid">${content}</div>`;
}


function plot(id,data,extra={}){
    const el=document.getElementById(id);
    if(!el||!window.Plotly) return;

    window.Plotly.newPlot(el,data,{
        paper_bgcolor:"rgba(0,0,0,0)",
        plot_bgcolor:"rgba(0,0,0,0)",
        font:{color:"#AFC2DC",family:"Montserrat, sans-serif",size:11},
        margin:{l:42,r:15,t:12,b:45},
        xaxis:{gridcolor:"rgba(130,160,200,.10)"},
        yaxis:{gridcolor:"rgba(130,160,200,.10)"},
        legend:{orientation:"h",y:-0.2},

        colorway:[
            C.blue,
            C.purple,
            C.cyan,
            C.orange,
            C.red,
            C.green
        ],

        barcornerradius: 10,

        ...extra
    },{responsive:true,displayModeBar:false});
}


function renderTable(id,headers,rows){
    const el=document.getElementById(id);
    if(!el)return;
    el.innerHTML=`<table class="intel-table">
    <thead><tr>${headers.map(h=>`<th>${h.label}</th>`).join("")}</tr></thead>
    <tbody>${rows.map(row=>`<tr>${headers.map(h=>
        `<td>${h.value? h.value(row):safe(row[h.key])}</td>`
    ).join("")}</tr>`).join("")}</tbody></table>`;
}

function pill(value){
    const v=String(value||"");
    const level=v.toUpperCase();
    const cls=level.includes("CRITICAL")||level.includes("HIGH")
        ?"danger":level.includes("MODERATE")||level.includes("ELEVATED")
        ?"warning":"good";
    return `<span class="intel-pill ${cls}">${safe(v)}</span>`;
}

async function cybersecurity(){
    const el=document.getElementById("cyber-detail");
    el.innerHTML='<p class="intel-loading">Loading threat intelligence…</p>';
    const rows=await records("cybersecurity");
    const levels=count(rows,"risk_level");
    const anomalies=rows.filter(r=>String(r.is_anomaly).toLowerCase()==="true").length;
    const ransomware=rows.filter(r=>String(r.knownRansomwareCampaignUse).toLowerCase()==="known").length;
    const top=[...rows].sort((a,b)=>n(b.risk_score)-n(a.risk_score)).slice(0,10);

    el.innerHTML=shell("THREAT INTELLIGENCE / LIVE DATA",
        "Vulnerability prioritization, ransomware campaign use and statistical anomalies. Risk scores are heuristic prioritization scores, not calibrated probabilities.",
        metric("Vulnerabilities",rows.length.toLocaleString(),"CVE records")+
        metric("Critical vulnerabilities",n(levels.CRITICAL).toLocaleString(),"Risk engine classification","red")+
        metric("Mean risk score",avg(rows,"risk_score").toFixed(2),"Heuristic score · 0–100")+
        metric("Known ransomware use",ransomware.toLocaleString(),"Known campaign-use records","orange")+
        metric("Statistical anomalies",anomalies.toLocaleString(),"Flagged for investigation","purple")+
        metric("Mean CVSS",avg(rows,"cvss_base_score").toFixed(2),"CVSS · 0–10"),
        chart("Risk severity","Vulnerability distribution","ic-severity")+
        chart("Ransomware campaign use","Known versus unknown","ic-ransomware")+
        chart("Anomaly investigation","Flagged versus not flagged","ic-anomalies")+
        table("Priority vulnerability watchlist","Top 10 by heuristic risk score","ic-table")
    );

    const order=["CRITICAL","HIGH","MEDIUM","LOW"];

    plot("ic-severity",[{
        type:"bar",
        x:order,
        y:order.map(k=>levels[k]||0),
        marker:{
            color:[
                "#FF557A",
                "#FFAA55",
                "#EEDB5E",
                "#36E6A7"
            ]
        }
    }]);

    const rw=count(rows,"knownRansomwareCampaignUse");

    plot("ic-ransomware",[{
        type:"pie",
        labels:["Unknown","Known"],
        values:[rw.Unknown||0,rw.Known||0],
        hole:.62,
        marker:{
            colors:[
                "#168BFF",
                "#FFAA55"
            ]
        }
    }]);

    plot("ic-anomalies",[{
        type:"pie",
        labels:["Flagged","Not flagged"],
        values:[anomalies,rows.length-anomalies],
        hole:.62,
        marker:{
            colors:[
                "#FF557A",
                "#36E6A7"
            ]
        }
    }]);

    renderTable("ic-table",[
        {label:"CVE",key:"cveID"},
        {label:"Vendor / product",value:r=>safe(`${r.vendorProject} / ${r.product}`)},
        {label:"CVSS",value:r=>n(r.cvss_base_score).toFixed(1)},
        {label:"Risk",value:r=>n(r.risk_score).toFixed(1)},
        {label:"Severity",value:r=>pill(r.risk_level)},
        {label:"Ransomware",key:"knownRansomwareCampaignUse"}
    ],top);
}

async function climate(){
    const el=document.getElementById("climate-detail");
    el.innerHTML='<p class="intel-loading">Loading climate intelligence…</p>';
    const rows=await records("climate");
    const cats=count(rows,"climate_exposure_category");
    const top=[...rows].sort((a,b)=>n(b.climate_exposure_index)-n(a.climate_exposure_index)).slice(0,10);

    el.innerHTML=shell("CLIMATE EXPOSURE / COUNTRY-YEAR",
        "Climate exposure, thermal extremes and precipitation anomalies. Each observation represents a country and year.",
        metric("Mean exposure index",avg(rows,"climate_exposure_index").toFixed(2),"Index · 0–100")+
        metric("Country-year records",rows.length.toLocaleString(),"Climate observations")+
        metric("Mean temperature",avg(rows,"mean_temperature").toFixed(1)+" °C","Across available records","orange")+
        metric("Extreme heat days",avg(rows,"extreme_heat_days").toFixed(1),"Average days per record","orange")+
        metric("Mean precipitation",avg(rows,"annual_precipitation_mm").toFixed(0)+" mm","Annual precipitation")+
        metric("High exposure records",n(cats.High).toLocaleString(),"Category: High","red"),
        chart("Exposure categories","Country-year distribution","icl-categories")+
        chart("Highest exposure records","Top country-year observations","icl-ranking")+
        chart("Thermal extremes","Average extreme heat and cold days","icl-extremes")+
        table("Climate exposure watchlist","Top 10 exposure records","icl-table")
    );

    plot("icl-categories",[{
        type:"pie",
        labels:Object.keys(cats),
        values:Object.values(cats),
        hole:.62,
        marker:{
            colors:[
                C.blue,
                C.purple,
                C.orange,
                C.green
            ]
        }
    }]);

    plot("icl-ranking",[{
    type:"bar",
    x:top.map(r=>`${r.country} (${r.year})`),
    y:top.map(r=>n(r.climate_exposure_index)),
    marker:{
        color:C.cyan,
        cornerradius: 8
    }
}],{margin:{l:42,r:15,t:12,b:95},xaxis:{tickangle:-35}});

    plot("icl-extremes",[
        {
            type:"bar",
            name:"Extreme heat",
            x:["Average days"],
            y:[avg(rows,"extreme_heat_days")],
            marker:{color:C.orange}
        },
        {
            type:"bar",
            name:"Extreme cold",
            x:["Average days"],
            y:[avg(rows,"extreme_cold_days")],
            marker:{color:C.purple}
        }
    ],{barmode:"group"});

    renderTable("icl-table",[
        {label:"Country",key:"country"},{label:"Year",key:"year"},
        {label:"Exposure",value:r=>n(r.climate_exposure_index).toFixed(2)},
        {label:"Category",value:r=>pill(r.climate_exposure_category)},
        {label:"Heat days",key:"extreme_heat_days"},
        {label:"Cold days",key:"extreme_cold_days"}
    ],top);
}

async function economy(){
    const el=document.getElementById("economy-detail");
    el.innerHTML='<p class="intel-loading">Loading economic intelligence…</p>';
    const rows=await records("economy");
    const cats=count(rows,"economic_risk_category");
    const top=[...rows].sort((a,b)=>n(b.economic_risk_score)-n(a.economic_risk_score)).slice(0,10);

    el.innerHTML=shell("ECONOMIC RISK / COUNTRY-YEAR",
        "Comparative risk indicators for growth, inflation and unemployment. These are normalized risk scores, not raw macroeconomic rates.",
        metric("Mean economic risk",avg(rows,"economic_risk_score").toFixed(2),"Score · 0–100")+
        metric("Country-year records",rows.length.toLocaleString(),"Economic observations")+
        metric("Growth risk",avg(rows,"growth_risk_score").toFixed(2),"Normalized indicator","purple")+
        metric("Inflation risk",avg(rows,"inflation_risk_score").toFixed(2),"Normalized indicator","orange")+
        metric("Unemployment risk",avg(rows,"unemployment_risk_score").toFixed(2),"Normalized indicator","blue")+
        metric("Moderate risk records",n(cats.MODERATE).toLocaleString(),"Category: Moderate","orange"),
        chart("Economic risk categories","Country-year distribution","ie-categories")+
        chart("Risk indicator comparison","Mean normalized component scores","ie-indicators")+
        chart("Highest economic risk","Top country-year observations","ie-ranking")+
        table("Economic risk watchlist","Top 10 economic risk records","ie-table")
    );

    plot("ie-categories",[{
        type:"pie",labels:Object.keys(cats),values:Object.values(cats),hole:.62
    }]);

    plot("ie-indicators",[{
        type:"bar",
        x:["Growth","Inflation","Unemployment"],
        y:[avg(rows,"growth_risk_score"),avg(rows,"inflation_risk_score"),avg(rows,"unemployment_risk_score")],
        marker:{
            color:[C.purple,C.orange,C.blue],
            cornerradius: 8
        }
    }]);

    plot("ie-ranking",[{
    type:"bar",
    x:top.map(r=>`${r.country} (${r.year})`),
    y:top.map(r=>n(r.economic_risk_score)),
    marker:{
        color:C.cyan,
        cornerradius: 8
    }
}],{margin:{l:42,r:15,t:12,b:95},xaxis:{tickangle:-35}});

    renderTable("ie-table",[
        {label:"Country",key:"country"},{label:"Year",key:"year"},
        {label:"Economic risk",value:r=>n(r.economic_risk_score).toFixed(2)},
        {label:"Growth",value:r=>n(r.growth_risk_score).toFixed(2)},
        {label:"Inflation",value:r=>n(r.inflation_risk_score).toFixed(2)},
        {label:"Unemployment",value:r=>n(r.unemployment_risk_score).toFixed(2)},
        {label:"Category",value:r=>pill(r.economic_risk_category)}
    ],top);
}

async function systemHealth(){
    const el=document.getElementById("system-detail");
    el.innerHTML='<p class="intel-loading">Checking system health…</p>';
    const [health,report]=await Promise.all([get("/health"),get("/domains")]);
    const domains=Object.entries(report.domains||{});
    const total=domains.reduce((s,[,d])=>s+n(d.records),0);

    el.innerHTML=shell("PLATFORM MONITORING / API STATUS",
        "Live operational checks from the Sentinel AI REST API and multidomain orchestrator.",
        metric("System status",health.status,"API health endpoint",health.status==="OPERATIONAL"?"green":"red")+
        metric("Available domains",`${health.domains_available}/${health.domains_total}`,"Orchestrator availability")+
        metric("Monitored records",total.toLocaleString(),"Across domain sources"),
        `<article class="intel-card intel-wide">
            <h3>Domain service status</h3>
            <div class="intel-health-list">
            ${domains.map(([name,d])=>`<div class="intel-health-row">
                <div><strong>${safe(name)}</strong><small>${safe(d.records)} records · ${safe(d.unit||"Data")}</small></div>
                ${pill(d.status)}
            </div>`).join("")}
            </div>
            <small>Last checked: ${safe(new Date().toLocaleString())}</small>
        </article>`
    );
}

async function renderAll(){
    const panels=[
        ["Cybersecurity","cyber-detail",cybersecurity],
        ["Climate","climate-detail",climate],
        ["Economy","economy-detail",economy],
        ["System Health","system-detail",systemHealth]
    ];
    for(const [name,id,fn] of panels){
        try{await fn();}
        catch(error){
            console.error(name,error);
            const el=document.getElementById(id);
            if(el)el.innerHTML=`<p class="intel-error">Unable to load ${safe(name)}. Check API connection.</p>`;
        }
    }
}

function initialize(){
    if(document.getElementById("cyber-detail"))renderAll();
}
if(document.readyState==="loading"){
    document.addEventListener("DOMContentLoaded",initialize,{once:true});
}else initialize();

window.SentinelPanels={refresh:renderAll};
})();
