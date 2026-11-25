from langgraph.graph import StateGraph, START, END
from github_ai_agent.core.state import State
from github_ai_agent.core.nodes import tool_node, llm, tools_condition, llm_or_card
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage

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


# 1. Print as Mermaid syntax (no extra dependencies)
print(graph.get_graph().draw_mermaid())

# 2. Print as ASCII in the terminal (requires: pip install grandalf)
print(graph.get_graph().draw_ascii())

# 3. Save as a PNG image
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == '__main__':
    while True:
        text = input("You: ")
        if text == 'exit':
            break
        config = {
            'configurable':{
                'thread_id':'1'
            }
        }
        response = graph.invoke({'messages':[HumanMessage(content=text)]},config=config)
        print(f"card:{response['card']}\nAI: {response['messages'][-1].content}")