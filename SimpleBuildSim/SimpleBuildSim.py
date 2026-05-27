# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 2025

@author: Yuecheng XU
"""

import os
import reflex as rx

from .GeometrySettingPy import sim_geometry
from .MaterialSettingPy import sim_material
from .ResidentialSettingPy import sim_resident


class GeometryState(rx.State):
    """State management for the Window Geometry simulation page."""
    # Store the selected type (Length or Height)
    selected_option: str = ""
    # Store the new input value from the user
    new_value: str = ""
    # Store the results of calculation to display in the UI
    results: str = ""
    # Store the dictionary values used for generating Recharts bar charts
    chart_data: list[dict] = []

    def handle_submit(self):
        """Process the geometry simulation request and update the state with results."""
        if not self.selected_option or not self.new_value:
            yield rx.window_alert("Please complete all fields!")
            return
            
        # Define paths for the EnergyPlus model and weather files
        idf_path = os.path.abspath('./Data/1ZoneIdealSys.idf') # abs path to the IDf model file
        epw_path = os.path.abspath('./Data/shanghai_2017.epw') # abs path to the EPW file
        
        self.chart_data = []
        self.results = "Simulation in progress. Please wait a moment..."
        yield
        
        # Call the backend simulation function with user inputs
        h_list, c_list = sim_geometry(
            float(self.new_value), 
            self.selected_option, 
            idf_path, 
            epw_path
            )
        
        if h_list and c_list:
            heating = h_list[0]
            cooling = c_list[0]
            self.results = f"Energy Consumption Result: Heating: {heating:.2f} kWh/year, Cooling: {cooling:.2f} kWh/year"
        else:
            self.results = "Simulation finished, but no data was extracted."
        yield
        
        # Update chart data: Construct a dictionary that conforms to the Recharts format
        new_entry = {
            "name": f"{self.selected_option}_{self.new_value}", # The name displayed on the horizontal coordinate
            "heating": heating,                                  # Vertical coordinate data 1
            "cooling": cooling                                   # Vertical coordinate data 2
        }
        self.chart_data.append(new_entry)
        yield
        

class MaterialState(rx.State):
    """State management for the Material Properties simulation page."""
    # Store the selected type (Window and Wall)
    selected_window: str = ""
    # Store the selected wall material
    selected_wall: str = ""
    # Store the results of calculation
    results: str = ""
    # Store the dictionary values used for generating Recharts bar charts
    chart_data: list[dict] = []

    def handle_submit(self):
        """Process the material simulation request and update the state with results."""
        if not self.selected_window or not self.selected_wall:
            yield rx.window_alert("Please complete all fields!")
            return
            
        # Define paths for the EnergyPlus model and weather files
        idf_path = os.path.abspath('./Data/1ZoneIdealSys.idf') # abs path to the IDf model file
        epw_path = os.path.abspath('./Data/shanghai_2017.epw') # abs path to the EPW file
        
        self.chart_data = []
        self.results = "Simulation in progress. Please wait a moment..."
        yield
        
        # Call the backend simulation function for materials
        h_list, c_list = sim_material(
            self.selected_window, 
            self.selected_wall, 
            idf_path, 
            epw_path
            )
        
        if h_list and c_list:
            heating = h_list[0]
            cooling = c_list[0]
            self.results = f"Energy Consumption Result: Heating: {heating:.2f} kWh/year, Cooling: {cooling:.2f} kWh/year"
        else:
            self.results = "Simulation finished, but no data was extracted."
        yield
        
        # Update chart data: Construct a dictionary that conforms to the Recharts format
        new_entry = {
            "name": f"Adopt {self.selected_window} and {self.selected_wall}", # The name displayed on the horizontal coordinate
            "heating": heating,                                  # Vertical coordinate data 1
            "cooling": cooling                                   # Vertical coordinate data 2
        }
        self.chart_data.append(new_entry)
        yield
        

class ResidentialState(rx.State):
    """State management for the Residential/Occupancy simulation page."""
    # Store the selected occupancy schedule type
    selected_option: str = ""
    # Store the number of occupants entered by user
    new_value: str = ""
    # Store the results of calculation
    results: str = ""
    # Store the dictionary values used for generating Recharts bar charts
    chart_data: list[dict] = []

    def handle_submit(self):
        """Validate input and process the occupancy simulation request."""
        if not self.selected_option or not self.new_value:
            yield rx.window_alert("Please complete all fields!")
            return
        # Validate that the number of occupants is a valid integer
        try:
            val_as_float = float(self.new_value)
            if not val_as_float.is_integer():
                yield rx.window_alert("Error: Floating point numbers (decimals) are not allowed!")
                return
        except ValueError:
            # If the input is a non-numeric string
            yield rx.window_alert("Error: Please enter a valid numeric integer!")
            return
            
        # Define paths for the EnergyPlus model and weather files
        idf_path = os.path.abspath('./Data/1ZoneIdealSys.idf') # abs path to the IDf model file
        epw_path = os.path.abspath('./Data/shanghai_2017.epw') # abs path to the EPW file
        
        self.chart_data = []
        self.results = "Simulation in progress. Please wait a moment..."
        yield
        
        # Call the backend simulation function for occupants
        h_list, c_list = sim_resident(
            self.new_value, 
            self.selected_option, 
            idf_path, 
            epw_path
            )
        
        if h_list and c_list:
            heating = h_list[0]
            cooling = c_list[0]
            self.results = f"Energy Consumption Result: Heating: {heating:.2f} kWh/year, Cooling: {cooling:.2f} kWh/year"
        else:
            self.results = "Simulation finished, but no data was extracted."
        yield
        
        # Update chart data: Construct a dictionary that conforms to the Recharts format
        new_entry = {
            "name": f"{self.selected_option} with {self.new_value} people", # The name displayed on the horizontal coordinate
            "heating": heating,                                  # Vertical coordinate data 1
            "cooling": cooling                                   # Vertical coordinate data 2
        }
        self.chart_data.append(new_entry)
        yield
        

def navbar() -> rx.Component:
    """Define the navigation bar component that appears on every page."""
    
    # Define the style of the navigation links (Home, Geometry, etc.)
    link_style = {
        "color": "white",
        "text_decoration": "none",
        "font_weight": "600",
        "padding": "0.5em 1em",
        "_hover": {"color": "#63B3ED"} # Highlight color on hover
    }

    return rx.hstack(
        # App Logo linked to the navigation bar
        rx.link(
            rx.image(
            src="/LOGO.png",
            width="160px",
            height="50px",
            ),
            href="/",
            text_decoration="none",
            color="white" 
        ),
        
        # Spacer pushes the navigation links to the right side
        rx.spacer(), 
        
        # Navigation menu items
        rx.hstack(
            rx.link("Home", href="/", style=link_style),
            rx.link("Geometry Setting", href="/GeometrySetting", style=link_style),
            rx.link("Material Setting", href="/MaterialSetting", style=link_style),
            rx.link("Residential Setting", href="/ResidentialSetting", style=link_style),
            rx.link("About", href="/About", style=link_style),

        ),
        
        # Layout and styling for the entire navbar container
        width="100%",
        padding="1em 2em", # Vertical and horizontal padding
        background_color="#10263B", # Dark blue background
        border_bottom="1px solid #4A5568", # Subtle border at the bottom
        position="sticky", # Keep the navbar at the top while scrolling
        top="0",
        z_index="999", # Ensure navbar stays above other UI elements
    )


def base_layout(page: rx.Component) -> rx.Component:
    """Wraps each page with a consistent navbar and container layout."""
    return rx.vstack(
        navbar(),  # Fixed navigation bar at the top
        rx.container(
            page,  # Specific content for the current page
            max_width="1000px",
            padding_top="2em",
            padding_bottom="2em",
            width="100%",
            ),
        width="100%",
        align_items="center",
    )


def index() -> rx.Component:
    """The landing (Home) page with navigation buttons to simulation modules."""
    button_style = {
        "min_width": "300px",
        "margin": "0.5em",
        "color_scheme": "blue", # Primary theme color for buttons
        "is_external": False, # Use internal routing
    }
    return base_layout(
        rx.center(
            rx.vstack(
                # Main welcome heading
                rx.heading("Welcome to EcoSim Pro Building Energy Simulation", 
                           size="8", 
                           margin_bottom="1em",
                           color="#3182CE" # Theme blue
                ),
                
                # Navigation links styled as large buttons
                rx.link(
                    rx.button("Geometry Setting", style=button_style, size="3"),
                    href="/GeometrySetting",
                    text_decoration="none",
                    font_size = "36px",
                    ),
                rx.link(
                    rx.button("Material Setting", style=button_style, size="3"),
                    href="/MaterialSetting",
                    text_decoration="none",
                    font_size = "36px",
                    ),
                rx.link(
                    rx.button("Residential Setting", style=button_style, size="3"),
                    href="/ResidentialSetting",
                    text_decoration="none",
                    font_size = "36px",
                    ),
                
                spacing="2",
                align_items="center",
                padding_top="1em",
            ),
            width="100%",
    )
        )


def GeometrySetting():
    """UI for the Geometry Setting page where users modify window dimensions."""
    return base_layout(
        rx.center(
            rx.vstack(
                rx.heading("Set Window Geometry to do simulation", size = "5"),
                rx.text(
                    "Which geometric property of the window should be modified?",
                    size="4",
                    white_space="nowrap",
                ),
                rx.select(
                    ["Length", "Height"],
                    placeholder="Modify the length or height of window?",
                    on_change=GeometryState.set_selected_option,
                    size="2",
                    width="300px",
                ),
                
                # Conditional rendering: Only show input fields after an option is selected
                rx.cond(
                    GeometryState.selected_option != "",
                    rx.vstack(
                        rx.text(
                            "Enter new value for " + GeometryState.selected_option + " (m) :",
                            size="4",
                            white_space="nowrap",
                        ),
                        rx.input(
                            placeholder="Input numeric value...",
                            on_change=GeometryState.set_new_value,
                            width="300px",
                        ),
                        rx.button(
                            "Start to simulation!",
                            on_click=GeometryState.handle_submit,
                            color_scheme="blue",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                ),

                rx.text(GeometryState.results, size = "5"),

                # Graph Section: Displayed only when simulation results are available
                rx.cond(
                    GeometryState.chart_data.length() > 0,
                    rx.recharts.bar_chart(
                        rx.recharts.bar(
                            data_key="heating",
                            stroke=rx.color("orange", 9),
                            fill=rx.color("orange", 8),
                            name="Heating Energy",
                        ),
                        rx.recharts.bar(
                            data_key="cooling",
                            stroke=rx.color("blue", 9),
                            fill=rx.color("blue", 8),
                            name="Cooling Energy",
                        ),
                        rx.recharts.x_axis(data_key="name"),
                        rx.recharts.y_axis(),
                        rx.recharts.legend(),
                        rx.recharts.graphing_tooltip(),
                        data=GeometryState.chart_data,
                        width="80%",
                        height=270,
                    ),
                ),
                spacing="4",
                width="100%",
            ),
            width="100%",
        )
    )


def MaterialSetting():
    """UI for the Material Setting page to select window and wall materials."""
    return base_layout(
        rx.vstack(
            rx.center(
                rx.vstack(
                    rx.heading("Set Material Properties to do simulation", size = "5"),
                    rx.text("Window Material Type?", size="4", white_space="nowrap"),
                    rx.select(
                        ["Double Pane Window", "Double Pane Low-E Window"], 
                        placeholder="Please select the window type",
                        on_change=MaterialState.set_selected_window,
                        size="2",
                        width="300px",
                    ),
                    rx.text("Wall Material Type?", size="4", white_space="nowrap"),
                    rx.select(
                        ["Light Timber Frame", "Common Brick Wall", "Aerated Concrete", "High-Efficiency Insulated Wall"], 
                        placeholder="Please select the wall type",
                        on_change=MaterialState.set_selected_wall,
                        size="2",
                        width="300px",
                    ),
                    rx.button(
                        "Start to simulation!", 
                        on_click=MaterialState.handle_submit,
                        color_scheme="blue",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                width="100%",
            ),
            
            rx.text(MaterialState.results, size = "5"),
            
            # Chart visualizing heating and cooling energy for materials
            rx.cond(
                MaterialState.chart_data.length() > 0,
                rx.recharts.bar_chart(
                    rx.recharts.bar(
                        data_key="heating",
                        stroke=rx.color("orange", 9),
                        fill=rx.color("orange", 8),
                        name="Heating Energy"
                    ),
                    rx.recharts.bar(
                        data_key="cooling",
                        stroke=rx.color("blue", 9),
                        fill=rx.color("blue", 8),
                        name="Cooling Energy"
                    ),
                    rx.recharts.x_axis(data_key="name"),
                    rx.recharts.y_axis(),
                    rx.recharts.legend(),
                    rx.recharts.graphing_tooltip(),
                    data=MaterialState.chart_data,
                    width="80%",
                    height=270,
                )
            ),
            spacing="4", 
            width="100%",
        )
    )


def ResidentialSetting():
    """UI for the Residential Setting page to configure occupant count and schedules."""
    return base_layout(
        rx.center(
            rx.vstack(
                rx.heading("Set Occupant Information to do simulation", size = "5"),
                rx.text(
                    "Select a schedule of people occupying",
                    size="4",
                    white_space="nowrap",
                ),
                rx.select(
                    ["OCCUPY-1"],
                    placeholder="The schedule of people occupying",
                    on_change=ResidentialState.set_selected_option,
                    size="2",
                    width="300px",
                ),
                
                # Conditional rendering for occupant input fields
                rx.cond(
                    ResidentialState.selected_option != "",
                    rx.vstack(
                        rx.text(
                            "Number of occupants (people)",
                            size="4",
                            white_space="nowrap",
                        ),
                        rx.input(
                            placeholder="Input numeric value...",
                            on_change=ResidentialState.set_new_value,
                            width="300px",
                        ),
                        rx.button(
                            "Start to simulation!",
                            on_click=ResidentialState.handle_submit,
                            color_scheme="blue",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                ),

                rx.text(ResidentialState.results, size = "5"),

                # Graph section for occupancy-based simulation results
                rx.cond(
                    ResidentialState.chart_data.length() > 0,
                    rx.recharts.bar_chart(
                        rx.recharts.bar(
                            data_key="heating",
                            stroke=rx.color("orange", 9),
                            fill=rx.color("orange", 8),
                            name="Heating Energy",
                        ),
                        rx.recharts.bar(
                            data_key="cooling",
                            stroke=rx.color("blue", 9),
                            fill=rx.color("blue", 8),
                            name="Cooling Energy",
                        ),
                        rx.recharts.x_axis(data_key="name"),
                        rx.recharts.y_axis(),
                        rx.recharts.legend(),
                        rx.recharts.graphing_tooltip(),
                        data=ResidentialState.chart_data,
                        width="80%",
                        height=270,
                    ),
                ),
                spacing="4",
                width="100%",
            ),
            width="100%",
        )
    )


def About():
    """The 'About' page introducing the developer and the project mission."""
    return base_layout(
        rx.vstack(
            rx.heading("Meet the Developer", size="8", margin_bottom="0.5em"),
            rx.text("The creator behind EcoSim Pro", color_scheme="gray", margin_bottom="2em"),

            # 1. Developer Profile Hover Card
            rx.hover_card.root(
                rx.hover_card.trigger(
                    rx.avatar(
                        fallback="DEV", 
                        size="8", 
                        radius="full",
                        src="/creator.jpg",
                        cursor="pointer",
                        border="2px solid #3182CE"
                    ),
                ),
                rx.hover_card.content(
                    rx.vstack(
                        rx.box(
                            rx.heading("York Stephen XU", size="3"),
                            rx.text("@sayyx7", size="2", color_scheme="blue"),
                        ),
                        rx.text(
                            "A sophomore passionate about building energy simulation and sustainable development.",
                            size="3",
                        ),
                        spacing="1",
                    ),
                    width="250px",
                ),
            ),

            rx.divider(margin_y="1em"),

            # 2. Project Information Accordion
            rx.vstack(
                rx.heading("About this project", size="6", margin_bottom="1em"),
                rx.accordion.root(
                    rx.accordion.item(
                        header="🚀 Mission of Development",
                        content="To make the complex EnergyPlus building simulation accessible and enable every designer to easily calculate energy consumption.",
                    ),
                    rx.accordion.item(
                        header="🛠️ Technology Stack",
                        content="This site uses Python Reflex to build the frontend and backend, and integrates the EnergyPlus simulation engine at the bottom layer.",
                    ),
                    rx.accordion.item(
                        header="☕ Developer's Postscript",
                        content="Actually, developing this software is a Coursework, but I learned a lot from this assignment. From the underlying construction of websites, to further exploration of Python, and then to the debugging of Terminals, this course has taught me a lot. Thank you again, Prof. Zhang, for your meticulous guidance!",
                    ),
                    width="100%",
                    collapsible=True,
                    variant="ghost",
                ),
                width="100%",
                max_width="600px",
            ),

            spacing="3",
            align_items="center",
            padding_top="1em",
        )
    )


# Initialize the Reflex application
app = rx.App()

# Register pages and their respective URL routes
app.add_page(index, route="/")
app.add_page(GeometrySetting, route="/GeometrySetting")
app.add_page(MaterialSetting, route="/MaterialSetting")
app.add_page(ResidentialSetting, route="/ResidentialSetting")
app.add_page(About, route="/About")