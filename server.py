from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider
from model import CliniqueModel

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.8,
        "Layer": 0,
        "text": str(agent.__class__.__name__)
    }
    
    name = agent.__class__.__name__.lower()
    
    if name == "patient":
        portrayal["Color"] = "red"
    elif name in ["userinterfaceagent", "prescriptionconsultationagent", "medicalrecordagent"]:
        portrayal["Color"] = "blue"
    else:
        portrayal["Color"] = "green"
    
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
chart = ChartModule([{"Label": "satisfaction moyenne", "Color": "Black"}], 
                   data_collector_name="datacollector")

model_params = {
    "num_agents": Slider("Nombre d'agent", 12, 1, 24, 1),
    "width": 10,
    "height": 10
}

server = ModularServer(
    CliniqueModel,
    [grid, chart],
    "Simulation Clinique Multi-agent",
    model_params
)

server.port = 8523
server.launch()  # ← adding this line to start the server
