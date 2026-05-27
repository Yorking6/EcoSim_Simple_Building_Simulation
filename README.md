# EcoSim Pro Simple Building Simulation

A Reflex-based web application for building services simulation and thermal comfort analysis.

---

## 1. Environment Setup & Installation

This guide will walk you through setting up a local development environment. It assumes you have **Python 3.8+** installed and configured in your system PATH.

### 1.1 Prerequisites & Virtual Environment

To prevent dependency conflicts, it is highly recommended to deploy the project within an isolated virtual environment (`virtualenv`).

#### Step 1: Install virtualenv
Run the following command to install the `virtualenv` tool via your current Python interpreter:
```bash
python -m pip install virtualenv
```


#### Step 2: Create a Virtual Environment

Create a dedicated virtual environment. While you can specify any local path, it is standard practice to create a `.venv` folder within your project root or user directory:

```bash
# Example using a custom path in the user directory

python -m virtualenv "C:\Users\<your_username>\venv1025"
```

>  **Tip:** Replace `<your_username>` with your actual Windows account name.

#### Step 3: Activate the Environment (Windows PowerShell)

Before running the activation script, you may need to adjust execution policies to allow script execution in PowerShell:

```powershell
# Set execution policy for the current user

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

When prompted by the system, type `Y` and press **Enter** to confirm.

Now, navigate to the directory and activate the environment:

```powershell
1. cd "C:\Users\<your_username>"

2. .\venv1025\Scripts\activate
```

**Verification:** Once successfully activated, you will see `(venv1025)` prepended to your terminal prompt.

---

### 1.2 Installing Reflex

With the virtual environment activated, install **Reflex v0.6.7**. For developers based in mainland China, a TUNA mirror is provided to accelerate the download source:

```bash
pip install reflex==0.6.7 -i [https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple)
```


------------
## 2. Project Acquisition & Deployment

You can acquire the latest source code using one of the following methods.

### 2.1 Acquire the Source Code

#### Option A: Clone via Git (Recommended)
If you have Git installed, clone the repository directly to your local workspace:
```bash
# Navigate to your workspace (e.g., C:\Users\<your_username>\EcoSim_Simple_Building_Simulation)

cd "C:\Users\<your_username>\EcoSim_Simple_Building_Simulation"

# Clone the repository

git clone https://github.com/Yorking6/EcoSim_Simple_Building_Simulation.git

# Enter the project directory

cd SimpleBuildingSimulation
```

#### Option B: Manual Download
1. Visit the project repository on GitHub.

2. Click the green Code button and select Download ZIP.

3. Extract the ZIP file to a folder, for example:
    > C:\Users\<your_username>\EcoSim_Simple_Building_Simulation
4. Open your Powershell and cd into that folder.
    ```bash
    cd "C:\Users\<your_username>\EcoSim_Simple_Building_Simulation"
    ```

----------

### 2.2 Initialize Project Dependencies
Once you are inside the project root directory, you need to trigger Reflex's internal setup. Unlike a blank project, running init here will detect the existing rxconfig.py and install the necessary web environment (Node.js/npm) required to run the simulation:

```Bash
# Ensure your virtual environment (venv1025) is activated first

reflex init --loglevel debug
```

**Note on Background Tasks:**
Reflex will automatically set up a standalone frontend environment. This process involves downloading several hundred megabytes of dependencies. Depending on your network conditions, this may take **10–20 **minutes. Please do not interrupt the process until it completes.

----------

## 3. Running the Application

After the environment is ready, you can launch the application to start the building simulation.

### 3.1 Start the Development Server

Run the following command within your project root directory **with your virtual environment still activated**:

```bash
reflex run --loglevel debug
```
---------------------------

### 3.2 Accessing the Web App

After the compilation and bundling processes finish, the terminal will display the local addresses for both the frontend user interface and the backend server.

* **Default Frontend URL:** Typically `http://localhost:3000` or `http://localhost:3001`

* **Accessing the Web App:** Open a web browser and navigate to the URL provided in the terminal output.

--------------

## 4. Web Application User Guide

Once the server is running and you have navigated to `http://localhost:3000`, you will interface with **EcoSim Pro**, a professional GUI dashboard engineered for seamless building energy simulation workflow management.

The application translates user-defined parameters into automated EnergyPlus input file (IDF) modifications, executes backend thermal calculations, and streams structured analysis results back to the frontend.

---

### 4.1 Interface Topology & Navigation

The interface uses a workflow-centric, multi-page navigation architecture designed to map perfectly to structural and load planning phases:

* **Home:** The dashboard entry page that provides a structural overview of the system's operational objectives.
* **Geometry Setting:** Dedicated view to control and mutate the spatial and parametric boundary definitions of window configurations.
* **Material Setting:** Envelope structural configuration page to assign material matrices to structural elements.
* **Residential Setting:** Zone runtime profile matrix where occupancy density arrays and operational schedules are applied.
* **About:** Context page hosting technical build parameters, backend stack configurations, and developer metadata.

---

### 4.2 Simulation Operations

#### Function A: Modifying Window Geometric Profiles
1. Navigate to the **Geometry Setting** workspace via the primary navigation bar.
2. Focus the geometric property selector dropdown to select whether your target transformation vector is window **Length** or **Height**.
3. Provide a valid floating-point unit token inside the numerical input box (e.g., inputting `3.0` sets a discrete 3.0-meter boundary dimension).
4. Click the **Start to simulation!** action trigger. The core process will modify the underlying zone boundary coordinates, re-initialize the baseline `1ZoneIdealSys.idf` matrix, run the calculation engine, and re-render the telemetry data block.

#### Function B: Material Layer & Thermal Performance Customization
1. Direct the app pointer to the **Material Setting** interface route.
2. Pull down the **Window Material Type** matrix and assign a targeted assembly layer (options step from a standard baseline **Double Pane Window** up to high-performance, low-emissivity **Double Pane Low-E Window** layouts).
3. Update the structural wall boundaries via the **Wall Material Type** configuration dropdown (options map standard structural **Common Brick Wall** assemblies against high-thermal-resistance **High-Efficiency Insulated Wall** systems).
4. Fire the simulation thread via **Start to simulation!** to evaluate how modified U-values and Solar Heat Gain Coefficients (SHGC) affect total annual baseline consumption figures.

#### Function C: Tuning Internal Thermal Gains & Schedules
1. Relocate to the **Residential Setting** control dashboard.
2. Identify the targeted internal schedule matrix dropdown and select an entry (e.g., `OCCUPY-1`) to accurately declare the operational time-blocks when personnel loads are active within the thermal zone envelope.
3. Provide a strict integer literal within the **Number of people** parameter entry slot (e.g., `5` to denote exactly 5 human units).
4. Click **Start to simulation!**. The application pipes this integer block down to calculate internal sensible and latent metabolic heat gains, re-evaluating the zone's thermodynamic loading trends against the localized weather dataset (`shanghai_2017.epw`).

---

### 4.3 Interpreting Telemetry and Analytical Output

When a state simulation runs, a temporary status string reads: `"Simulation in progress. Please wait a moment…"`. Once the thread exits normally, the localized client state store processes the raw data block using Pandas and delivers the processed metrics into two synchronized frontend analytics blocks:

1.  **Numerical Metrics Blocks:** An absolute consumption tracking summary layout that projects total calculated HVAC performance loads cleanly as exact numerical figures in kilowatt-hours per year (**kWh/year**).
2.  **Integrated Recharts Bar Chart:** An automated, reactive analytical visualization canvas displaying side-by-side quantitative performance values of annual **Cooling Energy** vs. **Heating Energy**. This graph allows you to quickly assess thermal performance changes and cross-compare variance responses across different test runs.
