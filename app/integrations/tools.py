



REWRITE_QUERY_TOOL = {
    "name": "rewrite_query",
    "description": "Return the rewritten user query.",
    "input_schema": {
        "type": "object",
        "properties": {
            "rewritten_query": {
                "type": "string",
                "description": "The rewritten user query."
            }
        },
        "required": ["rewritten_query"]
    }
}