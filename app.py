from datetime import date, datetime, timedelta
import random

import matplotlib.pyplot as plt
import pandas as pd
from shiny import reactive
from shiny.express import input, render, session, ui


# ============================================================================
# GLOBAL UI STYLING
# ============================================================================

ui.tags.style("""
:root {
    --warm-teal: #0A7E8C;
    --healthcare-blue: #1F4E79;
    --amber-gold: #E69F00;
    --light-bg: #F4F7F9;
    --border: #D9E2E7;
    --text: #24323A;
}


/* ==========================================================================
   GLOBAL PAGE
   ========================================================================== */

html,
body {
    min-height: 100%;
}

body {
    background: var(--light-bg);
    color: var(--text);
    font-family: "Segoe UI", Arial, sans-serif;
}

.bslib-page-navbar {
    background: var(--light-bg);
}

.navbar {
    margin-bottom: 0;
}


/* ==========================================================================
   SIDEBAR LAYOUT
   ========================================================================== */

.bslib-sidebar-layout {
    --bslib-sidebar-width: 285px;
}

.bslib-sidebar-layout > .main {
    padding: 24px 28px 40px 28px;
}

.bslib-sidebar-layout > .sidebar {
    padding: 22px 18px;
    background: #FFFFFF;
    border-right: 1px solid var(--border);
}


/* ==========================================================================
   ALL CARDS
   ========================================================================== */

.card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(31, 78, 121, 0.07);
    margin-bottom: 20px;

    /*
       Important:
       Do NOT clip chart, table, form, or other card content.
    */
    overflow: visible;
}

.card-header {
    font-weight: 700;
    font-size: 1rem;
    padding: 13px 17px;
    min-height: 48px;

    display: flex;
    align-items: center;

    line-height: 1.3;
}


/* ==========================================================================
   PAGE HEADINGS
   ========================================================================== */

.section-title {
    margin-top: 4px;
    margin-bottom: 12px;
    font-weight: 750;
    line-height: 1.25;
}

.help-text {
    color: #5E6D75;
    font-size: 0.92rem;
    line-height: 1.5;
    margin-bottom: 18px;
}


/* ==========================================================================
   SIDEBAR
   ========================================================================== */

.sidebar-title {
    font-weight: 750;
    margin-bottom: 20px;
    color: var(--healthcare-blue);
}


/* ==========================================================================
   KPI CARDS
   ========================================================================== */

.kpi-card {
    min-height: 135px;
    height: 135px;
    text-align: center;
    overflow: visible;
}

.kpi-card .card-header {
    height: 48px;
    min-height: 48px;

    font-size: 0.88rem;
    line-height: 1.2;

    display: flex;
    align-items: center;
    justify-content: center;
}

.kpi-card .card-body {
    min-height: 82px;
    padding: 0 !important;

    display: flex;
    align-items: center;
    justify-content: center;
}

.kpi-value {
    font-size: 2.1rem;
    line-height: 1.1;
    font-weight: 800;
    padding: 15px 10px;
    color: var(--healthcare-blue);
}


/* ==========================================================================
   DASHBOARD CHART CARDS
   ========================================================================== */

.dashboard-chart-card {
    min-height: 390px;
    height: 390px;
}

.dashboard-chart-card .card-body {
    min-height: 320px;
    padding: 12px 16px 16px 16px;
}

.dashboard-chart-card .shiny-plot-output {
    min-height: 300px !important;
}


/* ==========================================================================
   GENERAL CONTENT CARDS
   ========================================================================== */

.content-card {
    min-height: 200px;
}

.tall-card {
    min-height: 400px;
}

.large-card {
    min-height: 500px;
}


/* ==========================================================================
   PATHWAY BOX
   ========================================================================== */

.pathway-box {
    background: #F0F7F8;
    border: 1px solid #C9E2E5;
    border-radius: 10px;

    padding: 18px;

    text-align: center;
    margin: 8px 0;
}

.pathway-flow {
    font-weight: 800;
    color: var(--warm-teal);
    font-size: 1.15rem;
    letter-spacing: .02em;
    margin-bottom: 8px;
}


/* ==========================================================================
   FORMS
   ========================================================================== */

.form-section {
    background: white;
    padding: 4px;
}

.form-actions {
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid var(--border);
}

.form-group {
    margin-bottom: 16px;
}

.form-label {
    font-weight: 600;
}


/* ==========================================================================
   TABLES / DATA GRIDS
   ========================================================================== */

.shiny-data-grid {
    width: 100%;
}


/* ==========================================================================
   BUTTONS
   ========================================================================== */

.btn-primary {
    background-color: var(--warm-teal);
    border-color: var(--warm-teal);
    font-weight: 600;
}

.btn-primary:hover,
.btn-primary:focus {
    background-color: #086C77;
    border-color: #086C77;
}


/* ==========================================================================
   NAVIGATION
   ========================================================================== */

.nav-link {
    font-weight: 600;
}


/* ==========================================================================
   RESPONSIVE DESIGN
   ========================================================================== */

@media (max-width: 1100px) {

    .bslib-sidebar-layout > .main {
        padding: 18px;
    }

    .kpi-value {
        font-size: 1.8rem;
    }
}


@media (max-width: 800px) {

    .bslib-sidebar-layout > .main {
        padding: 14px;
    }

    .dashboard-chart-card {
        height: auto;
        min-height: 350px;
    }

    .kpi-card {
        height: 120px;
        min-height: 120px;
    }
}


@media (max-width: 600px) {

    .bslib-sidebar-layout > .main {
        padding: 10px;
    }

    .card-header {
        font-size: 0.92rem;
    }

    .kpi-value {
        font-size: 1.6rem;
    }
}
""")


# ============================================================================
# VISUAL IDENTITY & THEME
# ============================================================================

WARM_TEAL = "#0A7E8C"
HEALTHCARE_BLUE = "#1F4E79"
AMBER_GOLD = "#E69F00"
LIGHT_BG = "#F8F9FA"


# ============================================================================
# SAMPLE DATA GENERATION
# ============================================================================

REGIONS = [
    "Volta",
    "Ashanti",
    "Greater Accra",
    "Northern",
    "Eastern",
]

DISTRICTS = {
    "Volta": [
        "Wudoaba",
        "Ho",
        "Keta",
        "Hohoe",
    ],
    "Ashanti": [
        "Kumasi Metro",
        "Obuasi",
        "Ejisu",
    ],
    "Greater Accra": [
        "Accra Metro",
        "Tema",
        "Ga West",
    ],
    "Northern": [
        "Tamale Metro",
        "Yendi",
        "Savelugu",
    ],
    "Eastern": [
        "Koforidua",
        "Akropong",
        "Mpraeso",
    ],
}


DISCOVERY_SOURCES = [
    "TBA Referral",
    "CHW Surveillance",
    "Social Media Campaign",
    "Community Leader",
    "Hospital Birth",
]


CLEFT_TYPES = [
    "Cleft Lip",
    "Cleft Palate",
    "Combined Cleft Lip & Palate",
]


PATHWAY_STEPS = [
    "FIND - Intake",
    "CONNECT - Referral",
    "NAVIGATE - Logistics",
    "TREAT - Clinical Care",
    "TRACK - Follow-up",
]


def generate_sample_data(n=25):
    """Generate a small demonstration dataset."""

    data = []
    now = datetime.now()

    for i in range(n):

        region = random.choice(REGIONS)
        district = random.choice(DISTRICTS[region])

        # Weight Volta region higher for demonstration purposes.
        if random.random() < 0.30:
            region = "Volta"
            district = "Wudoaba"

        # Weight KATH-related cases.
        if random.random() < 0.25:
            region = "Ashanti"
            district = "Kumasi Metro"

        birth_date = now - timedelta(
            days=random.randint(30, 1095)
        )

        data.append(
            {
                "patient_id": f"GH-CLP-{i + 1:03d}",

                "name": f"Patient {i + 1}",

                "date_of_birth": birth_date.strftime(
                    "%Y-%m-%d"
                ),

                "age_months": (
                    now - birth_date
                ).days // 30,

                "gender": random.choice(
                    ["Male", "Female"]
                ),

                "region": region,

                "district": district,

                "community": (
                    f"Community {random.randint(1, 20)}"
                ),

                "discovery_source": random.choice(
                    DISCOVERY_SOURCES
                ),

                "cleft_type": random.choice(
                    CLEFT_TYPES
                ),

                "feeding_difficulty": random.randint(
                    1, 5
                ),

                "nutritional_distress": random.randint(
                    1, 5
                ),

                "speech_concern": random.choice(
                    ["Yes", "No", "Too Young"]
                ),

                "hearing_concern": random.choice(
                    ["Yes", "No", "Too Young"]
                ),

                "current_step": random.choice(
                    PATHWAY_STEPS
                ),

                "priority": (
                    "High Risk"
                    if random.random() < 0.30
                    else "Standard"
                ),

                "surgery_completed": random.choice(
                    [True, False]
                ),

                "date_registered": (
                    now
                    - timedelta(
                        days=random.randint(1, 365)
                    )
                ).strftime("%Y-%m-%d"),
            }
        )

    return pd.DataFrame(data)


# ============================================================================
# INITIAL DATA
# ============================================================================

initial_patients = generate_sample_data()


# ============================================================================
# REACTIVE PATIENT REGISTRY
# ============================================================================

patients = reactive.value(
    initial_patients.copy()
)


# ============================================================================
# REACTIVE DATA
# ============================================================================

@reactive.calc
def filtered_patients():

    df = patients().copy()

    region = input.region_filter()
    step = input.step_filter()
    priority = input.priority_filter()

    if region != "All":
        df = df[
            df["region"] == region
        ]

    if step != "All":
        df = df[
            df["current_step"] == step
        ]

    if priority != "All":
        df = df[
            df["priority"] == priority
        ]

    return df


@reactive.calc
def registry_patients():

    df = patients().copy()

    query = (
        input.search_registry()
        .strip()
        .lower()
    )

    if query:

        searchable = (
            df["name"]
            .fillna("")
            .astype(str)

            + " "

            + df["patient_id"]
            .fillna("")
            .astype(str)

            + " "

            + df["district"]
            .fillna("")
            .astype(str)
        ).str.lower()

        df = df[
            searchable.str.contains(
                query,
                regex=False,
                na=False,
            )
        ]

    return df


# ============================================================================
# REGISTER NEW PATIENT
# ============================================================================

@reactive.effect
@reactive.event(input.submit_intake)
def register_patient():

    name = (
        input.intake_name()
        .strip()
    )

    district = (
        input.intake_district()
        .strip()
    )

    community = (
        input.intake_community()
        .strip()
    )

    dob = input.intake_dob()

    if (
        not name
        or not district
        or not community
        or dob is None
    ):
        return

    dob_value = (
        dob
        if isinstance(dob, date)
        else date.fromisoformat(
            str(dob)
        )
    )

    today = date.today()

    # Prevent future date of birth.
    if dob_value > today:
        return

    current = patients().copy()

    patient_number = len(current) + 1

    birth_dt = datetime.combine(
        dob_value,
        datetime.min.time(),
    )

    age_months = max(
        0,
        (
            datetime.now() - birth_dt
        ).days // 30,
    )

    new_patient = pd.DataFrame(
        [
            {
                "patient_id": (
                    f"GH-CLP-{patient_number:03d}"
                ),

                "name": name,

                "date_of_birth": (
                    dob_value.isoformat()
                ),

                "age_months": age_months,

                "gender": input.intake_gender(),

                "region": input.intake_region(),

                "district": district,

                "community": community,

                "discovery_source": (
                    input.intake_source()
                ),

                "cleft_type": (
                    input.intake_cleft_type()
                ),

                "feeding_difficulty": (
                    input.intake_feeding()
                ),

                "nutritional_distress": (
                    input.intake_nutrition()
                ),

                "speech_concern": "Too Young",

                "hearing_concern": "Too Young",

                "current_step": "FIND - Intake",

                "priority": (
                    "High Risk"
                    if (
                        input.intake_feeding() >= 4
                        or
                        input.intake_nutrition() >= 4
                    )
                    else "Standard"
                ),

                "surgery_completed": False,

                "date_registered": (
                    today.isoformat()
                ),
            }
        ]
    )

    patients.set(
        pd.concat(
            [
                current,
                new_patient,
            ],
            ignore_index=True,
        )
    )

    # Refresh patient choices.
    choices = (
        patients()["patient_id"]
        .tolist()
    )

    session.send_input_message(
        "logistics_patient",
        {
            "options": [
                {
                    "value": x,
                    "label": x,
                }
                for x in choices
            ]
        },
    )

    session.send_input_message(
        "mdt_patient",
        {
            "options": [
                {
                    "value": x,
                    "label": x,
                }
                for x in choices
            ]
        },
    )


# ============================================================================
# PAGE SETTINGS
# ============================================================================

ui.page_opts(
    title="Cleft Care Pathway — Ghana",

    # IMPORTANT:
    # Normal page scrolling is used instead of forcing all
    # cards into the browser viewport.
    fillable=False,
)


# ============================================================================
# MAIN NAVIGATION
# ============================================================================

with ui.navset_bar(
    title="Cleft Care Pathway — Ghana"
):


    # ========================================================================
    # DASHBOARD
    # ========================================================================

    with ui.nav_panel("Dashboard"):

        with ui.layout_sidebar():

            # ----------------------------------------------------------------
            # DASHBOARD SIDEBAR
            # ----------------------------------------------------------------

            with ui.sidebar():

                ui.h4(
                    "Dashboard Filters",
                    class_="sidebar-title",
                    style=(
                        f"color: {HEALTHCARE_BLUE};"
                    ),
                )

                ui.input_select(
                    "region_filter",
                    "Region",
                    choices=[
                        "All"
                    ]
                    + sorted(REGIONS),
                )

                ui.input_select(
                    "step_filter",
                    "Pathway Step",
                    choices=[
                        "All"
                    ]
                    + sorted(PATHWAY_STEPS),
                )

                ui.input_select(
                    "priority_filter",
                    "Priority",
                    choices=[
                        "All",
                        "High Risk",
                        "Standard",
                    ],
                )


            # ----------------------------------------------------------------
            # DASHBOARD MAIN CONTENT
            # ----------------------------------------------------------------

            ui.h2(
                "Public Health Dashboard & Surveillance",
                class_="section-title",
                style=(
                    f"color: {HEALTHCARE_BLUE};"
                ),
            )

            ui.p(
                "Monitor cases, referral activity, "
                "surgery completion, and follow-up "
                "across the integrated cleft care pathway.",
                class_="help-text",
            )


            # ----------------------------------------------------------------
            # KPI ROW
            # ----------------------------------------------------------------

            with ui.layout_columns(
                col_widths=[3, 3, 3, 3],
                gap="1rem",
                fill=False,
            ):

                # ------------------------------------------------------------
                # TOTAL CASES
                # ------------------------------------------------------------

                with ui.card(
                    class_="kpi-card"
                ):

                    ui.card_header(
                        "Total Cases Identified",
                        style=(
                            f"background-color: "
                            f"{WARM_TEAL}; "
                            f"color: white;"
                        ),
                    )

                    @render.text
                    def kpi_total_cases():

                        return (
                            f"{len(filtered_patients()):,}"
                        )


                # ------------------------------------------------------------
                # ACTIVE REFERRALS
                # ------------------------------------------------------------

                with ui.card(
                    class_="kpi-card"
                ):

                    ui.card_header(
                        "Active Triage/Referrals",
                        style=(
                            f"background-color: "
                            f"{AMBER_GOLD}; "
                            f"color: white;"
                        ),
                    )

                    @render.text
                    def kpi_active_referrals():

                        df = filtered_patients()

                        active = (
                            df["current_step"]
                            .isin(
                                [
                                    "CONNECT - Referral",
                                    "NAVIGATE - Logistics",
                                ]
                            )
                            .sum()
                        )

                        return f"{active:,}"


                # ------------------------------------------------------------
                # COMPLETED SURGERIES
                # ------------------------------------------------------------

                with ui.card(
                    class_="kpi-card"
                ):

                    ui.card_header(
                        "Completed Surgeries",
                        style=(
                            f"background-color: "
                            f"{HEALTHCARE_BLUE}; "
                            f"color: white;"
                        ),
                    )

                    @render.text
                    def kpi_surgeries():

                        return (
                            f"{filtered_patients()['surgery_completed'].sum():,}"
                        )


                # ------------------------------------------------------------
                # FOLLOW-UP RATE
                # ------------------------------------------------------------

                with ui.card(
                    class_="kpi-card"
                ):

                    ui.card_header(
                        "Follow-up Tracking Rate",
                        style=(
                            f"background-color: "
                            f"{WARM_TEAL}; "
                            f"color: white;"
                        ),
                    )

                    @render.text
                    def kpi_tracking_rate():

                        df = filtered_patients()

                        if df.empty:
                            return "0.0%"

                        tracked = (
                            df["current_step"]
                            == "TRACK - Follow-up"
                        ).mean()

                        return f"{tracked:.1%}"


            # ----------------------------------------------------------------
            # DASHBOARD CHARTS
            # ----------------------------------------------------------------

            with ui.layout_columns(
                col_widths=[6, 6],
                gap="1rem",
                fill=False,
            ):

                # ------------------------------------------------------------
                # REGIONAL SURVEILLANCE
                # ------------------------------------------------------------

                with ui.card(
                    class_="dashboard-chart-card",
                    full_screen=True,
                ):

                    ui.card_header(
                        "Ghana Regional Surveillance Distribution"
                    )

                    @render.plot(height=300)
                    def regional_chart():

                        counts = (
                            filtered_patients()["region"]
                            .value_counts()
                            .sort_values(
                                ascending=True
                            )
                        )

                        fig, ax = plt.subplots(
                            figsize=(7, 4)
                        )

                        counts.plot.barh(
                            ax=ax
                        )

                        ax.set_xlabel(
                            "Number of cases"
                        )

                        ax.set_ylabel("")

                        ax.set_title(
                            "Cases by Region",
                            fontsize=13,
                            fontweight="bold",
                        )

                        fig.tight_layout()

                        return fig


                # ------------------------------------------------------------
                # CLEFT TYPE
                # ------------------------------------------------------------

                with ui.card(
                    class_="dashboard-chart-card",
                    full_screen=True,
                ):

                    ui.card_header(
                        "Cleft Type Distribution"
                    )

                    @render.plot(height=300)
                    def cleft_type_chart():

                        counts = (
                            filtered_patients()["cleft_type"]
                            .value_counts()
                        )

                        fig, ax = plt.subplots(
                            figsize=(7, 4)
                        )

                        counts.plot.bar(
                            ax=ax
                        )

                        ax.set_ylabel(
                            "Number of cases"
                        )

                        ax.set_xlabel("")

                        ax.tick_params(
                            axis="x",
                            rotation=20,
                        )

                        ax.set_title(
                            "Cleft Type",
                            fontsize=13,
                            fontweight="bold",
                        )

                        fig.tight_layout()

                        return fig


            # ----------------------------------------------------------------
            # PATHWAY FLOW
            # ----------------------------------------------------------------

            with ui.card(
                height="155px",
                fill=False,
            ):

                ui.card_header(
                    "Pathway Flow: Current vs. Integrated Care Model"
                )

                @render.ui
                def pathway_comparison():

                    return ui.div(

                        ui.div(

                            ui.p(
                                "FIND  →  CONNECT  →  "
                                "NAVIGATE  →  TREAT  →  TRACK",
                                class_="pathway-flow",
                            ),

                            ui.p(
                                "Community detection • "
                                "referral • logistics • "
                                "multidisciplinary care • "
                                "follow-up",
                                class_="help-text",
                            ),

                            class_="pathway-box",
                        )
                    )


    # ========================================================================
    # FIND - COMMUNITY INTAKE
    # ========================================================================

    with ui.nav_panel(
        "FIND - Community Intake"
    ):

        ui.h2(
            "STEP 1: FIND - Community Intake & Early Detection Registry",
            class_="section-title",
            style=(
                f"color: {HEALTHCARE_BLUE};"
            ),
        )

        ui.p(
            "Register children identified through "
            "community and facility-based detection "
            "pathways, then review the live registry.",
            class_="help-text",
        )


        # --------------------------------------------------------------------
        # INTAKE + REGISTRY
        # --------------------------------------------------------------------

        with ui.layout_columns(
            col_widths=[5, 7],
            gap="1.25rem",
            fill=False,
        ):

            # ----------------------------------------------------------------
            # NEW PATIENT FORM
            # ----------------------------------------------------------------

            with ui.card():

                ui.card_header(
                    "New Patient Intake Form",
                    style=(
                        f"background-color: "
                        f"{WARM_TEAL}; "
                        f"color: white;"
                    ),
                )

                ui.p(
                    "Enter the child's identification "
                    "and initial community screening "
                    "information.",
                    class_="help-text",
                )

                ui.input_text(
                    "intake_name",
                    "Child Name/ID",
                    placeholder="Enter name or ID",
                )

                ui.input_date(
                    "intake_dob",
                    "Date of Birth",
                )

                ui.input_select(
                    "intake_gender",
                    "Gender",
                    choices=[
                        "Male",
                        "Female",
                    ],
                )

                ui.input_select(
                    "intake_region",
                    "Region",
                    choices=sorted(REGIONS),
                )

                ui.input_text(
                    "intake_district",
                    "District",
                    placeholder="District name",
                )

                ui.input_text(
                    "intake_community",
                    "Community/Village",
                    placeholder="Community name",
                )

                ui.input_select(
                    "intake_source",
                    "Discovery Source",
                    choices=DISCOVERY_SOURCES,
                )

                ui.input_select(
                    "intake_cleft_type",
                    "Clinical Presentation",
                    choices=CLEFT_TYPES,
                )

                ui.input_slider(
                    "intake_feeding",
                    "Feeding Difficulty "
                    "(1=Mild, 5=Severe)",
                    min=1,
                    max=5,
                    value=3,
                )

                ui.input_slider(
                    "intake_nutrition",
                    "Nutritional Distress "
                    "(1=Mild, 5=Severe)",
                    min=1,
                    max=5,
                    value=3,
                )

                ui.div(

                    ui.input_action_button(
                        "submit_intake",
                        "Register New Patient",
                        class_="btn-primary",
                    ),

                    class_="form-actions",
                )


            # ----------------------------------------------------------------
            # LIVE REGISTRY
            # ----------------------------------------------------------------

            with ui.card(
                height="600px",
                full_screen=True,
            ):

                ui.card_header(
                    "Live Intake Registry"
                )

                ui.input_text(
                    "search_registry",
                    "Search Registry",
                    placeholder=(
                        "Search by name, ID, or district"
                    ),
                )

                @render.data_frame
                def intake_registry_table():

                    columns = [
                        "patient_id",
                        "name",
                        "region",
                        "district",
                        "cleft_type",
                        "priority",
                        "current_step",
                    ]

                    return render.DataGrid(
                        registry_patients()[columns],
                        filters=True,
                        height="450px",
                    )


    # ========================================================================
    # CONNECT & NAVIGATE
    # ========================================================================

    with ui.nav_panel(
        "CONNECT & NAVIGATE"
    ):

        ui.h2(
            "STEP 2 & 3: CONNECT & NAVIGATE - "
            "Referral Routing & Family Logistics",
            class_="section-title",
            style=(
                f"color: {HEALTHCARE_BLUE};"
            ),
        )

        ui.p(
            "Coordinate referral priority, transport, "
            "financial support, and family-centred "
            "psychosocial support.",
            class_="help-text",
        )


        # --------------------------------------------------------------------
        # REFERRAL ESCALATION ENGINE
        # --------------------------------------------------------------------

        with ui.card():

            ui.card_header(
                "Referral Escalation Engine",
                style=(
                    f"background-color: "
                    f"{WARM_TEAL}; "
                    f"color: white;"
                ),
            )

            @render.ui
            def referral_flow_diagram():

                return ui.div(

                    ui.div(

                        ui.p(
                            "FIND  →  CONNECT  →  "
                            "NAVIGATE  →  TREAT  →  TRACK",
                            class_="pathway-flow",
                        ),

                        ui.p(
                            "High-risk cases can be "
                            "prioritised for referral "
                            "and care coordination "
                            "according to the programme "
                            "protocol.",
                            class_="help-text",
                        ),

                        class_="pathway-box",
                    )
                )


        # --------------------------------------------------------------------
        # REFERRALS + LOGISTICS
        # --------------------------------------------------------------------

        with ui.layout_columns(
            col_widths=[5, 7],
            gap="1.25rem",
            fill=False,
        ):

            # ----------------------------------------------------------------
            # ACTIVE REFERRALS
            # ----------------------------------------------------------------

            with ui.card(
                height="350px",
                full_screen=True,
            ):

                ui.card_header(
                    "Active Referrals by Priority",
                    style=(
                        f"background-color: "
                        f"{AMBER_GOLD}; "
                        f"color: white;"
                    ),
                )

                @render.data_frame
                def referral_priority_table():

                    df = patients().copy()

                    df = df[
                        df["current_step"].isin(
                            [
                                "CONNECT - Referral",
                                "NAVIGATE - Logistics",
                            ]
                        )
                    ]

                    summary = (
                        df.groupby(
                            "priority",
                            as_index=False,
                        )
                        .size()
                        .rename(
                            columns={
                                "size":
                                "active_referrals"
                            }
                        )
                    )

                    return render.DataGrid(
                        summary,
                        height="230px",
                    )


            # ----------------------------------------------------------------
            # LOGISTICS & SUPPORT
            # ----------------------------------------------------------------

            with ui.card():

                ui.card_header(
                    "Logistics & Support Coordinator"
                )

                ui.h4(
                    "Transport & Financial Support"
                )

                ui.input_select(
                    "logistics_patient",
                    "Select Patient",
                    choices=(
                        initial_patients[
                            "patient_id"
                        ].tolist()
                    ),
                )

                ui.input_checkbox(
                    "transport_voucher",
                    "Transport Voucher Issued",
                )

                ui.input_checkbox(
                    "travel_grant",
                    "Travel Grant Approved",
                )

                ui.input_numeric(
                    "pre_op_weight",
                    "Current Weight (kg)",
                    value=0,
                    min=0,
                )

                ui.input_numeric(
                    "target_weight",
                    "Target Weight for Surgery (kg)",
                    value=0,
                    min=0,
                )


                @render.text
                def weight_progress():

                    current = (
                        input.pre_op_weight()
                    )

                    target = (
                        input.target_weight()
                    )

                    if (
                        not current
                        or current <= 0
                    ):
                        return (
                            "Enter the current weight."
                        )

                    if (
                        not target
                        or target <= 0
                    ):
                        return (
                            f"Current weight: "
                            f"{current:.1f} kg"
                        )

                    progress = (
                        current / target
                    )

                    return (
                        f"Weight: "
                        f"{current:.1f} / "
                        f"{target:.1f} kg "
                        f"({progress:.0%} of target)"
                    )


                ui.h4(
                    "Psychosocial Support",
                    style="margin-top: 24px;",
                )

                ui.input_checkbox(
                    "counseling",
                    "Anti-stigma Counseling Completed",
                )

                ui.input_checkbox(
                    "peer_group",
                    "Peer Support Group Paired",
                )

                ui.input_checkbox(
                    "edu_support",
                    "Educational Support Plan Active",
                )


    # ========================================================================
    # TREAT - CLINICAL CARE
    # ========================================================================

    with ui.nav_panel(
        "TREAT - Clinical Care"
    ):

        ui.h2(
            "STEP 4: TREAT - Multidisciplinary Care Coordination",
            class_="section-title",
            style=(
                f"color: {HEALTHCARE_BLUE};"
            ),
        )

        ui.p(
            "Document multidisciplinary involvement "
            "and key components of the child's "
            "clinical care plan.",
            class_="help-text",
        )


        # --------------------------------------------------------------------
        # MDT CLINICAL PORTAL
        # --------------------------------------------------------------------

        with ui.card(
            class_="large-card",
            full_screen=True,
        ):

            ui.card_header(
                "Multidisciplinary Team (MDT) Clinical Portal",
                style=(
                    f"background-color: "
                    f"{HEALTHCARE_BLUE}; "
                    f"color: white;"
                ),
            )


            # ---------------------------------------------------------------
            # PATIENT SELECTION
            # ---------------------------------------------------------------

            ui.input_select(
                "mdt_patient",
                "Select Patient",
                choices=(
                    initial_patients[
                        "patient_id"
                    ].tolist()
                ),
            )


            # ---------------------------------------------------------------
            # MDT CHECKLISTS
            # ---------------------------------------------------------------

            with ui.layout_columns(
                col_widths=[6, 6],
                gap="1.25rem",
                fill=False,
            ):

                # -----------------------------------------------------------
                # CARE TEAM
                # -----------------------------------------------------------

                with ui.card(
                    class_="content-card"
                ):

                    ui.card_header(
                        "Care Team Checklist"
                    )

                    ui.input_checkbox(
                        "midwife_check",
                        "Midwife/Nurse - "
                        "Birth & Postnatal Care",
                    )

                    ui.input_checkbox(
                        "paed_check",
                        "Paediatrician - General",
                    )

                    ui.input_checkbox(
                        "dietitian_check",
                        "Dietitian - "
                        "Feeding & Nutrition",
                    )

                    ui.input_checkbox(
                        "surgeon_check",
                        "Surgeon - "
                        "Cleft Assessment",
                    )


                # -----------------------------------------------------------
                # ADDITIONAL MDT
                # -----------------------------------------------------------

                with ui.card(
                    class_="content-card"
                ):

                    ui.card_header(
                        "Additional MDT Coordination"
                    )

                    ui.input_checkbox(
                        "speech_check",
                        "Speech & Language Assessment",
                    )

                    ui.input_checkbox(
                        "hearing_check",
                        "Hearing Assessment",
                    )

                    ui.input_checkbox(
                        "social_check",
                        "Social Work / Family Support",
                    )

                    ui.input_checkbox(
                        "followup_check",
                        "Follow-up Plan Documented",
                    )