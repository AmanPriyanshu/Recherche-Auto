function_template = """
<tool_description>
    <tool_name>get_search_query</tool_name>
    <description>
        Function for defining search query for topic to research and the number of queries that can be made. Search query needs to be strongly directed employing strong factors of google search. It may include things like "site:" or "filetype:" queries, to improve search quality. Also, number of queries should be between 1 to 10. 
    <parameters>
        <parameter>
            <name>search_query</name>
            <type>str</type>
            <description>Search Query for targetted research</description>
        </parameter>
        <parameter>
            <name>num_queries</name>
            <type>int</type>
            <description>Number of top N queries to analyze</description>
        </parameter>
    </parameters>
</tool_description>
"""