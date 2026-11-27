from langgraph.graph import StateGraph, START, END
from github_ai_agent.core.state import State
from github_ai_agent.core.nodes import tool_node, llm, tools_condition, llm_or_card
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk
import json
graph_compiler = StateGraph(State)

graph_compiler.add_node('llm',llm)
graph_compiler.add_node('llm_or_card',llm_or_card)
graph_compiler.add_node('tools',tool_node)
graph_compiler.add_edge(START, 'llm_or_card')
graph_compiler.add_conditional_edges('llm',tools_condition)
graph_compiler.add_edge('tools', 'llm')
graph_compiler.add_edge('llm',END)

memory = InMemorySaver()

graph = graph_compiler.compile(checkpointer=memory)


def draw_graph_image():
    graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


def send_message(thread_id:str, message:str):
    config = {
                'configurable':{
                    'thread_id':thread_id
                }
            }
    message = [HumanMessage(content=message)]
    response = graph.invoke({'messages':[HumanMessage(content=message)]},config=config)
    return {
        "card":response['card'],
        'response':response['messages'][-1].content
    }

def send_message_streamed(thread_id, message):
    config = {
                'configurable':{
                    'thread_id':thread_id
                }
            }
    message = [HumanMessage(content=message)]
    for chunk in graph.stream({'messages':message},stream_mode=['messages','updates'],config=config, version="v2"):
                
                if chunk["type"] == "updates":
                    if node_data := chunk["data"].get('llm_or_card'):
                        if card := node_data.get("card"):
                            yield f"data: {json.dumps({'type': 'card', 'content': None, 'card':node_data.get('card')})}\n\n"

                if chunk["type"] == "messages":
                    msg, metadata = chunk["data"]
                    if (
                        metadata.get("langgraph_node") == "llm"
                        and isinstance(msg, AIMessageChunk)
                        and msg.content
                    ):
                        yield f"data: {json.dumps({'type': 'token', 'content': msg.content, 'card': None})}\n\n"
    yield f"data: {json.dumps({'type': 'done'})}\n\n"

if __name__ == '__main__':
    while True:
        text = input("You: ")
        if text == 'exit':
            break
        gen = send_message_streamed('1',text)
        print("AI: ",end='')
        for chunk in gen:
            print(chunk, end='')
        print()