import time
from typing import TypedDict, Annotated

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.types import interrupt

from spot_agent.img_handler import ImageHandler
from spot_agent.llm import get_chat_model
from spot_agent.prompts import sys_msg_manager_content, sys_msg_vision_content
from spot_agent.utils import get_controller, get_config_from_yaml

config = get_config_from_yaml('../config/config.yaml')

vision_agent = get_chat_model(config.vision_model_name, temperature=config.vision_temperature)
manager_agent = get_chat_model(config.manager_model_name, temperature=config.manager_temperature)

img_handler = ImageHandler(config.save_img_path)

controller = get_controller()

controller.step("RotateLeft", degrees=18)
event = controller.step(action="Done")

img_handler.save_img(event.cv2img)


@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]


@tool
def rotate_robot(direction: str, degrees: int = 18):
    """
    Rotate the robot to the given direction by the specified degrees.
    The vision assistant will analyze the scene and provide a detailed description of the environment.

    Args:
        direction (str): 'right' or 'left'
        degrees (int): Degrees to rotate. Defaults to 18 for smooth turns.
        """
    if direction == 'right':
        controller.step(action="RotateRight", degrees=degrees)
    elif direction == 'left':
        controller.step(action="RotateLeft", degrees=degrees)
    time.sleep(0.1)
    event = controller.step(action="Done")
    img_handler.save_img(event.cv2img)

    return f"Robot rotated {direction} by {degrees} degrees."


@tool
def move(direction: str, distance: float = 0.25):
    """Moves the robot forward or backward the given distance.
    The vision assistant will analyze the scene and provide a detailed description of the environment.

    Args:
        direction (str): 'forward' or 'backward'
        distance (float): The distance to move. Defaults to 0.25."""
    if direction == 'forward':
        controller.step(action="MoveAhead", moveMagnitude=distance)
    elif direction == 'backward':
        controller.step(action="MoveBack", moveMagnitude=distance)
    time.sleep(0.1)
    event = controller.step(action="Done")
    img_handler.save_img(event.cv2img)

    return f"Robot moved {direction} by {distance}m."


@tool
def look_up_or_down(direction: str, degrees: int = 5):
    """
    Pitch the robot's head 'up' or 'down' by the specified degrees to get a better view of it's surroundings.
    The vision assistant will analyze the scene and provide a detailed description of the environment.

    Args:
        direction (str): 'up' or 'down'
        degrees (int): Degrees to rotate. Defaults to 5 for smooth turns.
        """
    if direction == 'up':
        controller.step(action="LookUp", degrees=degrees)
    elif direction == 'down':
        controller.step(action="LookDown", degrees=degrees)
    time.sleep(0.1)
    event = controller.step(action="Done")
    img_handler.save_img(event.cv2img)
    return f"Robot looked {direction}."


tools = [move, rotate_robot, look_up_or_down]
manager_llm_with_tools = manager_agent.bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    objective: str


def vision_node(state: AgentState) -> dict:
    objective = state["objective"]
    last_n_img = [
        {"type": "image_url", "image_url": {"url": f"{img_path}"}}
        for img_path in img_handler.get_last_n_img(config.use_last_n_img)
    ]

    vision_prompt = [
        SystemMessage(content=sys_msg_vision_content),
        HumanMessage(
            content=[{"type": "text", "text": f"My current goal is: {objective}"}] + last_n_img
        )
    ]

    response = vision_agent.invoke(vision_prompt)

    return {"messages": [HumanMessage(content=response.content, name="vision_assistant")]}


def manager_agent_node(state: AgentState) -> dict:
    messages_for_manager_llm = [SystemMessage(content=sys_msg_manager_content)] + state["messages"]

    response = manager_llm_with_tools.invoke(messages_for_manager_llm)
    return {"messages": [response]}


def build_agent():
    builder = StateGraph(AgentState)

    builder.add_node("vision", vision_node)
    builder.add_node("manager_agent", manager_agent_node)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "vision")
    builder.add_edge("vision", "manager_agent")
    builder.add_conditional_edges("manager_agent", tools_condition)
    builder.add_edge("tools", "vision")
    return builder.compile()


def invoke_agent(agent, user_objective: str):
    agent_config = {"recursion_limit": config.recursion_limit, }

    initial_state = {
        "messages": [],
        "objective": user_objective
    }
    response = agent.invoke(initial_state, agent_config)

    final_message = response['messages'][-1]
    print(f"Agent: {final_message.content}")


robotic_agent = build_agent()
# print(robotic_agent.get_graph().draw_ascii())

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        break
    invoke_agent(robotic_agent, user_input)
