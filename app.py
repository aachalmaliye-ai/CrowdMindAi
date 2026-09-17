import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import heapq
import random
import streamlit.components.v1 as components
from collections import deque

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CrowdMind AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #eef2ff 0%,
        #f8fafc 50%,
        #eefcf8 100%
    );
}

.block-container {
    padding-top: 1.5rem;
}

.hero {
    padding: 30px;
    border-radius: 25px;
    text-align: center;
    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed,
        #0891b2
    );
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
}

.hero h1 {
    font-size: 48px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 18px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.feature {
    background: white;
    padding: 20px;
    border-radius: 18px;
    border-left: 5px solid #6366f1;
    box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    margin-bottom: 15px;
    min-height: 130px;
}

.voice {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        #6366f1,
        #9333ea
    );
    color: white;
}

.big {
    font-size: 34px;
    font-weight: 800;
}

.small {
    color: #64748b;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak(text):

    safe_text = (
        text.replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("\n", " ")
    )

    components.html(
        f"""
        <script>

        window.speechSynthesis.cancel();

        let message = `{safe_text}`;

        let speech =
            new SpeechSynthesisUtterance(message);

        speech.rate = 0.9;
        speech.pitch = 1;
        speech.volume = 1;

        window.speechSynthesis.speak(speech);

        </script>
        """,
        height=0
    )


# ============================================================
# EVENT LOCATIONS / GRAPH
# ============================================================

event_graph = {

    "Main Gate": [
        ("Registration", 80),
        ("Food Court", 120)
    ],

    "Registration": [
        ("Main Gate", 80),
        ("Main Hall", 100),
        ("Help Desk", 60)
    ],

    "Food Court": [
        ("Main Gate", 120),
        ("Open Ground", 100)
    ],

    "Main Hall": [
        ("Registration", 100),
        ("Auditorium", 70),
        ("Exhibition", 90)
    ],

    "Help Desk": [
        ("Registration", 60),
        ("Medical Room", 80)
    ],

    "Open Ground": [
        ("Food Court", 100),
        ("Exhibition", 110)
    ],

    "Auditorium": [
        ("Main Hall", 70),
        ("Exhibition", 80)
    ],

    "Exhibition": [
        ("Main Hall", 90),
        ("Open Ground", 110),
        ("Auditorium", 80)
    ],

    "Medical Room": [
        ("Help Desk", 80)
    ]
}


# ============================================================
# GRAPH COORDINATES
# ============================================================

coordinates = {

    "Main Gate": (0, 0),
    "Registration": (1, 1),
    "Food Court": (1, -1),
    "Main Hall": (2, 1),
    "Help Desk": (2, 2),
    "Open Ground": (2, -1),
    "Auditorium": (3, 2),
    "Exhibition": (3, 0),
    "Medical Room": (3, 3)

}


# ============================================================
# BFS
# ============================================================

def bfs(graph, start, goal):

    queue = deque([[start]])
    visited = set()

    while queue:

        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path

        if node not in visited:

            visited.add(node)

            for neighbor, distance in graph[node]:

                if neighbor not in visited:

                    queue.append(
                        path + [neighbor]
                    )

    return None


# ============================================================
# DIJKSTRA
# ============================================================

def dijkstra(graph, start, goal):

    queue = [
        (0, start, [start])
    ]

    visited = set()

    while queue:

        cost, node, path = heapq.heappop(queue)

        if node == goal:
            return path, cost

        if node in visited:
            continue

        visited.add(node)

        for neighbor, distance in graph[node]:

            if neighbor not in visited:

                heapq.heappush(
                    queue,
                    (
                        cost + distance,
                        neighbor,
                        path + [neighbor]
                    )
                )

    return None, 0


# ============================================================
# PATH DISTANCE
# ============================================================

def path_distance(path):

    if not path:
        return 0

    total = 0

    for i in range(len(path) - 1):

        current = path[i]
        next_node = path[i + 1]

        for neighbor, distance in event_graph[current]:

            if neighbor == next_node:

                total += distance
                break

    return total


# ============================================================
# DRAW EVENT MAP
# ============================================================

def draw_event_map(highlight=None):

    G = nx.Graph()

    for node in event_graph:

        G.add_node(node)

        for neighbor, distance in event_graph[node]:

            G.add_edge(
                node,
                neighbor,
                weight=distance
            )

    fig, ax = plt.subplots(
        figsize=(12, 7)
    )

    nx.draw(
        G,
        coordinates,
        with_labels=True,
        node_size=2800,
        font_size=8,
        ax=ax
    )

    if highlight:

        edges = []

        for i in range(len(highlight) - 1):

            edges.append(
                (
                    highlight[i],
                    highlight[i + 1]
                )
            )

        nx.draw_networkx_edges(
            G,
            coordinates,
            edgelist=edges,
            width=5,
            ax=ax
        )

    labels = nx.get_edge_attributes(
        G,
        "weight"
    )

    nx.draw_networkx_edge_labels(
        G,
        coordinates,
        edge_labels=labels,
        ax=ax
    )

    ax.set_title(
        "🎪 Smart Event Digital Map"
    )

    ax.axis("off")

    st.pyplot(
        fig,
        clear_figure=True
    )


# ============================================================
# CROWD DATA
# ============================================================

crowd_data = pd.DataFrame({

    "Zone": [
        "Main Gate",
        "Registration",
        "Food Court",
        "Main Hall",
        "Help Desk",
        "Open Ground",
        "Auditorium",
        "Exhibition",
        "Medical Room"
    ],

    "Capacity": [
        500,
        150,
        300,
        400,
        80,
        600,
        300,
        350,
        50
    ],

    "People": [
        420,
        135,
        240,
        380,
        30,
        270,
        190,
        310,
        12
    ]

})

crowd_data["Occupancy"] = (
    crowd_data["People"]
    /
    crowd_data["Capacity"]
    * 100
)


# ============================================================
# CROWD STATUS
# ============================================================

def crowd_status(value):

    if value >= 90:
        return "🔴 Critical"

    elif value >= 70:
        return "🟠 High"

    elif value >= 40:
        return "🟡 Moderate"

    else:
        return "🟢 Low"


crowd_data["Status"] = crowd_data[
    "Occupancy"
].apply(crowd_status)


# ============================================================
# AI CROWD PREDICTION
# ============================================================

def predict_crowd(current, event_type, hour):

    multiplier = 1.0

    if event_type == "Concert":
        multiplier = 1.35

    elif event_type == "Workshop":
        multiplier = 0.90

    elif event_type == "Seminar":
        multiplier = 1.10

    elif event_type == "Exhibition":
        multiplier = 1.20

    if 12 <= hour <= 14:
        multiplier += 0.15

    if 17 <= hour <= 20:
        multiplier += 0.20

    prediction = current * multiplier

    return min(
        round(prediction),
        100
    )


# ============================================================
# QUEUE DATA
# ============================================================

queue_data = pd.DataFrame({

    "Queue": [
        "Registration",
        "Food Court",
        "Main Hall Entry",
        "Exhibition",
        "Help Desk"
    ],

    "People": [
        135,
        90,
        120,
        75,
        20
    ],

    "Avg Service Time": [
        2,
        3,
        1,
        2,
        2
    ]

})

queue_data["Estimated Wait"] = (
    queue_data["People"]
    *
    queue_data["Avg Service Time"]
)


# ============================================================
# AI QUEUE PRIORITY
# ============================================================

def queue_priority(people, service_time):

    score = (
        people * 0.7
        +
        service_time * 10 * 0.3
    )

    return round(score, 2)


queue_data["Priority Score"] = queue_data.apply(

    lambda row: queue_priority(
        row["People"],
        row["Avg Service Time"]
    ),

    axis=1
)


# ============================================================
# VOLUNTEER DATA
# ============================================================

volunteers = pd.DataFrame({

    "Volunteer": [
        "Aarav",
        "Diya",
        "Rahul",
        "Anaya",
        "Rohan",
        "Priya"
    ],

    "Skill": [
        "Registration",
        "Medical",
        "Crowd Control",
        "Registration",
        "Technical",
        "Crowd Control"
    ],

    "Availability": [
        "Available",
        "Available",
        "Available",
        "Busy",
        "Available",
        "Available"
    ]

})


# ============================================================
# EXPERT SYSTEM
# ============================================================

def crowd_expert(
    occupancy,
    queue_people,
    event_type
):

    recommendations = []

    if occupancy >= 90:

        recommendations.append(
            "Critical crowd detected. "
            "Open an alternate entry or zone."
        )

    elif occupancy >= 70:

        recommendations.append(
            "Crowd level is high. "
            "Deploy additional volunteers."
        )

    else:

        recommendations.append(
            "Crowd level is currently manageable."
        )

    if queue_people >= 100:

        recommendations.append(
            "Long queue detected. "
            "Open another service counter."
        )

    elif queue_people >= 50:

        recommendations.append(
            "Moderate queue detected. "
            "Monitor the waiting area."
        )

    else:

        recommendations.append(
            "Queue length is under control."
        )

    if event_type == "Concert":

        recommendations.append(
            "Use multiple entry gates for concert events."
        )

    elif event_type == "Exhibition":

        recommendations.append(
            "Use one-way visitor flow for exhibition zones."
        )

    else:

        recommendations.append(
            "Use normal crowd monitoring."
        )

    return recommendations


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🤖 CrowdMind AI"
)

st.sidebar.caption(
    "Intelligent Event Crowd & Queue Optimizer"
)

st.sidebar.divider()

menu = st.sidebar.radio(

    "📌 Navigation",

    [
        "🏠 Dashboard",
        "👥 Crowd Monitor",
        "🚶 Smart Route",
        "🚦 Queue Optimizer",
        "🔮 Crowd Predictor",
        "🧑‍💼 Volunteer Manager",
        "🧠 AI Event Advisor",
        "🔊 Voice Assistant"
    ]

)

st.sidebar.divider()

st.sidebar.info(
    "💡 AI-powered event management "
    "simulation system."
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

    <h1>🤖 CrowdMind AI</h1>

    <p>
    Intelligent Event Crowd & Queue Optimizer
    </p>

    <p>
    Predict • Analyze • Optimize • Assist
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DASHBOARD
# ============================================================

if menu == "🏠 Dashboard":

    st.subheader(
        "🌟 Event Intelligence Dashboard"
    )

    total_people = crowd_data["People"].sum()

    average_occupancy = crowd_data[
        "Occupancy"
    ].mean()

    critical_zones = len(
        crowd_data[
            crowd_data["Occupancy"] >= 90
        ]
    )

    total_queue = queue_data[
        "People"
    ].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "👥 Total Visitors",
        f"{total_people:,}"
    )

    c2.metric(
        "📊 Avg Occupancy",
        f"{average_occupancy:.1f}%"
    )

    c3.metric(
        "🔴 Critical Zones",
        critical_zones
    )

    c4.metric(
        "🚶 People in Queues",
        total_queue
    )

    st.divider()

    st.subheader(
        "✨ Smart Features"
    )

    a, b, c = st.columns(3)

    with a:

        st.markdown(
            """
            <div class="feature">

            👥 <b>Crowd Monitoring</b>

            <br><br>

            Monitor visitor density
            and identify crowded zones.

            </div>
            """,
            unsafe_allow_html=True
        )

    with b:

        st.markdown(
            """
            <div class="feature">

            🚶 <b>Smart Routing</b>

            <br><br>

            Find efficient paths and
            avoid crowded locations.

            </div>
            """,
            unsafe_allow_html=True
        )

    with c:

        st.markdown(
            """
            <div class="feature">

            🔮 <b>Crowd Prediction</b>

            <br><br>

            Predict future crowd levels
            using event conditions.

            </div>
            """,
            unsafe_allow_html=True
        )

    a, b, c = st.columns(3)

    with a:

        st.markdown(
            """
            <div class="feature">

            🚦 <b>Queue Optimizer</b>

            <br><br>

            Calculate waiting time and
            prioritize long queues.

            </div>
            """,
            unsafe_allow_html=True
        )

    with b:

        st.markdown(
            """
            <div class="feature">

            🧠 <b>AI Event Advisor</b>

            <br><br>

            Get intelligent crowd
            management recommendations.

            </div>
            """,
            unsafe_allow_html=True
        )

    with c:

        st.markdown(
            """
            <div class="feature">

            🔊 <b>Voice Assistant</b>

            <br><br>

            Listen to AI announcements
            using Text-to-Speech.

            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader(
        "🎪 Live Event Map"
    )

    draw_event_map()

    st.success(
        "🤖 CrowdMind AI is actively monitoring "
        "the simulated event."
    )


# ============================================================
# CROWD MONITOR
# ============================================================

elif menu == "👥 Crowd Monitor":

    st.subheader(
        "👥 Real-Time Crowd Monitoring"
    )

    st.dataframe(
        crowd_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    selected_zone = st.selectbox(
        "📍 Select Zone",
        crowd_data["Zone"]
    )

    selected = crowd_data[
        crowd_data["Zone"] == selected_zone
    ].iloc[0]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "👥 People",
        int(selected["People"])
    )

    c2.metric(
        "🏢 Capacity",
        int(selected["Capacity"])
    )

    c3.metric(
        "📊 Occupancy",
        f"{selected['Occupancy']:.1f}%"
    )

    st.progress(
        min(
            selected["Occupancy"] / 100,
            1.0
        )
    )

    st.info(
        f"Current Status: {selected['Status']}"
    )

    st.subheader(
        "📊 Occupancy by Zone"
    )

    chart = crowd_data.set_index(
        "Zone"
    )["Occupancy"]

    st.bar_chart(chart)

    if st.button(
        "🔊 Read Crowd Status"
    ):

        speak(
            f"The {selected_zone} currently "
            f"has {int(selected['People'])} people. "
            f"Occupancy is "
            f"{selected['Occupancy']:.1f} percent. "
            f"The current status is "
            f"{selected['Status']}."
        )


# ============================================================
# SMART ROUTE
# ============================================================

elif menu == "🚶 Smart Route":

    st.subheader(
        "🚶 AI Smart Visitor Route Planner"
    )

    st.write(
        "Find an efficient route between "
        "two event locations."
    )

    c1, c2 = st.columns(2)

    with c1:

        start = st.selectbox(
            "📍 Starting Location",
            list(event_graph.keys())
        )

    with c2:

        destination = st.selectbox(
            "🎯 Destination",
            list(event_graph.keys()),
            index=3
        )

    algorithm = st.selectbox(
        "🧠 Routing Algorithm",
        [
            "BFS",
            "Dijkstra"
        ]
    )

    if st.button(
        "🚀 Find Route",
        use_container_width=True
    ):

        if start == destination:

            st.warning(
                "Please choose different locations."
            )

        else:

            if algorithm == "BFS":

                path = bfs(
                    event_graph,
                    start,
                    destination
                )

                distance = path_distance(path)

            else:

                path, distance = dijkstra(
                    event_graph,
                    start,
                    destination
                )

            if path:

                route = " → ".join(path)

                st.success(
                    "✅ Route Found!"
                )

                st.markdown(
                    f"### 🛣️ {route}"
                )

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Algorithm",
                    algorithm
                )

                c2.metric(
                    "Distance",
                    f"{distance} m"
                )

                c3.metric(
                    "Locations",
                    len(path)
                )

                if st.button(
                    "🔊 Speak Route"
                ):

                    speak(
                        f"Your route from "
                        f"{start} to "
                        f"{destination} is "
                        f"{route}. "
                        f"The total distance is "
                        f"{distance} meters."
                    )

                draw_event_map(path)


# ============================================================
# QUEUE OPTIMIZER
# ============================================================

elif menu == "🚦 Queue Optimizer":

    st.subheader(
        "🚦 AI Queue Optimization System"
    )

    st.write(
        "The system calculates estimated waiting "
        "time and queue priority."
    )

    st.dataframe(
        queue_data,
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "📊 Estimated Waiting Time"
    )

    wait_chart = queue_data.set_index(
        "Queue"
    )["Estimated Wait"]

    st.bar_chart(
        wait_chart
    )

    highest = queue_data.loc[
        queue_data["Priority Score"].idxmax()
    ]

    st.warning(
        f"🚨 Highest Priority Queue: "
        f"{highest['Queue']}"
    )

    st.info(
        f"Estimated waiting time: "
        f"{highest['Estimated Wait']} minutes"
    )

    if st.button(
        "🤖 Generate Queue Action"
    ):

        if highest["People"] >= 100:

            action = (
                "Open an additional counter "
                "and deploy another volunteer."
            )

        else:

            action = (
                "Continue monitoring the queue."
            )

        st.success(
            f"AI Action: {action}"
        )

        if st.button(
            "🔊 Speak Queue Action"
        ):

            speak(
                f"The highest priority queue "
                f"is {highest['Queue']}. "
                f"The recommended action is "
                f"{action}"
            )


# ============================================================
# CROWD PREDICTOR
# ============================================================

elif menu == "🔮 Crowd Predictor":

    st.subheader(
        "🔮 AI Crowd Prediction"
    )

    st.write(
        "Predict expected crowd occupancy "
        "based on event conditions."
    )

    c1, c2 = st.columns(2)

    with c1:

        zone = st.selectbox(
            "📍 Select Zone",
            crowd_data["Zone"]
        )

        current = float(
            crowd_data[
                crowd_data["Zone"] == zone
            ]["Occupancy"].iloc[0]
        )

    with c2:

        event_type = st.selectbox(
            "🎪 Event Type",
            [
                "Seminar",
                "Workshop",
                "Concert",
                "Exhibition"
            ]
        )

        hour = st.slider(
            "🕐 Event Hour",
            0,
            23,
            18
        )

    if st.button(
        "🔮 Predict Crowd",
        use_container_width=True
    ):

        prediction = predict_crowd(
            current,
            event_type,
            hour
        )

        st.subheader(
            "📈 Prediction Result"
        )

        st.metric(
            "Predicted Occupancy",
            f"{prediction}%"
        )

        st.progress(
            prediction / 100
        )

        if prediction >= 90:

            st.error(
                "🔴 Critical crowd expected!"
            )

            advice = (
                "Open alternate gates "
                "and deploy additional volunteers."
            )

        elif prediction >= 70:

            st.warning(
                "🟠 High crowd expected."
            )

            advice = (
                "Monitor the area and "
                "increase crowd control."
            )

        else:

            st.success(
                "🟢 Crowd level expected to be manageable."
            )

            advice = (
                "Normal monitoring is sufficient."
            )

        st.info(
            f"🤖 AI Recommendation: {advice}"
        )

        if st.button(
            "🔊 Speak Prediction"
        ):

            speak(
                f"The predicted occupancy "
                f"for {zone} is "
                f"{prediction} percent. "
                f"{advice}"
            )


# ============================================================
# VOLUNTEER MANAGER
# ============================================================

elif menu == "🧑‍💼 Volunteer Manager":

    st.subheader(
        "🧑‍💼 Smart Volunteer Manager"
    )

    st.dataframe(
        volunteers,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    required_skill = st.selectbox(
        "🎯 Required Skill",
        volunteers["Skill"].unique()
    )

    available = volunteers[
        (
            volunteers["Skill"]
            ==
            required_skill
        )
        &
        (
            volunteers["Availability"]
            ==
            "Available"
        )
    ]

    st.subheader(
        "🤖 AI Volunteer Recommendation"
    )

    if len(available) > 0:

        selected_volunteer = available.iloc[0]

        st.success(
            f"Recommended Volunteer: "
            f"{selected_volunteer['Volunteer']}"
        )

        st.info(
            f"Skill: "
            f"{selected_volunteer['Skill']}"
        )

        if st.button(
            "🔊 Announce Volunteer"
        ):

            speak(
                f"{selected_volunteer['Volunteer']} "
                f"is recommended for "
                f"{required_skill} duty."
            )

    else:

        st.error(
            "No available volunteer found."
        )


# ============================================================
# AI EVENT ADVISOR
# ============================================================

elif menu == "🧠 AI Event Advisor":

    st.subheader(
        "🧠 AI Event Management Advisor"
    )

    c1, c2 = st.columns(2)

    with c1:

        occupancy = st.slider(
            "📊 Current Occupancy %",
            0,
            100,
            75
        )

        queue_people = st.slider(
            "🚶 Queue People",
            0,
            300,
            80
        )

    with c2:

        event_type = st.selectbox(
            "🎪 Event Type",
            [
                "Seminar",
                "Workshop",
                "Concert",
                "Exhibition"
            ]
        )

    if st.button(
        "🤖 Analyze Event",
        use_container_width=True
    ):

        recommendations = crowd_expert(
            occupancy,
            queue_people,
            event_type
        )

        st.subheader(
            "💡 AI Recommendations"
        )

        for item in recommendations:

            st.info(
                "🤖 " + item
            )

        speech = " ".join(
            recommendations
        )

        if st.button(
            "🔊 Speak AI Advice"
        ):

            speak(
                speech
            )


# ============================================================
# VOICE ASSISTANT
# ============================================================

elif menu == "🔊 Voice Assistant":

    st.subheader(
        "🔊 CrowdMind AI Voice Assistant"
    )

    st.markdown(
        """
        <div class="voice">

        <h2>🤖 AI Voice Center</h2>

        <p>
        Enter a message and CrowdMind AI
        will read it aloud.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    text = st.text_area(
        "✍️ Enter message",
        value=(
            "Welcome to CrowdMind AI. "
            "Your intelligent event "
            "management assistant."
        ),
        height=150
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "🔊 Speak Now",
            use_container_width=True
        ):

            if text.strip():

                speak(text)

                st.success(
                    "🔊 Voice announcement started."
                )

            else:

                st.warning(
                    "Please enter some text."
                )

    with c2:

        if st.button(
            "👋 Welcome Message",
            use_container_width=True
        ):

            speak(
                "Welcome to CrowdMind AI. "
                "I am your intelligent event "
                "crowd and queue optimizer."
            )

            st.success(
                "Welcome announcement played."
            )

    st.divider()

    st.subheader(
        "⚡ Quick Announcements"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button(
            "🚨 Crowd Alert",
            use_container_width=True
        ):

            speak(
                "Attention! A high crowd "
                "level has been detected. "
                "Please follow the alternate route."
            )

    with c2:

        if st.button(
            "🚦 Queue Alert",
            use_container_width=True
        ):

            speak(
                "Attention! A long queue "
                "has been detected. "
                "Please use another available counter."
            )

    with c3:

        if st.button(
            "🧑‍💼 Volunteer Alert",
            use_container_width=True
        ):

            speak(
                "Additional volunteers "
                "are required for crowd management."
            )

    st.info(
        "💡 Text-to-Speech uses the browser's "
        "built-in speech synthesis. "
        "No API key is required."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <center>

    <h3>🤖 CrowdMind AI</h3>

    <p>
    Intelligent Event Crowd & Queue Optimizer
    </p>

    <p>
    BFS • Dijkstra • Graph Analysis •
    Crowd Prediction • Queue Optimization •
    Expert System • Text-to-Speech
    </p>

    <small>
    Artificial Intelligence Practical Project
    </small>

    </center>
    """,
    unsafe_allow_html=True
)