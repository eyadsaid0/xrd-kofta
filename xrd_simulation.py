import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import Rectangle
import math

# Set page configuration
st.set_page_config(
    page_title="XRD Bragg's Law Simulator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🔬 X-ray Diffraction (XRD) Bragg's Law Simulator")
st.markdown("""
This is a simple interactive simulation for X-ray diffraction based on **Bragg's Law**.
Adjust the parameters below to see how the diffraction angle changes.

**Bragg's Law:** nλ = 2d sin(θ)
""")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_d_spacing(a, h, k, l, crystal_system):
    """
    Calculate d-spacing based on crystal system and Miller indices.
    
    Parameters:
    - a: Unit cell length (in Angstroms)
    - h, k, l: Miller indices
    - crystal_system: Type of crystal system
    
    Returns:
    - d: d-spacing value
    """
    h_sq = h**2
    k_sq = k**2
    l_sq = l**2
    
    if crystal_system == "Simple Cubic":
        d = a / np.sqrt(h_sq + k_sq + l_sq)
    
    elif crystal_system == "BCC":
        # For BCC, systematic absences: h+k+l must be even
        if (h + k + l) % 2 != 0:
            return None  # Forbidden reflection
        d = a / np.sqrt(h_sq + k_sq + l_sq)
    
    elif crystal_system == "FCC":
        # For FCC, systematic absences: h, k, l must be all even or all odd
        if not ((h % 2 == k % 2 == l % 2) and (h % 2 == l % 2)):
            return None  # Forbidden reflection
        d = a / np.sqrt(h_sq + k_sq + l_sq)
    
    elif crystal_system == "Tetragonal":
        # For tetragonal: a = b ≠ c
        # d-spacing formula: 1/d² = (h²+k²)/a² + l²/c²
        # Assuming c = a for simplicity (can be modified)
        c = a  # Simplified assumption
        d_sq_inv = (h_sq + k_sq) / (a**2) + l_sq / (c**2)
        d = 1 / np.sqrt(d_sq_inv)
    
    elif crystal_system == "Hexagonal":
        # For hexagonal: a = b ≠ c
        # d-spacing formula: 1/d² = (4/3)(h²+hk+k²)/a² + l²/c²
        c = a  # Simplified assumption
        d_sq_inv = (4/3) * (h_sq + h*k + k_sq) / (a**2) + l_sq / (c**2)
        d = 1 / np.sqrt(d_sq_inv)
    
    else:
        d = a / np.sqrt(h_sq + k_sq + l_sq)
    
    return d


def calculate_bragg_angle(wavelength, d_spacing, order=1):
    """
    Calculate Bragg angle using Bragg's Law: nλ = 2d sin(θ)
    
    Parameters:
    - wavelength: X-ray wavelength (in Angstroms)
    - d_spacing: d-spacing (in Angstroms)
    - order: Order of diffraction (n)
    
    Returns:
    - theta_deg: Bragg angle in degrees, or None if sin(θ) > 1
    """
    sin_theta = (order * wavelength) / (2 * d_spacing)
    
    if sin_theta > 1:
        return None  # Physically impossible
    
    theta_rad = np.arcsin(sin_theta)
    theta_deg = np.degrees(theta_rad)
    
    return theta_deg


def draw_bragg_diagram(theta_deg, d_spacing):
    """
    Draw a simple Bragg's Law diagram showing incident and reflected rays.
    
    Parameters:
    - theta_deg: Bragg angle in degrees
    - d_spacing: d-spacing value
    """
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    
    theta_rad = np.radians(theta_deg)
    
    # Draw lattice planes
    plane_spacing = 1.0  # Normalized for visualization
    num_planes = 4
    
    for i in range(num_planes):
        y_pos = i * plane_spacing
        ax.plot([-3, 3], [y_pos, y_pos], 'b-', linewidth=2, label='Lattice planes' if i == 0 else '')
    
    # Draw incident ray
    incident_start_x = -2.5
    incident_start_y = num_planes * plane_spacing + 1.5
    incident_end_x = 0
    incident_end_y = 0
    
    ax.arrow(incident_start_x, incident_start_y, 
             incident_end_x - incident_start_x, 
             incident_end_y - incident_start_y,
             head_width=0.15, head_length=0.1, fc='red', ec='red', linewidth=2)
    ax.text(incident_start_x - 0.3, incident_start_y + 0.3, 'Incident ray', fontsize=10, color='red', fontweight='bold')
    
    # Draw reflected ray
    reflected_end_x = 2.5
    reflected_end_y = num_planes * plane_spacing + 1.5
    
    ax.arrow(incident_end_x, incident_end_y,
             reflected_end_x - incident_end_x,
             reflected_end_y - incident_end_y,
             head_width=0.15, head_length=0.1, fc='green', ec='green', linewidth=2)
    ax.text(reflected_end_x + 0.2, reflected_end_y + 0.3, 'Reflected ray', fontsize=10, color='green', fontweight='bold')
    
    # Draw normal line
    ax.plot([0, 0], [-0.5, num_planes * plane_spacing + 0.5], 'k--', linewidth=1, alpha=0.5, label='Normal')
    
    # Draw angle arc
    arc_radius = 0.7
    arc_angles = np.linspace(np.pi/2, np.pi/2 + theta_rad, 50)
    arc_x = arc_radius * np.cos(arc_angles)
    arc_y = arc_radius * np.sin(arc_angles)
    ax.plot(arc_x, arc_y, 'k-', linewidth=1.5)
    ax.text(0.3, 0.5, f'θ = {theta_deg:.2f}°', fontsize=11, fontweight='bold', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # Draw d-spacing indicator
    ax.annotate('', xy=(2.8, 0), xytext=(2.8, plane_spacing),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
    ax.text(3.1, plane_spacing/2, f'd = {d_spacing:.3f} Å', fontsize=10, color='purple', fontweight='bold')
    
    # Set axis properties
    ax.set_xlim(-3.5, 4)
    ax.set_ylim(-1, num_planes * plane_spacing + 2.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Position (arbitrary units)', fontsize=11)
    ax.set_ylabel('Position (arbitrary units)', fontsize=11)
    ax.set_title("Bragg's Law Diffraction Diagram", fontsize=13, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    
    plt.tight_layout()
    return fig


# ============================================================================
# SIDEBAR INPUTS
# ============================================================================

st.sidebar.header("⚙️ Simulation Parameters")

# Wavelength input
wavelength = st.sidebar.slider(
    "X-ray Wavelength (λ) [Å]",
    min_value=0.1,
    max_value=3.0,
    value=1.54,
    step=0.01,
    help="Typical X-ray wavelengths range from 0.5 to 2.5 Å"
)

# Unit cell length
a = st.sidebar.slider(
    "Unit Cell Length (a) [Å]",
    min_value=1.0,
    max_value=10.0,
    value=4.0,
    step=0.1,
    help="Lattice parameter of the crystal"
)

# Crystal system selection
crystal_system = st.sidebar.selectbox(
    "Crystal System",
    ["Simple Cubic", "BCC", "FCC", "Tetragonal", "Hexagonal"],
    help="Select the crystal structure type"
)

# Miller indices
st.sidebar.subheader("Miller Indices (h, k, l)")
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    h = st.number_input("h", min_value=0, max_value=5, value=1, step=1)
with col2:
    k = st.number_input("k", min_value=0, max_value=5, value=0, step=1)
with col3:
    l = st.number_input("l", min_value=0, max_value=5, value=0, step=1)

# Order of diffraction
order = st.sidebar.slider(
    "Order of Diffraction (n)",
    min_value=1,
    max_value=3,
    value=1,
    step=1,
    help="Higher orders correspond to larger diffraction angles"
)

# ============================================================================
# CALCULATIONS
# ============================================================================

d_spacing = calculate_d_spacing(a, int(h), int(k), int(l), crystal_system)

if d_spacing is None:
    st.warning(f"⚠️ **Forbidden Reflection**: The Miller indices ({int(h)}, {int(k)}, {int(l)}) are not allowed for {crystal_system}. Please choose different indices.")
    bragg_angle = None
else:
    bragg_angle = calculate_bragg_angle(wavelength, d_spacing, order)

# ============================================================================
# RESULTS DISPLAY
# ============================================================================

st.header("📊 Results")

# Create two columns for results
col1, col2 = st.columns(2)

with col1:
    st.subheader("Calculation Summary")
    
    result_data = {
        "Parameter": [
            "Wavelength (λ)",
            "Unit Cell Length (a)",
            "Crystal System",
            "Miller Indices (h, k, l)",
            "Order (n)",
            "d-spacing",
            "Bragg Angle (θ)"
        ],
        "Value": [
            f"{wavelength:.3f} Å",
            f"{a:.3f} Å",
            crystal_system,
            f"({int(h)}, {int(k)}, {int(l)})",
            f"{order}",
            f"{d_spacing:.4f} Å" if d_spacing else "N/A",
            f"{bragg_angle:.2f}°" if bragg_angle else "N/A (sin θ > 1)"
        ]
    }
    
    # Display as formatted text
    for param, value in zip(result_data["Parameter"], result_data["Value"]):
        st.write(f"**{param}:** `{value}`")

with col2:
    st.subheader("Bragg's Law Equation")
    st.latex(r"n\lambda = 2d \sin(\theta)")
    st.latex(r"\sin(\theta) = \frac{n\lambda}{2d}")
    
    if bragg_angle is not None:
        st.success(f"✅ **Bragg Angle:** θ = **{bragg_angle:.2f}°**")
        st.info(f"**2θ (Detector angle):** {2 * bragg_angle:.2f}°")
    else:
        st.error("❌ **No solution**: The condition sin(θ) > 1 is physically impossible. Try adjusting the wavelength or d-spacing.")

# ============================================================================
# VISUALIZATION
# ============================================================================

st.header("🎨 Diffraction Diagram")

if bragg_angle is not None and d_spacing is not None:
    fig = draw_bragg_diagram(bragg_angle, d_spacing)
    st.pyplot(fig)
    plt.close(fig)
else:
    st.warning("Cannot display diagram: Invalid parameters. Please adjust your inputs.")

# ============================================================================
# EDUCATIONAL NOTES
# ============================================================================

st.header("📚 Educational Notes")

with st.expander("ℹ️ About Bragg's Law"):
    st.markdown("""
    **Bragg's Law** describes the condition for constructive interference of X-rays diffracted from crystal planes:
    
    - **n**: Order of diffraction (1, 2, 3, ...)
    - **λ**: Wavelength of X-rays
    - **d**: Spacing between crystal planes (d-spacing)
    - **θ**: Bragg angle (angle between incident ray and crystal plane)
    
    When Bragg's Law is satisfied, X-rays reflected from successive crystal planes interfere constructively,
    producing a strong diffraction peak.
    """)

with st.expander("ℹ️ Crystal Systems"):
    st.markdown("""
    - **Simple Cubic**: d = a / √(h² + k² + l²)
    - **BCC**: Same formula, but h+k+l must be even
    - **FCC**: Same formula, but h, k, l must be all even or all odd
    - **Tetragonal**: d = 1 / √[(h²+k²)/a² + l²/c²]
    - **Hexagonal**: d = 1 / √[(4/3)(h²+hk+k²)/a² + l²/c²]
    """)

with st.expander("ℹ️ Miller Indices"):
    st.markdown("""
    **Miller indices (h, k, l)** describe the orientation of crystal planes:
    
    - (100): Planes perpendicular to the [100] direction
    - (110): Planes perpendicular to the [110] direction
    - (111): Planes perpendicular to the [111] direction
    
    Common examples:
    - (100) planes in cubic: d = a
    - (110) planes in cubic: d = a/√2
    - (111) planes in cubic: d = a/√3
    """)

with st.expander("ℹ️ Typical X-ray Wavelengths"):
    st.markdown("""
    | Element | Kα (Å) | Common Use |
    |---------|--------|-----------|
    | Cu      | 1.54   | Most common |
    | Mo      | 0.71   | High-energy |
    | Cr      | 2.29   | Low-energy |
    | Co      | 1.79   | Alternative |
    | Fe      | 1.94   | Alternative |
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 12px; color: #666;'>
    <p>🔬 XRD Bragg's Law Simulator | Educational Tool</p>
    <p>Built with Streamlit | Python Physics Simulation</p>
</div>
""", unsafe_allow_html=True)
