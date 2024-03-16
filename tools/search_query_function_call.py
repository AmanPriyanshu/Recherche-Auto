function_template = """
<tool_description>
    <tool_name>get_search_query</tool_name>
    <description>
        Function for defining search query for topic to research and the number of queries that can be made. Search query needs to be strongly directed employing strong factors of google news search. Also, number of queries should be between 1 to 10. Note: That inlcuding terms like "latest news" or "latest news" or "news" would perform poorly, so please just stick to the core key phrase. 
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