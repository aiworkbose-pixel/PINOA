
import streamlit as st
import pandas as pd
from datetime import datetime

from network_monitor import collect_metrics
from alarm_detector import detect_alarms
from congestion_monitor import analyze_congestion
from incident_correlation import correlate_incidents


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="PINOA - Network Operations",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 PINOA")
st.subheader("PRTG Intelligent Network Operations Assistant")

st.success("SIMULATED NETWORK MONITORING")

st.caption(
    "Read-only laboratory environment | "
    "No live PRTG connection"
)


# --------------------------------------------------
# COLLECT SHARED MONITORING DATA
# --------------------------------------------------

monitoring_results = collect_metrics()

alarm_results = detect_alarms(monitoring_results)

congestion_results = analyze_congestion()

last_updated = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# --------------------------------------------------
# DEVICE ROLE INFORMATION
# --------------------------------------------------

device_roles = {
    "ISP-CORE-R1": "Core Router",
    "ISP-CORE-R2": "Core Router",
    "ISP-PE-R1": "Provider Edge",
    "ISP-PE-R2": "Provider Edge",
    "ISP-POP-DELHI": "POP Router",
    "ISP-POP-MUMBAI": "POP Router",
    "ISP-UPLINK-01": "Backbone Uplink",
    "ISP-FW-01": "Firewall",
    "ISP-SW-01": "Switch",
    "ISP-BNG-01": "Broadband Gateway"
}


# --------------------------------------------------
# DEVICE HEALTH DASHBOARD
# --------------------------------------------------

records = []

for item in monitoring_results:

    records.append({
        "Device": item["device"],
        "Role": device_roles.get(item["device"], "Network Device"),
        "CPU (%)": item["cpu"],
        "Memory (%)": item["memory"],
        "Bandwidth (Mbps)": item["bandwidth"],
        "Latency (ms)": item["latency"],
        "Packet Loss (%)": item["packet_loss"],
        "Severity": item["severity"],
        "Issues": ", ".join(item["issues"])
        if item["issues"] else "None"
    })

df = pd.DataFrame(records)

critical = len(alarm_results["critical"])
high = len(alarm_results["high"])
medium = len(alarm_results["medium"])
normal = len(alarm_results["normal"])


st.caption(f"Last simulated update: {last_updated}")

st.header("📊 Network Health Overview")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Devices", len(df))
c2.metric("Critical", critical)
c3.metric("High", high)
c4.metric("Medium", medium)
c5.metric("Normal", normal)


# --------------------------------------------------
# NETWORK DEVICE MONITORING
# --------------------------------------------------

st.divider()

st.header("🖥️ Network Device Health")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# BACKBONE CONGESTION MONITORING
# --------------------------------------------------

st.divider()

st.header("📈 Backbone Uplink Monitoring")

samples = congestion_results["samples"]

if samples:

    latest_sample = samples[-1]

    traffic = latest_sample["traffic"]
    utilization = latest_sample["utilization"]
    congestion_status = latest_sample["status"]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Link Capacity",
        f'{congestion_results["capacity"]} Mbps'
    )

    c2.metric(
        "Latest Traffic Sample",
        f"{traffic} Mbps"
    )

    c3.metric(
        "Latest Utilization",
        f"{utilization:.1f}%"
    )

    c4.metric(
        "Peak Utilization",
        f'{congestion_results["peak_utilization"]:.1f}%'
    )

    st.progress(
        min(int(utilization), 100)
    )

    if congestion_status == "CRITICAL":
        st.error(f"Backbone Status: {congestion_status}")
    elif congestion_status == "WARNING":
        st.warning(f"Backbone Status: {congestion_status}")
    else:
        st.success(f"Backbone Status: {congestion_status}")

    # Traffic history from shared congestion module
    chart_df = pd.DataFrame({
        "Sample": [item["sample"] for item in samples],
        "Traffic (Mbps)": [item["traffic"] for item in samples]
    })

    chart_df = chart_df.set_index("Sample")

    st.subheader("Backbone Traffic History")

    st.line_chart(chart_df)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Critical Samples",
        congestion_results["critical_count"]
    )

    c2.metric(
        "Warning Samples",
        congestion_results["warning_count"]
    )

    c3.metric(
        "Normal Samples",
        congestion_results["normal_count"]
    )

else:
    st.info("No congestion samples available.")


# --------------------------------------------------
# NOC ALARM CENTRE
# --------------------------------------------------

st.divider()

st.header("🚨 NOC Alarm Centre")

alarm_records = []

for severity in ["critical", "high", "medium"]:
    for device in alarm_results[severity]:
        alarm_records.append({
            "Device": device,
            "Severity": severity.upper()
        })

if alarm_records:
    alarm_df = pd.DataFrame(alarm_records)
    st.dataframe(alarm_df, use_container_width=True, hide_index=True)
else:
    st.success("No active simulated device alarms.")


# --------------------------------------------------
# INCIDENT CORRELATION
# --------------------------------------------------

st.divider()

st.header("🔍 Incident Correlation")

st.caption(
    "Topology-based investigation using the shared "
    "simulated device metrics."
)

if st.button("Run Incident Correlation"):

    with st.spinner("Analyzing potential incident relationships..."):

        correlation_result = correlate_incidents(monitoring_results)

    if correlation_result:

        st.warning(
            "Potential common source identified: "
            + correlation_result["root"]
        )

        st.write(
            "Correlated downstream devices:",
            ", ".join(correlation_result["impacted"])
        )

        st.write(
            "Correlated alert count:",
            correlation_result["correlated_count"]
        )

    else:
        st.info(
            "No potential common source identified "
            "in this simulated snapshot."
        )

    st.caption(
        "Correlation does not prove causation. "
        "Verify actual measurements and timestamps."
    )


# --------------------------------------------------
# NOC RECOMMENDATIONS
# --------------------------------------------------

st.divider()

st.header("🧠 NOC Recommendations")

if congestion_results["peak_utilization"] >= 95:

    st.error(
        "Possible backbone congestion. "
        "Investigate traffic trends, interface errors "
        "and packet discards."
    )

elif congestion_results["peak_utilization"] >= 85:

    st.warning(
        "Elevated backbone utilization. "
        "Monitor traffic patterns during peak hours."
    )

else:

    st.success(
        "Backbone utilization is within normal limits."
    )


if critical > 0:

    st.error(
        f"{critical} device(s) have CRITICAL severity. "
        "Prioritize investigation."
    )

elif high > 0:

    st.warning(
        f"{high} device(s) have HIGH severity. "
        "Review their reported issues."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.info(
    "PINOA is currently operating in a simulated "
    "laboratory environment. No production network "
    "or live PRTG system is connected."
)

st.caption(
    "PINOA | Network Intelligence Lab | Read-only simulation"
)
