import streamlit as st
# from Agentic.google import scrape_and_save_text
from Headless.gnews_scraper import scrape_and_save_text
from tools.search_query_function_call import function_template
import anthropic
import json
import matplotlib.pyplot as plt
import networkx as nx
import re

client = anthropic.Client(api_key=st.secrets["anthropic_key"])

def get_csv_response(prompt):
	system_prompt = "Observe the following news list in short and create a knowledge graph by employing the \"entity\",\"relation\",\"entity\" sequence as CSV. Note: Do not return non-neccessary words, just return the CSV. Ensure the entity and relations, all have less than 5 words."
	MODEL_NAME = "claude-3-haiku-20240307"
	data_string = client.messages.create(
		model=MODEL_NAME,
		max_tokens=512,
		messages=[{"role": "user", "content": "Contents to be used:\n\n"+str(prompt)}],
		system=system_prompt
	).content[0].text
	try:
		edges = []
		for line in data_string.strip().split("\n"):
			source, relation, target = line.split(",")
			edges.append((source, target))
		G = nx.DiGraph()
		G.add_edges_from(edges)
		plt.figure(figsize=(12, 8))
		pos = nx.spring_layout(G, seed=42)
		nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10, arrows=True)
		plt.title("Generated Knowledge Graph")
		st.pyplot(plt)
		return True
	except:
		return False

def get_summary_response(prompt):
	system_prompt = "Observe the following news list in short and create a 400 word research report, which employs these discussed recent advances in the field."
	MODEL_NAME = "claude-3-haiku-20240307"
	function_calling_message = client.messages.create(
		model=MODEL_NAME,
		max_tokens=512,
		messages=[{"role": "user", "content": "Contents to be used:\n\n"+str(prompt)}],
		system=system_prompt
	).content[0].text
	return function_calling_message

def get_llm_response(messages):
	MODEL_NAME = "claude-3-haiku-20240307"#"claude-3-opus-20240229"
	system_prompt = """You are an AI assistant who creates search queries in conjunction with the user. Default number of top_num_sequence to analyze will be 7, unless otherwise specified by the user. Remember, that exlain to the user why you came up with a certain idea for the search query and then combine it with a follow up question to work with them to improve it. Your response needs to be short. Note: Do not include terms like "news" or "latest news" as you're already searching a news site, so including those will not be able to search effectively.

In this environment you have access to a set of tools you can use to answer the user's question. 

You may call them like this:
<function_calls>
	<invoke>
		<tool_name>$TOOL_NAME</tool_name>
		<parameters>
			<$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>
			...
		</parameters>
	</invoke>
</function_calls>

Here are the tools available:
<tools>{function_template}</tools>

Note: Always use the tool: get_search_query
"""
	function_calling_message = client.messages.create(
		model=MODEL_NAME,
		max_tokens=512,
		messages=messages,
		system=system_prompt
	).content[0].text
	return function_calling_message

def extract_between_tags(text):
	regex_1 = r"<query>(.*?)<\/query>"
	regex_2 = r"<top_num_sequence>(.*?)<\/top_num_sequence>"
	matches_1 = re.search(regex_1, text, re.DOTALL)
	matches_2 = re.search(regex_2, text, re.DOTALL)
	if matches_1 and matches_2:
		query_string = matches_1.group(1)
		top_num_sequence_string = matches_2.group(1)
		try:
			top_num_sequence_string = int(top_num_sequence_string)
		except:
			top_num_sequence_string = 7
		return query_string, int(top_num_sequence_string)
	else:
		print("No match found.")
		return None, None

def extract_function_call(text):
	regex = r"<function_calls>(.*?)<\/function_calls>"
	matches = re.search(regex, text, re.DOTALL)
	if matches:
		substring = matches.group(1)
		return substring
	else:
		print("No match found.")

def main():
	query_string, top_num_sequence_string = "", 7
	st.title("Talk to Recherche-Auto")
	if "messages" not in st.session_state:
		st.session_state.messages = []
	col1, col2 = st.columns([3, 1])
	for message in st.session_state.messages:
		with st.chat_message(message["role"]):
			st.markdown(message["content"])
	if prompt := st.chat_input("What is up?"):
		st.chat_message("user").markdown(prompt)
		st.session_state.messages.append({"role": "user", "content": prompt})
		function_calling_message = get_llm_response(st.session_state.messages)
		query_string, top_num_sequence_string = extract_between_tags(function_calling_message)
		function_params = extract_function_call(function_calling_message)
		print(function_params)
		function_calling_message = function_calling_message.replace(function_params, "").replace("<function_calls>", "").replace("</function_calls>", "")
		dictionary = {"current_query": query_string, "n_queries": top_num_sequence_string}
		response = f"Recherche-Auto: {str(function_calling_message)}"
		with st.chat_message("assistant"):
			st.markdown(response)
			st.info("If this Query is ok, please click \"Begin Research!\""+str(dictionary))
			with open("search.json", "w") as f:
				json.dump(dictionary, f, indent=4)
		st.session_state.messages.append({"role": "assistant", "content": response})
	if st.button("Begin Research!"):
		with open("search.json", "r") as f:
			dictionary = json.load(f)
		news = scrape_and_save_text(dictionary["current_query"].strip(), dictionary["n_queries"])
		if type(news) == str:
			st.error("Use the following re-direction: "+news)
		else:
			summary = get_summary_response(json.dumps(news, indent=4))
			st.success(summary)
			knowledge_graph = get_csv_response(json.dumps(news, indent=4))
			if not knowledge_graph:
				st.error("Sorry couldn't plot the knowledge graph for this query, not enough information for structuring.")

if __name__ == '__main__':
	main()
