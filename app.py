import streamlit as st
# from Agentic.google import scrape_and_save_text
from duckduckgo_search import DDGS
from tools.search_query_function_call import function_template
import anthropic
import re

client = anthropic.Client(api_key=st.secrets["anthropic_key"])

def get_llm_response(messages):
	MODEL_NAME = "claude-3-haiku-20240307"#"claude-3-opus-20240229"
	system_prompt = """You are an AI assistant who creates search queries in conjunction with the user. Default number of top_num_sequence to analyze will be 3, unless otherwise specified by the user. Remember, that exlain to the user why you came up with a certain idea for the search query and then combine it with a follow up question to work with them to improve it. Your response needs to be short.

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
			top_num_sequence_string = 3
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

def scrape_and_save_text(query_string, top_num_sequence_string):
	results = DDGS().text(query_string, max_results=top_num_sequence_string)
	print(results)

def main():
	query_string, top_num_sequence_string = "", 3
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
		dictionary = str({"current_query": query_string, "n_queries": top_num_sequence_string})
		response = f"Recherche-Auto: {str(function_calling_message)}"
		with st.chat_message("assistant"):
			st.markdown(response)
			st.info("If this Query is ok, please click \"Begin Research!\""+str(dictionary))
		st.session_state.messages.append({"role": "assistant", "content": response})
	if st.button("Begin Research!"):
		scrape_and_save_text(query_string, top_num_sequence_string)

if __name__ == '__main__':
	main()
